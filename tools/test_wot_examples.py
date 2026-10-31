import json
import re
from pathlib import Path
from urllib.parse import quote, unquote_to_bytes, urlsplit


EXTENSIONS = Path(__file__).resolve().parents[1] / "cloudevents" / "extensions"
TYPE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*")
SAFE_VALUE = "!$'()*,:@/?"


def _source_parameters(source):
    uri = urlsplit(source)
    assert uri.scheme == "wot-td"
    assert uri.hostname
    assert uri.username is None and uri.password is None
    assert "#" not in source
    parts = uri.query.split(";")
    assert len(parts) in (1, 2)
    values = {}
    for part in parts:
        name, separator, encoded = part.partition("=")
        assert separator and encoded and "=" not in encoded
        assert name not in values
        assert not re.search(r"%(?![0-9A-Fa-f]{2})", encoded)
        value = unquote_to_bytes(encoded).decode("utf-8", errors="strict")
        assert quote(value, safe=SAFE_VALUE) == encoded
        values[name] = value
    assert list(values) in (["wotid"], ["wotid", "wotversion"])
    return values


def _assert_wot_context(event):
    assert event["specversion"] == "1.0"
    assert event["id"]
    assert TYPE.fullmatch(event["type"])
    assert event["subject"] == "#" or event["subject"].startswith("#/")
    assert not {"wotid", "wotversion", "wotdigest"} & event.keys()
    return _source_parameters(event["source"])


def test_wot_json_examples_use_canonical_core_attributes():
    text = (EXTENSIONS / "wot.md").read_text(encoding="utf-8")
    examples = [
        json.loads(block)
        for block in re.findall(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    ]
    assert len(examples) == 2
    affordance, whole_thing = examples
    assert _assert_wot_context(affordance) == {
        "wotid": "urn:example:pump:7",
        "wotversion": "3.0.0",
    }
    assert _assert_wot_context(whole_thing) == {"wotid": "urn:example:pump:7"}
    assert affordance["subject"] == "#/properties/processData"
    assert affordance["type"] == "com.example.models.tm.pump.properties.processData"
    assert affordance["data"] == {"Speed": 1500, "Pressure": 4.5}
    assert whole_thing["subject"] == "#"
    assert whole_thing["type"] == "com.example.models.tm.pump"
    assert whole_thing["data"]["processData"] == affordance["data"]


def test_opcua_binary_example_retains_native_writer_and_uint32_sequence():
    text = (EXTENSIONS / "opcua.md").read_text(encoding="utf-8")
    section = text.split("### WoT and OPC UA telemetry message", 1)[1]
    example = section.split("```text", 1)[1].split("```", 1)[0]
    properties = example.split("------------- User Properties ----------------", 1)[1]
    properties, payload = properties.split("------------------ payload -------------------", 1)
    event = dict(
        line.split(": ", 1) for line in properties.strip().splitlines() if line.strip()
    )
    assert _assert_wot_context(event) == {
        "wotid": "urn:example:pump:7",
        "wotversion": "3.0.0",
    }
    assert event["type"] == "com.example.models.tm.pump.properties.processData"
    assert event["subject"] == "#/properties/processData"
    assert event["opcuapublisherid"] == "UInt16:12"
    assert event["opcuadatasetwritername"] == "PumpProcessData"
    assert "opcuadatasetwriterid" not in event
    assert event["opcuamessagetype"] == "ua-keyframe"
    assert event["opcuasequence"] == "4294967295"
    assert "sequence" not in event
    payload_json = payload.split("-----------------------------------------------", 1)[0]
    assert json.loads(payload_json) == {"Speed": 1500, "Pressure": 4.5}


def test_ua_only_sequence_examples_preserve_lexicographic_order():
    text = (EXTENSIONS / "opcua.md").read_text(encoding="utf-8")
    sections = [
        "### Telemetry message\n",
        "### Event message\n",
        "### Telemetry message with different Encoding\n",
    ]
    examples = [
        text.split(heading, 1)[1].split("\n### ", 1)[0] for heading in sections
    ]
    sequences = [
        re.search(r"^sequence: (\S+)$", example, re.MULTILINE).group(1)
        for example in examples
    ]
    sources = [
        re.search(r"^source: (\S+)$", example, re.MULTILINE).group(1)
        for example in examples
    ]
    assert sequences == ["0000000007", "0000000018", "0000003141"]
    assert [int(sequence) for sequence in sequences] == [7, 18, 3141]
    assert sources[0] == sources[1]
    assert sequences[0] < sequences[1]
