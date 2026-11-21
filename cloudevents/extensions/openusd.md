# OpenUSD

An event reporting pump telemetry can link to the pump's
[OpenUSD](https://openusd.org/) asset so a Consumer can locate the pump in
a scene. The event's [`describedby`](descriptor.md#describedby) URL points to a
[Descriptor](descriptor.md) with a `usdasset` entry. A *prim* is an element
in the OpenUSD scene, such as the object that represents the pump. The
following Descriptor associates the event with the `/Pump7` prim:

```json
{
  "descriptorid": "pump7-geometry",
  "versionid": "1",
  "entries": {
    "geometry": {
      "class": "usdasset",
      "url": "https://assets.example/pump7.usda",
      "primpath": "/Pump7"
    }
  }
}
```

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is
used. For example, an attribute marked as "REQUIRED" needs to be included
when the event uses this extension and meets the stated conditions.

## Attributes

### describedby

[`describedby`](descriptor.md#describedby) is REQUIRED to associate an
event with an OpenUSD asset through this extension. It identifies the
Descriptor that supplies the asset entries. Core attributes retain their
CloudEvents meanings.

## Asset selection

An entry with class `usdasset` MUST link to the OpenUSD asset itself at
`url`. The Consumer can use the linked asset or the entry's bundled
`document`.

A publication profile is the agreed set of rules for using the Descriptor.
It MAY select several asset entries. If it needs one,
the Consumer MUST use the exact entry name specified by the profile or the
unique `usdasset` entry if the profile supplies no name. The Consumer MUST
report a missing, invalid, ambiguous, or unavailable asset when needed. It
MUST NOT infer a selection from `subject`, a filename, or entry order.

### primpath

- Type: String
- Description: The [absolute OpenUSD prim path][Prim Path] within the stage
  composed from the asset at `url`. The stage is the scene formed from
  the asset and its dependencies. The path associates the whole event
  with that prim and anchors any field mappings.
- Constraints:
  - OPTIONAL. Omission selects the asset as a whole.
  - If present, MUST identify an existing prim in that stage. Null, empty,
    root (`/`), relative, and property paths are invalid, as are paths
    containing variant selections.
  - The Consumer MUST resolve the value as an OpenUSD path. If resolution
    fails, it MUST report the failure and leave the prim unselected.

### Field mappings

A `usdasset` entry can associate individual JSON payload fields with
descendants of the anchor prim. If `fieldmode` or `fieldmappings` is
present, `primpath` is REQUIRED. The Consumer MUST derive field associations
only from these members. The event-level association still comes from
`primpath`. Writing USD property values is outside the scope of this extension.

The OPTIONAL `fieldmappings` array contains objects with two REQUIRED
string members:

| Member | Meaning |
| --- | --- |
| `field` | A non-empty [RFC 6901 JSON Pointer][JSON Pointer] in string form, rooted at CloudEvents `data`. |
| `prim` | A relative OpenUSD prim path to an existing descendant of the anchor. Absolute paths, parent traversal (`..`), property paths, and paths containing variant selections are invalid. |

Duplicate `field` pointers are invalid. Apply each mapping independently
of its position in the array. If an event omits a field, skip its mapping
for that event and leave any prior value unchanged. The Consumer MUST
report an invalid mapping or an unresolved explicit prim target and leave
that field unmapped.

The OPTIONAL string `fieldmode` accepts only `"byname"`. In this mode,
the Consumer matches each top-level member of a JSON object in `data` to a
direct child of the anchor with the exact same name. An explicit mapping for
that field takes precedence. When `fieldmode` is omitted, only explicit
mappings apply. Fields with neither kind of match stay unmapped.

Mapping an OpenUSD prim to a WoT affordance is outside the scope of this
extension. Resolve asset dependencies under OpenUSD rules even when a
[Descriptor bundle](descriptor.md#bundled-document) supplies the asset.

The [OpenUSD entry schema](openusd.schema.json) checks entry shape.
Consumers using the entry verify path syntax, targets, and pointer
uniqueness under the rules above.

## Examples

The following event reports Pump 7 telemetry in HTTP binary mode. Its
`ce-describedby` header identifies the Descriptor that selects the asset and
its pump prim.

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

The Descriptor's `geometry` entry uses an xRegistry document-view URL for
the asset version and selects `/Pump7` in that asset. The stage contains
`/Pump7/Sensors/PressureGauge`, `/Pump7/pressure`,
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

The explicit mapping takes precedence and associates `pressure` with
`/Pump7/Sensors/PressureGauge`. By-name matching associates `speed` with
`/Pump7/speed`. The `status` field stays unmapped. Without either field-mapping
member, the event would still describe `/Pump7` as a whole.

## Security Considerations

Follow the [Descriptor retrieval policy](descriptor.md#security-considerations)
for the asset. Authorize access to each dependency separately and apply
resource limits during resolution.

[Prim Path]: https://openusd.org/release/api/class_sdf_path.html
[JSON Pointer]: https://www.rfc-editor.org/rfc/rfc6901
