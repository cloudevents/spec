#!python
from argparse import ArgumentParser
from pathlib import Path
from typing import Iterable, NewType, Sequence, Set, Tuple
import re

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

Issue = NewType("Issue", str)
TaggedIssue = Tuple[Path, Issue]


def _line_of_match(match: re.Match, origin_text: str) -> int:
    return (
        #  count all newlines in the text before the given match
        len(_NEWLINE_PATTERN.findall(origin_text, 0, match.start(0)))
        + 1  # adding one because line count starts from 1 and not 0
    )


def _query_all_docs(directory: Path) -> Set[Path]:
    return set(directory.rglob("**/*.md")) | set(directory.rglob("**/*.htm*"))


def _issue(match: re.Match, origin_text: str, issue_message: str) -> Issue:
    return Issue(f"line {_line_of_match(match, origin_text)}: {issue_message}")


def _is_text_capitalized(text: str) -> bool:
    return text == text.upper()


def _should_skip_text(text: str):
    return "<!-- no verify-specs -->" in text


def _text_issues(text: str) -> Iterable[Issue]:
    if not _should_skip_text(text):
        for match in _BANNED_PHRASES_PATTERN.finditer(text):
            yield _issue(match, text, f"{repr(match.group(0))} is banned")
        for match in _PHRASES_THAT_MUST_BE_CAPITALIZED_PATTERN.finditer(text):
            phrase = match.group(0)
            if not _is_text_capitalized(phrase):
                yield _issue(
                    match,
                    text,
                    f"{repr(phrase)} MUST be capitalized ({repr(phrase.upper())})",
                )


def test_text_issues():
    assert (
        set(
            _text_issues(
                """
                Hello World this MUST be a test
                SHOULD NOT be something
                should be CloudEvents 
                CloudEvent
                Cloud
                Event
                Cloud Events 
                Cloud
                Events 
                must
                MAY
                MUST
                ShOULD        nOt
                mAy
                Optionally
                "required"
                """
            )
        )
        == {
            "line 6: 'Cloud\\n                Event' is banned",
            "line 8: 'Cloud Events' is banned",
            "line 9: 'Cloud\\n                Events' is banned",
            "line 4: 'should' MUST be capitalized ('SHOULD')",
            "line 11: 'must' MUST be capitalized ('MUST')",
            "line 14: 'ShOULD        nOt' MUST be capitalized ('SHOULD        NOT')",
            "line 15: 'mAy' MUST be capitalized ('MAY')",
        }
    )


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


def _query_issues(directory: Path, verbose: bool) -> Iterable[TaggedIssue]:
    for path in sorted(_query_all_docs(directory)):
        if verbose:
            print(f"> {path}")
        for issue in _text_issues(path.read_text()):
            tagged_issue = (path, issue)
            if verbose:
                _print_issue(tagged_issue)
            yield tagged_issue


parser = ArgumentParser()
parser.add_argument("root")
parser.add_argument("-v", dest="verbose", action="store_true")
args = parser.parse_args()
test_text_issues()

issues = list(_query_issues(Path(args.root), verbose=args.verbose))
if issues:
    _print_issues(issues)
    exit(1)
else:
    exit(0)
