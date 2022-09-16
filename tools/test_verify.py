from verify import _text_issues, _SKIP_TEXT_PATTERN
import pytest


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


@pytest.mark.parametrize(
    "given, expected",
    [
        (
            "sadnakskd bad <!--  no verify specs --> dasdasd",
            "<!--  no verify specs -->",
        ),
        (
            "sadnakskd bad <!--\t no-verify-docs --> dasdasd",
            "<!--\t no-verify-docs -->",
        ),
        ("sadnakskd bad <!--no-verify-specs--> dasdasd", "<!--no-verify-specs-->"),
    ],
)
def test_skip_text(given, expected):
    assert _SKIP_TEXT_PATTERN.search(given).group() == expected
