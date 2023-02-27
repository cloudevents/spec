from pathlib import Path, PurePosixPath
from re import Match
from typing import Optional

import pytest
from verify import (
    _BANNED_PHRASES_PATTERN,
    _FAKE_DOCS_DIR,
    _MARKDOWN_BOOKMARK_PATTERN,
    _PHRASES_THAT_MUST_BE_CAPITALIZED_PATTERN,
    _SKIP_TEXT_PATTERN,
    Settings,
    _directory_issues,
    _is_text_all_uppercase,
    _plain_text_issues,
    _render_markdown_to_html,
)


def test_text_issues():
    assert set(
        _plain_text_issues(
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
    ) == {
        "line 6: 'Cloud\\n                Event' is banned",
        "line 8: 'Cloud Events' is banned",
        "line 9: 'Cloud\\n                Events' is banned",
        "line 4: 'should' MUST be capitalized ('SHOULD')",
        "line 11: 'must' MUST be capitalized ('MUST')",
        "line 14: 'ShOULD        nOt' MUST be capitalized ('SHOULD        NOT')",
        "line 15: 'mAy' MUST be capitalized ('MAY')",
    }


@pytest.mark.parametrize(
    "given, expected",
    (
        (
            "sadnakskd bad <!--  no verify specs --> dasdasd",
            "<!--  no verify specs -->",
        ),
        (
            "sadnakskd bad <!--\t no-verify-docs --> dasdasd",
            "<!--\t no-verify-docs -->",
        ),
        ("sadnakskd bad <!--no-verify-specs--> dasdasd", "<!--no-verify-specs-->"),
    ),
)
def test_skip_text(given, expected):
    assert _SKIP_TEXT_PATTERN.search(given).group() == expected


def _maybe_group(match: Optional[Match]) -> Optional[str]:
    if match is None:
        return None
    else:
        return match.group()


@pytest.mark.parametrize(
    "given, expected",
    (
        (
            "sadnakskd bad [Hello][World] dasdasd",
            "[Hello][World]",
        ),
        (
            "sadnakskd bad [What is going][on]dasdasd",
            "[What is going][on]",
        ),
        ("This is [not] [a bookmark]", None),
    ),
)
def test_bookmark_pattern_matches_given_patterns(given, expected):
    assert _maybe_group(_MARKDOWN_BOOKMARK_PATTERN.search(given)) == expected


@pytest.mark.parametrize(
    "given, expected",
    (
        (
            "this sHouLd\n\nnot jsakhndja",
            "sHouLd\n\nnot",
        ),
        (
            "asdjkasbndkj optional asjdkjasjd",
            "optional",
        ),
        ("optionally", None),
        (" asd asd shall            not asdasdas", "shall            not"),
        ('asd "required" not asdasdas', None),
        ("this Must, handle commas", "Must"),
        ("this (must) handle braces", "must"),
        ("marshall is ok not to be matched", None),
        ("may be matched", "may"),
        ("maybe", None),
        ("`required`", None),
        (" dasa shall not asjdbajsbd", "shall not"),
        ("ds as must not asd ", "must not"),
    ),
)
def test_capitalization_phrases(given, expected):
    assert (
        _maybe_group(_PHRASES_THAT_MUST_BE_CAPITALIZED_PATTERN.search(given))
        == expected
    )


@pytest.mark.parametrize(
    "given, expected",
    (
        (
            "sad asd Cloud Events asd asd",
            "Cloud Events",
        ),
        (
            "sad asd Cloud Event asd asd",
            "Cloud Event",
        ),
        (
            "CloudEvent",
            None,
        ),
        (
            "CloudEvents",
            None,
        ),
        (
            "sad asd cloud\t\t\t  events asd asd",
            "cloud\t\t\t  events",
        ),
        (
            "sad asd cloud\nevent asd asd",
            "cloud\nevent",
        ),
        (
            "cloudevent",
            None,
        ),
        (
            "cloudevents",
            None,
        ),
    ),
)
def test_bookmark_pattern_matches_given_patterns(given, expected):
    assert _maybe_group(_BANNED_PHRASES_PATTERN.search(given)) == expected


def test_upper_text_must_be_detected_as_such():
    assert _is_text_all_uppercase("YES")


def test_non_upper_text_must_be_detected_as_such():
    assert not _is_text_all_uppercase("tHis Is NoT cOrRect")


def test_headers_must_be_rendered_with_ids():
    assert (
        _render_markdown_to_html("#Hello World")
        == '<h1 id="hello-world">Hello World</h1>'
    )


def test_rtl_unicode_must_be_rendered_in_the_id():
    assert (
        _render_markdown_to_html("#כותרת בעברית")
        == '<h1 id="כותרת-בעברית">כותרת בעברית</h1>'
    )


@pytest.mark.asyncio
async def test_app(monkeypatch):
    monkeypatch.chdir(str(Path(__file__).parent))
    assert {
        (PurePosixPath(path.as_posix()), issue)
        for path, issue in await _directory_issues(
            _FAKE_DOCS_DIR.absolute().relative_to(Path(".").absolute()),
            Settings(
                excluded_paths=set(), http_max_get_attemps=2, http_timeout_seconds=2
            ),
        )
    } == {
        (
            PurePosixPath("fake-docs/link-verification.md"),
            "Could Not access 'http://non-existing-website.sadkjaskldjalksjd'",
        ),
        (
            PurePosixPath("fake-docs/link-verification.md"),
            "'https://google.com/non-existing-page' was not found",
        ),
        (
            PurePosixPath("fake-docs/link-verification.md"),
            "fake-docs/README.md does not contain '#non-existing' segment",
        ),
        (
            PurePosixPath("fake-docs/link-verification.md"),
            "fake-docs/link-verification.md does not contain '#non-existing' segment",
        ),
        (
            PurePosixPath("fake-docs/link-verification.md"),
            "fake-docs/non-existing.md does not exist",
        ),
        (
            PurePosixPath("fake-docs/link-verification.md"),
            "line 23: Undefined markdown bookmark referenced ('[link to non existing "
            "bookmark][non-existing]')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            r"line 13: 'Cloud\n\nEvent' is banned",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 23: 'must' MUST be capitalized ('MUST')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 25: 'must NOT' MUST be capitalized ('MUST NOT')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            r"line 35: 'must\n\nnot' MUST be capitalized ('MUST\n\nNOT')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 39: 'sHoulD' MUST be capitalized ('SHOULD')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 41: 'should not' MUST be capitalized ('SHOULD NOT')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 43: 'optionaL' MUST be capitalized ('OPTIONAL')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 47: 'shall' MUST be capitalized ('SHALL')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 49: 'shall not' MUST be capitalized ('SHALL NOT')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 53: 'required' MUST be capitalized ('REQUIRED')",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 9: 'Cloud Event' is banned",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "line 9: 'Cloud Events' is banned",
        ),
        (
            PurePosixPath("fake-docs/README.md"),
            "Translation file fake-docs/languages/your-lang/README.md does not exist",
        ),
        (
            PurePosixPath("fake-docs/README.md"),
            "Translation file fake-docs/languages/my-lang/README.md does not exist",
        ),
        (
            PurePosixPath("fake-docs/link-verification.md"),
            "Translation file fake-docs/languages/your-lang/link-verification.md does"
            " not exist",
        ),
        (
            PurePosixPath("fake-docs/text-verification.md"),
            "Translation file fake-docs/languages/my-lang/text-verification.md does not"
            " exist",
        ),
        (
            PurePosixPath("fake-docs/yourspec/spec.md"),
            "title ('# Your Spec - Version 1.0.1') does not "
            "match the title of fake-docs/yourspec/README.md ('# His Spec - Version "
            "1.0.0')",
        ),
        (
            PurePosixPath("fake-docs/languages/your-lang/myspec/spec.md"),
            "title ('# Your Spec - Version"
            " 1.0.0') does not match the title of"
            " fake-docs/languages/your-lang/myspec/README.md ('# His Spec - Version"
            " 1.0.0')",
        ),
        (
            PurePosixPath("fake-docs/myspec/README.md"),
            "title ('# My Spec - Version 1.0.0') does not "
            "match the title of fake-docs/languages/your-lang/myspec/README.md ('# His "
            "Spec - Version 1.0.0')",
        ),
        (
            PurePosixPath("fake-docs/myspec/spec.md"),
            "title ('# My Spec - Version 1.0.0') does not"
            " match the title of fake-docs/languages/your-lang/myspec/spec.md ('# Your"
            " Spec - Version 1.0.0')",
        ),
    }
