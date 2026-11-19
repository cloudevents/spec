# Descriptor Reference

The OPTIONAL `describedby` attribute identifies an [xRegistry
Descriptor][Descriptor Registry] with shared inputs for interpreting an
event. The profile defines which inputs the Descriptor supplies. It need
not describe the event's source or subject.

xRegistry defines the Descriptor representation, retrieval of its metadata
and bundles, and [publication and Version stability][Publication Stability].
Producers need not host or query a Registry. Producers and Consumers agree
on the profile through a specification or configuration, not through
untrusted event or Descriptor metadata.

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
  - Consumers MUST use the URL unchanged for requests and cache lookup.
    Cache selection MUST account for representation and authorization context.
  - Consumers MUST NOT derive other URLs, including by adding `$details`,
    a view path or query parameter, or removing `/versions/<id>`.
  - An empty string or otherwise invalid set value is invalid, not absent.

In the JSON event format, `describedby` is a top-level string member. In HTTP
binary content mode, it is the `ce-describedby` header, encoded and decoded
according to the [HTTP binding](../bindings/http-protocol-binding.md). Other
bindings use their normal extension-attribute mapping.

Consumers MUST decode attributes before checking presence. In the [JSON
format](../formats/json-format.md#22-type-system-mapping), `"describedby":
null` means unset, so the profile can use its route for an
omitted `describedby`. This is not a failed explicit reference.

The name expresses a descriptive relationship, consistent with the
[`describedby` Web link relation][Link Relations]; it does not define an HTTP
`Link` header or a list of links.

## Descriptor Retrieval

When `describedby` is present, the Consumer MUST use it to select the
Descriptor. Retrieve it at the supplied URL with HTTP `GET`, using
`Accept: application/json` for metadata or bundle
negotiation as defined by the [Descriptor Registry][Descriptor Registry].
The Consumer MUST check response status, media type and Descriptor validity
before using it, including any applicable selectors. `describedby` MUST
identify a Descriptor that supplies the processing inputs the profile requires
from it. Those inputs need not duplicate inputs already in the event. The
Consumer MUST NOT supplement them from another description.

A Producer SHOULD omit `describedby` if the event and agreed profile
already supply all REQUIRED inputs. An absent `describedby` supplies no
Descriptor through this extension and does not authorize lookup through
another attribute. The applicable profile defines how it interprets other
event attributes and whether it requires a Descriptor Version.

### Failure outcomes

| Condition | Result |
| --- | --- |
| REQUIRED inputs obtained and selected | Processing context available; this does not itself validate the payload or authorize an operation. |
| Missing, ambiguous, unavailable or unsupported REQUIRED input | Processing context unavailable. |
| Invalid shape, selector or profile value | Invalid metadata. |
| Applicable validation completed | Payload valid or invalid, according to that validator. |
| Validation not performed or could not complete | Payload not checked; not a successful validation. |

If an explicit `describedby` is invalid, unavailable or incomplete, the
Consumer MUST report the failure and MUST NOT substitute another description
for it. A profile MAY permit processing that does not depend on the Descriptor,
but the Consumer MUST NOT report successful Descriptor-based interpretation or
validation without REQUIRED inputs. Unless the profile dictates the outcome,
local policy determines whether to defer, reject, retain or forward an
uninterpreted event. These outcomes add no event attributes or HTTP error codes.

## Examples

### Actor and processing description

An application profile reports an actor's maintenance decision about Pump 7. It
defines `pump7` as the subject identifier within that actor's context.

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

The Descriptor below omits Core bookkeeping. Its schema
describes the decision payload, not the TD document. The WoT profile defines
the `thingdescription` Reference type; the Schema Descriptor profile defines
`schema`. The type keys group References; `pump7` and `payload` name entries.

```json
{
  "descriptorid": "pump7-maintenance",
  "versionid": "1",
  "references": {
    "thingdescription": {
      "pump7": {
        "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
      }
    },
    "schema": {
      "payload": {
        "url": "https://schemas.example/maintenance-decision/versions/1"
      }
    }
  },
  "data": { "schema": { "schemaref": "payload" } }
}
```

No actor lookup is needed.

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

[Descriptor Registry]: https://github.com/marcschier/xregistry-drafts/blob/e6f5b6af95e6abb8dfcd0311251e4244f54374aa/workingdrafts/models/descriptor/spec.md
[Publication Stability]: https://github.com/marcschier/xregistry-drafts/blob/e6f5b6af95e6abb8dfcd0311251e4244f54374aa/workingdrafts/models/descriptor/spec.md#46-versions-and-publication-stability
[Link Relations]: https://www.iana.org/assignments/link-relations/
