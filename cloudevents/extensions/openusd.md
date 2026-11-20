# OpenUSD

This extension associates a CloudEvent with an [OpenUSD](https://openusd.org/)
asset or a prim within it. It uses the
[Descriptor Reference extension](descriptors.md) and adds no CloudEvents
attributes or headers. Core attributes, including `source` and `subject`,
retain their meanings.

## Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "MAY", and "OPTIONAL" are
to be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).
These requirements apply only to events using this extension.

## Attributes

### describedby

Use the existing [`describedby`](descriptors.md#describedby) attribute to
identify the Descriptor that supplies OpenUSD context. In HTTP binary
content mode it is carried in the `ce-describedby` header. If `describedby`
is absent, this extension supplies no OpenUSD context.

## Asset selection

An entry with class `usdasset` MUST link to an OpenUSD asset at `url`.
When an xRegistry server hosts the asset, the Publisher MUST use the
document-view URL, not the Registry metadata URL. The Consumer can use the
linked asset or the entry's bundled `document`.

A publication profile MAY select several asset entries. If it needs one,
the Consumer MUST use the exact entry name specified by the profile or the
unique `usdasset` entry if the profile supplies no name. The Consumer MUST
report a missing, invalid, ambiguous, or unavailable asset when needed. It
MUST NOT infer a selection from `subject`, a filename, or entry order.

### primpath

- Type: String
- Description: The [absolute OpenUSD prim path][Prim Path] within the stage
  composed from the asset selected by `url`. It associates the event as a
  whole with that prim and anchors any field mappings.
- Constraints:
  - OPTIONAL. Omission selects the asset without selecting an individual
    prim.
  - If present, MUST identify an existing prim in that stage. Null, empty,
    root (`/`), relative, and property paths are invalid, as are paths
    containing variant selections.
  - The Consumer MUST treat the value as an OpenUSD path, not a URL
    fragment or a CloudEvents subject selector. If it cannot resolve the
    path, it MUST report the failure and MUST NOT substitute another prim.

### Field mappings

A `usdasset` entry can associate individual JSON payload fields with
descendants of the anchor prim. If `fieldmode` or `fieldmappings` is
present, `primpath` is REQUIRED. With neither member, the Consumer MUST NOT
infer field associations. Field associations do not change the event-level
association or specify writes to USD properties.

The OPTIONAL `fieldmappings` array contains objects with two REQUIRED
string members:

| Member | Meaning |
| --- | --- |
| `field` | A nonempty [RFC 6901 JSON Pointer][JSON Pointer] rooted at CloudEvents `data`, in string form, not a URI fragment. |
| `prim` | A relative OpenUSD prim path to an existing descendant of the anchor. Absolute paths, parent traversal (`..`), property paths, and paths containing variant selections are invalid. |

Duplicate `field` pointers are invalid. Array order does not affect
selection. A field absent from an event, such as an omitted delta frame
field, produces no association for that event and does not clear a prior
value. The Consumer MUST report an invalid mapping or an unresolved explicit
prim target rather than infer a replacement.

The OPTIONAL string `fieldmode` accepts only `"byname"`. In this mode,
the Consumer matches each top-level member of a JSON object in `data` to a
direct child of the anchor with the exact same name. An explicit mapping for
that field takes precedence. Without `"byname"`, only explicit mappings apply.
A field without a matching child or an explicit mapping stays unmapped; it
does not fall back to the anchor.

This extension does not define a mapping between an OpenUSD prim and a WoT
affordance. Asset dependencies follow OpenUSD resolution rules and are not
automatically included in a Descriptor bundle.

## Examples

The following event reports Pump 7 telemetry in HTTP binary mode. Its
`ce-describedby` header identifies the Descriptor that selects the asset and
its pump prim. The `ce-subject` value is not used for that selection.

```http
POST /events HTTP/1.1
Host: consumer.example
Content-Type: application/json
Content-Length: 43
ce-specversion: 1.0
ce-id: pump7-telemetry-47
ce-source: urn:example:asset:pump7
ce-type: com.example.pump.telemetry
ce-subject: pump7
ce-describedby: https://registry.example/descriptorgroups/streams/descriptors/pump7-geometry/versions/1

{"pressure":4.5,"speed":1200,"status":"ok"}
```

The Descriptor's `geometry` entry selects `/Pump7` in the linked asset
version. The stage contains `/Pump7/Sensors/PressureGauge`, `/Pump7/pressure`,
and `/Pump7/speed`, but no `/Pump7/status`:

```json
{
  "descriptorid": "pump7-geometry",
  "versionid": "1",
  "entries": {
    "geometry": {
      "class": "usdasset",
      "url": "https://assets.example/usdassetgroups/line1/usdassets/pump7/versions/2",
      "primpath": "/Pump7",
      "fieldmode": "byname",
      "fieldmappings": [
        { "field": "/pressure", "prim": "Sensors/PressureGauge" }
      ]
    }
  }
}
```

The explicit mapping associates `pressure` with `/Pump7/Sensors/PressureGauge`
instead of `/Pump7/pressure`. By-name matching associates `speed` with
`/Pump7/speed`. The `status` field stays unmapped. Without either field-mapping
member, the event would still describe `/Pump7` as a whole.

## Security Considerations

Follow the [Descriptor retrieval policy](descriptors.md#security-considerations)
for the asset and apply authorization and resource limits to its dependencies.
Access to a Descriptor does not grant access to either.

[Prim Path]: https://openusd.org/release/api/class_sdf_path.html
[JSON Pointer]: https://www.rfc-editor.org/rfc/rfc6901
