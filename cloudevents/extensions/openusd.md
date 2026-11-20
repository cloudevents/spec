# OpenUSD

This profile defines how an event's [Descriptor](descriptors.md) identifies
an [OpenUSD](https://openusd.org/) asset. It adds no CloudEvents attributes
and does not change `source` or `subject`.

The keywords "MUST" and "MAY" have the meanings in
[RFC 2119](https://tools.ietf.org/html/rfc2119).

## Asset selection

An entry with class `usdasset` MUST link to an OpenUSD asset at `url`.
When an xRegistry server hosts the asset, the Publisher MUST use the
document-view URL, not the Registry metadata URL. Use the asset directly
or from the entry's bundled `document`.

A profile MAY select several asset entries. If it needs one, use the
exact entry name specified by the profile, or the unique `usdasset` entry
if it specifies none. The Consumer MUST report a missing, invalid,
ambiguous or unavailable asset when needed. It MUST NOT infer a selection
from the CloudEvents `subject` string, an asset filename or map order.

This profile does not select a prim or define a mapping between a prim
and a WoT affordance. A profile that needs either operation defines it
explicitly. Asset dependencies follow OpenUSD resolution rules and are
not automatically included in a Descriptor bundle.

For example, the `geometry` entry identifies Pump 7's asset version:

```json
{
  "descriptorid": "pump7-geometry",
  "versionid": "1",
  "entries": {
    "geometry": {
      "class": "usdasset",
      "url": "https://assets.example/usdassetgroups/line1/usdassets/pump7/versions/2"
    }
  }
}
```

## Security considerations

Follow the [Descriptor retrieval policy](descriptors.md#security-considerations)
for the asset and apply authorization and resource limits to its dependencies.
Access to a Descriptor does not grant access to either.
