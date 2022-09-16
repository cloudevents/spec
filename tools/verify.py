#!python
from argparse import ArgumentParser
from contextlib import closing
from functools import lru_cache
from itertools import chain
from pathlib import Path
from typing import Iterable, List, NewType, Optional, Sequence, Set, Tuple
import re
from markdown import markdown
from bs4 import BeautifulSoup
from tenacity import Retrying, stop_after_attempt
from aiohttp import ClientSession
from tqdm.asyncio import tqdm
from http import HTTPStatus
from pymdownx import slugs
import asyncio

Issue = NewType("Issue", str)
TaggedIssue = Tuple[Path, Issue]
Uri = NewType("Uri", str)
HttpUri = NewType("HttpUri", Uri)

_HTTP_MAX_GET_ATTEMPTS = 5
_HTTP_TIMEOUT_SECONDS = 10

_SKIP_TEXT_PATTERN = re.compile(
    r"<!--\s*no[\s-]+verify[\s-]+(?P<type>\w+)[\s-]*-->", re.IGNORECASE
)
_NEWLINE_PATTERN = re.compile(r"\n")
_MARKDOWN_BOOKMARK_PATTERN = re.compile(r"\[.+?\]\[.+?\]", re.IGNORECASE)
_PHRASES_THAT_MUST_BE_CAPITALIZED_PATTERN = re.compile(
    r"(MUST(\s+NOT)?|"
    # catch the "required" in the jsonschema of the json-format.md
    r'(?<!")REQUIRED(?!")|'
    r"(?<!mar)SHALL(\s+NOT)?|"  # catch the word "marshall"
    r"SHOULD(\s+NOT)?|"
    r"RECOMMENDED|"
    r"MAY|"
    r"OPTIONAL(?!LY)"  # catch the word "optionally"
    r")",
    flags=re.IGNORECASE,  # we want to catch all the words that were not capitalized
)
_BANNED_PHRASES_PATTERN = re.compile(r"Cloud\s+Events?", flags=re.IGNORECASE)
_NEWLINE_PATTERN = re.compile(r"\n")


def _is_text_all_uppercase(text: str) -> bool:
    return text == text.upper()


def _banned_phrase_issues(text: str) -> Iterable[Issue]:
    for match in _BANNED_PHRASES_PATTERN.finditer(text):
        yield _pattern_issue(match, text, f"{repr(match.group(0))} is banned")


def _miscased_phrase_issues(text: str) -> Iterable[Issue]:
    for match in _PHRASES_THAT_MUST_BE_CAPITALIZED_PATTERN.finditer(text):
        phrase = match.group(0)
        if not _is_text_all_uppercase(phrase):
            yield _pattern_issue(
                match,
                text,
                f"{repr(phrase)} MUST be capitalized ({repr(phrase.upper())})",
            )


def _text_issues(text: str) -> Iterable[Issue]:
    if _skip_type(text) != "specs":
        yield from _banned_phrase_issues(text)
        yield from _miscased_phrase_issues(text)


def _line_of_match(match: re.Match, origin_text: str) -> int:
    return (
        #  count all newlines in the text before the given match
        len(_NEWLINE_PATTERN.findall(origin_text, 0, match.start(0)))
        + 1  # adding one because line count starts from 1 and not 0
    )


def _pattern_issue(match: re.Match, origin_text: str, issue_message: str) -> Issue:
    return Issue(f"line {_line_of_match(match, origin_text)}: {issue_message}")


@lru_cache
def _html_parser(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def _query_all_docs(directory: Path) -> Set[Path]:
    return set(directory.rglob("**/*.md")) | set(directory.rglob("**/*.htm*"))


def _skip_type(text: str) -> Optional[str]:
    match = _SKIP_TEXT_PATTERN.search(text)
    if match:
        return match.groupdict().get("type")
    return None


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
    else:
        return []


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
            return await _uri_availability_issues(HttpUri(uri))
        case "mailto":
            return []
        case _:
            return _local_path_uri_issues(uri, path)


def _undefined_bookmark_issues(html: str) -> Iterable[Issue]:
    """
    Assuming the html was already rendered from markdown and all the unreferenced
    bookmarks remain as-is in the html text.
    """
    for match in _MARKDOWN_BOOKMARK_PATTERN.finditer(html):
        yield _pattern_issue(
            match,
            html,
            f"Undefined markdown bookmark referenced ({repr(match.group(0))})",
        )


async def _html_issues(path: Path) -> Iterable[Issue]:
    html = read_html_text(path)
    if _skip_type(html) != "links":
        return [
            issue
            for issues in await asyncio.gather(
                *[_uri_issues(uri, path) for uri in _find_all_uris(html)]
            )
            for issue in issues
        ] + list(_undefined_bookmark_issues(html))
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
def _read_text(path: Path):
    return path.read_text(encoding="utf-8")


@lru_cache
def read_html_text(path: Path) -> str:
    if path.name.endswith(".md"):
        return markdown(
            _read_text(path),
            extensions=["toc"],  # need toc so headers will generate ids
            extension_configs={
                # we need this for unicode titles
                "toc": {"slugify": slugs.slugify(case="lower", percent_encode=False)}
            },
        )  # Convert markdown to html
    else:
        return _read_text(path)


async def _query_file_issues(path: Path) -> Sequence[TaggedIssue]:
    result: List[TaggedIssue] = []
    for issue in list(await _html_issues(path)) + list(_text_issues(_read_text(path))):
        result.append((path, issue))
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


async def main():
    parser = ArgumentParser()
    parser.add_argument("root", default=".", nargs="?")
    args = parser.parse_args()
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
