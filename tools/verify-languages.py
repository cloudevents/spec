#!python
from argparse import ArgumentParser
from ctypes.wintypes import tagRECT
from pathlib import Path
import re
from typing import Dict, Iterator, NewType, Sequence, Set

expected_paths: Set[Path] = set()
EnglishDirectory = NewType("EnglishDirectory", Path)
_SETTINGS = {
    "cloudevents": ["zh-CN", "he"],
    "cesql": ["zh-CN"],
    "discovery": ["zh-CN"],
    "docs": ["zh-CN"],
    "pagination": ["zh-CN"],
    "schemaregistry": ["zh-CN"],
    "subscriptions": ["zh-CN"],
}


def _language_directory(directory: EnglishDirectory, language_code: str) -> Path:
    return directory / "languages" / language_code


def _query_all_markdowns(directory: Path) -> Set[Path]:
    return set(directory.rglob("**/*.md"))


def _query_english_markdowns(directory: EnglishDirectory) -> Set[Path]:
    return _query_all_markdowns(directory) - _query_all_markdowns(
        directory / "languages"
    )


def _query_missing_paths(paths: Set[Path]) -> Set[Path]:
    return {path for path in paths if not path.exists()}


def _query_expected_paths(
    root_directory: Path, settings: Dict[str, Sequence[str]]
) -> Iterator[Path]:
    for project_name, language_codes in settings.items():
        directory = EnglishDirectory(root_directory / project_name)
        for markdown in _query_english_markdowns(directory):
            for language_code in language_codes:
                yield Path(
                    re.sub(
                        f"^{directory}",
                        str(_language_directory(directory, language_code)),
                        str(markdown),
                    )
                )


parser = ArgumentParser()
parser.add_argument("root")
parser.add_argument("-v", dest="verbose", action="store_true")
args = parser.parse_args()

missing_paths = _query_missing_paths(_query_expected_paths(Path(args.root), _SETTINGS))

if args.verbose:
    for path in missing_paths:
        print(f"{path} is missing")

if missing_paths:
    exit(1)
else:
    exit(0)
