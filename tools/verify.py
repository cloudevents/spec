#!python
import asyncio
import re
from argparse import ArgumentParser
from contextlib import closing
from dataclasses import dataclass
from functools import lru_cache
from http import HTTPStatus
from pathlib import Path
from typing import Iterable, List, NewType, Optional, Sequence, Set, Tuple, TypeVar

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from markdown import markdown
from pymdownx import slugs
from tenacity import Retrying, stop_after_attempt
from tqdm.asyncio import tqdm

Issue = NewType("Issue", str)
TaggedIssue = Tuple[Path, Issue]
Uri = NewType("Uri", str)
HttpUri = NewType("HttpUri", Uri)
T = TypeVar("T")
HtmlText = NewType("HtmlText", str)
ExistingPath = NewType("ExistingPath", Path)
TranslationsDir = NewType("TranslationsDir", ExistingPath)

_TOOLS_DIR = Path(__file__).parent
_REPO_ROOT = _TOOLS_DIR.parent
_FAKE_DOCS_DIR = Path(__file__).parent / "fake-docs"
_FAKE_DOCS = set(_FAKE_DOCS_DIR.rglob("**/*"))
_LANGUAGES_DIR_NAME = "languages"
_ROOT_LANGUAGES_DIR = _REPO_ROOT / _LANGUAGES_DIR_NAME


@dataclass
class Settings:
    excluded_paths: Set[Path]
    http_max_get_attemps: int = 5
    http_timeout_seconds: int = 10


_SKIP_TEXT_PATTERN = re.compile(
    r"<!--\s*no[\s-]+verify[\s-]+(?P<type>\w+)[\s-]*-->", re.IGNORECASE
)
_NEWLINE_PATTERN = re.compile(r"\n")
_MARKDOWN_BOOKMARK_PATTERN = re.compile(r"\[[^\?=].+?\]\[.+?\]", re.IGNORECASE)
_PHRASES_THAT_MUST_BE_CAPITALIZED_PATTERN = re.compile(
    r"(?<!`)(MUST(\s+NOT)?|"
    # ignore the "required" in the jsonschema of the json-format.md
    r'(?<![`"])REQUIRED(?!")|'
    r"(?<!mar)SHALL(\s+NOT)?|"  # ignore the word "marshall"
    r"(?<!`)SHOULD(\s+NOT)?|"
    r"(?<!`)RECOMMENDED|"
    r"(?<![`A-Z])MAY(?![A-Z])|"
    r"(?<![`A-Z])OPTIONAL(?![A-Z])"  # ignore the word "optionally"
    r")",
    flags=re.IGNORECASE,  # we want to catch all the words that were not capitalized
)
_BANNED_PHRASES_PATTERN = re.compile(r"Cloud\s+Events?", flags=re.IGNORECASE)
_LANGUAGES_DIR_PATTERN = re.compile(f"[/^]{_LANGUAGES_DIR_NAME}[/$]")


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


def _should_skip_plain_text_issues(text: str) -> bool:
    return _skip_type(text) == "specs"


def _plain_text_issues(text: str) -> Iterable[Issue]:
    if not _should_skip_plain_text_issues(text):
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


def _all_docs(directory: Path, excluded_paths: Set[Path]) -> Set[ExistingPath]:
    excluded_paths = {path.absolute() for path in excluded_paths}
    return {
        ExistingPath(path)
        for path in set(directory.rglob("**/*.md")) | set(directory.rglob("**/*.htm*"))
        if path.absolute() not in excluded_paths
    }


def _skip_type(text: str) -> Optional[str]:
    match = _SKIP_TEXT_PATTERN.search(text)
    if match:
        return match.groupdict().get("type")
    return None


def _find_all_uris(html: HtmlText) -> Iterable[Uri]:
    for a in _html_parser(html).findAll("a"):
        uri = a.get("href")
        if uri:
            yield Uri(uri.strip())


async def _uri_availability_issues(uri: HttpUri, settings: Settings) -> Sequence[Issue]:
    if "example.com"  in uri: return []
    if "ietf.org"     in uri: return []
    if "rfc-edit.org" in uri: return []

    try:
        for attempt in Retrying(stop=stop_after_attempt(settings.http_max_get_attemps)):
            with attempt:
                async with ClientSession() as session:
                    with closing(
                        await session.get(
                            uri, timeout=settings.http_timeout_seconds, ssl=False
                        )
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
    return Issue(f"{path.as_posix()} does not contain {repr('#' + segment)} segment")


def _missing_file_issue(path: Path) -> Issue:
    return Issue(f"{path.as_posix()} does not exist")


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


async def _uri_issues(uri: Uri, path: Path, settings: Settings) -> Sequence[Issue]:
    schema = uri.split(":")[0]
    match schema:
        case "http" | "https":
            return await _uri_availability_issues(HttpUri(uri), settings)
        case "mailto":
            return []  # mail URIs cannot have issues
        case _:  # assuming it is a local path markdown reference
            return _local_path_uri_issues(uri, path)


def _undefined_bookmark_issues(html: HtmlText) -> Iterable[Issue]:
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


def _flatten(lists: List[List[T]]) -> List[T]:
    return [item for a_list in lists for item in a_list]


def _should_skip_html_issues(html: HtmlText) -> bool:
    return _skip_type(html) == "links"


async def _html_issues(path: Path, settings: Settings) -> Iterable[Issue]:
    html = read_html_text(path)

    if _should_skip_html_issues(html):
        return []

    return _flatten(
        await asyncio.gather(
            *[_uri_issues(uri, path, settings) for uri in _find_all_uris(html)]
        )
    ) + list(_undefined_bookmark_issues(html))


def _print_issue(tagged_issue: TaggedIssue) -> None:
    path, issue = tagged_issue
    print(f"{path}: {issue}")


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


def _render_markdown_to_html(markdown_text: str) -> HtmlText:
    return HtmlText(
        markdown(
            markdown_text,
            extensions=["toc"],  # need toc so headers will generate ids
            extension_configs={
                # we need this for unicode titles
                "toc": {"slugify": slugs.slugify(case="lower", percent_encode=False)}
            },
        )
    )


@lru_cache
def read_html_text(path: Path) -> HtmlText:
    if path.name.endswith(".md"):
        return _render_markdown_to_html(_read_text(path))
    else:
        return HtmlText(_read_text(path))  # assuming given file is already html


def _is_english_file(path: Path) -> bool:
    return not bool(_LANGUAGES_DIR_PATTERN.search(str(path.absolute().as_posix())))


def _is_english_text(text: str) -> bool:
    try:
        text.encode(encoding="utf-8").decode("ascii")
    except UnicodeDecodeError:
        return False
    else:
        return True


def _is_translation_file(path: Path) -> bool:
    return not _is_english_file(
        path
    )  # assuming every non english file is a translation


def _is_root_languages_dir(path: Path) -> bool:
    return path.absolute() == _ROOT_LANGUAGES_DIR.absolute()


def _translations_directory(path: Path) -> Optional[TranslationsDir]:
    if not _is_english_file(path):
        return None  # non english files do not have a translation directory
    languages_dir = path.parent / _LANGUAGES_DIR_NAME
    if languages_dir.exists() and not _is_root_languages_dir(languages_dir):
        return TranslationsDir(ExistingPath(languages_dir))  # found dir, end recursion
    if path.parent == path:  # reached end of path, end recursion
        return None
    return _translations_directory(path.parent)


def _relative_to_absolute(a: Path, b: Path) -> Path:
    return a.absolute().relative_to(b.absolute())


def _expected_language_codes(my_dir: TranslationsDir):
    return [path.name for path in my_dir.glob("*") if path.is_dir()]


def _expected_translation_files(path: Path) -> Sequence[Path]:
    if not _is_english_file(path):
        return []  # non english files are not expected to be translated
    translations_directory = _translations_directory(path)
    if translations_directory is None:
        return []  # no translations dir - no translation is expected

    # assuming translation directory located in the project dir root
    project_dir = translations_directory.parent
    return [
        translations_directory / lang_code / _relative_to_absolute(path, project_dir)
        for lang_code in _expected_language_codes(translations_directory)
    ]


def _should_skip_translation_issues(path: Path) -> bool:
    return _skip_type(_read_text(path)) == "translation"


def _translation_issues(path: Path) -> Iterable[Issue]:
    if _should_skip_translation_issues(path):
        return []
    if not _is_english_file(path):
        return []
    for translation_file in _expected_translation_files(path):
        if not translation_file.exists():
            yield Issue(
                f"Translation file {translation_file.as_posix()} does not exist"
            )


def _tag_issues(issues: Iterable[Issue], tag: Path) -> Sequence[TaggedIssue]:
    return [(tag, issue) for issue in issues]


def _existing_paths(paths: Iterable[Path]) -> Sequence[ExistingPath]:
    return [ExistingPath(path) for path in paths if path.exists()]


def _files_that_should_have_matching_titles(path: Path) -> Iterable[Path]:
    yield from _expected_translation_files(path)
    if path.name == "spec.md":
        yield path.parent / "README.md"


def _file_title(path: ExistingPath) -> str:
    return _read_text(path).splitlines()[0].rstrip()


def _non_matching_titles_issue(path_a: ExistingPath, path_b: ExistingPath) -> Issue:
    return Issue(
        f"title ({repr(_file_title(path_a))}) does not match "
        f"the title of {path_b.as_posix()} ({repr(_file_title(path_b))})"
    )


def _titles_match(title_a: str, title_b: str) -> bool:
    if _is_english_text(title_a) and _is_english_text(title_b):
        return title_a == title_b
    else:
        return True  # Translations probably have specific titles


def _title_issues(path: ExistingPath) -> Iterable[Issue]:
    for other_path in _existing_paths(_files_that_should_have_matching_titles(path)):
        if not _titles_match(_file_title(path), _file_title(other_path)):
            yield _non_matching_titles_issue(path, other_path)


async def _file_issues(path: ExistingPath, settings: Settings) -> Sequence[TaggedIssue]:
    return _tag_issues(
        list(await _html_issues(path, settings))
        + list(_plain_text_issues(_read_text(path)))
        + list(_translation_issues(path))
        + list(_title_issues(path)),
        tag=path,
    )


async def _directory_issues(
    directory: Path, settings: Settings
) -> Iterable[TaggedIssue]:
    return _flatten(
        await tqdm.gather(
            *[
                _file_issues(path, settings)
                for path in sorted(_all_docs(directory, settings.excluded_paths))
            ],
            unit="files",
        )
    )


def _cache_files(path: Path) -> Set[Path]:
    return set(path.rglob("**/.pytest_cache/**/*"))


async def main():
    parser = ArgumentParser()
    parser.add_argument("root", default=".", nargs="?")
    args = parser.parse_args()
    root = Path(args.root)
    settings = Settings(excluded_paths=_FAKE_DOCS | _cache_files(root))
    issues = list(await _directory_issues(root, settings))
    if issues:
        _print_issues(issues)
        exit(1)
    else:
        print("Spec verification succeeded")
        exit(0)


if __name__ == "__main__":
    # Need async because we perform alot of http requests.
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
