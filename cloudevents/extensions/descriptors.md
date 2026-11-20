# Descriptor Reference

The OPTIONAL `describedby` attribute identifies a Descriptor that supplies
information for interpreting an event. This extension defines the document
and how to retrieve it. Descriptor profiles define which entries supply the
information and how to use them. A static HTTP server or an xRegistry
Registry can serve the same document. Producers and Consumers agree on the
profile through a specification or configuration.

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
  - If present, MUST be an absolute HTTP(S) URL identifying a Descriptor and
    MUST NOT contain a fragment.
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
null` means unset. In this case a profile can define the route for an
omitted `describedby`.

The name expresses a descriptive relationship, consistent with the
[`describedby` Web link relation][Link Relations].

## Descriptor Retrieval

When `describedby` is present, the Consumer MUST retrieve the Descriptor at
the supplied URL with HTTP `GET`. A Consumer can request metadata with
`Accept: application/json` or request a bundle with
`Accept: application/vnd.xregistry.descriptor-bundle+json`.

A server supporting negotiation MUST return the preferred available
representation, with its `Content-Type` and `Vary: Accept`. If both are
acceptable and neither is preferred, the server MUST return metadata.
A Consumer that also accepts metadata can send
`Accept: application/vnd.xregistry.descriptor-bundle+json, application/json;q=0.5`.
A server supporting negotiation MUST return `406 Not Acceptable` when
neither representation is acceptable. A static server can publish a
prebuilt bundle at `describedby` or at the advertised `bundleurl`.
When following `bundleurl`, the Consumer MUST use the advertised URL, not
construct it from `describedby`. The returned bundle MUST have the same
`descriptorid` and `versionid` as the metadata that advertised it.

The Consumer MUST check response status, media type and Descriptor validity
before using it, including any applicable selectors. `describedby` MUST
reference a Descriptor that supplies the information the profile requires
from it. The Consumer MUST NOT fill gaps in that information from another
description. The Descriptor SHOULD NOT duplicate information in the event.

A Producer SHOULD omit `describedby` if the event and agreed profile
already supply all REQUIRED information. The applicable profile MAY define
how to interpret other event attributes and whether a URL that always
identifies the same Descriptor version is REQUIRED.

### Descriptor document

The [Descriptor JSON Schema](descriptor.schema.json) defines the response
shape. Validate against `metadata` or `bundle` in the schema's `$defs`,
according to the representation received. Profile and URL validation still
apply. xRegistry Core properties can accompany the document but Consumers
MUST NOT require them for this extension.

| Member | Presence | Meaning |
| --- | --- | --- |
| `descriptorid` | REQUIRED | Nonempty identifier of the Descriptor in its publication scope. |
| `versionid` | REQUIRED | Nonempty version identifier in that Descriptor's scope. |
| `entityid` | OPTIONAL | Absolute, fragment-free URI identifying the primary described entity. It does not trigger retrieval. |
| `bundleurl` | OPTIONAL | Absolute, fragment-free HTTP(S) URL for a direct GET of the same version's bundle. Omit it when the server does not support a bundle for this Descriptor. When present in the bundle, it points to the bundle itself. |
| `entries` | REQUIRED | Map of named entries. An empty map is valid. |

Entry names are one to 63 lowercase ASCII letters, digits, colons, hyphens,
underscores or dots, starting with a letter or digit. Each entry has a
REQUIRED `class`. The `class` identifies the linked document type, if any,
and defines the inline fields. Standard classes use short lowercase
alphanumeric tokens starting with a letter. Independent classes use
reverse DNS names under the defining party's control. Each class key is at
most 63 characters. An entry with a linked document MUST have an absolute,
fragment-free HTTP(S) `url`. An inline-only entry MUST omit `url`. A null
value is invalid. The profile defines whether a class links to a document.

The same class MAY appear under different entry names. Profiles define how
to select entries, including where a name comes from when needed. When a
profile needs one entry and its rules leave several candidates, the Consumer
MUST report ambiguity, not choose by map order. This extension defines no
Descriptor-wide selector.

Publishers MUST keep the entries, their inline fields, and their referenced
representations stable for the intended use and replay of a published
version. Publish a new version when those inputs change. The identifiers
alone do not establish that a URL selects a fixed version.

### Bundled document

A bundle has the same Descriptor members as metadata. For each entry with
a `url`, it adds a `document` object to that entry. It MUST NOT add a
`document` to an inline-only entry. Metadata responses omit all `document`
members. A bundle contains the directly linked documents only; its server
MUST NOT automatically follow links from profile fields or from the documents.

Each `document` has a REQUIRED `contenttype` and exactly one of `content`
(a JSON value) and `contentbase64` (base64-encoded bytes). Non-JSON
representations use `contentbase64`. When the retrieved document has no
media type, use `application/octet-stream`. The server MUST decode HTTP content
codings before embedding bytes. If an allowed redirect changed the retrieval
URL, `document.baseurl` MUST give the final URL. The entry's `url` stays
unchanged. Consumers resolve any format-specific relative links against
`baseurl` if present, or the entry `url` otherwise.

The server MUST verify authorization and obtain the complete document for
every linked entry before returning a successful bundle. If it cannot do so,
it MUST report failure rather than return a partial bundle. The Consumer
MAY retry the unchanged `describedby` URL for metadata and retrieve only
the entries it needs. That is a different representation of the same
Descriptor, not a fallback to another description.

### Failure outcomes

| Condition | Result |
| --- | --- |
| REQUIRED inputs obtained and selected | Processing context available. It does not validate the payload or authorize an operation. |
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

### Maintenance decision

A maintenance service reports a decision about Pump 7. The event's
`describedby` URL identifies the Descriptor for interpreting that decision.

```json
{
  "specversion": "1.0",
  "id": "decision-47",
  "source": "urn:example:maintenance-service:planner7",
  "subject": "pump7",
  "type": "com.example.maintenance.decision.v1",
  "describedby": "https://registry.example/descriptorgroups/streams/descriptors/pump7-maintenance/versions/1",
  "datacontenttype": "application/json",
  "data": {
    "inspectionNeeded": true
  }
}
```

The `pump7` entry identifies the pump's Thing Description. The `payload`
entry supplies the schema for the decision.

```json
{
  "descriptorid": "pump7-maintenance",
  "versionid": "1",
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/maintenance-decision/versions/1"
    }
  }
}
```

### Bundled schema

The client requests a bundle without constructing a new URL. The
`bundleurl` in the response identifies the same bundle for direct retrieval.

```http
GET /descriptors/inspection-schema/versions/1 HTTP/1.1
Host: registry.example
Accept: application/vnd.xregistry.descriptor-bundle+json
```

```http
HTTP/1.1 200 OK
Content-Type: application/vnd.xregistry.descriptor-bundle+json
Vary: Accept
Cache-Control: no-store
Connection: close
```

```json
{
  "descriptorid": "inspection-schema",
  "versionid": "1",
  "bundleurl": "https://registry.example/bundles/inspection-schema/1",
  "entries": {
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/maintenance-decision/versions/1",
      "document": {
        "contenttype": "application/schema+json",
        "content": {
          "$schema": "https://json-schema.org/draft/2020-12/schema",
          "type": "object",
          "properties": { "inspectionNeeded": { "type": "boolean" } },
          "required": ["inspectionNeeded"]
        }
      }
    }
  }
}
```

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

Bundle freshness MUST NOT outlast the Descriptor or any included document.
If the server cannot establish a combined policy, it MUST send
`Cache-Control: no-store`. An `ETag` for a bundle validates the whole
representation, not just its Descriptor metadata.

Descriptive entity IDs, TD security declarations and references to actions are
not authenticated principals, execution grants or current readiness. Device
admission and operation outcomes remain governed by their own protocols and
trusted authorities.

[Link Relations]: https://www.iana.org/assignments/link-relations/
