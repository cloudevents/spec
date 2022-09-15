#!python
from argparse import ArgumentParser
from contextlib import closing
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from random import random
from typing import Iterable, List, NewType, Optional, Sequence, Set, Tuple
import re
from markdown import markdown
from bs4 import BeautifulSoup
from tenacity import Retrying, stop_after_attempt
from aiohttp import ClientSession
from tqdm.asyncio import tqdm
import random
from http import HTTPStatus
from pymdownx import slugs
import asyncio

# it is ok, we use insecure https only to verify that the links are valid
Issue = NewType("Issue", str)
TaggedIssue = Tuple[Path, Issue]
Uri = NewType("Uri", str)
HttpUri = NewType("HttpUri", Uri)
_HTTP_MAX_GET_ATTEMPTS = 5
_HTTP_TIMEOUT_SECONDS = 10
_SKIP_TEXT_PATTERN = re.compile(r"<!--\s+no\s+verify-links", re.IGNORECASE)
_NEWLINE_PATTERN = re.compile(r"\n")
_UNDEFINED_BOOKMARK_PATTERN = re.compile(r"\[.+?\]\[.+?\]", re.IGNORECASE)


def _line_of_match(match: re.Match, origin_text: str) -> int:
    return (
        #  count all newlines in the text before the given match
        len(_NEWLINE_PATTERN.findall(origin_text, 0, match.start(0)))
        + 1  # adding one because line count starts from 1 and not 0
    )


def _query_all_docs(directory: Path) -> Set[Path]:
    return set(directory.rglob("**/*.md")) | set(directory.rglob("**/*.htm*"))


def _pattern_issue(match: re.Match, origin_text: str, issue_message: str) -> Issue:
    return Issue(f"line {_line_of_match(match, origin_text)}: {issue_message}")


@lru_cache
def _html_parser(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def _query_all_docs(directory: Path) -> Set[Path]:
    return set(directory.rglob("**/*.md")) | set(directory.rglob("**/*.htm*"))


def _should_skip_text(text: str) -> bool:
    return bool(_SKIP_TEXT_PATTERN.search(text))


def _find_all_uris(html: str) -> Iterable[Uri]:
    for a in _html_parser(html).findAll("a"):
        uri = a.get("href")
        if uri:
            yield Uri(uri.strip())


async def _uri_availability_issues(uri: HttpUri) -> Sequence[Issue]:
    try:
        for attempt in Retrying(stop=stop_after_attempt(_HTTP_MAX_GET_ATTEMPTS)):
            with attempt:
                async with ClientSession() as session:
                    with closing(
                        await session.get(uri, timeout=_HTTP_TIMEOUT_SECONDS, ssl=False)
                    ) as response:
                        match response.status:
                            case HTTPStatus.NOT_FOUND:
                                return [Issue(f"{repr(uri)} was not found")]
                            case _:
                                return []  # no issues

    except Exception:  # noqa
        return [Issue(f"Could Not access {repr(uri)}")]


async def _http_uri_issue(uri: HttpUri) -> Sequence[Issue]:
    return await _uri_availability_issues(uri)


def _does_html_contains_id(html: str, id: str) -> bool:
    return _html_parser(html).find(id=id) is not None


def _missing_segment_issue(path: Path, segment: str) -> Issue:
    return Issue(f"{path} does not contain {repr('#' + segment)} segment")


def _missing_file_issue(path: Path) -> Issue:
    return Issue(f"{path} does not exist")


def _local_path_uri_issues(uri: Uri, current_path: Path) -> Sequence[Issue]:
    path: Optional[Path] = None
    path_segment: Optional[str] = None

    match uri.split("#"):
        case ["", segment]:
            path = current_path
            path_segment = segment
        case [relative_path, segment]:
            path = current_path.parent / relative_path
            path_segment = segment
        case [relative_path]:
            path = current_path.parent / relative_path
        case _:
            return [Issue("Invalid local path uri")]

    if not path.exists():
        return [_missing_file_issue(path)]
    if path_segment and not _does_html_contains_id(read_html_text(path), path_segment):
        return [_missing_segment_issue(path, path_segment)]
    return []


async def _uri_issues(uri: Uri, path: Path) -> Sequence[Issue]:
    schema = uri.split(":")[0]
    match schema:
        case "http" | "https":
            return await _http_uri_issue(HttpUri(uri))
        case "mailto":
            return []
        case _:
            return _local_path_uri_issues(uri, path)


def _undefined_bokkmark_issues(html: str) -> Iterable[Issue]:
    for match in _UNDEFINED_BOOKMARK_PATTERN.finditer(html):
        yield _pattern_issue(
            match,
            html,
            f"Undefined markdown bookmark referenced ({repr(match.group(0))})",
        )


async def _html_issues(path: Path) -> Iterable[Issue]:
    html = read_html_text(path)
    if not _should_skip_text(html):
        return [
            issue
            for issues in await asyncio.gather(
                *[_uri_issues(uri, path) for uri in _find_all_uris(html)]
            )
            for issue in issues
        ] + list(_undefined_bokkmark_issues(html))
    else:
        return []


def _print_issue(tagged_issue: TaggedIssue) -> None:
    path, issue = tagged_issue
    print(f"{path}:{issue}")


def _print_issues(tagged_issues: Sequence[TaggedIssue]):
    print("-" * 88)
    for tagged_issue in tagged_issues:
        _print_issue(tagged_issue)
    print(
        f"ERROR: Had {len(tagged_issues)} issues, in {len({p for p, _ in tagged_issues})} files"
    )


@lru_cache
def read_html_text(path: Path) -> str:
    if path.name.endswith(".md"):
        return markdown(
            path.read_text(encoding="utf-8"),
            extensions=["toc"],  # need toc so headers will generate ids
            extension_configs={
                # we need this for unicode titles
                "toc": {"slugify": slugs.slugify(case="lower", percent_encode=False)}
            },
        )  # Convert markdown to html
    else:
        return path.read_text()


async def _query_file_issues(path: Path) -> Sequence[TaggedIssue]:
    result: List[TaggedIssue] = []
    for issue in await _html_issues(path):
        tagged_issue = (path, issue)
        result.append(tagged_issue)
    return result


async def _query_directory_issues(directory: Path) -> Iterable[TaggedIssue]:
    return [
        issue
        for issues in await tqdm.gather(
            *[_query_file_issues(path) for path in sorted(_query_all_docs(directory))],
            unit="files",
        )
        for issue in issues
    ]


parser = ArgumentParser()
parser.add_argument("root", default=".", nargs="?")
args = parser.parse_args()


async def main():
    issues = list(await _query_directory_issues(Path(args.root)))
    if issues:
        _print_issues(issues)
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    # Need async because we perform alot of http requests.
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
