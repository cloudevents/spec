# Web of Things

This profile maps a [Web of Things Thing Description][TD] (TD) to CloudEvents
Core context attributes and optionally the [Descriptor Reference
extension](describedby.md). The REQUIRED `subject` identifies a Thing or
affordance, either through a selected Descriptor or through a self-contained TD
document URL. The `type` names the event contract.

The profile defines no new CloudEvents extension attributes. Producers and
Consumers agree on its use through a publication profile or configuration. It
does not define a transport binding, provision a Thing, or require a particular
registry implementation. A direct TD subject can supply the REQUIRED description
without a Descriptor; an explicit `describedby` can supply additional shared
information when needed.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

The scope of these key words is limited to events using this profile. An
attribute marked REQUIRED here is not REQUIRED in every CloudEvent.

## Mapping Core Context Attributes

### source

The Core [`source`](../spec.md#source) identifies the context in which the event
occurred and follows Core's URI-reference rules. It does not have to identify
the Thing selected by `subject`; an actor can emit an event concerning a
different device.

For example, `https://factory.example.com/line1/pump7` and
`mqtt://site/line/cell/device/sensor` are valid sources.

An agreed source-Descriptor binding MAY use an absolute, fragment-free
Descriptor URL as `source` when it identifies the originating context. Consumers
MUST NOT infer that binding merely from URL-like spelling. The
[description-selection rules](#description-selection) determine whether the
source is retrieved; a direct TD subject does not require that lookup.

#### Event identity

Core requires `source` and `id` together to identify each distinct event.
Changing the `source` changes the event identity and
[Sequence extension](sequence.md) scope.
Returning to an earlier `source` returns to its existing scope: Producers MUST
NOT reuse event identities or restart a claimed source-wide sequence within
that scope.

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
OPTIONAL does not change the contract revision. A change to `describedby`, the
selected TD URL or the selected schema alone also does not change the revision;
if it changes the payload contract, the Producer MUST use a new revision.

The Producer MUST configure a valid complete type when the derivation is
unavailable, produces an invalid symbol, or collides with a different event
contract in the Producer's type namespace. A slash-to-dot conversion is not
reversible: `/tm/pump.v1` and `/tm/pump/v1` produce the same suffix. The
Producer MUST disambiguate such contracts by configuration rather than
silently rewriting identifiers or member names.

### subject

The [`subject`](../spec.md#subject) is REQUIRED. It MUST be an [RFC 6901][JSON
Pointer] URI-fragment pointer with one of the prefixes defined below. The
pointer is evaluated against the selected ordinary, resolved TD, not Descriptor
metadata or an unresolved projection plan.

| Subject form | Meaning |
| --- | --- |
| `#` or `#/properties/processData` | Select the unique TD Reference in the selected Descriptor, then the whole Thing or affordance. |
| `pump7#/properties/processData` | Select the Descriptor's named `thingdescription` Reference `pump7`, then its affordance. |
| `https://example.com/td/pump7/versions/3#/properties/processData` | Identify the Thing's affordance through a TD document URL; description selection follows the rules below. |

The Consumer MUST split the value at the first literal `#`. A missing delimiter
is invalid. It recognizes a direct-URL candidate by an `http://` or `https://`
prefix, case-insensitively, and MUST validate that prefix as a complete absolute
HTTP(S) URL. Otherwise, the prefix MUST be empty or a Descriptor Reference name.
Reference names follow the Descriptor Registry's map-key rules and cannot
contain `/`; `http:pump7` can therefore be a name, but is not an HTTP URL.
Invalid input MUST NOT be retried through another form or resolved against
`source`.

The suffix including `#` MUST be a valid JSON Pointer URI fragment. For the
whole Thing, the Producer MUST use an empty fragment, such as `#`, `pump7#` or
`https://example.com/td/pump7/versions/3#`. For an affordance event, the pointer
MUST identify the concrete affordance in that TD, such as
`#/properties/processData`, `#/actions/setSetpoint` or `#/events/alarm`.

The Producer MUST escape JSON Pointer tokens before applying URI-fragment
encoding. For example, property `pressure/bar` is addressed by
`#/properties/pressure~1bar`; a literal `#` in a name is percent-encoded. The
Consumer MUST apply URI-fragment decoding once, then JSON Pointer token decoding
as specified by RFC 6901. It MUST report a correlation failure if the encoding
or pointer is invalid or the pointer does not select the intended Thing or
affordance.

The subject identifies the Thing or affordance, not an occurrence. Different
events can have the same subject and different CloudEvents `id` values. A
binding-specific writer identifier or native occurrence identifier is not
appended to this pointer.

The concrete TD path and corresponding TM declaration path can differ. This
profile does not infer a declaration-lineage mapping between them.

Changing a direct subject's TD Version URL changes the subject string used for
filtering and correlation, not the source-plus-id event identity. A
Descriptor-relative subject with an independently versioned `describedby` can
avoid that coupling.

### dataschema and datacontenttype

Core [`dataschema`](../spec.md#dataschema) identifies the schema that the
CloudEvent's actual `data` adheres to.
[`datacontenttype`](../spec.md#datacontenttype) identifies that data's media
type. Neither identifies the TD document's format.

The Consumer follows the Descriptor Reference extension's [schema
precedence](describedby.md#message-and-schema-selection): `dataschema`, then the
selected Descriptor's schema, then the schema declared by its selected Message
definition. Without a Descriptor, the second and third sources are absent. The
Producer SHOULD omit `dataschema` when a selected Descriptor already supplies
the schema.

A TD describes interactions and can contain several DataSchemas. The
Producer MUST NOT use the whole TD as `dataschema` merely because the TD
contains a schema for the selected affordance. A TD's retrieval URL is a
valid `dataschema` only if the identified representation is itself the
schema applicable to `data`.

The publication profile or protocol binding defines how the selected
affordance's DataSchema maps to the wire payload. An object containing several
property values, an event payload and a protocol envelope can need different
schemas. When `dataschema` is present, the Producer MUST ensure that it
identifies the schema of the representation actually sent, including any
encoding or envelope selected by the binding. The same requirement applies to a
schema supplied by a Descriptor.

An xRegistry Schema Resource's document-view URL can identify that external
schema. It is not the WoT Resource's metadata-view URL. A profile MAY require
an exact schema Version independently of the selected TD Version.

## Description Selection

This profile uses the [Descriptor Reference selection
rules](describedby.md#one-selected-processing-description), including when
`describedby` is absent. Apply event-format decoding before testing presence;
JSON `null` means unset. Selection proceeds as follows:

1. If `describedby` is present, retrieve and validate its Descriptor. It is
   authoritative; a failure MUST NOT cause fallback to source or direct TD
   subject retrieval.
2. Otherwise, if `subject` has a direct HTTP(S) TD URL prefix, retrieve that
   document. Use the prefix unchanged, including its query; the fragment is
   evaluated locally and is not sent in HTTP. Do not retrieve a source
   Descriptor or construct a synthetic Descriptor from the TD.
3. Otherwise, use the agreed source-Descriptor binding. Retrieve the exact
   `source` URL, which MUST be an absolute URL without a fragment for this
   binding. If no such binding was agreed, report a correlation failure.

When a Descriptor is selected, select its TD Reference as follows:

- For an empty subject prefix, the Descriptor MUST have exactly one
  `thingdescription` Reference.
- For a Reference-name prefix, that entry MUST exist and its `class` MUST be
  `thingdescription`.
- For a direct URL prefix, exactly one `thingdescription` Reference MUST
  have a `url` equal to that prefix. Consumers MUST compare the strings exactly,
  without URI normalization. Missing or duplicate matches are correlation
  failures. A named subject can disambiguate duplicate URLs.

The selected `url` identifies the ordinary TD document, not its Registry
metadata. The Consumer uses that representation directly or from an accepted
Descriptor bundle. It MUST NOT construct another URL from the Descriptor URL or
Reference. Redirect destinations, TD `id` and equal `entityid` values MUST NOT
be used to repair a subject-to-Reference mismatch.

A `thingmodel` Reference cannot replace an instance TD. A document marked as an
unresolved [WoT projection plan][WoT Projections] MUST NOT be used as an
ordinary TD or re-resolved to replace the published result. OPTIONAL `planurl`
provenance follows the Descriptor Registry's class rules. Failure to retrieve
OPTIONAL provenance does not invalidate an otherwise usable TD, unless the
agreed profile requires that provenance. A detected invalid plan/view pairing is
invalid metadata.

The Producer MUST supply all REQUIRED inputs through the selected route, the
event and the agreed publication profile. A direct TD subject without a
Descriptor does not supply missing Message definitions or native publisher
metadata. A Producer needing those shared inputs can use a complete Descriptor
with `describedby`. A Consumer MUST NOT merge them from source descriptions.

If selection, retrieval or correlation fails, the Consumer MUST report the
failure and leave the event uncorrelated. It MAY retain or forward the event
without TD-based interpretation, but MUST NOT switch routes or substitute
another TD. This does not authenticate the originating entity or authorize an
action described by the TD.

The Publisher MUST make the selected TD available before configuring Producers
with its URL or a Descriptor that references it. The Publisher SHOULD publish an
explicit TD Version. A change to the resolved logical view requires a new TD
Version; the Publisher MUST NOT change that view at a previously published
Version URL. Descriptor publication and Version stability follow the Descriptor
Registry rules.

Changing only `describedby` does not change identity or sequence scope. A
Producer MUST NOT reuse an `id` or restart a source-wide sequence merely because
a description changes. An exact Version or successful resolution does not itself
prove that retrieved bytes are unchanged.

## Relationship to Other Extensions

This profile does not redefine native message types, sequence counters, or
writer identities. An event that also uses the [OPC UA extension](opcua.md)
MUST follow that extension's conditional WoT mapping.

## Examples

### Single Affordance

This CloudEvent identifies a pump and its `processData` property. Its Descriptor
selects version `3` of the resolved TD and supplies the payload schema. Another
TD in the same Descriptor describes a gateway.

```json
{
  "specversion": "1.0",
  "id": "sample-4711",
  "source": "https://registry.example/descriptorgroups/devices/descriptors/pump7",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "pump7#/properties/processData",
  "datacontenttype": "application/json",
  "describedby": "https://registry.example/descriptorgroups/streams/descriptors/pump7-telemetry/versions/1",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

The Descriptor has the following metadata. Core bookkeeping and any
profile-specific shared metadata are omitted from this excerpt.

```json
{
  "descriptorid": "pump7-telemetry",
  "versionid": "1",
  "schemaref": "payload",
  "references": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3",
      "planurl": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7-plan/versions/3"
    },
    "gateway1": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/gateway1/versions/1"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/pump-process-data/versions/3"
    },
    "geometry": {
      "class": "usdasset",
      "url": "https://assets.example/usdassetgroups/line1/usdassets/pump7/versions/2"
    }
  }
}
```

The subject prefix selects `pump7`, not the first TD in the map. The suffix
selects its property. The payload directly contains the property's object value
without a `processData` wrapper. The selected schema describes that object, not
the TD document. The OPTIONAL plan and USD asset do not have to be retrieved for
this correlation.

### Direct TD Subject

This event needs only the TD and an external payload schema, so it omits
`describedby`. The source identifies an actor's originating context rather than
the pump; it is not retrieved.

```json
{
  "specversion": "1.0",
  "id": "sample-4712",
  "source": "urn:example:actor:telemetry-service",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3#/properties/processData",
  "dataschema": "https://schemas.example/pump-process-data/versions/3",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

The Consumer retrieves the subject's fragment-free TD URL and evaluates
`#/properties/processData`. The URI fragment is not sent in HTTP.

### Direct Subject with a Descriptor

The preceding event can instead select the same telemetry Descriptor:

```json
{
  "specversion": "1.0",
  "id": "sample-4714",
  "source": "urn:example:actor:telemetry-service",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3#/properties/processData",
  "describedby": "https://registry.example/descriptorgroups/streams/descriptors/pump7-telemetry/versions/1",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

The direct subject matches exactly the `pump7` Reference. The Descriptor now
supplies the schema. Changing just the subject's TD Version to `4` would fail
correlation because this Descriptor names Version `3`. Adding another TD
Reference with that same Version `3` URL would also make the direct match
ambiguous; a named subject would then be REQUIRED.

### Source-selected Descriptor

When the agreed source-Descriptor binding is enabled, the Single Affordance
event can use the following complete envelope without `describedby`:

```json
{
  "specversion": "1.0",
  "id": "sample-4715",
  "source": "https://registry.example/descriptorgroups/streams/descriptors/pump7-telemetry/versions/1",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "pump7#/properties/processData",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

This intentionally identifies the stream Descriptor as the originating context.
Its source-plus-id namespace differs from the device-source example. A new
Version in `source` changes that namespace; a new Version in `describedby` alone
does not.

### Whole Thing

This CloudEvent carries aggregated data for the same pump. Its Descriptor
selects version `3` of the resolved TD and the aggregate payload schema. The
publication profile defines a payload containing the `processData` and `running`
property values. The subject selects the whole TD.

```json
{
  "specversion": "1.0",
  "id": "sample-4713",
  "source": "https://factory.example.com/line1/pump7",
  "type": "com.example.models.tm.pump.v1",
  "subject": "#",
  "datacontenttype": "application/json",
  "describedby": "https://registry.example/descriptorgroups/streams/descriptors/pump7-state/versions/1",
  "data": {
    "processData": {
      "Speed": 1500,
      "Pressure": 4.5
    },
    "running": true
  }
}
```

The referenced Descriptor Version contains the following metadata.

```json
{
  "descriptorid": "pump7-state",
  "versionid": "1",
  "schemaref": "payload",
  "references": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/pump-state/versions/3"
    }
  }
}
```

The empty subject prefix selects the unique TD Reference. The TD document itself
is not the payload. `schemaref` selects the schema of the aggregate JSON object,
not the TD or either property's DataSchema alone. A direct whole-Thing subject
would end in `#` after its TD document URL.

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
[JSON Pointer]: https://www.rfc-editor.org/rfc/rfc6901
[WoT Projections]: https://github.com/marcschier/wot-thing-description/pull/1
