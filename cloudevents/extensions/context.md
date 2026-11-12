# Event Context

The `contexturl` extension attribute identifies shared information that a
Consumer needs to interpret an event. Instead of repeating a Message definition
URL, schema URL, and emitter description URL in every event, a Producer names
one Context that references those representations by Role.

This proposal aligns with the [xRegistry Event Context working draft][Context
Registry] in [xregistry/spec#796][Context PR]. The attribute name and the
resolved-view media type remain provisional. A Context is a metadata-only
xRegistry Resource, not a document attached to that Resource. This extension
does not require a Producer to host or query a Registry.

A Publisher creates Contexts and their referenced representations. A Producer
emits events, and a Consumer processes them.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

The scope of these key words is limited to events using this extension.

## Attributes

### contexturl

- Type: `URI`
- Description: The absolute URL of the Context that applies to this event.
- Constraints:
  - OPTIONAL.
  - If present, MUST identify a Context Resource or Context Version and MUST
    NOT contain a fragment.
  - SHOULD identify a Context Version.
  - Consumers MUST use the value unchanged as the request URL and as the URL
    component of the cache key. Cache selection MUST also account for the
    selected representation and authorization context.
  - Consumers MUST NOT derive other URLs from the value. In particular, they
    MUST NOT append `$details`, a view path, or a query parameter, or remove
    `/versions/<id>`.
  - When absent, this extension supplies no Context for the event.

In the JSON event format, `contexturl` is a top-level string member. In HTTP
binary content mode, it is the `ce-contexturl` header, encoded and decoded
according to the [HTTP binding](../bindings/http-protocol-binding.md).
Other bindings use their normal extension-attribute mapping.

## Context Representation

An ordinary `GET` of `contexturl` with `Accept: application/json` returns
Context metadata directly. The xRegistry Context model sets `hasdocument` to
`false`; no `$details` request or separate Context document is needed.

The REQUIRED `references` map contains at least one entry. Each key is a Role,
and each value is an object with a REQUIRED `url` member. That member is an
absolute URL without a fragment. Consumers MUST use each referenced URL
unchanged when retrieving its representation.

The working draft defines these Roles.

| Role | Referenced representation |
| --- | --- |
| `message` | Message definition metadata describing the event. |
| `schema` | Schema document for the event's `data`. |
| `emitter` | Description of the emitting entity, such as a WoT Thing Description Version document. |
| `target` | Model that the event concerns, such as an OpenUSD asset. |

Roles follow the working draft's map-key rules. Unprefixed names are reserved
for that draft. Other Roles MUST use an identifying prefix followed by `:`,
such as `acme:policy`. Consumers MUST ignore Roles they do not use and Reference
attributes they do not understand.

Contexts and References permit extension attributes. A profile can use those
attributes for metadata shared by a message stream. Such metadata is not
automatically a CloudEvents attribute: the profile MUST define its meaning and
how it relates to attributes carried in the event.

## Processing and Versioning

When including `contexturl`, a Producer MUST name a Context whose references
apply to the event. A Publisher MUST make referenced representations available
before configuring Producers with the Context URL. Producers SHOULD reuse a
configured Context Version URL for events with the same shared information.
A Context with a `message` Reference applies to one event type; Producers
that emit several types use a separate Context for each type in that case.

A Publisher MUST NOT change a Context Version's `references` after any
Producer is configured with its URL. Changing references requires a new
Version and reconfigured Producers. Profiles that store shared metadata in
Context extension attributes MUST define equivalent stability rules for those
values.

A Context Resource URL serves the current default Version. That default can
change without changing `contexturl`, so Consumers SHOULD bound the lifetime
of cached Resource representations. A Context Version fixes its references,
not the bytes of referenced representations. Publishers SHOULD reference
explicit Target Versions when replay requires reproducible interpretation and
SHOULD retain Contexts and referenced representations for the replay period.

A Consumer retrieves the Context from the unchanged URL or uses a valid cache
entry for that URL, representation, and authorization context. It MUST check
the response status, media type, and Context representation against the
working draft. A failed response, unsupported representation, or missing or
empty `references` map makes the Context unavailable. For a valid Context, the
Consumer retrieves the representations for the Roles it needs, subject to its
access and content-trust policies. A missing Role that the Consumer needs
makes the Context incomplete.

When retrieval fails or the Context is invalid or incomplete, the Consumer
MUST NOT derive replacement URLs from `contexturl`. It SHOULD record the
condition. Local policy determines whether to defer, reject, or process the
event without that information, unless another profile requires a particular
outcome.

### Resolved Context view

A supporting server can return the Context and all directly referenced
representations in one response. A Consumer requests that view at the same
unchanged URL with:

```http
Accept: application/vnd.xregistry.context-view+json, application/json;q=0.5
```

The Consumer MUST inspect `Content-Type` rather than assume that the server
supports the view. Ordinary `application/json` returns Context metadata;
`application/vnd.xregistry.context-view+json` returns `context` and `documents`
as defined by the working draft. The view includes every direct Reference or
returns an error. It does not recursively retrieve their dependencies or
establish a snapshot across Registries.

## Relationship to Other Attributes

Core attributes retain their meaning. In particular, `contexturl` does not
replace REQUIRED `id`, `source`, or `type`, and does not locate the event's
`data` as the [Dataref extension](dataref.md) does.

A Consumer selects the first applicable schema source in this order:

1. The event's `dataschema`.
2. The Context's `schema` Reference.
3. The schema declared by the Context's `message` representation.

Producers SHOULD omit `dataschema` when the Context supplies the schema.
Publishers and Producers SHOULD supply only one schema source, or identify
the same schema when several are supplied. Consumers apply the precedence
without comparing the sources.

An `emitter` Reference does not authenticate the event or redefine `source`.
The [WoT profile](wot.md) defines how it selects a Thing Description (TD) when
this extension is used. The
[OPC UA extension](opcua.md#shared-stream-metadata-in-a-context)
defines which stream metadata can be supplied by a Context. Neither rule
applies to generic events merely because they contain `contexturl`.

## Example

This event references shared emitter and payload-schema information.

```json
{
  "specversion": "1.0",
  "id": "sample-4711",
  "source": "mqtt://site/line/cell/device/sensor",
  "type": "com.example.models.tm.pump.properties.processData.v1",
  "subject": "#/properties/processData",
  "datacontenttype": "application/json",
  "contexturl": "https://registry.example/contextgroups/line1/contexts/pump-process-data/versions/1",
  "data": {
    "Speed": 1500,
    "Pressure": 4.5
  }
}
```

The Context Version has the following metadata. Other Core metadata is omitted
from this excerpt.

```json
{
  "contextid": "pump-process-data",
  "versionid": "1",
  "references": {
    "emitter": {
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
    },
    "schema": {
      "url": "https://example.com/schemas/pump-process-data/versions/3"
    }
  }
}
```

## Security Considerations

Consumers and servers that assemble resolved views MUST apply authorization,
URL, redirect, and content-trust policies before retrieving or using a Context
or any referenced representation. An event-provided URL MUST NOT authorize
arbitrary network access or credential forwarding. Implementations SHOULD
bound response sizes, retrieval times, and dependency processing.

Caches MUST NOT share representations across authorization contexts unless
the applicable access policy permits it. A resolved view does not bypass the
Consumer's trust checks. Context Versions and Target Versions do not by
themselves authenticate content or prove that its bytes are unchanged.

[Context PR]: https://github.com/xregistry/spec/pull/796
[Context Registry]: https://github.com/xregistry/spec/blob/e46561facacb672ed3d7603be1574a75b1a11789/workingdrafts/models/context/spec.md
