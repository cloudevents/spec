import json
from pathlib import Path

import pytest
from jsonschema import Draft7Validator

_SCHEMA_PATH = (
    Path(__file__).parent.parent / "cloudevents" / "formats" / "cloudevents.json"
)
_REQUIRED_ATTRIBUTES = {
    "specversion": "1.0",
    "type": "com.example.someevent",
    "source": "/mycontext",
    "id": "A234-1234-1234",
}


@pytest.fixture(scope="module")
def validator():
    schema = json.loads(_SCHEMA_PATH.read_text())
    Draft7Validator.check_schema(schema)
    return Draft7Validator(schema)


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"data": {"key": "value"}},
        {"data": None},
        {"data_base64": "Zm9vYg=="},
    ],
)
def test_valid_event(validator, payload):
    assert validator.is_valid({**_REQUIRED_ATTRIBUTES, **payload})


@pytest.mark.parametrize(
    "payload",
    [
        {"data": {"key": "value"}, "data_base64": "Zm9vYg=="},
        {"data": None, "data_base64": "Zm9vYg=="},
    ],
)
def test_data_and_data_base64_are_mutually_exclusive(validator, payload):
    assert not validator.is_valid({**_REQUIRED_ATTRIBUTES, **payload})
