# Web of Things

A Consumer can use a pump's [Web of Things][TD] (WoT) Thing Description
(TD) to identify the property that a telemetry event reports. The event's
`subject` can point directly to the TD and select one interaction, called
an *affordance* in WoT:

```json
{
  "specversion": "1.0",
  "id": "sample-1",
  "source": "urn:example:pump7",
  "type": "com.example.pump.pressure.v1",
  "subject": "https://devices.example/pump7/td.json#/properties/pressure",
  "data": 4.5
}
```

The Consumer retrieves the TD and evaluates `/properties/pressure` in that
document. In this example, the Producer and Consumer agree that the event
`type` identifies a numeric pressure reading.

For streams that share processing inputs such as a payload schema or an
event binding, [`describedby`](descriptor.md#describedby) can point to a
[Descriptor](descriptor.md) that supplies them. The **Processing
Descriptor** is the Descriptor selected for that purpose. A publication
profile is the set of rules, agreed by specification or configuration,
that tells Producers and Consumers how to interpret the event.

The publication profile chooses how to identify the Thing or affordance.
In *subject-driven selection*, `subject` supplies the selection. In
*Descriptor-driven selection*, `describedby` selects the Processing
Descriptor and a TD entry supplies the selection. For example, a
Descriptor for the same pump property can contain:

```json
{
  "descriptorid": "pump7-pressure",
  "versionid": "1",
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://devices.example/pump7/td.json",
      "affordanceselector": "/properties/pressure"
    }
  }
}
```

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this profile is
used. For example, an attribute marked as "REQUIRED" needs to be included
when the event uses this profile and meets the stated conditions.

## Mapping Core Context Attributes

### source

The Core [`source`](../spec.md#source) identifies the context in which the event
occurred and follows Core's URI-reference rules. An actor can emit an event
concerning a different device.

For example, `https://factory.example.com/line1/pump7` and
`mqtt://site/line/cell/device/sensor` are valid sources.

An agreed binding MAY use an absolute, fragment-free Descriptor URL as
`source` if it identifies the originating context.
[Description Selection](#description-selection) defines when to retrieve
the source.

#### Event identity

Changing `source` to a Descriptor URL changes the
[event identity scope](../spec.md#id) and the scope of the
[Sequence extension](sequence.md). Changing `describedby` or `subject` leaves
both scopes unchanged.

### type

Core [`type`](../spec.md#type) identifies the event contract: the payload
representation, members, types and semantics defined by the publication
profile or protocol binding. Things can share a type when they share a
contract. The dot-separated type supports code generation.

The type MUST contain one or more segments separated by single dots. Each
segment MUST start with an ASCII letter or underscore; the rest can contain
only ASCII letters, digits and underscores. These restrictions apply only
to `type`; generators still handle language keywords. The last segment MUST
be the contract revision `vN`, with positive decimal `N` and no leading zeros.

A [Thing Model][TM] (TM) defines a reusable model for Things. A Producer
MAY configure the complete type. Otherwise, it derives the type from a
governing TM and, for an affordance event, the corresponding
model-affordance path. When composition or derivation leaves the mapping
ambiguous, the publication configuration MUST select it explicitly.
A Producer MUST NOT infer the mapping solely from
matching names or select the first TM link.

A TM entry in the Processing Descriptor MAY carry `type` to expose an
event binding. To use it, match the entry's `type` to the decoded event
`type` exactly. If the publication profile names a TM entry, only that
entry can match; otherwise, exactly one match is REQUIRED. An OPTIONAL
`affordanceselector` identifies a declaration in that TM using the [pointer
rules](#subject-descriptor-selection); omission selects no individual
declaration. Consumers using the binding MUST report missing, ambiguous, or invalid
bindings and unavailable TMs. Retrieve a TM when the operation needs it.

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

Changing a value or omitting or including an OPTIONAL member does not change
the revision. Changes to `describedby`, a TD URL, the selected schema or subject metadata
require a new revision only if they change the payload contract.

The Producer MUST configure a valid complete type when the derivation is
unavailable, produces an invalid symbol, or collides with a different event
contract in the Producer's type namespace. A slash-to-dot conversion is not
reversible: `/tm/pump.v1` and `/tm/pump/v1` produce the same suffix. The
Producer MUST disambiguate such contracts by configuration rather than
silently rewriting identifiers or member names.

### subject

The publication profile MUST choose Descriptor-driven or subject-driven
selection before the Consumer interprets [`subject`](../spec.md#subject).
In Descriptor-driven selection, `describedby` is REQUIRED and `subject`
is OPTIONAL with its Core meaning. The Consumer MUST use the selected TD
entry as the sole input for Thing or affordance retrieval and correlation.
In subject-driven selection, `subject` is REQUIRED and MUST use a form in
the following table. The Consumer MUST determine the mode from the
publication profile and the form from the decoded `subject`.

| Subject form | Meaning |
| --- | --- |
| `#` or `#/properties/processData` | Select the unique TD entry in the Processing Descriptor, then the whole Thing or affordance. |
| `pump7#/properties/processData` | Select the Processing Descriptor's named TD entry `pump7`, then its affordance. |
| `https://example.com/td/pump7/versions/3#/properties/processData` | Identify the Thing's affordance through a TD document URL; description selection follows the rules below. |
| `https://example.com/descriptorgroups/subjects/descriptors/pump7-process/versions/1` | Identify a Subject Descriptor Version. Its selected TD entry identifies the Thing and optionally one affordance. |

In subject-driven selection, the Consumer MUST classify the decoded `subject`
as follows:

1. If there is no literal `#`, the value MUST be an absolute HTTP(S) URL.
   It selects a Subject Descriptor Version under the rules below.
2. Otherwise, split at the first literal `#`. If the prefix begins with
   `http://` or `https://`, case-insensitively, it MUST be a valid absolute
   HTTP(S) URL and selects the direct-TD form.
3. Any other prefix MUST be empty or a valid Descriptor entry name.
   It selects the Descriptor-relative form.

The absence of a fragment and an empty fragment are different forms.
`https://example.com/document#` selects a whole TD;
`https://example.com/document` selects a Subject Descriptor Version and MUST
meet that form's requirements. A percent-encoded `%23` is part of the URL, not
the delimiter. Consumers MUST classify before percent-decoding a fragment.

Entry names follow the [Descriptor rules](descriptor.md#entries). For
example, `http:pump7#` has the Descriptor-relative form and names the entry
`http:pump7`. Invalid input or an unexpected
representation MUST NOT be retried through another form or resolved against
`source`.

For the forms containing `#`, the suffix including it MUST be a valid [RFC
6901][JSON Pointer] URI fragment. For the whole Thing, the Producer MUST use an
empty fragment, such as `#`, `pump7#` or
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

The subject identifies what the event concerns. Use the TD pointer as
defined above, without appending a writer or occurrence identifier.

The concrete TD path and corresponding TM declaration path can differ. This
profile does not infer a declaration-lineage mapping between them.

A Descriptor-relative subject can stay stable when `describedby` selects
a new version.

### dataschema and datacontenttype

Core [`dataschema`](../spec.md#dataschema) and
[`datacontenttype`](../spec.md#datacontenttype) describe the schema and media
type of `data`.

The publication profile or protocol binding determines whether an external
payload schema is REQUIRED. The Consumer MUST use `dataschema` when
present; otherwise, select the Processing Descriptor's [schema
entry][Schema Descriptor Profile]. Without a Processing Descriptor,
`dataschema` is the only candidate.

The Consumer MUST report a missing REQUIRED schema. An ambiguous selection,
invalid selector, unavailable schema or unsupported format MUST NOT cause
fallback to another schema. If `dataschema` is present, the Consumer MUST
still validate applicable Descriptor selectors and use `dataschema` as the
sole schema input. Producers and Descriptor
publishers SHOULD supply one schema source or identify the same schema in
both. Producers SHOULD omit `dataschema` when the Processing Descriptor
supplies the schema.

A TD can contain several DataSchemas. A Producer MUST NOT use a TD URL as
`dataschema` unless the URL identifies the schema for `data` itself.
The profile or binding maps an affordance's DataSchema to the wire payload.
Aggregated properties, event data and protocol envelopes can need different
schemas. A schema supplied through `dataschema` or a Descriptor MUST describe
the actual payload, including its encoding and envelope.

A profile MAY require an exact schema version independently of the selected
TD version.

## Description Selection

Apply [CloudEvents event-format decoding](../formats/json-format.md#22-type-system-mapping)
before checking attribute presence. An explicit `describedby` selects the
Processing Descriptor under the [Descriptor Reference
rules](descriptor.md#describedby). A **Subject Descriptor** serves a separate
role: in subject-driven selection, a fragment-free `subject` URL can select
a Descriptor for the Thing or affordance. Only the Processing Descriptor
can supply Descriptor-based event binding, schema, or writer metadata.

In Descriptor-driven selection, use the Processing Descriptor's [selected
TD entry](#subject-descriptor-selection). Missing or invalid input fails
correlation in that mode.

In subject-driven selection, use the decoded `subject` form:

1. For a fragment-free HTTP(S) URL, retrieve its Subject
   Descriptor Version and apply [Subject Descriptor
   selection](#subject-descriptor-selection). `describedby`, when present,
   remains the Processing Descriptor. The Consumer MUST limit lookup in
   this form to the Descriptors selected by those attributes.
2. For a direct-TD subject without `describedby`, retrieve its TD
   document at the exact prefix URL, including its query. Evaluate the
   fragment locally. The Consumer MUST use the retrieved TD directly as
   the sole description for correlation on this route.
3. Otherwise, use the Processing Descriptor selected through `describedby`,
   or the agreed source-Descriptor binding if `describedby` is absent. In the
   latter case, retrieve the exact `source` URL, which MUST be an absolute URL
   without a fragment. If no such binding was agreed, report a correlation
   failure.

For a Descriptor-relative or direct-TD subject using a Processing Descriptor,
select only entries of class `thingdescription`:

- For an empty subject prefix, the Processing Descriptor MUST have exactly
  one TD entry.
- For an entry-name prefix, the named entry MUST have that class.
- For a direct URL prefix, exactly one TD entry MUST
  have a `url` equal to that prefix. Consumers MUST compare the strings exactly,
  without URI normalization. Missing or duplicate matches are correlation
  failures. A named subject can disambiguate duplicate URLs.

Use the selected TD directly or from its bundled `document`. A URL mismatch
is a correlation failure even when a redirect destination, TD `id`, or
`entityid` matches.

The Producer MUST supply all REQUIRED inputs through the selected route,
event and profile. When the Producer uses `describedby`, the Consumer MUST
take Descriptor-based processing inputs exclusively from that Descriptor.

If selection, retrieval or correlation fails, the Consumer MUST report the
failure and leave the event uncorrelated. It MAY retain or forward the
uncorrelated event, but MUST NOT switch routes or substitute another TD.
See the [Descriptor Reference failure rules](descriptor.md#failure-outcomes)
for an explicit `describedby`.

The Publisher MUST make the selected TD available before configuring
Producers to use its URL or a Descriptor that references it. The Publisher
SHOULD use a TD Version URL.

### Subject Descriptor selection

When `subject` selects a Descriptor, its URL MUST identify a fixed **Version**
under an agreed binding. The Consumer MUST verify that the response is the
addressed Version under that binding, including after any redirect. A
`/versions/` substring or `versionid` alone is insufficient. Report a
correlation failure if verification fails. Use the URL unchanged.

When a Descriptor supplies the Thing or affordance selection, select the TD
entry named by the publication profile, or the unique TD entry if it names
none. Report missing or ambiguous entries. Retrieve that TD and apply the entry's
`affordanceselector`. A subject carrying its own fragment uses that fragment
instead.

Put `affordanceselector` in the selected TD entry, or omit it there to
select the whole Thing. A present selector
MUST be a plain RFC 6901 string selecting one existing affordance:
`/properties/<name>`, `/actions/<name>` or `/events/<name>`. Consumers MUST
apply only RFC 6901 string-form decoding. A present member with a null,
empty, object, root, or deeper selector is invalid. Annotations belong
beside the selector; their profile defines
their scope, type and omission rules.

Consumers MUST report invalid subject metadata, unavailable TDs and
unresolved selectors as correlation failures. Consumers MUST limit Subject
Descriptor selection to the directly selected Descriptor and TD.

When `subject` selects a Descriptor and `describedby` is present, its TD URL
MUST match the `url` of exactly one TD entry in the Processing Descriptor. This
comparison is byte-for-byte, without URI normalization, redirect substitution or
inference from TD or entity IDs. A missing or duplicate match is a correlation
failure. The Consumer MUST use the matching TD representation with the
selection and annotations from the Subject Descriptor alone. Missing or
invalid subject metadata is a correlation failure.

If `subject` and `describedby` name the same Version, follow the
[Descriptor caching rules](descriptor.md#caching) for response reuse.
Consumers MUST validate both roles independently.

## WoT Descriptor entries

A **TD entry** has class `thingdescription`; a **TM entry** has class
`thingmodel`. Both MUST link to the resolved document itself at `url`.
For example, with xRegistry, use the document-view URL. The base
[Descriptor rules](descriptor.md#entries) define the entry names.

A TD or TM entry MAY include `planurl`, an absolute, fragment-free HTTP(S)
URL for the projection plan that produced the view at `url`. The publication
profile defines its format. Consumers using the plan MUST verify that it
produced the linked view. The resolved view remains valid when this
OPTIONAL provenance is unavailable.

The [WoT entry schema](wot.schema.json) checks entry shape. The linked
document and selector target are checked under the relevant selection rules.

## Relationship to Other Extensions

An event that also uses the [OPC UA extension](opcua.md) MUST follow
its [combined WoT mapping](opcua.md#wot-mapping) for native message types,
sequence counters, and writer identities.

## Examples

### Single Affordance

This CloudEvent identifies a pump and its `processData` property. Its Descriptor
selects version `3.0.0` of the resolved TD and supplies the payload schema.
Another TD in the same Descriptor describes a gateway.

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

The Descriptor has the following entries:

```json
{
  "descriptorid": "pump7-telemetry",
  "versionid": "1",
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
    },
    "gateway1": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/gateway1/versions/1.0.0"
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

The subject prefix selects `pump7` by name, and the suffix selects its
`processData` property. The `payload` entry supplies the schema for the
object in `data`. This correlation uses the selected TD; the `geometry`
entry is available to an OpenUSD Consumer.

### Direct TD Subject

This event needs only the TD and an external payload schema, so it omits
`describedby`. The source identifies the service that emitted the event.

```json
{
  "specversion": "1.0",
  "id": "sample-4712",
  "source": "urn:example:actor:telemetry-service",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0#/properties/processData",
  "dataschema": "https://schemas.example/pump-process-data/versions/3",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

The Consumer retrieves the TD at the URL before `#` and evaluates
`/properties/processData` locally.

### Direct Subject with a Descriptor

The preceding event can instead select the same telemetry Descriptor:

```json
{
  "specversion": "1.0",
  "id": "sample-4714",
  "source": "urn:example:actor:telemetry-service",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0#/properties/processData",
  "describedby": "https://registry.example/descriptorgroups/streams/descriptors/pump7-telemetry/versions/1",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

The direct subject matches exactly the `pump7` entry. The Descriptor now
supplies the schema. Changing just the subject's TD Version to `4.0.0` would
fail correlation because this Descriptor names Version `3.0.0`. Adding another TD
entry with that same Version `3.0.0` URL would also make the direct match
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

Here `source` identifies the stream Descriptor as the originating context.
Changing this source URL changes the event identity scope.

### Subject Descriptor with Separate Processing Inputs

This event selects a Subject Descriptor Version through a fragment-free
`subject` URL. Its `describedby` independently selects the `pump7-telemetry`
Processing Descriptor shown in the Single Affordance example. For these
examples, the configured xRegistry HTTP base is `https://registry.example`, with
`descriptorgroups` and `descriptors` as the Descriptor collections.

```json
{
  "specversion": "1.0",
  "id": "sample-4716",
  "source": "urn:example:actor:telemetry-service",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "https://registry.example/descriptorgroups/subjects/descriptors/pump7-process/versions/1",
  "describedby": "https://registry.example/descriptorgroups/streams/descriptors/pump7-telemetry/versions/1",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

This deployment defines `acme_purpose` as an OPTIONAL non-empty string
that describes the selected affordance. Null is invalid.

```json
{
  "descriptorid": "pump7-process",
  "versionid": "1",
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0",
      "affordanceselector": "/properties/processData",
      "acme_purpose": "maintenance"
    },
    "pumpmodel": {
      "class": "thingmodel",
      "url": "https://registry.example/thingmodelgroups/factory/thingmodels/pump/versions/1.0.0",
      "type": "com.example.models.tm.pump.properties.processData.v1",
      "affordanceselector": "/properties/processData"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/pump-process-data/versions/3"
    }
  }
}
```

The TD's `processData` property supplies the subject. Access and operation
authorization follow the [security considerations](#security-considerations).
A second matching TD URL in the Processing Descriptor fails correlation.

The Descriptor-driven variant selects `pump7-process` through `describedby`
and omits `subject`. The same Descriptor supplies the concrete TD selector,
the schema, and the `type` binding to `pumpmodel`. The TM pointer need not
match the TD pointer.

```json
{
  "specversion": "1.0",
  "id": "sample-4717",
  "source": "urn:example:actor:telemetry-service",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "describedby": "https://registry.example/descriptorgroups/subjects/descriptors/pump7-process/versions/1",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

An event using this URL only as `subject` supplies an external payload
schema through `dataschema` when needed.

#### Whole Thing through a Subject Descriptor

The following Subject Descriptor selects the whole Thing by omitting
`affordanceselector`. Its `description` member describes the whole Thing.

```json
{
  "descriptorid": "pump7-whole",
  "versionid": "1",
  "description": "Pump 7 operating state",
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
    }
  }
}
```

Under the configured example Registry, its subject URL is
`https://registry.example/descriptorgroups/subjects/descriptors/pump7-whole/versions/1`.
An aggregate-state event can select this URL with the aggregate type and
Processing Descriptor used in the Whole Thing example. The direct-TD
form selects the whole Thing with a TD URL followed by `#`.

### Whole Thing

This CloudEvent carries aggregated data for the same pump. Its Descriptor
selects version `3.0.0` of the resolved TD and the aggregate payload schema. The
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
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/pump-state/versions/3"
    }
  }
}
```

The empty subject prefix selects the unique TD entry. The `payload` entry
supplies the schema for the complete object in `data`, which contains both
property values.

## Security Considerations

Resolvers MUST apply their configured trust, authorization and retrieval
policies before accessing documents. An untrusted identity or schema URI
MUST NOT authorize arbitrary network access, redirects or credential
forwarding. Implementations SHOULD bound document sizes and dependency
resolution.

Treat context attributes as Producer-supplied values unless another
mechanism authenticates them. Establish trust and access independently
for each referenced document, its model lineage, and its dependencies.
Correlating an event with an affordance does not authorize invoking it.

[TD]: https://www.w3.org/TR/wot-thing-description11/
[TM]: https://www.w3.org/TR/wot-thing-description11/#thing-model
[JSON Pointer]: https://www.rfc-editor.org/rfc/rfc6901
[Schema Descriptor Profile]: descriptor.md#schema
