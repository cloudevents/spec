# Web of Things

This profile maps a [Web of Things Thing Description][TD] (TD) to CloudEvents
Core context attributes and optionally the [Descriptor Reference
extension](descriptors.md). The REQUIRED `subject` identifies a Thing or
affordance through a Processing Descriptor, a self-contained TD document URL, or
a Subject Descriptor Version containing a TD pointer and subject annotations.
The `type` names the event contract.

The profile defines no new CloudEvents extension attributes. Producers and
Consumers agree on its use through a publication profile or configuration. It
does not define a transport binding, provision a Thing, or require a particular
registry implementation. A direct TD subject can supply the REQUIRED description
without a Descriptor; an explicit `describedby` can supply additional shared
information when needed.

The [WoT Descriptor profile][WoT Descriptor Profile] owns these representation
class identifiers:

| Representation | Class identifier |
| --- | --- |
| Thing Description | `https://xregistry.io/classes/thingdescription` |
| Thing Model | `https://xregistry.io/classes/thingmodel` |

In this document, a **TD Reference** has the first URI as its exact `class`
value. A **TM Reference** has the second URI. The former bare class names
`thingdescription` and `thingmodel` are not aliases. The class identifiers are
not retrieval instructions.

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
source is retrieved. A direct TD subject or Subject Descriptor URL does not
trigger that lookup.

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

A change to a Subject Descriptor's pointer or annotations follows the same rule:
whether the payload contract changed determines the type revision, not the
presence of a new Descriptor Version.

The Producer MUST configure a valid complete type when the derivation is
unavailable, produces an invalid symbol, or collides with a different event
contract in the Producer's type namespace. A slash-to-dot conversion is not
reversible: `/tm/pump.v1` and `/tm/pump/v1` produce the same suffix. The
Producer MUST disambiguate such contracts by configuration rather than
silently rewriting identifiers or member names.

### subject

The [`subject`](../spec.md#subject) is REQUIRED. It MUST use one of the forms
below. The agreed profile determines their meaning before retrieval; Consumers
MUST NOT choose a form by inspecting a response body or guessing from a URL
path. Each form ultimately selects the ordinary resolved TD and the Thing or
affordance that the event concerns.

| Subject form | Meaning |
| --- | --- |
| `#` or `#/properties/processData` | Select the unique TD Reference in the Processing Descriptor, then the whole Thing or affordance. |
| `pump7#/properties/processData` | Select the Processing Descriptor's named TD Reference `pump7`, then its affordance. |
| `https://example.com/td/pump7/versions/3#/properties/processData` | Identify the Thing's affordance through a TD document URL; description selection follows the rules below. |
| `https://example.com/descriptorgroups/subjects/descriptors/pump7-process/versions/1` | Identify a Subject Descriptor Version whose `wotsubject` selects the TD and pointer. The URL has no literal `#`. |

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

For a Subject Descriptor, the profile's `wotsubject.pointer` uses the JSON
Pointer **string** representation: `""` selects the whole Thing, and a non-empty
pointer starts with `/`. Consumers MUST NOT apply URI-fragment or percent
decoding to that stored pointer. For example, `/properties/pressure~1bar`
selects `pressure/bar`, while `/properties/pressure%2Fbar` selects the literal
name `pressure%2Fbar`. The latter MUST NOT be interpreted as `pressure/bar`.

The subject identifies the Thing or affordance, not an occurrence. Different
events can have the same subject and different CloudEvents `id` values. A
binding-specific writer identifier or native occurrence identifier is not
appended to this pointer.

The concrete TD path and corresponding TM declaration path can differ. This
profile does not infer a declaration-lineage mapping between them.

Changing a direct subject's TD Version URL or a Subject Descriptor Version URL
changes the subject string used for filtering and correlation, not the
source-plus-id event identity. A Descriptor-relative subject with an
independently versioned `describedby` can avoid that coupling when subject
annotations do not need their own versioned description.

### dataschema and datacontenttype

Core [`dataschema`](../spec.md#dataschema) identifies the schema that the
CloudEvent's actual `data` adheres to.
[`datacontenttype`](../spec.md#datacontenttype) identifies that data's media
type. Neither identifies the TD document's format.

The Consumer follows the Descriptor Reference extension's [schema
precedence](descriptors.md#schema-selection): `dataschema`, then the selected
Processing Descriptor's schema. A Subject Descriptor does not supply that second
candidate merely because it contains schema References or `schemaref`. Without a
Processing Descriptor, the second source is absent. The Producer SHOULD omit
`dataschema` when a selected Processing Descriptor already supplies the schema.

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
rules](descriptors.md#one-selected-processing-description), including when
`describedby` is absent. Apply event-format decoding before testing presence;
JSON `null` means unset, including for `subject`. An unset subject fails this
profile's REQUIRED-subject constraint. Selection proceeds as follows:

1. If `describedby` is present, retrieve and validate its Descriptor. It is
   authoritative for processing inputs; a failure MUST NOT cause fallback to
   source, direct TD or Subject Descriptor processing.
2. If the subject is a fragment-free HTTP(S) URL, retrieve its Subject
   Descriptor Version and apply [Subject Descriptor
   selection](#subject-descriptor-selection). `describedby`, when present,
   remains the Processing Descriptor. When absent, this route selects no
   Processing Descriptor and MUST NOT trigger source retrieval.
3. Otherwise, for a direct-TD subject without `describedby`, retrieve its TD
   document. Use the prefix unchanged, including its query; the fragment is
   evaluated locally and is not sent in HTTP. Do not retrieve a source
   Descriptor or construct a synthetic Descriptor from the TD.
4. Otherwise, use the Processing Descriptor selected through `describedby`,
   or the agreed source-Descriptor binding if `describedby` is absent. In the
   latter case, retrieve the exact `source` URL, which MUST be an absolute URL
   without a fragment. If no such binding was agreed, report a correlation
   failure.

For a Descriptor-relative or direct-TD subject using a Processing Descriptor,
select its TD Reference as follows:

- For an empty subject prefix, the Processing Descriptor MUST have exactly
  one TD Reference.
- For a Reference-name prefix, that entry MUST exist and MUST be a TD
  Reference.
- For a direct URL prefix, exactly one TD Reference MUST
  have a `url` equal to that prefix. Consumers MUST compare the strings exactly,
  without URI normalization. Missing or duplicate matches are correlation
  failures. A named subject can disambiguate duplicate URLs.

The selected `url` identifies the ordinary TD document, not its Registry
metadata. The Consumer uses that representation directly or from an accepted
Descriptor bundle. It MUST NOT construct another URL from the Descriptor URL or
Reference. Redirect destinations, TD `id` and equal `entityid` values MUST NOT
be used to repair a subject-to-Reference mismatch.

A TM Reference cannot replace an instance TD. The selected representation MUST
be an ordinary resolved TD. The [WoT Descriptor profile][WoT Descriptor Profile]
defines the TD/TM admission and provenance rules, including profile-specific
`planurl` and plan/view pairing. Consumers using that profile MUST apply its
admission and provenance rules. Failure to obtain or validate a REQUIRED profile
input MUST cause a reported correlation failure. Unavailable OPTIONAL provenance
does not prevent correlation with an otherwise usable TD. The generic Descriptor
model does not define those provenance attributes.

The Producer MUST supply all REQUIRED inputs through the selected route, the
event and the agreed publication profile. A direct TD or a Subject Descriptor
alone does not supply an external payload schema or native publisher metadata. A
Producer needing shared processing inputs can use a complete Processing
Descriptor with `describedby`. A Consumer MUST NOT merge them from source or
subject descriptions.

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
Registry rules. This also applies to a Subject Descriptor's selected pointer,
annotations and TD Reference: publishing a changed subject description requires
a new Descriptor Version.

Changing only `describedby` does not change identity or sequence scope. A
Producer MUST NOT reuse an `id` or restart a source-wide sequence merely because
a description changes. An exact Version or successful resolution does not itself
prove that retrieved bytes are unchanged.

### Subject Descriptor selection

The subject URL MUST identify a Descriptor **Version**, not a Resource's
changing default. The Producer and Consumer MUST use an agreed registry or
publication binding that identifies the Version addressed by this URL. Consumers
MUST verify that the retrieved Descriptor is that Version.

For the xRegistry HTTP binding, a configured Registry base and Descriptor model
provide the Version-addressing structure:
`/<GROUPS>/<GID>/<RESOURCES>/<RID>/versions/<VID>`. The Consumer validates the
request URL under that complete binding and checks the returned Descriptor
identity and `versionid` against the addressed entity. It MUST NOT infer Version
identity merely from an arbitrary `/versions/` substring or the presence of
`versionid` in a response: default Resource responses also expose Version
metadata.

An external publication binding MAY map an opaque absolute URL to a fixed
Descriptor Version. That mapping MUST identify the Version and define how the
Consumer verifies it. If no supported binding can establish the Version
identity, the Consumer MUST report a correlation failure. Redirects do not
authorize substitution of a default or different Version. Requests use the
subject URL unchanged; they do not append or remove a version segment.

The Consumer MUST validate the Subject Descriptor and its `wotsubject` according
to the [WoT Descriptor profile][WoT Descriptor Profile]. That object requires an
exact local `reference` naming a TD Reference and a `pointer` in RFC 6901 string
form. The object and both members MUST be present and non-null; an empty pointer
string is valid. CE's event-attribute null decoding does not apply to members of
retrieved Descriptor metadata. Typed subject annotations follow the defining
profile's value and null rules.

The selected Reference MUST identify an ordinary resolved TD. The stored pointer
MUST select the intended whole Thing or concrete affordance. Consumers MUST
report missing or malformed subject metadata, a wrong Reference class, an
invalid pointer, an unavailable TD or a pointer that does not select the
intended member. Other References do not become retrieval prerequisites solely
because they occur in the same Descriptor. The Consumer MUST NOT follow
recursive Subject Descriptor chains.

If `describedby` is present, the selected Subject Descriptor TD URL MUST match
the `url` of exactly one TD Reference in the Processing Descriptor. This
comparison is byte-for-byte, without URI normalization, redirect substitution or
inference from TD or entity IDs. A missing or duplicate match is a correlation
failure. The Consumer uses the matching TD representation with the Subject
Descriptor's pointer and annotations; it does not merge Descriptor fields or
substitute the Processing Descriptor's own subject pointer for a missing or
invalid one.

If `describedby` is absent, the Subject Descriptor still supplies only subject
semantics. Its `schemaref`, schema References, publisher or writer metadata MUST
NOT supply processing inputs. The event and agreed profile MUST supply those
inputs; an external payload schema uses `dataschema`. The Consumer MUST NOT
query source metadata to supplement this route.

The same Version URL MAY be explicitly used for both `subject` and
`describedby`. Consumers MAY reuse an authorized cached or retrieved
representation for the same URL, representation and authorization context, but
MUST validate each role independently, including the exactly-one TD URL match.
The explicit processing role MAY then supply the schema and shared metadata; the
subject role alone cannot do so.

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
      "class": "https://xregistry.io/classes/thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3"
    },
    "gateway1": {
      "class": "https://xregistry.io/classes/thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/gateway1/versions/1"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/pump-process-data/versions/3"
    },
    "geometry": {
      "class": "https://xregistry.io/classes/usdasset",
      "url": "https://assets.example/usdassetgroups/line1/usdassets/pump7/versions/2"
    }
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

The Subject Descriptor at the event's `subject` URL contains the following
metadata. Core bookkeeping is omitted. This example's deployment profile defines
`acme_purpose` as an OPTIONAL non-empty String annotation on `wotsubject`; a
present null is invalid under that example profile. It describes the purpose of
the subject view, not processing policy.

```json
{
  "descriptorid": "pump7-process",
  "versionid": "1",
  "wotsubject": {
    "reference": "pump7",
    "pointer": "/properties/processData",
    "acme_purpose": "maintenance"
  },
  "references": {
    "pump7": {
      "class": "https://xregistry.io/classes/thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3"
    }
  }
}
```

For this example, the selected TD at that Reference's URL is:

```json
{
  "@context": "https://www.w3.org/2022/wot/td/v1.1",
  "id": "urn:example:asset:pump7",
  "title": "Pump 7",
  "securityDefinitions": {
    "nosec_sc": {
      "scheme": "nosec"
    }
  },
  "security": ["nosec_sc"],
  "properties": {
    "processData": {
      "type": "object",
      "readOnly": true,
      "properties": {
        "Speed": { "type": "number" },
        "Pressure": { "type": "number" }
      },
      "required": ["Speed", "Pressure"],
      "forms": [
        {
          "href": "https://devices.example/pump7/process-data",
          "op": "readproperty",
          "contentType": "application/json"
        }
      ]
    }
  }
}
```

The TD URL matches exactly one TD Reference in the Processing Descriptor. The
Consumer evaluates `/properties/processData` as a stored JSON Pointer, uses
`acme_purpose` only as defined subject annotation, and selects the payload
schema from the Processing Descriptor's `schemaref`. It does not read the TD
form merely to correlate the event. The TD's example security declaration does
not authorize access to either Descriptor.

Changing the Subject Descriptor's TD URL to Version `4` without a matching
Processing Descriptor update fails correlation. Adding a second matching TD URL
to the Processing Descriptor also fails. Changing the pointer to null fails even
when the Processing Descriptor contains a usable pointer; there is no
cross-Descriptor repair.

The following variant retains the Subject Descriptor but selects no Processing
Descriptor. Its external schema is carried by the event:

```json
{
  "specversion": "1.0",
  "id": "sample-4717",
  "source": "urn:example:actor:telemetry-service",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "https://registry.example/descriptorgroups/subjects/descriptors/pump7-process/versions/1",
  "dataschema": "https://schemas.example/pump-process-data/versions/3",
  "datacontenttype": "application/json",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

Adding a schema Reference to the Subject Descriptor would not replace this
event's `dataschema`. If a REQUIRED schema were missing, the Consumer would
report that condition rather than select it from the Subject Descriptor or query
the source.

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
      "class": "https://xregistry.io/classes/thingdescription",
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
[WoT Descriptor Profile]: https://github.com/marcschier/xregistry-drafts/blob/12024152a0b10588e98ed33879fd7a5269f1290b/workingdrafts/models/wot/spec.md#66-wot-descriptor-profile
