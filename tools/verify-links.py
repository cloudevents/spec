#!python
from argparse import ArgumentParser
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from random import random
from typing import Iterable, List, NewType, Sequence, Set, Tuple
import re
from markdown import markdown
from bs4 import BeautifulSoup
from tenacity import Retrying, stop_after_attempt
from aiohttp import ClientSession
import urllib3
from tqdm.asyncio import tqdm
import random
from http import HTTPStatus

# it is ok, we use insecure https only to verify that the links are valid
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
Issue = NewType("Issue", str)
TaggedIssue = Tuple[Path, Issue]
Uri = NewType("Uri", str)
HttpUri = NewType("HttpUri", Uri)

_HTTP_MAX_GET_ATTEMPTS = 5
_HTTP_TIMEOUT_SECONDS = 10
_SKIP_TEXT_PATTERN = re.compile(r"<!--\s+no\s+verify-links", re.IGNORECASE)
# TODO: unreferenced bookmarks


def _line_of_match(match: re.Match, origin_text: str) -> int:
    return (
        #  count all newlines in the text before the given match
        len(_NEWLINE_PATTERN.findall(origin_text, 0, match.start(0)))
        + 1  # adding one because line count starts from 1 and not 0
    )


def _query_all_docs(directory: Path) -> Set[Path]:
    return set(directory.rglob("**/*.md")) | set(directory.rglob("**/*.htm*"))


def _should_skip_text(text: str) -> bool:
    return bool(_SKIP_TEXT_PATTERN.search(text))


def _find_all_uris(html: str) -> Iterable[Uri]:
    for a in BeautifulSoup(html, "html.parser").findAll("a"):
        uri = a.get("href")
        if uri:
            yield Uri(uri.strip())


def _is_http_uri(uri: Uri) -> bool:
    return uri.startswith("http:") or uri.startswith("https:")


def _is_mail_uri(uri: Uri) -> bool:
    return uri.startswith("mailto")


async def _uri_availability_issues(uri: HttpUri) -> Sequence[Issue]:
    try:
        for attempt in Retrying(stop=stop_after_attempt(_HTTP_MAX_GET_ATTEMPTS)):
            with attempt:
                async with ClientSession() as session:
                    # TODO: check response code
                    with closing(
                        await session.get(uri, timeout=_HTTP_TIMEOUT_SECONDS, ssl=False)
                    ) as response:
                        match response.status:
                            case HTTPStatus.OK | HTTPStatus.FORBIDDEN:
                                return []  # no issues
                            case HTTPStatus.TOO_MANY_REQUESTS:
                                await asyncio.sleep(
                                    random.randint(20, 30)
                                )  # sleep so after retry we will not have rate limiting
                                raise RuntimeError("Rate limited")
                            case _:
                                return [
                                    Issue(
                                        f"GET {repr(uri)} returned "
                                        f"status code {response.status}"
                                    )
                                ]
    except Exception:  # noqa
        return [Issue(f"Could Not access {repr(uri)}")]


async def _http_uri_issue(uri: HttpUri) -> Sequence[Issue]:
    return await _uri_availability_issues(uri)


async def _uri_issues(uri: Uri) -> Sequence[Issue]:
    if _is_http_uri(uri):
        return await _http_uri_issue(HttpUri(uri))
    elif _is_mail_uri(uri):
        return []  # this uri SHOULD NOT have any issues
    else:
        return []


async def _html_issues(html: str) -> Iterable[Issue]:
    if not _should_skip_text(html):
        return [
            issue
            for issues in await asyncio.gather(
                *[_uri_issues(uri) for uri in _find_all_uris(html)]
            )
            for issue in issues
        ]
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


def read_html_text(path: Path) -> str:
    if path.name.endswith(".md"):
        return markdown(path.read_text())  # Convert markdown to html
    else:
        return path.read_text()


async def _query_file_issues(path: Path) -> Sequence[TaggedIssue]:
    result: List[TaggedIssue] = []
    for issue in await _html_issues(read_html_text(path)):
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
parser.add_argument("root")
args = parser.parse_args()
import asyncio


async def main():
    issues = list(await _query_directory_issues(Path(args.root)))
    if issues:
        _print_issues(issues)
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    # Need async because we perform alot of http requests.
    loop = asyncio.get_running_loop()
    loop.run_until_complete(main())
