# Web of Things

This profile maps a [Web of Things Thing Description][TD] (TD) to CloudEvents
Core context attributes and the [Event Context extension](context.md).
The REQUIRED `contexturl` identifies shared metadata whose `emitter` Reference
selects the resolved TD. The `subject` identifies the part of that TD associated
with the event, and the `type` names the event contract.

The profile defines no CloudEvents extension attributes or URI scheme.
Producers and Consumers agree on its use through a publication profile or out
of band. It does not define a transport binding, provision a Thing, or require
a particular registry implementation. Events use the xRegistry Context
representation defined by the Event Context extension.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

The scope of these key words is limited to events using this profile. An
attribute marked REQUIRED here is not REQUIRED in every CloudEvent.

## Source

The Core [`source`](../spec.md#source) identifies the context in which the
event occurred and follows Core's URI-reference rules. It can identify a Thing,
topology, publisher, or another Producer-defined context. This profile does not
prescribe a URI scheme or query parameters. The Context's `emitter` Reference,
not `source`, selects the resolved TD.

For example, a Producer can use `https://factory.example.com/line1/pump7` or
`mqtt://site/line/cell/device/sensor` as a source. Another possible form is
`wot-td://factory/line1`; this profile does not define that scheme or propose
its registration. A source is an identifier and is not necessarily a retrieval
URL for a TD.

### Event identity

Core requires `source` and `id` together to identify each distinct event.
Changing the `source`, including any query parameters, changes the event
identity and [Sequence extension](sequence.md) scope.
Returning to an earlier `source` returns to its existing scope: Producers MUST
NOT reuse event identities or restart a claimed source-wide sequence within
that scope.

Changing `contexturl` alone does not change event identity or sequence scope.
A Producer MUST NOT reuse an `id` or restart a source-wide sequence merely
because it publishes a new Context Version.

## Resolving the Thing Description

Every event using this profile MUST include `contexturl`. The Producer and
Consumer MUST implement the [Event Context extension](context.md). The Context
MUST contain an `emitter` Reference whose `url` identifies the resolved TD
document, not its Registry metadata. The Context Publisher SHOULD reference an
explicit TD Version and publish the resolved TD view at that URL. The Consumer
retrieves the document directly or uses the corresponding document in an
accepted resolved Context view. It MUST NOT derive a TD URL from `contexturl`
or from the `emitter` URL.

The Context's `emitter` is authoritative for TD selection. The Consumer MUST
evaluate `subject` against that TD and MUST NOT select another TD from `source`.
This rule does not change Core's meaning of `source` or authenticate the
emitting entity.

If `contexturl` is missing, the Context cannot be retrieved or is invalid, its
`emitter` Reference is missing or invalid, or the referenced TD is unavailable
or not resolved, the Consumer MUST report a resolution failure and leave the
event uncorrelated. It MUST NOT fall back to selection through `source`. It
MAY retain or forward the event without TD-based interpretation.

The Context Publisher MUST make the TD available before configuring Producers
with the Context Version URL. Changes to its Reference require a new Context
Version. A change to the TD's resolved logical view requires a new TD Version;
the Context Publisher MUST NOT change that view at a previously published
Version URL. Context versioning alone does not make an unversioned TD URL
stable.

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
OPTIONAL does not change the contract revision. A change to `contexturl`, its
`emitter` Reference, or the selected schema alone also does not change the
revision; if it changes the payload contract, the Producer MUST use a new
revision.

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

The Consumer follows the Event Context extension's schema precedence:
`dataschema`, then the Context's `schema` Reference, then the schema declared
by its `message` representation. The Producer SHOULD omit `dataschema` when
the Context supplies the schema.

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
The same requirement applies to a schema supplied by the Context.

An xRegistry Schema Resource's document-view URL can identify that external
schema. It is not the WoT Resource's metadata-view URL. A profile MAY require
an exact schema Version independently of the selected TD Version.

### Relationship to Other Extensions

This profile does not redefine native message types, sequence counters, or
writer identities. An event that also uses the [OPC UA extension](opcua.md)
MUST follow that extension's conditional WoT mapping.

## Examples

### Single Affordance

This CloudEvent identifies a pump and its `processData` property. Its Context
selects version `3.0.0` of the resolved TD and supplies the payload schema.

```json
{
  "specversion": "1.0",
  "id": "sample-4711",
  "source": "mqtt://site/line/cell/device/sensor",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "#/properties/processData",
  "datacontenttype": "application/json",
  "contexturl": "https://registry.example/contextgroups/line1/contexts/pump-process-data/versions/1",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

The Context metadata is shown in the
[Event Context example](context.md#example). Its `emitter` selects the TD,
and its `schema` selects the payload schema.
The subject selects the property in that resolved view. The payload directly
contains the property's object value without a `processData` wrapper. The
separate schema describes that object, not the TD document. Another pump can
use the same event type with a different Thing identity in its `source` and a
Context whose `emitter` describes that pump.

### Whole Thing

This CloudEvent carries aggregated data for the same pump. Its Context
selects version `3.0.0` of the resolved TD and the aggregate payload schema.
The publication profile defines a payload containing the `processData` and
`running` property values. The subject selects the whole TD.

```json
{
  "specversion": "1.0",
  "id": "sample-4713",
  "source": "https://factory.example.com/line1/pump7",
  "type": "com.example.models.tm.pump.v1",
  "subject": "#",
  "datacontenttype": "application/json",
  "contexturl": "https://registry.example/contextgroups/line1/contexts/pump-state/versions/1",
  "data": {
    "processData": {
      "Speed": 1500,
      "Pressure": 4.5
    },
    "running": true
  }
}
```

The referenced Context Version contains the following metadata.

```json
{
  "contextid": "pump-state",
  "versionid": "1",
  "references": {
    "emitter": {
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
    },
    "schema": {
      "url": "https://example.com/schemas/pump-state/versions/3"
    }
  }
}
```

The `emitter` selects the TD used to interpret these property values. The TD
document itself is not the payload. The `schema` identifies the aggregate JSON
object, not the TD or either property's DataSchema alone.

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
