# Descriptor Reference

The OPTIONAL `describedby` extension attribute identifies a Descriptor
containing shared information for interpreting an event. A Descriptor can
reference schemas, Message definitions, WoT Thing Descriptions or other
representations, and can contain typed metadata such as a publisher identity. It
describes information relevant to the event, not necessarily only the event's
source or subject.

This proposal is developed with the Descriptor Registry revision of
[xregistry/spec#796][Descriptor Registry]. That domain defines the metadata-only
Descriptor Resource, its Asset, Actor and Context specializations, named
References, selectors and OPTIONAL bundle. These are drafts, not released
standards. This document defines their CloudEvents binding; it does not require
a Producer to host or query a Registry.

A Publisher publishes Descriptors and their referenced representations. A
Producer emits events, and a Consumer processes them. A publication profile is
an agreement defining message interpretation and REQUIRED inputs. Producers and
Consumers establish that agreement through a specification or configuration, not
by trusting a profile asserted in untrusted metadata.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

The scope of these key words is limited to events using this extension or a
profile that explicitly uses its description-selection rules.

## Attributes

### describedby

- Type: `URI`
- Description: The absolute URL of the Descriptor selected for interpreting
  this event.
- Constraints:
  - OPTIONAL.
  - If present, MUST identify a Descriptor Resource or Descriptor Version
    and MUST NOT contain a fragment.
  - SHOULD identify a Descriptor Version. Profiles MAY require one.
  - Consumers MUST use the value unchanged as the request URL and as the URL
    component of the cache key. Cache selection MUST also account for the
    selected representation and authorization context.
  - Consumers MUST NOT derive other URLs from the value. In particular, they
    MUST NOT append `$details`, a view path or query parameter, or remove
    `/versions/<id>`.
  - An empty string or otherwise invalid set value is invalid, not absent.

In the JSON event format, `describedby` is a top-level string member. In HTTP
binary content mode, it is the `ce-describedby` header, encoded and decoded
according to the [HTTP binding](../bindings/http-protocol-binding.md). Other
bindings use their normal extension-attribute mapping.

Consumers MUST apply the event format's decoding rules before testing attribute
presence. In particular, the [JSON
format](../formats/json-format.md#22-type-system-mapping) treats `"describedby":
null` as unset, equivalent to omission. That is not a failed explicit reference
and does not prohibit a profile-defined route for events without `describedby`.
The same presence rule applies to the migration check for simultaneous old and
new attributes.

The name expresses a descriptive relationship, consistent with the
[`describedby` Web link relation][Link Relations]; it does not define an HTTP
`Link` header or a list of links.

## Core Attributes and Description Selection

Core attributes retain their meaning:

| Attribute | Meaning |
| --- | --- |
| `source` | Identifies the context in which the event occurred. It is not necessarily one physical Producer. |
| `subject` | Identifies what the event concerns within that originating context. It is a String, not inherently a retrieval URL. |
| `dataschema` | Identifies the schema that the event's `data` adheres to. |
| `describedby` | Identifies additional shared information for interpreting the event. It does not replace any of the above. |

A Producer SHOULD omit `describedby` when the event and agreed profile already
supply all REQUIRED inputs. If only an external payload schema is needed,
`dataschema` supplies that relationship without a Descriptor.

### Profile-defined source and subject retrieval

A profile MAY use a Descriptor URL as `source` when that URL also identifies the
originating context. It MAY define a subject that identifies a Thing or other
entity and permits retrieval of its description. Such a profile MUST define the
selected representation, any fragment processing, REQUIRED inputs and failure
behavior. An arbitrary processing metadata URL MUST NOT replace `subject` if it
no longer identifies what the event concerns under that profile.

Generic Consumers MUST NOT infer retrieval from an HTTPS scheme, a URL path
containing `descriptors`, or the absence of `describedby`. They MUST NOT resolve
arbitrary subject strings against `source`. Core URNs and relative source
references remain valid; a profile needing direct retrieval MUST define an
appropriate retrievable value or use `describedby`.

The [WoT profile](wot.md#description-selection) defines both Descriptor-relative
subjects and self-contained TD URL subjects. The latter can select a TD without
any Descriptor. This extension does not define a universal syntax for following
references from an entity record into another document.

### One selected processing description

| Condition | Processing |
| --- | --- |
| `describedby` is present and valid | Select that Descriptor, whether or not source or subject descriptions are also available. |
| `describedby` is present but invalid, unavailable or incomplete | Report the condition. Do not fall back to source or subject descriptions. |
| `describedby` is absent and the agreed profile defines source or subject retrieval | Use the profile's selected route. |
| `describedby` is absent and no retrieval mapping applies | This extension supplies no description. Do not probe source or subject. |
| `source` and `describedby` have the same URL | One retrieval per representation and authorization context can serve both uses; event identity is unchanged. |

When present, `describedby` MUST select a Descriptor supplying all Descriptor
inputs REQUIRED by the profile. It need not duplicate information already
supplied by the event. A Consumer MUST NOT merge missing fields from a source or
subject description, including when both descriptions identify the same entity.
The Source Descriptor and Processing Descriptor can describe different entities,
such as an actor and a device; differing entity identities alone are not a
metadata conflict.

When `describedby` is absent, a profile MUST distinguish its retrieval routes
before access. There is no general "try source, then subject" algorithm. A
failure in the selected route MUST NOT cause an implicit switch to another
route. OPTIONAL descriptive lookups for display do not supply missing processing
inputs.

For example, a source description might contain PublisherId. If an explicit
Processing Descriptor and the event omit that REQUIRED OPC UA value, the
Consumer reports missing metadata rather than borrowing it from the source
description. Conversely, an unavailable source description does not prevent
processing when the explicit Descriptor and event supply all REQUIRED inputs.

## Descriptor Representation and Processing

An ordinary `GET` of the selected Descriptor URL with `Accept: application/json`
returns Descriptor metadata directly. Its `hasdocument` model aspect is `false`;
no `$details` request or separate Descriptor document is needed.

The [Descriptor Registry][Descriptor Registry] defines these members:

| Member | Use |
| --- | --- |
| `references` | REQUIRED map of local Reference names to objects containing `class` and `url`. An empty map is valid. |
| `entityid`, `entitytype` | Describe a primary entity when one exists; not replacements for event source identity or authenticated principals. |
| `messageref`, `schemaref` | Select named Message and payload-schema References. |
| Profile attributes | Typed shared metadata whose meaning and relation to event fields are defined by the applicable profile. |

Representation classes include `message`, `schema`, `thingdescription`,
`thingmodel` and `usdasset`. Vendor classes use URI identifiers. Multiple
References can have the same class. Reference names do not establish emitter,
target, authority or execution roles.

A Consumer MUST check response status, media type and Descriptor validity
against that domain. A missing or incorrectly typed `references` map is invalid.
An empty map can be valid but insufficient for a profile requiring a TD or
schema. Explicit selectors MUST name an existing Reference of the expected
class, even when the event supplies `dataschema`.

For a valid Descriptor, the Consumer retrieves only the representations it
needs, subject to its access and content-trust policies. It MUST use their URLs
unchanged. A Reference's `class` identifies a representation, not a requirement
to retrieve it or permission to execute anything it describes. An unknown class
can be ignored if the profile does not need it; an unsupported REQUIRED input
makes interpretation unavailable. Entity identity and class URIs are not
automatic retrieval instructions.

### Message and schema selection

The Consumer uses the Descriptor Registry's selection rule: an explicit selector
names one Reference; without a selector, a unique Reference of the requested
class is selected. Zero candidates means absence; multiple candidates mean
ambiguity, not permission to select the first entry.

The Consumer selects the first applicable payload schema source:

1. The event's `dataschema`.
2. The Processing Descriptor's selected `schema` Reference.
3. The schema declared by its selected `message` representation.

Only absence permits proceeding to the next source. Ambiguity, an invalid
selector, unavailable selected content or an unsupported selected format MUST
NOT cause fallback to a different schema. With no Processing Descriptor, the
second and third candidates are absent; the Consumer MUST NOT synthesize one
from the TD or other retrieved content.

When `dataschema` is present, otherwise unselected schema inventory is
irrelevant to precedence. Explicit Descriptor selector validity is still
checked. Publishers and Producers SHOULD supply one applicable schema source, or
identify the same schema when several are supplied. Consumers apply the
precedence without comparing schema documents.

The Producer MUST ensure that the selected schema describes the actual `data`
representation, including any protocol envelope. A TD containing several
DataSchemas is not automatically the payload schema. The selected Message
definition applies only according to the publication profile; Consumers MUST NOT
guess it by matching `type` or by inspecting names when selection is ambiguous.

### Failure outcomes

| Condition | Result |
| --- | --- |
| REQUIRED inputs obtained and selected | Processing context available; this does not itself validate the payload or authorize an operation. |
| Missing, ambiguous, unavailable or unsupported REQUIRED input | Processing context unavailable. |
| Invalid shape, selector or profile value | Invalid metadata. |
| Repeated profile-defined values disagree after REQUIRED decoding | Metadata conflict. |
| Applicable validation completed | Payload valid or invalid, according to that validator. |
| Validation not performed or could not complete | Payload not checked; not a successful validation. |

These are processing outcomes, not new event attributes or HTTP error codes. The
Consumer SHOULD record a failure. Unless a profile requires an outcome, local
policy determines whether to defer, reject, or retain/forward the event without
that interpretation. It MUST NOT claim successful interpretation or validation
when the REQUIRED inputs are missing. Retaining an uninterpreted event does not
permit bypassing a failed explicit `describedby`.

## Publication, Identity and Replay

The Descriptor Registry defines publication and Version stability for all
processing-significant fields, including References, selectors and typed
metadata. A Publisher MUST make the representations REQUIRED by the profile
available before configuring Producers to emit the selected Descriptor URL. A
Producer MUST select information applicable to the event and SHOULD reuse
configured Version URLs when that information is unchanged. Producers are not
REQUIRED to perform runtime validation of each event by this extension.

A Descriptor Resource URL selects its current default Version, which can change.
Consumers SHOULD bound the freshness of cached Resource responses. A Version
fixes its published metadata, not the bytes at referenced URLs. Publishers
SHOULD pin REQUIRED representation Versions and retain them with the Descriptor
for the replay period. There is no lookup of the Version intended at event
`time`, and an ETag does not reconstruct that history.

`source` plus `id` retains its Core uniqueness rule. Changing `source`,
including a Version segment or query, changes the identity and source-wide
Sequence scope. Changing only `describedby` does not. Producers MUST NOT reuse
event identities or restart a claimed source-wide sequence when returning to an
earlier source.

Changing `subject` can change subscription filtering and correlation; it does
not change the source-plus-id identity scope. A profile using a versioned
description URL as subject MUST account for that coupling. A stable subject with
an independently versioned `describedby` avoids it.

## OPTIONAL Descriptor Bundle

A supporting endpoint can return the Descriptor and its direct referenced
representations at the same URL:

```http
Accept: application/vnd.xregistry.descriptor-bundle+json, application/json;q=0.5
```

The Consumer MUST inspect `Content-Type`. Ordinary `application/json` returns
metadata; the bundle media type returns `descriptor` and `documents` as defined
by the [Descriptor Registry][Descriptor Registry]. Each document entry uses the
same Reference name and records its exact URL, content type, content or base64
bytes, and redirect base URL when applicable.

The bundle covers each direct `references.*.url` or returns an error. It does
not fetch `planurl`, entity/class identifiers or transitive dependencies, and is
not a snapshot across Registries. An empty Reference map has an empty document
map. Relative dependencies use the target's recorded retrieval base, not the
Descriptor's URL.

This behavior is additional to Core metadata serving. Content negotiation alone
does not collect referenced URLs. A Publisher can prebuild a bundle for a
suitably configured endpoint, but the same completeness, access, freshness and
representation requirements apply.

A Consumer MAY retry ordinary JSON at the same unchanged Descriptor URL after a
bundle error and retrieve only its REQUIRED representations. This is a
representation retry, not fallback to another Descriptor or source. Consumers
and caches MUST distinguish negotiated representations and authorization
contexts, following the bundle's `Vary` and freshness rules.

## Examples

### Actor and processing description

An application profile reports an actor's maintenance decision about Pump 7. It
defines `pump7` as the subject identifier within that actor's context; this
generic example does not assert the WoT or OPC UA profile.

```json
{
  "specversion": "1.0",
  "id": "decision-47",
  "source": "https://registry.example/descriptorgroups/actors/descriptors/planner7",
  "subject": "pump7",
  "type": "com.example.maintenance.decision.v1",
  "describedby": "https://registry.example/descriptorgroups/streams/descriptors/pump7-maintenance/versions/1",
  "datacontenttype": "application/json",
  "data": {
    "inspectionNeeded": true
  }
}
```

The Processing Descriptor contains the following metadata; Core bookkeeping is
omitted. Its schema describes the decision payload, not the TD document.

```json
{
  "descriptorid": "pump7-maintenance",
  "versionid": "1",
  "schemaref": "payload",
  "references": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/maintenance-decision/versions/1"
    }
  }
}
```

The actor's independently retrieved description can have `references: {}` and
actor identity metadata. It is not merged with the Processing Descriptor.
Neither description is an authorization to inspect or operate the pump.

### Without an additional link

For the same application profile, if the event and an explicit `dataschema`
already supply every REQUIRED input, no `describedby` is needed. A profile can
also select a sufficient Descriptor through `source`, or retrieve a subject
description through a defined mapping. Neither case is inferred by a generic
Consumer.

The [WoT examples](wot.md#examples) show a concrete direct TD subject without a
Descriptor and a source-selected Descriptor. The [OPC UA
mapping](opcua.md#shared-stream-metadata-in-a-descriptor) defines when a
selected Descriptor Version supplies native stream metadata.

## Migration from Event Context

This revision replaces the draft `contexturl` extension and Role-keyed Context
representation. Existing events retain their original attribute and profile
semantics; Consumers MUST NOT silently reinterpret them as the new binding.
Deployments retaining such events need the old reader or an explicit conversion
policy. A profile using this revision MUST reject an event with both
`contexturl` and `describedby` unless a separate migration agreement defines
that combination.

Do not rewrite historical sources merely to adopt registry-based identity. Names
discussed only during design, such as `contracturl`, `refset` and `contextref`,
are not aliases defined by this extension.

## Security Considerations

Consumers and bundle endpoints MUST apply authorization, URL, redirect and
content-trust policies before retrieving or using Descriptors or their
representations. An event-provided URL MUST NOT authorize arbitrary network
access or credential forwarding. Implementations SHOULD bound response sizes,
decompression, retrieval time, redirects and dependency processing.

Read access to a Descriptor does not grant access to its targets. Caches MUST
NOT share representations across authorization contexts unless the applicable
access policy permits it. A bundle does not bypass trust checks. Versions do not
authenticate content or prove unchanged bytes.

Descriptive entity IDs, TD security declarations and references to actions are
not authenticated principals, execution grants or current readiness. Device
admission and operation outcomes remain governed by their own protocols and
trusted authorities.

[Descriptor Registry]: https://github.com/xregistry/spec/pull/796
[Link Relations]: https://www.iana.org/assignments/link-relations/
