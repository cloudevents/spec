# Web of Things

A Consumer can use a pump's [Web of Things][TD] (WoT) Thing Description
(TD) to identify the property that a telemetry event reports. The event's
[`describedby`](descriptor.md#describedby) URL points to a
[Descriptor](descriptor.md) that links to the TD and can identify an
interaction in it, called an *affordance*.

For example, this event reports a reading from the `processData` property
of Pump 7:

```json
{
  "specversion": "1.0",
  "id": "sample-4711",
  "source": "urn:example:actor:telemetry-service",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "pump7",
  "describedby": "https://devices.example/pump7/descriptors/process-data.json",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

An HTTP `GET` of `describedby` returns the following Descriptor. The
Consumer resolves the TD at `url` and evaluates `affordanceselector` in it.
The `payload` entry supplies the schema for the object in `data`.

```json
{
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://devices.example/pump7/td.json",
      "affordanceselector": "/properties/processData"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/pump-process-data/versions/3"
    }
  }
}
```

A *publication profile* is the set of rules, agreed by specification or
configuration, that tells Producers and Consumers how to interpret the
event. It can name an entry when a Descriptor contains several entries
of the same class. The example uses the only TD entry.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this profile is
used. For example, an attribute marked as "REQUIRED" needs to be included
when the event uses this profile and meets the stated conditions.

## Description Selection

[`describedby`](descriptor.md#describedby) is REQUIRED for this profile.
The Consumer MUST use the Descriptor at that URL as the sole source of
Descriptor entries for the event. The publication profile selects the TD
entry by name or, if it supplies no name, by the unique `thingdescription`
entry. A named entry MUST exist and have class `thingdescription`. With
no name, exactly one entry of that class is REQUIRED.

Use the selected TD at its `url` or from its bundled `document`. Apply
the entry's [affordance selector](#affordanceselector) to identify the
Thing or affordance. The Publisher MUST make the selected TD available
before configuring Producers to use the Descriptor and SHOULD link to a
specific TD version.

Correlation fails if `describedby` is missing or invalid, the URL does not
yield a valid Descriptor, or the Consumer cannot select the TD entry or
resolve its TD or selector. The Consumer MUST report the failure and MAY
retain or forward the uncorrelated event.

## WoT Descriptor entries

A TD entry has class `thingdescription`. A [Thing Model][TM] (TM) defines
a reusable model for Things; a TM entry has class `thingmodel`. Both
classes MUST link to the resolved document itself at `url`. For example,
with xRegistry, use the document-view URL. The
[Descriptor rules](descriptor.md#entries) define the entry names.

### affordanceselector

A TD entry MAY include `affordanceselector` to select an affordance.
Omission selects the whole Thing. In a TM entry, this member selects a
model declaration; omission selects no individual declaration.

When present, the member MUST be a plain [RFC 6901][JSON Pointer] string
of the form `/properties/<name>`, `/actions/<name>`, or `/events/<name>`.
It MUST identify an existing affordance or declaration in the linked
document. The Consumer MUST apply only RFC 6901 string-form decoding.
Null, empty, root, and more deeply nested selectors are invalid. Put
profile-defined annotations beside the selector; their profile defines
their scope, type, and omission rules.

### Event binding

A TM entry MAY carry `type` to associate an event contract with a TM or
one of its declarations. For a Consumer using this binding, the entry's
`type` MUST match the decoded event `type` exactly. If the publication
profile names a TM entry, only that entry can match. Otherwise, exactly
one match is REQUIRED. The Consumer MUST report missing, ambiguous, or
invalid bindings and unavailable TMs. The concrete TD path and the TM
declaration path can differ; derivation uses the model declaration.

### planurl

A TD or TM entry MAY include `planurl`, an absolute, fragment-free
HTTP(S) URL for the projection plan that produced the view at `url`.
The publication profile defines the plan's format. Consumers using the
plan MUST verify that it produced the linked view. The resolved view
remains valid when this OPTIONAL provenance is unavailable.

The [WoT entry schema](wot.schema.json) checks entry shape. Apply the
selection rules to check the linked document and selector target.

## Mapping Core Context Attributes

### source

[`source`](../spec.md#source) identifies the event's originating context
and follows Core's URI-reference rules. The WoT example uses the reporting
telemetry service as `source`; the [OpenUSD profile example](openusd.md)
uses the asset as `source`.
CloudEvents event identity and the
[Sequence extension](sequence.md) use the event's `source` even when
`describedby` changes.

A publication profile MAY declare that `source` identifies the described
entity. When it does, the Producer MUST set `source` to the `entityid` of
the Descriptor for that entity, using the exact string without
normalization. A Consumer MAY use that value to look up the entity
Descriptor where lookup is supported. This is independent of Description
Selection: only the Descriptor at `describedby` supplies Descriptor
entries for interpreting the event.

### subject

[`subject`](../spec.md#subject) is OPTIONAL and retains its Core meaning.
For example, a Producer can supply `pump7` to support filtering. WoT
retrieval and correlation use the Descriptor selected by `describedby`.

### type

Core [`type`](../spec.md#type) identifies the event contract: the payload
representation, members, types, and semantics defined by the publication
profile or protocol binding. Things can share a type when they share a
contract. The dot-separated type supports code generation.

The type MUST contain one or more segments separated by single dots. Each
segment MUST start with an ASCII letter or underscore; the rest can contain
only ASCII letters, digits, and underscores. Generators still handle
language keywords. The last segment MUST be the contract revision `vN`,
with positive decimal `N` and no leading zeros.

A Producer MAY configure the complete type. Otherwise, it derives the type
from a governing TM and, for an affordance event, the corresponding
model-affordance path. When composition or derivation leaves the mapping
ambiguous, the publication configuration MUST select it explicitly.
A Producer MUST NOT infer the mapping solely from matching names or select
the first TM link.

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
then append the revision. The publication profile defines how interaction
data is aggregated into the payload.

The publication profile MUST assign the same revision to the same event
contract. A Producer MUST use a new revision when the contract changes,
including when a member is added or removed, a member's type or meaning
changes, or the payload envelope changes. This applies even to
backward-compatible changes. A Producer MUST NOT reuse a revision for a
different contract with the same base type.

For example, adding a `quality` member to
`com.example.models.tm.pump.properties.processData.v1` requires
`com.example.models.tm.pump.properties.processData.v2`, even if Consumers
can ignore the new member. Changing a value or omitting or including an
OPTIONAL member preserves the revision. Changes to `describedby`, a TD
URL, the selected schema, or `subject` require a new revision only if they
change the payload contract.

The Producer MUST configure a valid complete type when the derivation is
unavailable, produces an invalid symbol, or collides with a different
event contract in the Producer's type namespace. For example,
`/tm/pump.v1` and `/tm/pump/v1` produce the same suffix. Disambiguate
such contracts by configuration.

### dataschema and datacontenttype

Core [`dataschema`](../spec.md#dataschema) and
[`datacontenttype`](../spec.md#datacontenttype) describe the schema and
media type of `data`. The publication profile or protocol binding
determines whether an external payload schema is REQUIRED.

If `dataschema` is present, the Consumer MUST use it as the sole schema
input and still validate applicable Descriptor selectors. Otherwise,
select the Descriptor's [schema entry][Schema Descriptor Profile] by the
name in the publication profile. If the profile supplies no name, select
the sole `schema` entry; zero entries means no schema, and multiple entries
are ambiguous. A named entry that is missing or has the wrong class is
invalid. Use the selected schema at its `url` or from its bundled
`document`.

Producers and Descriptor publishers SHOULD supply one schema source or
identify the same schema in both. Producers SHOULD omit `dataschema`
when the Descriptor supplies the schema.

The Consumer MUST report a missing REQUIRED schema. An ambiguous
selection, invalid selector, unavailable schema, or unsupported format
MUST NOT cause fallback to another schema. The selected schema MUST
describe the actual payload, including its encoding and envelope. For
example, a TD URL belongs in `dataschema` only when it identifies the
schema for `data` itself. The profile or binding maps an affordance's
DataSchema to the wire payload and can require a specific schema version
independently of the TD version.

## Whole-Thing example

To report the pump's aggregate state, the Producer uses
`com.example.models.tm.pump.v1` as `type` and points `describedby` to a
Descriptor whose TD entry omits `affordanceselector`. The schema entry
describes the aggregate object, including both `processData` and `running`.

```json
{
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://devices.example/pump7/td.json"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/pump-state/versions/3"
    }
  }
}
```

## Relationship to Other Extensions

An event that also uses the [OPC UA extension](opcua.md) MUST follow
its [combined WoT mapping](opcua.md#wot-mapping) for native message types,
sequence counters, and writer identities.

## Security Considerations

Apply the [Descriptor Reference security rules](descriptor.md#security-considerations)
to the Descriptor and its linked documents. Treat context attributes as
Producer-supplied values unless another mechanism authenticates them.
Establish trust and access independently for each document, its model
lineage, and its dependencies. Correlating an event with an affordance
does not authorize invoking it.

[TD]: https://www.w3.org/TR/wot-thing-description11/
[TM]: https://www.w3.org/TR/wot-thing-description11/#thing-model
[JSON Pointer]: https://www.rfc-editor.org/rfc/rfc6901
[Schema Descriptor Profile]: descriptor.md#schema
