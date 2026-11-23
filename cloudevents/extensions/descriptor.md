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

A static HTTP server or an [xRegistry](https://xregistry.io) server can serve
the document.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is
used. For example, an attribute being marked as "REQUIRED" does not mean
it needs to be in all CloudEvents, rather it needs to be included only when
this extension is being used.

In pseudo-JSON examples, `?` marks an OPTIONAL member and `...` stands for
additional members. Whitespace is for readability.

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

## Descriptor document

A Descriptor document MUST be a JSON object with the following structure.

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

Extensions MAY add members to the document and its entries.

### `descriptorid`

REQUIRED. A non-empty string that identifies the Descriptor within its
publication scope.

### `versionid`

REQUIRED. A non-empty string that identifies the version of the Descriptor.
Publishers MUST keep the entries, their inline fields, and their referenced
representations stable for the intended use and replay of a published version.
Publish a new version when those inputs change. The identifiers alone do not
establish that a URL selects a fixed version.

### `entityid`

OPTIONAL. An absolute, fragment-free URI that identifies the primary described
entity. It does not trigger retrieval.

### `bundleurl`

OPTIONAL. An absolute, fragment-free HTTP(S) URL for retrieving a
[bundle](#bundled-document) of this Descriptor document. A Descriptor MAY
include `bundleurl` only when the server offers a bundle for it. In a bundle,
`bundleurl`, when present, MUST point to the bundle itself.

### `entries`

REQUIRED. A map with zero or more members. Each key is an entry name and
its value is an [entry](#entry).

Entry names are one to 63 lowercase ASCII letters, digits, colons, hyphens,
underscores, or dots, starting with a letter or digit.

#### Entry

An entry is a JSON object with the following members. Its class can define
additional members.

##### `class`

REQUIRED. Identifies the kind of information the entry supplies and
determines whether the entry links to a document or carries its information
inline. The same class MAY appear under different entry names.

##### `url`

REQUIRED for entries that link to a document. The value MUST be an absolute,
fragment-free HTTP(S) URL. Entries that supply only inline fields MUST omit
`url`.

### Bundled document

A Consumer MAY retrieve an advertised bundle by sending HTTP `GET` to the
supplied `bundleurl`. A successful response at that URL MUST use
`Content-Type: application/json`. The bundle MUST have the same `descriptorid`
and `versionid` as the Descriptor that advertised it.

A bundle is an expanded view of a Descriptor. Each entry with a `url`
MUST include a `document` member containing the linked document. This
lets the Consumer retrieve the directly linked documents in one response.
Inline-only entries and ordinary Descriptor metadata responses MUST omit
`document`. The server MUST NOT automatically follow links from profile
fields or from the linked documents.

The server MUST verify authorization and obtain the complete document for
every linked entry before returning a successful bundle. If it cannot do so,
it MUST report failure rather than return a partial bundle. If a request to
`bundleurl` fails, the Consumer MAY use the original Descriptor to retrieve
only the entries it needs. This does not select another Descriptor.

#### `document`

The `document` object contains `contenttype` and exactly one of `content`
and `contentbase64`. It has the following structure:

```text
{
  "contenttype": "<media type>",
  "content": <JSON value>, ?
  "contentbase64": "<base64-encoded bytes>", ?
  "baseurl": "<final retrieval URL>" ?
}
```

##### `contenttype`

REQUIRED. The media type of the linked document. Use
`application/octet-stream` if the retrieved document has no media type.

##### `content`

The linked document as a JSON value.

##### `contentbase64`

The linked document as base64-encoded bytes. Non-JSON representations use
this member. The server MUST decode HTTP content codings before embedding
bytes.

##### `baseurl`

REQUIRED when an allowed redirect changed the retrieval URL. The value MUST
give the final URL. The entry's `url` stays unchanged. Consumers resolve
format-specific relative links against `baseurl` when present, or the
entry's `url` otherwise.

### JSON Schema

The [Descriptor JSON Schema](descriptor.schema.json) is available for
validation. Under `$defs`, use `metadata` for a Descriptor without embedded
documents and `bundle` for a bundle. Schema validation does not replace URL
or entry-specific checks.

## Descriptor profiles

A class definition specifies the representation that HTTP `GET` on an
entry's `url` returns, or the fields the entry supplies inline. A profile
can also specify how to select entries for a particular use or require
a URL that identifies a fixed Descriptor version.

Standard classes use short lowercase alphanumeric tokens starting with a
letter. Other specifications can define their own classes using reverse DNS
names under the defining party's control. A `class` string is at most 63
characters.

The following `class` values are well-known class names:

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

If an explicit `describedby` URL is invalid or fails to return a valid
Descriptor response with the REQUIRED inputs, the Consumer MUST report the
failure and MUST NOT substitute another description for it.

A profile MAY permit processing that does not depend on the Descriptor,
but the Consumer MUST NOT report successful Descriptor-based interpretation or
validation without REQUIRED inputs. Unless the profile dictates the outcome,
local policy determines whether to defer, reject, retain or forward an
uninterpreted event. These outcomes add no event attributes or HTTP error codes.

### Schema

A `schema` entry's `url` MUST identify a schema document for the event
payload. Use the linked document or the entry's bundled `document`.
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

[Endpoint Group]: https://github.com/xregistry/spec/blob/main/endpoint/spec.md
