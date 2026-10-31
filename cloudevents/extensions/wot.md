# Web of Things

This profile maps a [Web of Things Thing Description][TD] (TD) to CloudEvents
Core context attributes. The `source` identifies the Thing and, when provided,
a version of its resolved TD. The `subject` identifies the part of that TD
associated with the event, and the `type` names the event contract.

The profile defines no CloudEvents extension attributes or URI scheme.
Producers and Consumers agree on its use through a publication profile or out
of band. It does not define a transport binding, provision a Thing, or require
a particular registry implementation.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

The scope of these key words is limited to events using this profile. An
attribute marked REQUIRED here is not REQUIRED in every CloudEvent.

## Source

The Core [`source`](../spec.md#source) identifies a Thing within the Producer's
chosen context. It MUST contain the `wotid` query parameter and MAY contain
`wotversion` and additional parameters. This profile does not prescribe the URI
scheme or the rest of the URI-reference. Core permits relative URI-references
and recommends an absolute URI.

For example:

```text
https://factory.example.com/line1?wotid=urn:example:pump:7;wotversion=3.0.0;site=north
```

The `site` parameter is defined by the Producer, not this profile. An HTTPS
source is an identifier and is not necessarily a retrieval URL for a TD.

An MQTT source identifier can use the same query parameters:

```text
mqtt://site/line/cell/device/sensor?wotid=urn:example:sensor:7;wotversion=3.0.0
```

Another possible form is:

```text
wot-td://factory/line1?wotid=urn:example:pump:7;wotversion=3.0.0
```

This profile does not define the `wot-td` scheme or propose its registration.
The part of `source` outside the standardized parameters can identify a
topology, publisher, or another Producer-defined context. This profile does
not prescribe its structure or derive a TD retrieval location from it.

### Query syntax and encoding

The `source` query uses `;` as the parameter separator. This profile
standardizes two query parameters, not CloudEvents attributes: `wotid` is
REQUIRED and appears first; `wotversion` is OPTIONAL and, when present,
immediately follows `wotid`. Their names are case-sensitive and MUST appear
literally. Each MUST use `name=value` with a non-empty value. `wotid` MUST
appear exactly once, and `wotversion` MUST NOT appear more than once.

A Producer MAY include additional parameters after the standardized parameters.
This profile does not assign them a meaning; a publication contract MAY define
their semantics. A Consumer MUST NOT reject a source solely because it contains
parameters not defined by this profile.

For the standardized values, the unescaped characters are the
[RFC 3986][URI] `unreserved` characters and `!`, `$`, `'`, `(`, `)`, `*`,
`,`, `:`, `@`, `/`, and `?`. A Producer MUST leave these characters
unescaped. It MUST percent-encode the UTF-8 bytes of all other characters using
uppercase hexadecimal digits. In particular, a literal `%`, `;`, `=`, `&`,
`+`, or `#` in a standardized value MUST be encoded. A Producer MUST NOT use
form-query encoding or encode a space as `+` for those values.

A Consumer MUST split the query at `;` before decoding the standardized values.
It MUST reject a missing or empty `wotid`, an empty `wotversion`, a duplicate
standardized parameter, or a standardized parameter in the wrong position. For
a standardized value, it MUST reject an invalid percent escape, invalid UTF-8,
or an unescaped character outside the permitted set. It MUST percent-decode
each standardized value exactly once and MUST NOT interpret `+` as a space.

For example, an identifier containing U+00E9 followed by the literal characters
`%2F` encodes that portion as `%C3%A9%252F`. One decoding pass recovers the
original characters, including the literal `%2F`; it does not turn them into
a slash.

### Thing identity and version

The decoded `wotid` MUST be a non-empty absolute IRI as defined in
[RFC 3987][IRI]. When the authored TD has an `id`, `wotid` MUST equal that
value verbatim and the resolved TD MUST retain it. When the authored TD has
no `id`, the publication contract MUST assign a stable absolute WoT identity
for the Thing. Publishing another version MUST NOT by itself change that
identity.

The OPTIONAL `wotversion` selects one exact version of the resolved TD within
the configured resolution scope. It is not a version range, the CloudEvents
`specversion`, a WoT vocabulary version, or a payload-schema version. Its
meaning is defined by the publication contract; a Consumer MUST NOT substitute
a different version when the requested version is unavailable. Selecting that
version does not by itself establish the compatibility of its dependencies.

An explicit version identifies a stable resolved view. A Producer MUST NOT
change the logical view identified by a published version. It MUST publish a
new version when the view changes, including changes introduced by its source
closure. A serialization or formatting change alone does not require a new
version.

When `wotversion` is absent, the Consumer resolves the current default view.
That default can change, so a delayed event can resolve to a different view
than the one available when the event was produced. A publication profile
that requires repeatable replay MUST require `wotversion`.

Core requires `source` and `id` together to identify each distinct event.
Changing the `source`, including its context, version, or other parameters,
changes the event identity and [Sequence extension](sequence.md) scope.
Returning to an earlier `source` returns to its existing scope: Producers MUST
NOT reuse event identities or restart a claimed source-wide sequence within
that scope.

## Resolving the Thing Description

The Producer and Consumer MUST agree on a resolver and its scope out of band
or through their publication profile. The scope selects a registry and Group,
tenant, or equivalent boundary in which the Thing identity is resolved. This
profile does not prescribe a discovery protocol.

The resolver MUST find exactly one Resource or equivalent publication for
`wotid` within that scope. It MUST select the exact version named by
`wotversion`, or the current default when the parameter is absent. A missing
or ambiguous match is a resolution failure; selecting the first match does not
establish which Thing the Producer meant.

The Consumer MUST obtain the resolved TD selected by that publication. It MAY
retrieve a published resolved view or reconstruct the same logical view from
a complete, pinned source closure and the applicable resolution rules. The
closure and rules MUST establish one unambiguous view. The JSON serialization
does not need to be byte-identical.

If the selected view cannot be retrieved or reconstructed, the Consumer MUST
report a resolution failure and leave the event uncorrelated. It MAY retain
or forward the event without interpreting its payload. The Consumer MUST NOT
claim successful TD-based interpretation when the resolved view or its
identity cannot be established.

The [xRegistry WoT working draft][WoT Registry] describes one resolution
mechanism. It is a working draft, not a universal dependency of this profile.
In that draft, `wotid` is the WoT identity rather than the Resource ID, and
`wotversion` corresponds to the Resource's exact `versionid`. The default
Version is not necessarily the most recently created Version and MUST NOT be
inferred by sorting version identifiers.

The draft stores authored documents and describes a publication closure.
Some closure reference mappings remain unresolved; the closure schema alone
does not establish that every resolved view can be reconstructed. Where the
closure and applicable rules cannot establish the view, the publication
contract MUST provide the resolved view for this profile to use it.

The event carries no digest of the TD. An exact version or a successful
resolution does not by itself prove that retrieved bytes are unchanged.

## Mapping Core Context Attributes

### type

The Core [`type`](../spec.md#type) identifies the event contract. The contract
is the payload representation defined by the publication profile or protocol
binding, including its members, member types, and semantics. Two Things can
produce events of the same type when their event contracts are the same. This
profile uses a dot-separated symbol so a Consumer can map the type to a
code-generation symbol.

The type MUST contain one or more segments separated by single dots. Each
segment MUST start with an ASCII letter or underscore and contain only ASCII
letters, digits, or underscores thereafter. These character restrictions apply
only to `type`; they do not change the Thing identifier, TD member names,
`source`, `subject`, or payload. A code generator remains responsible for
language-specific keywords. The final segment MUST identify the event-contract
revision as `vN`, where `N` is a positive decimal integer without leading zeros.

A Producer MAY configure the complete type. Otherwise, it derives the type
from a governing [Thing Model][TM] (TM) and, for an affordance event, the
corresponding model-affordance path. When composition or derivation does not
identify that mapping unambiguously, the publication configuration MUST
select it explicitly. A Producer MUST NOT infer the mapping solely from
matching names or select the first TM link.

For an eligible HTTPS TM identifier, derive the type as follows:

1. Require an ASCII DNS hostname without empty labels or a trailing root dot.
   The identifier cannot contain user information, a port, a query, or a
   fragment for this derivation.
2. Lowercase the hostname, reverse its labels, and join them with dots.
3. Append the TM identifier's path, replacing each `/` with `.`.
4. For an affordance event, append the model-affordance JSON Pointer path.
   Decode its [RFC 6901][JSON Pointer] token escaping, then replace each `/`
   with `.`.
5. Append the event-contract revision as the final segment.

For example, TM `https://models.example.com/tm/pump` and model affordance
`/properties/processData` with event-contract revision 1 produce:

```text
com.example.models.tm.pump.properties.processData.v1
```

For a whole-Thing event, use the TM-derived type without an affordance path,
then append the revision. The publication profile defines how interaction data
is aggregated into the payload.

The publication profile MUST assign the same revision to the same event
contract. A Producer MUST use a new revision when the contract changes,
including when a member is added or removed, a member's type or meaning
changes, or the payload envelope changes. This applies even when the change is
backwardly compatible. A Producer MUST NOT reuse a revision for a different
contract with the same base type.

For example, adding a `quality` member to
`com.example.models.tm.pump.properties.processData.v1` requires
`com.example.models.tm.pump.properties.processData.v2`, even if Consumers can
ignore the new member.

A change to an individual value or the presence of a member already defined as
OPTIONAL does not change the contract revision. A change to `wotversion` or
`dataschema` alone also does not change the revision; if it changes the payload
contract, the Producer MUST use a new revision.

The Producer MUST configure a valid complete type when the derivation is
unavailable, produces an invalid symbol, or collides with a different event
contract in the Producer's type namespace. A slash-to-dot conversion is not
reversible: `/tm/pump.v1` and `/tm/pump/v1` produce the same suffix. The
Producer MUST disambiguate such contracts by configuration rather than
silently rewriting identifiers or member names.

### subject

The [`subject`](../spec.md#subject) is REQUIRED. It MUST be an
[RFC 6901][JSON Pointer] URI-fragment pointer evaluated against the resolved
TD. For an event describing the whole Thing, the Producer MUST use `#`. For
an affordance event, the pointer MUST identify the concrete affordance in the
resolved TD, for example `#/properties/processData` or `#/events/alarm`.

The Producer MUST escape JSON Pointer tokens before applying URI-fragment
encoding. For example, the property name `pressure/bar` is addressed by
`#/properties/pressure~1bar`. The Consumer MUST report a failure and leave
the event uncorrelated if the pointer is invalid or does not select the
intended member of the resolved view.

The subject identifies the Thing or affordance, not an occurrence. Different
events can have the same subject and different CloudEvents `id` values. A
binding-specific writer identifier or native occurrence identifier is not
appended to this pointer.

The concrete TD path and corresponding TM declaration path can differ. This
profile does not infer a declaration-lineage mapping between them.

### dataschema and datacontenttype

Core [`dataschema`](../spec.md#dataschema) identifies the schema that the
CloudEvent's actual `data` adheres to.
[`datacontenttype`](../spec.md#datacontenttype) identifies that data's media
type. Neither identifies the TD document's format.

A TD describes interactions and can contain several DataSchemas. The
Producer MUST NOT use the whole TD as `dataschema` merely because the TD
contains a schema for the selected affordance. A TD's retrieval URL is a
valid `dataschema` only if the identified representation is itself the
schema applicable to `data`.

The publication profile or protocol binding defines how the selected
affordance's DataSchema maps to the wire payload. An object containing
several property values, an event payload and a protocol envelope can need
different schemas. When `dataschema` is present, the Producer MUST ensure
that it identifies the schema of the representation actually sent, including
any encoding or envelope selected by the binding.

An xRegistry Schema Resource's document-view URL can identify that external
schema. It is not the WoT Resource's metadata-view URL. A profile MAY require
an exact schema Version independently of the `wotversion` query parameter.

### Relationship to Other Extensions

This profile does not redefine native message types, sequence counters, or
writer identities. An event that also uses the [OPC UA extension](opcua.md)
MUST follow that extension's conditional WoT mapping.

## Examples

### Single Affordance

This CloudEvent identifies a pump and its `processData` property. The
configured resolver selects version `3.0.0` of the resolved TD.

```json
{
  "specversion": "1.0",
  "id": "sample-4711",
  "source": "https://factory.example.com/line1?wotid=urn:example:pump:7;wotversion=3.0.0;site=north",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "#/properties/processData",
  "datacontenttype": "application/json",
  "dataschema": "https://example.com/schemas/pump-process-data/versions/3",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

The subject selects the property in that resolved view. The payload directly
contains the property's object value without a `processData` wrapper. The
separate schema describes that object, not the TD document. Another pump can
use the same event type with a different Thing identity in its `source`.

### Whole Thing

This CloudEvent carries aggregated data for the same pump. Its unversioned
source selects the current default resolved TD, which this example assumes is
version `3.0.0`. The publication profile defines a payload containing the
`processData` and `running` property values. The subject selects the whole TD.

```json
{
  "specversion": "1.0",
  "id": "sample-4713",
  "source": "https://factory.example.com/line1?wotid=urn:example:pump:7;site=north",
  "type": "com.example.models.tm.pump.v1",
  "subject": "#",
  "datacontenttype": "application/json",
  "dataschema": "https://example.com/schemas/pump-state/versions/3",
  "data": {
    "processData": {
      "Speed": 1500,
      "Pressure": 4.5
    },
    "running": true
  }
}
```

The source selects the TD used to interpret these property values. If the
default changes, a later resolution of this event can select another version.
The TD document itself is not the payload. `dataschema` identifies the schema
of the aggregate JSON object, not the TD or either property's DataSchema alone.

## Security Considerations

Resolvers MUST apply their configured trust, authorization and retrieval
policies before accessing documents. An untrusted identity or schema URI
MUST NOT authorize arbitrary network access, redirects or credential
forwarding. Implementations SHOULD bound document sizes and dependency
resolution.

The Producer controls the context attributes unless another mechanism
authenticates them. A version does not establish that a TD, its model lineage,
or a schema is authorized for the Consumer's use. It does not grant access to
referenced documents or make their dependencies available.

[TD]: https://www.w3.org/TR/wot-thing-description11/
[TM]: https://www.w3.org/TR/wot-thing-description11/#thing-model
[IRI]: https://www.rfc-editor.org/rfc/rfc3987
[URI]: https://www.rfc-editor.org/rfc/rfc3986
[JSON Pointer]: https://www.rfc-editor.org/rfc/rfc6901
[WoT Registry]: https://github.com/xregistry/spec/blob/main/workingdrafts/models/wot/spec.md
