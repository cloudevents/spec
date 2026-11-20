# Descriptor Reference

Events can stay small when they link to additional information instead of
carrying it in every message. The Descriptor Reference extension adds
`describedby`, a single URL for information beyond what the event carries.
An HTTP `GET` at that URL returns a JSON document called a Descriptor.

For example, a maintenance event can set `describedby` to
`https://maintenance.example/pump7/versions/1`. The returned Descriptor links
to the inspection service's endpoint metadata:

```json
{
  "descriptorid": "pump7",
  "versionid": "1",
  "entries": {
    "inspection": {
      "class": "endpoint",
      "url": "https://maintenance.example/endpoints/inspection"
    }
  }
}
```

This specification defines how to retrieve the document, not how to host it.
A static HTTP server or an [xRegistry](https://xregistry.io) server can serve
the same document.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is
used. For example, an attribute being marked as "REQUIRED" does not mean
it needs to be in all CloudEvents, rather it needs to be included only when
this extension is being used.

## Attributes

### describedby

- Type: `URI`
- Description: The URL of the Descriptor for this event.
- Constraints:
  - REQUIRED.
  - MUST be a non-empty absolute HTTP(S) URL without a fragment.
  - The URL MUST support retrieval of the Descriptor by HTTP `GET`.
    A successful response serving the Descriptor metadata MUST use
    `Content-Type: application/json`.

Use the supplied URL, including its query if present. Other extensions can
reuse the Descriptor document format and define how to locate a Descriptor
without using `describedby`.

## Descriptor document

A Descriptor document MUST be a JSON object with the following structure.
A question mark identifies an OPTIONAL member. The structure shows one named
entry; the `entries` object can hold any number of entries.

```text
{
  "descriptorid": "<descriptor identifier>",
  "versionid": "<version identifier>",
  "entityid": "<entity URI>", ?
  "bundleurl": "<bundle URL>", ?
  "entries": {
    "<entry name>": {
      "class": "<entry class>",
      "url": "<linked document URL>", ?
      ...
    }
  },
  ...
}
```

The ellipses stand for additional fields. This specification does not define
their meaning or require registry-specific fields. The entry's class determines
whether it needs `url`.

### `descriptorid`

REQUIRED. A non-empty string that identifies the Descriptor within its
publication scope.

### `versionid`

REQUIRED. A non-empty string that identifies the version within that Descriptor.
Publishers MUST keep the entries, their inline fields, and their referenced
representations stable for the intended use and replay of a published version.
Publish a new version when those inputs change. The identifiers alone do not
establish that a URL selects a fixed version.

### `entityid`

OPTIONAL. An absolute, fragment-free URI that identifies the primary described
entity. It does not trigger retrieval.

### `bundleurl`

OPTIONAL. An absolute, fragment-free HTTP(S) URL for retrieving a
[bundle](#bundled-document) of this version. Omit it when the server does not
support a bundle for this Descriptor. In a bundle, this URL points to the bundle
itself.

### `entries`

REQUIRED. An object whose members are named entries. An empty object is valid.

Entry names are one to 63 lowercase ASCII letters, digits, colons, hyphens,
underscores or dots, starting with a letter or digit. Each entry has a
REQUIRED `class` that identifies the kind of information the entry supplies.
An entry with a linked document MUST have an absolute, fragment-free HTTP(S)
`url`. An entry that supplies only inline fields MUST omit `url`. A null `url`
is invalid. The same class MAY appear under different entry names.

### Bundled document

A Consumer can retrieve an advertised bundle by sending HTTP `GET` to the
supplied `bundleurl`. A successful response at that URL MUST use
`Content-Type: application/json`. The bundle MUST have the same `descriptorid`
and `versionid` as the Descriptor that advertised it. The
[xRegistry Descriptor working draft][Descriptor Registry] defines how to
negotiate a bundle at the original Descriptor URL.

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

### JSON Schema

The [Descriptor JSON Schema](descriptor.schema.json) is available for
validation. Under `$defs`, use `metadata` for a Descriptor without embedded
documents and `bundle` for a bundle. Schema validation does not replace URL
or entry-specific checks.

## Descriptor profiles

A Descriptor profile is an agreement about how Producers and Consumers use
the information in a Descriptor. A specification or configuration can define
which entry classes to use, what their linked documents and inline fields
mean, and how to select entries when several have the same class. A profile
can also define how event attributes affect selection or require a URL that
always identifies the same Descriptor version.

Standard classes use short lowercase alphanumeric tokens starting with a
letter. Other specifications can define their own classes using reverse DNS
names under the defining party's control. A `class` string is at most 63
characters. A class definition specifies whether entries link to a document
and which additional fields they carry.

The following `class` strings are assigned:

- `endpoint`: [Endpoint Descriptor profile](#endpoint)
- `opcuawriter`: [OPC UA Descriptor profile](opcua.md#descriptor-entry)
- `schema`: [Schema Descriptor profile](#schema)
- `thingdescription`: [Web of Things profile](wot.md)
- `thingmodel`: [Web of Things profile](wot.md)
- `usdasset`: [OpenUSD profile](openusd.md#asset-selection)

When a profile needs one entry and its rules leave several candidates, the
Consumer MUST report ambiguity rather than select by map order.

### Failure outcomes

Descriptor-based interpretation requires a successful response with the
specified media type and a valid document that supplies the inputs the
profile needs. The following table distinguishes unavailable or invalid
inputs from a failed payload validation.

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

```http
HTTP/1.1 200 OK
Content-Type: application/json
Connection: close
```

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

The response includes the endpoint metadata in the `inspection` entry:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Connection: close
```

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

Read access to a Descriptor does not grant access to its targets.
A bundle does not bypass trust checks.
Versions do not authenticate content or prove unchanged bytes.

Descriptive entity IDs, TD security declarations and references to actions are
not authenticated principals, execution grants or current readiness. Device
admission and operation outcomes remain governed by their own protocols and
trusted authorities.

### Caching

Consumers can reuse responses under HTTP caching rules. When choosing a cached
response, account for the requested URL, the representation, and the
authorization context. A cache MUST NOT share a representation across
authorization contexts unless the applicable access policy permits it.

Bundle freshness MUST NOT outlast the Descriptor or any included document.
If the server cannot establish a combined policy, it MUST send
`Cache-Control: no-store`. An `ETag` for a bundle validates the whole
representation, not just its Descriptor metadata.

[Descriptor Registry]: https://github.com/marcschier/xregistry-drafts/blob/d6e659fa15da069fe10eae53132ffeea36953f8c/workingdrafts/models/descriptor/spec.md#55-bundled-representations
[Endpoint Group]: https://github.com/xregistry/spec/blob/main/endpoint/spec.md
