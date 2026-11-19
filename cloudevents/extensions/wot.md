# Web of Things

This profile maps [Web of Things][TD] (WoT) Thing Descriptions (TDs) to
CloudEvents Core attributes and the OPTIONAL
[Descriptor Reference extension](descriptors.md). Either the event's
`subject` or its Processing Descriptor selects the Thing or affordance.
The `type` names the event contract.

Producers and Consumers agree on this mapping through a publication profile
or configuration. A direct TD subject can stand alone; see [Description
Selection](#description-selection) for use with `describedby`. This mapping
adds no attributes, transport binding or provisioning rules, and requires
no particular Registry implementation.

The [WoT Descriptor profile][WoT Descriptor Profile] defines the Reference
types `thingdescription` and `thingmodel`. A **TD Reference** is a named
entry in `references.thingdescription`; a **TM Reference** is a named entry in
`references.thingmodel`. Selectors name local entries, not Reference types.

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
occurred and follows Core's URI-reference rules. An actor can emit an event
concerning a different device.

For example, `https://factory.example.com/line1/pump7` and
`mqtt://site/line/cell/device/sensor` are valid sources.

An agreed binding MAY use an absolute, fragment-free Descriptor URL as
`source` if it identifies the originating context. Consumers MUST NOT infer
that binding from URL syntax. [Description Selection](#description-selection)
defines when to retrieve the source; neither direct TD nor Subject
Descriptor URLs trigger that lookup.

#### Event identity

Core requires `source` and `id` together to identify each distinct event.
Changing the `source` changes the event identity and
[Sequence extension](sequence.md) scope.
When returning to an earlier `source`, Producers MUST preserve the uniqueness
of `source` plus `id`. When using the Sequence extension, their `sequence`
values MUST remain ordered relative to earlier events from that same source.

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

A Producer MAY configure the complete type. Otherwise, it derives the type
from a governing [Thing Model][TM] (TM) and, for an affordance event, the
corresponding model-affordance path. When composition or derivation does not
identify that mapping unambiguously, the publication configuration MUST
select it explicitly. A Producer MUST NOT infer the mapping solely from
matching names or select the first TM link.

An OPTIONAL `data.wot.event` object in the Processing Descriptor exposes
that mapping to Consumers. Its REQUIRED `modelref` MUST name an exact entry
in `references.thingmodel`. To use the binding, Consumers MUST match its
REQUIRED `type` to the decoded CloudEvents `type` exactly and retrieve the
resolved TM under the [WoT Descriptor profile][WoT Descriptor Profile].
An OPTIONAL `affordanceselector` identifies one declaration using the same
pointer syntax as the subject selector; omission selects no individual
declaration. Consumers MUST report a mismatched type, invalid mapping or
unavailable model when using this binding; they MUST NOT guess another
model. Listing a TM or binding does not itself require retrieval.

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
In Descriptor-driven selection, `subject` is OPTIONAL. It retains its
Core meaning, but Consumers MUST NOT use it for retrieval or correlation.
In subject-driven selection, `subject` is REQUIRED and MUST use a form below.
Consumers MUST NOT infer the mode or form from a response body or URL path.

| Subject form | Meaning |
| --- | --- |
| `#` or `#/properties/processData` | Select the unique TD Reference in the Processing Descriptor, then the whole Thing or affordance. |
| `pump7#/properties/processData` | Select the Processing Descriptor's named TD Reference `pump7`, then its affordance. |
| `https://example.com/td/pump7/versions/3#/properties/processData` | Identify the Thing's affordance through a TD document URL; description selection follows the rules below. |
| `https://example.com/descriptorgroups/subjects/descriptors/pump7-process/versions/1` | Identify a Subject Descriptor Version. Its `data.wot.subject` selects the TD and optionally one affordance. |

After event-format decoding, the Consumer MUST classify the subject as follows:

1. If there is no literal `#`, the value MUST be an absolute HTTP(S) URL.
   It selects a Subject Descriptor Version under the rules below.
2. Otherwise, split at the first literal `#`. If the prefix begins with
   `http://` or `https://`, case-insensitively, it MUST be a valid absolute
   HTTP(S) URL and selects the direct-TD form.
3. Any other prefix MUST be empty or a valid Descriptor Reference name.
   It selects the Descriptor-relative form.

The absence of a fragment and an empty fragment are different forms.
`https://example.com/document#` selects a whole TD;
`https://example.com/document` selects a Subject Descriptor Version and MUST
meet that form's requirements. A percent-encoded `%23` is part of the URL, not
the delimiter. Consumers MUST classify before percent-decoding a fragment.

Reference names follow the Descriptor Registry's map-key rules and cannot
contain `/`; `http:pump7#` can use a Reference name, but is not an HTTP URL. A
name without a literal `#` is invalid. Invalid input or an unexpected
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

The subject identifies what the event concerns, not an occurrence. Do not
append a writer or native occurrence identifier to a subject pointer.

The concrete TD path and corresponding TM declaration path can differ. This
profile does not infer a declaration-lineage mapping between them.

A changed URL in `subject` affects filtering and correlation, not event
identity. A Descriptor-relative or descriptive subject can stay stable when
`describedby` changes Version.

### dataschema and datacontenttype

Core [`dataschema`](../spec.md#dataschema) and
[`datacontenttype`](../spec.md#datacontenttype) describe the schema and media
type of `data`, not the TD format.

The publication profile or protocol binding determines whether an external
payload schema is REQUIRED. The Consumer MUST use `dataschema` when
present; otherwise, use the Processing Descriptor's schema under the [Schema
Descriptor profile][Schema Descriptor Profile]. `data.schema.schemaref`
selects a named entry in `references.schema`. Without a Processing Descriptor,
`dataschema` is the only candidate.

The Consumer MUST report a missing REQUIRED schema. An ambiguous selection,
invalid selector, unavailable schema or unsupported format MUST NOT cause
fallback to another schema. If `dataschema` is present, the Consumer MUST
still validate applicable Descriptor selectors, but does not select a
Descriptor schema or compare schema documents. Producers and Descriptor
publishers SHOULD supply one schema source or identify the same schema in
both. Producers SHOULD omit `dataschema` when the Processing Descriptor
supplies the schema.

A TD can contain several DataSchemas. A Producer MUST NOT use a TD URL as
`dataschema` unless the URL identifies the schema for `data` itself.
The profile or binding maps an affordance's DataSchema to the wire payload.
Aggregated properties, event data and protocol envelopes can need different
schemas. A schema supplied through `dataschema` or a Descriptor MUST describe
the actual payload, including its encoding and envelope.

An xRegistry Schema Resource's document-view URL can identify that external
schema. It is not the WoT Resource's metadata-view URL. A profile MAY require
an exact schema Version independently of the selected TD Version.

## Description Selection

Apply event-format decoding before checking presence; JSON `null` means
unset. Retrieve and validate an explicit `describedby` under the [Descriptor
Reference rules](descriptors.md#descriptor-retrieval). It is authoritative
for processing inputs; failure MUST NOT cause fallback.

In Descriptor-driven selection, `describedby` and the selected Processing
Descriptor's [`data.wot.subject`](#subject-descriptor-selection) are REQUIRED.
Use that selector alone. Missing or invalid input is a correlation failure,
not a reason to look up `subject` or `source`.

In subject-driven selection, use the decoded `subject` form:

1. For a fragment-free HTTP(S) URL, retrieve its Subject
   Descriptor Version and apply [Subject Descriptor
   selection](#subject-descriptor-selection). `describedby`, when present,
   remains the Processing Descriptor. When absent, this route selects no
   Processing Descriptor and MUST NOT trigger source retrieval.
2. For a direct-TD subject without `describedby`, retrieve its TD
   document. Use the prefix unchanged, including its query; the fragment is
   evaluated locally and is not sent in HTTP. Do not retrieve a source
   Descriptor or construct a synthetic Descriptor from the TD.
3. Otherwise, use the Processing Descriptor selected through `describedby`,
   or the agreed source-Descriptor binding if `describedby` is absent. In the
   latter case, retrieve the exact `source` URL, which MUST be an absolute URL
   without a fragment. If no such binding was agreed, report a correlation
   failure.

For a Descriptor-relative or direct-TD subject using a Processing Descriptor,
select a Reference only from `references.thingdescription`, as follows:

- For an empty subject prefix, the Processing Descriptor MUST have exactly
  one TD Reference.
- For a Reference-name prefix, the named entry MUST exist in that bucket.
- For a direct URL prefix, exactly one TD Reference MUST
  have a `url` equal to that prefix. Consumers MUST compare the strings exactly,
  without URI normalization. Missing or duplicate matches are correlation
  failures. A named subject can disambiguate duplicate URLs.

The selected `url` identifies the ordinary TD document, not its Registry
metadata. The Consumer uses that representation directly or from an accepted
Descriptor bundle. It MUST NOT construct another URL from the Descriptor URL or
Reference. Redirect destinations, TD `id` and equal `entityid` values MUST NOT
be used to repair a subject-to-Reference mismatch.

The representation MUST be an ordinary resolved TD, not a TM. Apply the
[WoT Descriptor profile's][WoT Descriptor Profile] admission and provenance
rules, including `planurl` and plan/view pairing. Unavailable OPTIONAL
provenance does not prevent use of an otherwise valid TD.

The Producer MUST supply all REQUIRED inputs through the selected route,
event and profile. A direct TD or Subject Descriptor supplies neither an
external payload schema nor native publisher metadata. Producers can use
`describedby` for shared processing inputs; Consumers MUST NOT merge source
or subject fields.

If selection, retrieval or correlation fails, the Consumer MUST report the
failure and leave the event uncorrelated. It MAY retain or forward the event
without TD-based interpretation, but MUST NOT switch routes or substitute
another TD. This does not authenticate the originating entity or authorize an
action described by the TD.

The Publisher MUST make the selected TD available before configuring
Producers to use its URL or a Descriptor that references it. The Publisher
SHOULD use a TD Version URL. The [WoT Descriptor profile][WoT Descriptor Profile]
defines publication and stability of TDs and Subject Descriptors.

Changing only `describedby` does not change identity or sequence scope. A
Producer MUST NOT reuse an `id` or restart a source-wide sequence merely because
a description changes. An exact Version or successful resolution does not itself
prove that retrieved bytes are unchanged.

### Subject Descriptor selection

When `subject` selects a Descriptor, its URL MUST identify a fixed **Version**
under an agreed binding. The Consumer MUST use the URL unchanged and
verify that the response is the addressed Version. For xRegistry HTTP, check
the configured Registry base, [Version addressing][Descriptor Registry] and
returned identity. A `/versions/` substring or `versionid` alone is not
sufficient. An opaque URL is valid only if the binding identifies the Version
and defines how to verify it. The Consumer MUST report a correlation failure
if verification fails; redirects do not authorize a different Version.

In either mode, the Consumer MUST validate the selected `data.wot.subject`
under the [WoT Descriptor profile][WoT Descriptor Profile]. Its REQUIRED
`thingref` names one entry in `references.thingdescription`. Retrieve that TD.

Omit `affordanceselector` to select the whole Thing. A present selector
MUST be a plain RFC 6901 string selecting one existing affordance:
`/properties/<name>`, `/actions/<name>` or `/events/<name>`. Consumers MUST
NOT URI-fragment-decode or percent-decode it. Null, empty, object, root and
deeper selectors are invalid, not omission. Top-level selectors are not
aliases. Annotations belong beside the selector; their profile defines
their scope, type and omission rules.

Consumers MUST report invalid subject metadata, unavailable TDs and
unresolved selectors as correlation failures. Listing other References does
not require their retrieval. Consumers MUST NOT follow recursive Subject
Descriptor chains.

When `subject` selects a Descriptor and `describedby` is present, its TD URL
MUST match the `url` of exactly one TD Reference in the Processing Descriptor. This
comparison is byte-for-byte, without URI normalization, redirect substitution or
inference from TD or entity IDs. A missing or duplicate match is a correlation
failure. The Consumer uses the matching TD representation with the Subject
Descriptor's whole-Thing selection or affordance selector and annotations.
It does not merge Descriptor fields or substitute a selector from the
Processing Descriptor to repair missing or invalid subject metadata.

`data.wot.subject` and `data.wot.event` MAY appear independently. A subject
lookup MUST NOT supply event binding, schema or writer metadata, or trigger
a source lookup. Only the selected Processing Descriptor supplies those
Descriptor inputs. If both attributes name the same Version, Consumers MAY
reuse retrieval within the same representation and authorization context,
but MUST validate both roles, including the single TD URL match.

## Relationship to Other Extensions

This profile does not redefine native message types, sequence counters, or
writer identities. An event that also uses the [OPC UA extension](opcua.md)
MUST follow that extension's conditional WoT mapping.

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

The Descriptor has the following metadata. Core bookkeeping and any
profile-specific shared metadata are omitted from this excerpt.

```json
{
  "descriptorid": "pump7-telemetry",
  "versionid": "1",
  "references": {
    "thingdescription": {
      "pump7": {
        "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
      },
      "gateway1": {
        "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/gateway1/versions/1.0.0"
      }
    },
    "schema": {
      "payload": {
        "url": "https://schemas.example/pump-process-data/versions/3"
      }
    },
    "usdasset": {
      "geometry": {
        "url": "https://assets.example/usdassetgroups/line1/usdassets/pump7/versions/2"
      }
    }
  },
  "data": {
    "schema": { "schemaref": "payload" }
  }
}
```

The subject prefix selects `pump7`, not the first TD in the map. The suffix
selects its property. The payload directly contains the property's object value
without a `processData` wrapper. The selected schema describes that object, not
the TD document. The USD asset does not have to be retrieved for
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
  "subject": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0#/properties/processData",
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
  "subject": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0#/properties/processData",
  "describedby": "https://registry.example/descriptorgroups/streams/descriptors/pump7-telemetry/versions/1",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

The direct subject matches exactly the `pump7` Reference. The Descriptor now
supplies the schema. Changing just the subject's TD Version to `4.0.0` would
fail correlation because this Descriptor names Version `3.0.0`. Adding another TD
Reference with that same Version `3.0.0` URL would also make the direct match
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

The Subject Descriptor below omits Core bookkeeping. This deployment
defines `acme_purpose` as an OPTIONAL non-empty String about the selected
affordance, not processing policy. Null is invalid.

```json
{
  "descriptorid": "pump7-process",
  "versionid": "1",
  "references": {
    "thingdescription": {
      "pump7": {
        "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
      }
    },
    "thingmodel": {
      "pumpmodel": {
        "url": "https://registry.example/thingmodelgroups/factory/thingmodels/pump/versions/1.0.0"
      }
    },
    "schema": {
      "payload": {
        "url": "https://schemas.example/pump-process-data/versions/3"
      }
    }
  },
  "data": {
    "wot": {
      "subject": {
        "thingref": "pump7",
        "affordanceselector": "/properties/processData",
        "acme_purpose": "maintenance"
      },
      "event": {
        "type": "com.example.models.tm.pump.properties.processData.v1",
        "modelref": "pumpmodel",
        "affordanceselector": "/properties/processData"
      }
    },
    "schema": { "schemaref": "payload" }
  }
}
```

The TD's `processData` property supplies the subject. Correlation does not
invoke its form; TD security declarations do not authorize either lookup.
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

In contrast, an event using this URL only as `subject` needs `dataschema`
if an external schema is REQUIRED. A subject-only lookup MUST NOT supply it.

#### Whole Thing through a Subject Descriptor

The following Subject Descriptor selects the whole Thing by omitting
`affordanceselector`. The Core `description` describes the whole Thing.
The Descriptor does not use an empty or null pointer.

```json
{
  "descriptorid": "pump7-whole",
  "versionid": "1",
  "description": "Pump 7 operating state",
  "references": {
    "thingdescription": {
      "pump7": {
        "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
      }
    }
  },
  "data": { "wot": { "subject": { "thingref": "pump7" } } }
}
```

Under the configured example Registry, its subject URL is
`https://registry.example/descriptorgroups/subjects/descriptors/pump7-whole/versions/1`.
An aggregate-state event can select this URL with the aggregate type and
Processing Descriptor used in the Whole Thing example below. The existing
direct-TD whole-Thing subject remains the TD URL followed by `#`; it does
not use the stored affordance selector.

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
  "references": {
    "thingdescription": {
      "pump7": {
        "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
      }
    },
    "schema": {
      "payload": {
        "url": "https://schemas.example/pump-state/versions/3"
      }
    }
  },
  "data": { "schema": { "schemaref": "payload" } }
}
```

The empty subject prefix selects the unique TD Reference. The TD document itself
is not the payload. `data.schema.schemaref` selects the aggregate object schema,
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
[Descriptor Registry]: https://github.com/marcschier/xregistry-drafts/blob/e6f5b6af95e6abb8dfcd0311251e4244f54374aa/workingdrafts/models/descriptor/spec.md
[Schema Descriptor Profile]: https://github.com/xregistry/spec/pull/796/files#diff-392fa7cefe828f037942a4b1cc7901449d3578fbb5704d00f851f252e5f2e44a
[WoT Descriptor Profile]: https://github.com/marcschier/xregistry-drafts/pull/8/files#diff-275076606a2e5d246231a8182b3238d3ae6823028f628b2500cb0dc2baa63018
