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
  composed from the asset selected by `url`.
- Constraints:
  - OPTIONAL. Omission selects the asset without selecting an individual
    prim.
  - If present, MUST identify an existing prim in that stage. Null, empty,
    root (`/`), relative, and property paths are invalid, as are paths
    containing variant selections.
  - The Consumer MUST treat the value as an OpenUSD path, not a URL
    fragment or a CloudEvents subject selector. If it cannot resolve the
    path, it MUST report the failure and MUST NOT substitute another prim.

This extension does not define a mapping between an OpenUSD prim and a WoT
affordance. Asset dependencies follow OpenUSD resolution rules and are not
automatically included in a Descriptor bundle.

## Examples

The following event reports Pump 7 telemetry in HTTP binary mode. Its
`ce-describedby` header identifies the Descriptor that selects the asset and
the pressure gauge prim. The `ce-subject` value is not used for that selection.

```http
POST /events HTTP/1.1
Host: consumer.example
Content-Type: application/json
Content-Length: 16
ce-specversion: 1.0
ce-id: pump7-pressure-47
ce-source: urn:example:asset:pump7
ce-type: com.example.pump.pressure
ce-subject: pump7-pressure
ce-describedby: https://registry.example/descriptorgroups/streams/descriptors/pump7-geometry/versions/1

{"pressure":4.5}
```

The Descriptor's `geometry` entry selects `/Pump7/PressureGauge` in the
linked asset version:

```json
{
  "descriptorid": "pump7-geometry",
  "versionid": "1",
  "entries": {
    "geometry": {
      "class": "usdasset",
      "url": "https://assets.example/usdassetgroups/line1/usdassets/pump7/versions/2",
      "primpath": "/Pump7/PressureGauge"
    }
  }
}
```

## Security Considerations

Follow the [Descriptor retrieval policy](descriptors.md#security-considerations)
for the asset and apply authorization and resource limits to its dependencies.
Access to a Descriptor does not grant access to either.

[Prim Path]: https://openusd.org/release/api/class_sdf_path.html
