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
the supplied URL with HTTP `GET`. To retrieve an advertised bundle, use
HTTP `GET` on `bundleurl` as supplied. The bundle MUST have the same
`descriptorid` and `versionid` as the Descriptor that advertised it.
Negotiating a bundle at the original URL is defined in the
[xRegistry Descriptor working draft][Descriptor Registry].

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

The following `class` strings are assigned:

- `endpoint`: [Endpoint Descriptor profile](#endpoint)
- `opcuawriter`: [OPC UA Descriptor profile](opcua.md#descriptor-entry)
- `schema`: [Schema Descriptor profile](#schema)
- `thingdescription`: [Web of Things profile](wot.md)
- `thingmodel`: [Web of Things profile](wot.md)
- `usdasset`: [OpenUSD profile](openusd.md#asset-selection)

The same class MAY appear under different entry names. Profiles define how
to select entries, including where a name comes from when needed. When a
profile needs one entry and its rules leave several candidates, the Consumer
MUST report ambiguity, not choose by map order.

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
media type, use `application/octet-stream`. The server MUST decode HTTP
content codings before embedding bytes. If an allowed redirect changed the
retrieval URL, `document.baseurl` MUST give the final URL. The entry's `url`
stays unchanged. Consumers resolve any format-specific relative links against
`baseurl` if present, or the entry `url` otherwise.

The server MUST verify authorization and obtain the complete document for
every linked entry before returning a successful bundle. If it cannot do so,
it MUST report failure rather than return a partial bundle. If a request to
`bundleurl` fails, the Consumer MAY use the original Descriptor to retrieve
only the entries it needs. This does not select another Descriptor.

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

## Descriptor profiles

A publication profile determines whether an operation uses either of the
following classes and whether it needs one entry or several.

### Schema

A `schema` entry MUST link to a payload schema document at `url`, not its
Registry metadata. Use the linked document or the entry's bundled
`document`. A schema registry is not REQUIRED.
The [Descriptor JSON Schema](descriptor.schema.json) defines `schemaEntry`
in `$defs` for validating this entry.

To select one schema, use the `schema` entry named by the publication
profile. If the profile supplies no name, one `schema` entry selects that
schema, no entries means absence, and multiple entries are ambiguous.
A specified name that is missing or has the wrong class is invalid, not
absence. An invalid or ambiguous selection, unsupported format, or
unavailable selected document MUST NOT cause fallback to another schema.
The event binding defines precedence between this entry and `dataschema`.

### Endpoint

An `endpoint` entry MUST link to a representation of endpoint metadata
at `url`. For an xRegistry [Endpoint Group][Endpoint Group], use the
Group's metadata URL. The entry does not authorize invoking the endpoint.
The [Descriptor JSON Schema](descriptor.schema.json) defines `endpointEntry`
in `$defs` for validating this entry.

To select one endpoint, use the `endpoint` entry named by the publication
profile or the unique entry of that class if no name is supplied.
An absent entry, wrong class or ambiguous selection MUST be reported
when the operation needs that endpoint. The Consumer MUST NOT replace a
failed selection with an unrelated endpoint.

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

The `pump7` entry identifies the pump's Thing Description. The `inspection`
entry links to metadata for the inspection service endpoint.

```json
{
  "descriptorid": "pump7-maintenance",
  "versionid": "1",
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
    },
    "inspection": {
      "class": "endpoint",
      "url": "https://registry.example/endpoints/inspection"
    }
  }
}
```

### Bundled endpoint

The client retrieves the Descriptor metadata:

```http
GET /descriptors/inspection-endpoint/versions/1 HTTP/1.1
Host: static.example
```

The response advertises a bundle:

```json
{
  "descriptorid": "inspection-endpoint",
  "versionid": "1",
  "bundleurl": "https://static.example/bundles/inspection-endpoint/1",
  "entries": {
    "inspection": {
      "class": "endpoint",
      "url": "https://registry.example/endpoints/inspection"
    }
  }
}
```

The client retrieves the bundle directly from `bundleurl`:

```http
GET /bundles/inspection-endpoint/1 HTTP/1.1
Host: static.example
```

The bundle includes the endpoint metadata in the `inspection` entry:

```json
{
  "descriptorid": "inspection-endpoint",
  "versionid": "1",
  "bundleurl": "https://static.example/bundles/inspection-endpoint/1",
  "entries": {
    "inspection": {
      "class": "endpoint",
      "url": "https://registry.example/endpoints/inspection",
      "document": {
        "contenttype": "application/json",
        "content": {
          "endpointid": "inspection",
          "self": "https://registry.example/endpoints/inspection",
          "xid": "/endpoints/inspection",
          "epoch": 1,
          "createdat": "2026-10-29T12:00:00Z",
          "modifiedat": "2026-10-29T12:00:00Z",
          "usage": ["producer"],
          "protocol": "HTTP",
          "protocoloptions": {
            "endpoints": [
              { "uri": "https://maintenance.example/inspection-requests" }
            ]
          }
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
[Descriptor Registry]: https://github.com/xregistry/spec/pull/796
[Endpoint Group]: https://github.com/xregistry/spec/blob/main/endpoint/spec.md
