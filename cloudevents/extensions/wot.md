# Web of Things

This extension identifies the [Web of Things Thing Description][TD] (TD) that
describes the interaction associated with a CloudEvent. It separates the
Thing's identity, the selected TD representation, its revision and
verification of its bytes. The selected representation can be the authored TD
or a resolved TD derived from it.

The extension also defines a convention for event types derived from a
[Thing Model][TM] (TM), affordance subjects and the relationship between a TD
and the payload schema. It does not define a transport binding, provision a
Thing, or require a particular registry implementation.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

The scope of these key words is limited to events using this extension. An
attribute marked REQUIRED here is not REQUIRED in every CloudEvent.

## Attributes

### wotid

- Type: `String`
- Description: The stable WoT identity of the Thing described by the
  referenced TD. It is not the location of a registry entry or the schema of
  the CloudEvent's `data`.
- Constraints:
  - REQUIRED
  - MUST be a non-empty absolute IRI as defined in [RFC 3987][IRI].
  - MUST equal the TD's `id` value verbatim when that member is present.
  - A resolved TD MUST retain the authored TD's `id` when it is present.
  - When the authored TD has no `id`, the Producer MUST use the stable WoT
    identity assigned to it by its publication contract. A resolved TD for
    that Thing MUST use the same identity.
  - MUST NOT change merely because another revision of the same TD is
    published.

The CloudEvents `URI` type uses RFC 3986 and does not include IRIs containing
non-ASCII characters. This attribute uses `String` to preserve those identifiers
without percent-encoding or otherwise rewriting the TD's `id`. Absolute URIs
are also valid absolute IRIs.

An IRI used as an identity is not necessarily a document retrieval URL. A
Consumer MUST NOT assume that an arbitrary `wotid` can be fetched directly.
The deployment or publication profile defines the resolver and its lookup
scope. The identity can name either an authored TD or a resolved TD for the
same Thing; it does not select between those representations.

### wotversion

- Type: `String`
- Description: The exact revision of the TD identified by `wotid`, within the
  configured resolution scope and selected representation. This is a document
  revision, not the CloudEvents `specversion`, the version of a WoT vocabulary
  or the version of the wire-payload schema.
- Constraints:
  - OPTIONAL
  - If present, MUST be non-empty and MUST identify exactly one revision.
  - MUST NOT be interpreted as a minimum acceptable version or a version range.
  - MUST NOT be inferred from, or appended to, `wotid`.
  - If absent, the Consumer MUST use the default revision selected by the
    configured resolver for the selected representation.

A publication profile MAY require `wotversion`. An exact revision is
RECOMMENDED when later interpretation of a stored event depends on the same
description. An unversioned reference can resolve differently after the
resolver's default changes; it does not pin the description that existed
when the event was produced.

Version identifiers are opaque outside their governing publication contract.
A Consumer MUST NOT substitute a different revision when the requested
revision is unavailable.

### wotdigest

- Type: `String`
- Description: A digest of the selected authored or resolved TD document's
  exact bytes.
- Constraints:
  - OPTIONAL
  - If present, MUST have the form `sha-256:` followed by exactly 64 lowercase
    hexadecimal characters.
  - The hexadecimal value MUST be the SHA-256 digest of the TD document bytes
    obtained after removing transport framing and content coding, but before
    parsing or reserializing the document.
  - When a Consumer uses the referenced TD to interpret the event, it SHOULD
    verify a supplied digest before using that TD.

The digest covers the entire selected TD representation, including its `id`
member when present. No document members are excluded. It does not cover the
CloudEvent, its payload, a registry metadata response or the documents referenced
by the TD. It does not require JSON-LD expansion or JSON canonicalization.
Whitespace changes can change the digest.

When `wotversion` is absent, `wotdigest` verifies the default revision and
representation selected by the resolver; it does not define a search for some
historical revision or representation having that digest. A missing or unchecked
digest provides no byte-verification result. A Consumer that skips verification
MUST NOT report that the TD's bytes have been verified against `wotdigest`.
A matching digest is not a signature and does not authenticate the Producer.

## Resolving the Thing Description

The Producer and Consumer MUST agree on the resolution scope out of band or
through their publication profile. That scope includes any registry, tenant
or Group selection needed to distinguish copies of the same WoT identity and,
where necessary, the authored and resolved representations. This extension
does not prescribe a discovery protocol.

A Consumer using this extension to interpret `data` MUST resolve the
representation and revision selected by the publication profile without
substituting a document with another identity. The profile MUST select the
authored or resolved representation when the configured scope can return
both. The Consumer MUST use the configured resolver for `wotid`,
`wotversion` and that representation selection. An unavailable revision,
ambiguous representation, mismatching TD `id`, malformed digest or failed
digest comparison MUST be treated as unresolved description metadata. A
Consumer MAY retain or forward the CloudEvent without interpreting its
payload; it MUST NOT report successful TD-based interpretation using an
unresolved reference.

The [xRegistry WoT working draft][WoT Registry] describes one resolution
mechanism. It is a working draft, not a universal dependency of this extension.
In that draft:

- `wotid` is the authored WoT identity, distinct from a registry Resource id.
- `wotversion`, when present, corresponds to the Resource's exact `versionid`.
- An unversioned Resource reference serves its configured default Version,
  which is not necessarily the most recently created Version. A Consumer
  MUST NOT infer that default by sorting `versionid` values.
- The Consumer retrieves the TD document view, not the registry metadata view.

The xRegistry WoT draft stores authored documents. A deployment that makes a
resolved TD available MUST define how its resolver selects that representation
for the same `wotid`. A registry Resource URL MUST NOT be treated as the
resolved TD unless its document view actually returns that TD.

The Consumer still needs a configured registry scope. A registry-wide identity
query can return more than one Resource; choosing the first match does not
establish which description the Producer meant. The same applies when a scope
can return both authored and resolved representations.

## Mapping Core Context Attributes

### type

The Core [`type`](../spec.md#type) describes the semantic event type. A
Thing's identity in `wotid` is not its event type: two Things can produce
events described by the same model.

For TM-derived publications, the Producer MUST select a governing TM. For a
publication describing one affordance, the Producer MUST also select the
corresponding model-affordance path. When composition or derivation does not
identify the governing TM or affordance mapping unambiguously, the publication
configuration MUST select it explicitly. A Producer MUST NOT infer that
correspondence solely from matching names or select the first TM link
arbitrarily.

The following naming convention constructs a reverse-DNS-prefixed type base
from an HTTPS TM identifier:

1. Parse the absolute identifier without removing its path, query or fragment.
   The authority MUST contain an ASCII DNS hostname with no empty labels or
   trailing root dot, and MUST NOT contain user information. Other authorities,
   including IP addresses, require an explicit base instead.
2. Lowercase the ASCII DNS hostname and reverse its labels.
3. Encode the identifier's exact suffix after the hostname, including any
   explicit port, path, query and fragment, as one token using the encoding
   below.
4. Append `.` and that token to the reversed hostname.

The type does not include a separate WoT marker; the presence of `wotid`
identifies use of this extension.

For other TM identifier schemes, or HTTPS identifiers not meeting these
conditions, the publication configuration MUST supply an explicit
reverse-DNS-prefixed base. That configuration MUST assign distinct bases to
distinct governing TMs in its type namespace.

For a publication describing one affordance, append `.affordance.` and the
encoded model-affordance path tokens to the base. The model path is an
[RFC 6901][JSON Pointer] JSON Pointer within the TM that identifies an
interaction affordance. Decode its JSON Pointer escaping before encoding
each token, and join the resulting tokens with `.`.

For a publication describing the Thing as a whole, the Producer MUST use the
base without an affordance suffix. The publication profile defines how the
Thing's interaction data is aggregated into the payload.

For both uses of token encoding, encode the input's UTF-8 bytes. Leave only
ASCII letters, digits, `-` and `_` unescaped. Encode every other byte as `%`
followed by two uppercase hexadecimal digits. Represent an empty token as
`~`; a literal tilde is encoded as `%7E`. Dots and percent signs are escaped,
so a literal dot in a name cannot be confused with a path-token separator.
This encoding is part of the type String, not an instruction to dereference it.

For example, TM `https://models.example.com/tm/pump` and model affordance
`/properties/processData` produce:

```text
com.example.models.%2Ftm%2Fpump.affordance.properties.processData
```

Changing the encoded TM suffix, governing base or model-affordance path
changes this derived type; changing only the hostname's letter case does not.
The Producer MUST NOT change that derivation merely because a different TD
instance or registry location is used. Versioning the payload schema is
separate from naming a semantic event type.

A TD can be published without a governing TM. This extension does not invent
one: publications without a TM-derived type follow Core's producer-defined
type rules. A profile requiring TM-derived types MUST reject missing or
ambiguous model mappings rather than inventing a base.

### subject

The [`subject`](../spec.md#subject), when present, MUST be an RFC 6901 JSON
Pointer to the concrete interaction affordance within the referenced TD,
such as `/properties/processData` or `/events/alarm`. It is not a URI
fragment and MUST NOT be prefixed with `#`.

For a publication describing the Thing as a whole, the Producer MUST omit
`subject` rather than use an empty pointer or an arbitrary affordance.

The subject identifies an affordance, not an occurrence. Different events
from that affordance can have the same subject and different CloudEvents
`id` values. A binding-specific writer identifier or native occurrence
identifier is not appended to this pointer.

The concrete TD path and the corresponding TM declaration path can differ.
This extension does not infer a declaration-lineage mapping between them.

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
an exact schema Version independently of `wotversion`.

### Relationship to Other Extensions

This extension does not redefine native message types, sequence counters,
writer identities or source identities. A profile that also uses the
[OPC UA extension](opcua.md) MUST specify how its TM-derived type and
affordance subject interact with that extension's existing type and subject
mappings. Merely adding `wotid` does not permit overriding them or establish
conformance to the OPC UA extension.

## Examples

### Single Affordance

The following CloudEvents describe the same pump and affordance. Both use the
authored TD's stable `wotid`; their publication profiles select the authored
and resolved representations, respectively.

```json
{
  "specversion": "1.0",
  "id": "sample-4711",
  "source": "urn:example:plant:publisher",
  "type": "com.example.models.%2Ftm%2Fpump.affordance.properties.processData",
  "subject": "/properties/processData",
  "datacontenttype": "application/json",
  "dataschema": "https://example.com/schemas/pump-process-data/versions/3",
  "wotid": "urn:example:pump:7",
  "wotversion": "3",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

For an authored TD selected by `wotid`, the Consumer resolves revision `3`
through its configured resolver. The subject selects that TD's `processData`
property.

The resolved-view form uses the same event attributes. Its publication profile
selects the resolved TD representation for `wotid`:

```json
{
  "specversion": "1.0",
  "id": "sample-4712",
  "source": "urn:example:plant:publisher",
  "type": "com.example.models.%2Ftm%2Fpump.affordance.properties.processData",
  "subject": "/properties/processData",
  "datacontenttype": "application/json",
  "dataschema": "https://example.com/schemas/pump-process-data/versions/3",
  "wotid": "urn:example:pump:7",
  "wotversion": "3",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

In either form, the separate schema describes the JSON object containing
`Speed` and `Pressure`; it does not describe the TD document. Another pump
with the same model and model-affordance mapping can use the same type with a
different `wotid`.

### Whole Thing

This CloudEvent carries aggregated data for the pump described by the same TD.
The publication profile selects the authored TD and defines a payload containing
the `processData` and `running` property values. The type uses the governing TM's
base without an affordance suffix, and `subject` is absent because the event is
not scoped to one affordance.

```json
{
  "specversion": "1.0",
  "id": "sample-4713",
  "source": "urn:example:plant:publisher",
  "type": "com.example.models.%2Ftm%2Fpump",
  "datacontenttype": "application/json",
  "dataschema": "https://example.com/schemas/pump-state/versions/3",
  "wotid": "urn:example:pump:7",
  "wotversion": "3",
  "data": {
    "processData": {
      "Speed": 1500,
      "Pressure": 4.5
    },
    "running": true
  }
}
```

`wotid` and `wotversion` select the TD used to interpret these property values.
The TD document itself is not the payload. `dataschema` identifies the schema
of the aggregate JSON object, not the TD or either property's DataSchema alone.

## Security Considerations

Resolvers MUST apply their configured trust, authorization and retrieval
policies before accessing documents. An untrusted identity or schema URI
MUST NOT authorize arbitrary network access, redirects or credential
forwarding. Implementations SHOULD bound document sizes and dependency
resolution.

The Producer controls these attributes unless another mechanism authenticates
them. A matching digest does not establish that a TD, its model lineage or a
schema is authorized for the Consumer's use. Exact revisions and digests do
not grant access to referenced documents or make their dependencies available.

[TD]: https://www.w3.org/TR/wot-thing-description11/
[TM]: https://www.w3.org/TR/wot-thing-description11/#thing-model
[IRI]: https://www.rfc-editor.org/rfc/rfc3987
[JSON Pointer]: https://www.rfc-editor.org/rfc/rfc6901
[WoT Registry]: https://github.com/xregistry/spec/blob/main/workingdrafts/models/wot/spec.md
