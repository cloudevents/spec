#!python
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, NewType, Sequence, Set, Tuple
import re
from markdown import markdown
from bs4 import BeautifulSoup
from tenacity import Retrying, stop_after_attempt
from aiohttp import ClientSession
import urllib3

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


async def _uri_availability_issues(uri: HttpUri) -> Iterable[Issue]:
    try:
        for attempt in Retrying(stop=stop_after_attempt(_HTTP_MAX_GET_ATTEMPTS)):
            with attempt:
                async with ClientSession() as session:
                    # TODO: check response code
                    response = await session.get(
                        uri, timeout=_HTTP_TIMEOUT_SECONDS, ssl=False
                    )
                    response.close()
    except Exception as e:
        return [Issue(f"Could Not access {repr(uri)}: due to {e.__class__}({e})")]
    else:
        return []


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


async def _query_issues(directory: Path, verbose: bool) -> Iterable[TaggedIssue]:
    result: List[TaggedIssue] = []

    for path in sorted(_query_all_docs(directory)):
        if verbose:
            print(f"> {path}")

        if path.name.endswith(".md"):
            html = markdown(path.read_text())
        else:
            html = path.read_text()
        for issue in await _html_issues(html):
            tagged_issue = (path, issue)
            if verbose:
                _print_issue(tagged_issue)
            result.append(tagged_issue)
    return result


parser = ArgumentParser()
parser.add_argument("root")
parser.add_argument("-v", dest="verbose", action="store_true")
args = parser.parse_args()
import asyncio


async def main():
    issues = list(await _query_issues(Path(args.root), verbose=args.verbose))
    if issues:
        _print_issues(issues)
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())