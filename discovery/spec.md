# CloudSubscriptions: Discovery - Version 0.1-wip

## Abstract

CloudSubscriptions Discovery API is a vendor-neutral API specification for
determining what events are available from a particular service, as well as how
to subscribe to those events.

## Table of Contents

- [Overview](#overview)
- [Notations and Terminology](#notations-and-terminology)
- [Resource Model](#resource-model)
- [API Specification](#api-specification)
- [Privacy & Security](#privacy-and-security)

## Overview

In order for consumers to receive events from services, they need to first
subscribe, or ask for, events from those services. To do so, there is often a
process necessary that involves steps such as discovering which service is of
interest, what events it generates and how to create the subscription for those
events.

This specification defines a set of APIs to allow for consumers to perform these
queries against a "Discovery Endpoint". A Discovery Endpoint acts as a catalog
of [Services](#service) (event producers), that consumers can query to find the
ones of interest. Once found, additional metadata is provided in order to
consume and subscribe to events. The goal of this API is to be such that tooling
can be built where all possible services and event types aren't known in
advance.

The deployment relationship of a Discovery Endpoint to the Services and Event
Producers that it advertises is out of scope of this specification. For example,
a Discovery Endpoint could choose to be implemented as part of a Service, or
Event Producer, or it could be acting as an independent aggregator of this
metadata. This implementation detail will be transparent to consumers.

The main use-case to consider from the viewpoint of the event consumer is what
services are available, and what event types do they generate?

The CloudEvent `source` attribute is a potential cause of high fan-out. For
example, consider a blob storage system where each directory constitutes a
distinct `source` attribute value. For this reason, the exact CloudEvents
`source` attribute value that might appear in a CloudEvent will not appear in
the Discovery API query result. Instead, a higher level classifier (`service`)
will be used to represent the abstract notion of the generic event producer of
those events - in the example case, the blob storage service itself.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

### Terminology

Note: some of the terms defined below are taken from the [CloudEvents](../cloudevents/spec.md)
specification, and are marked with a reference to the original definition. Any
difference between the definitions is accidental and the CloudEvents version
takes precedence.

This specification defines the following terms:

#### Discovery Endpoint

A compliant implementation of this specification that advertises the set of
Services, Event Types and other metadata to aid in the creation of an Event
Subscription.

#### Service

A "service" represents the entity which manages one or more event
[sources](#source-ce) and is associated with [producers](#producer-ce) that are
responsible for the generation of events.

For example, an Object Store service might have a set of event sources where
each event source maps to a bucket.

#### Source [[CE](../cloudevents/spec.md#source)]

The "source" is the context in which the occurrence happened. In a distributed
system it might consist of multiple Producers. If a source is not aware of
CloudEvents, an external producer creates the CloudEvent on behalf of the
source.

#### Producer [[CE](../cloudevents/spec.md#producer)]

The "producer" is a specific instance, process or device that creates the data
structure describing the CloudEvent.

#### Intermediary [[CE](../cloudevents/spec.md#intermediary)]

An "intermediary" receives a message containing an event for the purpose of
forwarding it to the next receiver, which might be another intermediary or a
[Consumer](#consumer-ce). A typical task for an intermediary is to route the
event to receivers based on the information in the event
[Context](../cloudevents/spec.md#context).

#### Consumer [[CE](../cloudevents/spec.md#consumer)]

A "consumer" receives the event and acts upon it. It uses the context and data
to execute some logic, which might lead to the occurrence of new events.

#### Subscription

The request for events from a Service.

## Resource Model

This section defines the resource model of a Discovery Endpoint.

### Services

At the core of the data model is the concept of a [Service](#service). The API
then exposes multiple ways to query over a list of Services. To help explain the
Service resource, the following non-normative pseudo json shows its basic
structure:

(`*` means zero or more, `+` means one or more, `?` means optional)

Service:

```
{
  "id": "[a unique URI segment within the authority]",
  "authority": "[URI reference to the authority providing the service]", ?
  "epoch": "[discovery entry epoch value]",
  "name": "[unique name for this services]",
  "url": "[unique URL to this service]",
  "description": "[human string]", ?
  "docsurl": "[URL reference for human documentation]", ?
  "specversions": [ "[ce-specversion value]" + ],
  "subscriptionurl": "[URL to which the Subscribe request will be sent]",
  "subscriptionconfig": { ?
    "[key]": "[type]", *
  },
  "subscriptiondialects": [ "[dialect]" ], ?
  "authscope": "[string]", ?
  "protocols": [ "[string]" + ],
  "events": [ ?
    { *
      "type": "[ce-type value]",
      "description": "[human string]", ?
      "datacontenttype": "[ce-datacontenttype value]", ?
      "dataschema": "[ce-dataschema URI]", ?
      "dataschematype": "[string per RFC 2046]", ?
      "dataschemacontent": "[schema]", ?
      "sourcetemplate": "[URI template per RFC 6570, level 1]", ?
      "extensions": [ ?
        { *
          "name": "[CE context attribute name]",
          "type": "[CE type string]",
          "specurl": "[URL to specification defining the extension]" ?
        }
      ]
    }
  ]
}
```

An example:

```json
{
  "id": "cbdd62e8-c095-11ea-b3de-0242ac130004",
  "authority": "https://example.com",
  "epoch": 1,
  "name": "widgets",
  "url": "https://example.com/services/widgetService",
  "specversions": ["1.0"],
  "subscriptionurl": "https://events.example.com",
  "subscriptiondialects": [ "basic" ],
  "protocols": ["HTTP"],
  "events": [
    {
      "type": "com.example.widget.create"
    },
    {
      "type": "com.example.widget.delete"
    }
  ]
}
```

Note: the above is just a sample and implementations are free to use any
internal model they wish to store the data as long as they are compliant with
the wire format/API defined by this specification.

#### Service Attributes

The following sections define the attributes that appear in a Service entity.
##### id

- Type: `String`
- Description: A unique identifier for this Service. This value MUST be unique
  within the authority. While other metadata about this Service MAY change,
  this value MUST NOT so that clients can use this attribute to know whether a Service 
  returned by a query is the same Service returned by a previous query.

  Whether a change to a Service would result in changing of the Service's
  metadata (except `id`) and thus be just an update of an existing Service, or
  whether the change would result in a brand new Service (with a new `id`) is
  not defined by this specification.

  For example, if a Service's implementation is upgraded to a new version then
  whether this would result in a new Service (and `id`) or is an update to the
  existing Service's metadata, is an implementation choice. Likewise, this
  specification makes no statement, or guarantees, as to the forwards or
  backwards compatibility of a Service as it changes over time.

  See the Primer for more information.

- Constraints:
  - REQUIRED in responses from the Discovery Endpoint.
  - MUST be a non-empty string
  - MUST conform with [RFC3986/3.3](https://datatracker.ietf.org/doc/html/rfc3986#section-3.3) `segment-nz-nc` syntax.
- Examples:
  - `bf5ff5cc-d059-4c79-a89a-2513e45a1340`
  - `com.example.myservice.v1`

#### authority (service authority)

- Type: `URI`
- Description: Identifies the authority for this service. Similar to schemas authority.
  When `authority` and `id` are combined they MUST be globally unique.
- Constraints:
  - OPTIONAL. If the attribute is absent or empty, its implied default value is the base
    URI of the API endpoint.
  - MUST be a valid URI.
  - For services imported from other discovery endpoints in replication scenarios, the
    attribute is REQUIRED to be not empty. If the value is empty or absent
    during import, it MUST be explicitly set to its implied default value.
- Examples:
  - `urn:com-example`
  - `https://example.com`

##### epoch

- Type: `Unsigned 32-bit Integer`
- Description: The Discovery Endpoint's `epoch` value for this Service Entry.
  This specification does not mandate any particular semantic meaning to
  the value used. For example, implementations are free to use a value that
  represents a timestamp or could choose to simply use a monotonically
  increasing number. The only requirement is that the value MUST always
  increase each time the Service Entry is updated. This allows for a quick
  integer comparision to determine which version of this Service Entry is the
  latest - meaning, the one with the larger integer value.

- Constraints:
  - REQUIRED in responses from the Discovery Endpoint.
  - MUST be an unsigned 32-bit integer
- Examples:
  - `42`
  - `915148800`

##### name

- Type: `String`
- Description: A unique human readable identifier for this Service. This value
  MUST be unique (case insensitive) within the scope of this Discovery Endpoint.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
- Examples:
  - `my storage service`
  - `cool git offering`

##### url

- Type: `URL`
- Description: An absolute URL that references this Service within this
  Discovery Endpoint. This value MUST be usable in subsequent requests, by
  authorized clients, to retrieve this Service
  entity.
- Constraints:
  - REQUIRED
  - MUST be a non-empty URL
  - MUST end with `fsegments` (per RFC1738) of: `/services/{id}` where `id` is
    the Service's `id` attribute.
- Examples:
  - `http://example.com/services/bf5ff5cc-d059-4c79-a89a-2513e45a1340`
  - `http://discovery.github.com/services/892abefc-0293-9273-bead-92830efaefa0`

##### description (Service)

- Type: `String`
- Description: Human readable description.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string

##### docsurl

- Type: `URL`
- Description: Absolute URL that provides a link to additional documentation
  about the service. This is intended for a developer to use in order to learn
  more about this service's events produced.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty absolute URI
- Examples:
  - `http://cloud.example.com/docs/blobstorage`

##### specversions

- Type: Array of `String` values
- Description: CloudEvents
  [`specversions`](../cloudevents/spec.md#specversion)
  that can be used for events published for this service.
- Constraints:
  - REQUIRED
  - MUST be a non-empty array of non-empty strings

##### subscriptionurl

- Type: `URL`
- Description: An absolute URL indicating where CloudSubscriptions `subscribe`
  API calls MUST be sent to.
- Constraints:
  - REQUIRED

##### subscriptionconfig

- Type: `Map` of `String` to `String`
- Description: A map indicating supported options for the `config` parameter for
  the CloudSubscriptions subscribe() API call. Keys are the name of keys in the
  allowed config map, the values indicate the type of that parameter, conforming
  to the CloudEvents
  [type system](../cloudevents/spec.md#type-system).
  TODO: Needs resolution with CloudSubscriptions API
- Constraints:
  - OPTIONAL
- Examples:
  - ??

##### subscriptiondialects

- Type: List of `String` values
- Description: An array of filter dialects that MAY be used in the
  Cloud Subscriptions subscribe() API call.
- Constraints:
  - OPTIONAL
- Examples:
  - `basic`

##### authscope

- Type: `String`
- Description: Authorization scope needed for creating subscriptions. The actual
  meaning of this field is determined on a per-service basis.
- Constraints:
  - OPTIONAL
- Example:
  - `storage.read`

##### protocols

- Type: `List` of `String`
- Description: This field describes the different values that might be passed in
  the `protocol` field of the CloudSubscriptions API. The protocols with
  existing CloudEvents bindings are identified as AMQP, MQTT3, MQTT5, HTTP,
  KAFKA, and NATS. An implementation MAY add support for further protocols. All
  services MUST support at least one delivery protocol, and MAY support
  additional protocols.
- Constraints:
  - REQUIRED
  - MUST be non-empty.
- Examples:
  - `[ "HTTP" ]`
  - `[ "HTTP", "AMQP", "KAFKA" ]`

##### events

- Type: List of `EventType` objects
- Description: This field contains the EventType definitions available from this service.
- Constraints:
  - OPTIONAL
- Examples:
  - `[ { "type": "com.example.object.delete.v2" } ]`

#### EventType Attributes

The following sections define the attributes that appear in EventType definitions of a Service object.

##### type

- Type: `String`
- Description: CloudEvents
  [`type`](../cloudevents/spec.md#type)
  attribute.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string, following the constraints as defined in the
    CloudEvents spec.
- Examples:
  - `com.github.pull.create`
  - `com.example.object.delete.v2`

###### description (type)

- Type: `String`
- Description: Human readable description.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string

###### datacontenttype

- Type: `String`
- Description: CloudEvents
  [`datacontenttype`](../cloudevents/spec.md#datacontenttype)
  attribute. Indicating how the `data` attribute of subscribed events will be
  encoded.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)

###### dataschema

- Type: `URI`
- Description: CloudEvents
  [`dataschema`](../cloudevents/spec.md#dataschema)
  attribute. This identifies the canonical storage location of the schema of the
  `data` attribute of subscribed events.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI

###### dataschematype

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: If using `dataschemacontent` for inline schema storage, the
  `dataschematype` indicates the type of schema represented there.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Examples:
  - `application/json`

###### dataschemacontent

- Type: `String`
- Description: An inline representation of the schema of the `data` attribute
  encoding mechanism. This is an alternative to using the `dataschema`
  attribute.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string containing a schema compatible with
    the `datacontenttype`.
  - If `dataschema` is present, this field MUST NOT be present.

###### sourcetemplate

- Type: `URI Template`
- Description: A URI Template according to
  [RFC 6570](https://tools.ietf.org/html/rfc6570) that defines how the source
  attribute will be generated.
- Constraints:
  - OPTIONAL
  - If present, MUST be a Level 1 template compliant to
    [RFC 6570](https://tools.ietf.org/html/rfc6570)
- Examples:
  - "http://blob.store/{bucket}"

###### extensions

- Type: `Array` of structures
- Description: An array or CloudEvents
  [Extension Context Attributes](../cloudevents/spec.md#extension-context-attributes)
  that are used for this event `type`. The structure contains the following
  attributes:
  - `name` - the CloudEvents context attribute name used by this extension. It
    MUST adhere to the CloudEvents context attribute naming rules
  - `type` - the data type of the extension attribute. It MUST adhere to the
    CloudEvents [type system](../cloudevents/spec.md#type-system)
  - `specurl` - an attribute pointing to the specification that defines the
    extension
- Constraints:
  - OPTIONAL
  - if present, the `name` attribute in the structure is REQUIRED
  - if present, the `type` attribute in the structure is REQUIRED
  - if present, the `specurl` attribute in the structure is OPTIONAL
- Examples:
  - `{ "name": "dataref", "type": "URI-reference", "specurl": "https://github.com/cloudevents/spec/blob/main/cloudevents/extensions/dataref.md" }`

#### Service Examples

```json
{
  "id": "3db60532-e839-417e-8644-e255f338776a",
  "epoch": 1,
  "url": "https://storage.example.com/service/storage",
  "name": "storage",
  "description": "Blob storage in the cloud",
  "protocols": ["HTTP"],
  "subscriptionurl": "https://cloud.example.com/docs/storage",
  "events": [
    {
      "type": "com.example.storage.object.create",
      "specversions": ["1.x-wip"],
      "datacontenttype": "application/json",
      "dataschema": "http://schemas.example.com/download/com.example.storage.object.create.json",
      "sourcetemplate": "https://storage.example.com/service/storage/{objectID}"
    }
  ]
}
```

### Endpoint Features

Each Discovery Endpoint will have its own customizations. For example,
the list of filter attributes can vary between implementations. The following
describes the "features" of the endpoint such that clients can determine
which set of capabilities are available. Additional properties MAY be specified,
however, care SHOULD be taken to avoid potential overlap with future
specification defined properties. For example, a company specific prefix
of `bigcompany` might be used.

#### `servicefilterattributes`

This is an array of attributes names that the Discovery Endpoint supports
for the purpose of filtering the query of available Services. For nested
attributes a dot(.) notation MUST be used.

Sample attribute names:
- `name`
- `specversions`
- `events.type`

Note: this property MUST NOT be empty, or missing, since all implementations
MUST support filtering by `name`.

#### `pagination`

This is a boolean value indicating support for the
[Pagination](../pagination/spec.md) specification. If not specified, the
default value is `false`.

#### `updates`

This is a booleam value indicating support for updates to the Services within
the Discovery endpoint. This can be used to determine whether support, in
general, is supported and a value of `true` does not guarantee that all
users have access or that all update operations will succeed. If not specified,
the default value is `false`..

## API Specification

The endpoints defined by this specification are broken into two categories:
- Features APIs - used to obtains the features of the Discovery Endpoint
- Discovery APIs - used to find Services
- Management APIs - used to manage the Services within a Discovery Endpoint

The relative paths specified below are NOT REQUIRED to be at the root of
the `fpath` (per RFC1738). However, they are REQUIRED to match the end of it.
For example, the follow are valid URLs/paths:

```
https://example.com/services
https://example.com/myAggregator/services
```

If a Discovery Endpoint can perform authorization checks to determine
which client can see which Service, and the requesting client is not allowed
access to a particular Service, then the Discovery Endpoint MUST respond
as if that Service does not exist. For example, it would be excluded from
any array of Services returned and it would result in a `404 Not Found`
error for a request to that Service directly.

All APIs MUST support JSON encoding, which means that HTTP requests
including an HTTP `Content-Type` Header of `application/json` and body in that
format MUST be supported. Likewise requests with `Accept` header of
`application/json` MUST be supported.

Unknown query parameters on the APIs MUST be ignored.

### Features APIs

All of the API endpoints specified in this section MUST be supported by
compliant Discovery Endpoint implementations.

#### `GET /features`

This MUST return the set of features supported by the implementation.
The result of this query SHOULD take into account the specific user issuing
the query, if an authentication scheme is being used.

The result MUST be a JSON object of the following form:
```
{
  "servicefilterattributes": [ "name", ... ],
  "pagination": true,
  "update": true
}
```

The following additional constraints apply:
- The feature names are case sensitive.
- The `servicefilterattributes` property MUST be present, and MUST have at
  least the `name` attribute in its list. The filter attribute names are case
  sensitive. See the [`/services` API](#get-services) for more information
  about the format of nested attribute names.
- The `pagination` attribute is OPTIONAL with an implied default value of
  `false`.
- The `update` attribute it OPTIONAL with an implied default value of `false`.

### Discovery APIs

All of the API endpoints specified in this section MUST be supported by
compliant Discovery Endpoint implementations.

#### `GET /services`

This MUST return an array of zero or more Services. The array MUST contain the
latest version of all Services available via this Discovery Enpoint.

The collection of services MAY be filtered by supplying one or more
[service attributes](#service-attributes) under the `filter` query parameter.
The format for the `filter` query parameter MUST be:

```
?filter=ATTRIBUTE[=VALUE]
```

Nested attribute names MUST be specified by using a dot (`.`) as the
nesting operator. For example: `events.type` references the `type`
attribute under the `events` attribute.


The following rules constrain the filter processing:
- The `=VALUE` portion is OPTIONAL and if not present then the implied
  meaning is that the filter MUST only match Services that contain the
  specified attribute with a non-empty-string value.
- a `VALUE` of "" (empty string) is valid and a filter expression of
  `?filter=ATTRIBUTE=` MUST only match Services that contain the specified
  attribute with an empty string value. Note that an attribute with no
  value (or `null` depending on the data store used) MUST be treated the
  same as an attribute with an empty string (`""`) for the purpose of this
  filter feature.
- when `VALUE` is a non-empty string, then the filter expression MUST only
  match Services that contain the specified attribute with `VALUE` in any
  part of its value.
- Matching of attribute names MUST be case sensitive.
- Matching of attribute values MUST be case insensitive.
- If there are mulitple filter expressions, they MUST be specified as separate
  `filter` query parameters. When there are multiple filters, the resulting
  set of Services MUST only include ones that match all of the filters
  specified. When multiple nested attribute names are used, each nested
  attribute MUST be treated independently and the nested attributes do not
  need to be present in the same nested scope. See the sample filters below.
- Requests with unsupported filter attributes, MUST be rejected with a
  `400 Bad Request` response. Endpoints SHOULD return an error message that
  indicates which filter attributes were not supported.

Discovery endpoints MUST support filtering by the following attributes:

- `name`

Other attribute MAY be supported and SHOULD be included in the Features API
output.

Note: an empty result set is not an error and a `200 OK` with a zero sized
array MUST be returned in those cases.

Some sample filter expressions:
| Expression | Results |
| :--- | :--- |
| ?filter=description | All Services that have a non-empty string value for `description` |
| ?filter=description= | All Services that have no value for `description`. Note: either `null` or `""` is a match |
| ?filter=description=test&filter=name=mine | All Services that have a `description` containing the string `test` (in any case), and a `name` containing the string `mine` (in any case) |
| ?filter=description=test,name=mine | All Services that have a `description` with the string `test,name=mine` (in any case) as part of its value |
| ?filter=events.type=abc&filter=events.description=mine | All Services that have an `events.type` containing the string `abc` (in any case) and an `events.description` containing `mine` (in any case) but these two attribute do not need to be part of the same `event` definition |


Any Service previously returned to a client that does not appear in this
result can be assumed to be no longer available in the scope of the query
specified. In the unfiltered query case this means the Service has been
deleted. In the filtered case it is not possible to know if the Service has
been deleted or if the filters no longer apply to that Service, and therefore
it can not be assumed to be deleted.

In the case of `200 OK`, the response format MUST be a JSON array of Services
that adheres to the following:

```
200 OK
Content-Type: application/json

[
  {
    "id": "{id}",
    "epoch": {int},
    "url": "{url}",
    "name": "{name}",
    ... remainder of Service attributes ...
  }
  ...
]
```

Implementations MAY use the [pagination](../pagination/spec.md) specification
if the number of Services returned is large. Clients SHOULD be
prepared to support paginated responses.

Implementations MAY choose to support other filter mechanism, in particular
to support a richer set of queries. Support for those SHOULD be expressed
via the Features API.

#### `GET /services/{id}`

This MUST return the latest version of the Service with the given `{id}` if it
exists.

The following responses are defined by this specification:
- `200 OK` and the Service representation in the HTTP Response Body.
- `404 Not Found` if the Service does not exist.

Other responses are allowed, but not defined by this specification.

In the case of `200 OK`, the response format MUST adhere to the following:

```
200 OK
Content-Type: application/json

{
  "id": "{id}",
  "epoch": {int},
  "url": "{url}",
  "name": "{name}",
  ... remainder of Service attributes ...
}
```

### Management APIs

All of the API endpoints specified in this section MUST be supported by
compliant Discovery Endpoint implementations that support being managed.

#### Asynchronous Processing

For any of the following API endpoints, if the Discovery Endpoint chooses
to process the incoming request asynchronous then the following rules apply:
- A `202 Accepted` MUST be returned to the request. This indicates that the
  request has been accepted but not processed yet.
- The `202 Accepted` response MUST include a `Location` HTTP Header that
  points to a "status endpoint", which can be used to determine the status
  of the original request. The HTTP Response body MAY be empty.
- The `202 Accepted` response MAY include a `Retry-After` HTTP Header
  indicating the time, in seconds, that the sender SHOULD wait before
  querying the status endpoint.

A `GET` MAY be sent to the status endpoint to determine the status of the
original request. The following responses are defined:

- `200 OK` indicates that the original request was successfully processed.
  - Unless otherwise noted for a specific operation, the response MUST also
    include the HTTP Headers and HTTP Response Body that is defined for the
    original operation as if the response were sent synchronously.
- `202 Accepted` indicates that the original request is still being processed.
  The response body MAY be empty.
- `406 Not Acceptable` to indicate that the original request failed to be
  processed correctly. The HTTP response Body SHOULD include additional
  information as to why it failed.

Other responses are allowed, but not defined by this specification, however
they MUST be related to the `GET` itself and not the original request.

How long a Discovery Endpoint supports requests to the status endpoint
is an implementation choice, however, it MUST be available immediately
upon return of the `202 Accepted` from the original request.

#### `POST /services`

This MUST update the collection of Services in the Discovery Endpoint to
contain all Services in the request or fail. The body of the request message
MUST contain an array of zero or more Service entries.

The following rules apply to processing the Services specified in the request:
- any error processing the request MUST result in the entire operation failing
  and no updates to the Discovery Endpoint are to happen.
- the Services MUST be processed in the order in which they appear in the
  request.
- a Service (as identified by its `id`) MUST NOT appear more than once in the
  request.
- any existing Service (as identified by its `id`) MUST be completely
  replaced by the Service definition in the request.
  - if the incoming Service has an `epoch` value then the request MUST fail if
    that values does not equal the current Service's `epoch` value.
  - if the incoming Service does not have an `epoch` value then the Discovery
    Endpoint MUST assign an appropriate value. The value MUST be greater than
	the existing Service's value.
- if the incoming Service contains an `id` but no Service with that `id` exists
  then the request MUST fail.
- if the incoming Service does not contain an `id` then the Discovery Endpoint
  MUST assign an appropriate value. The value MUST be globally unique.
- aside from `id` and `epoch`, unless there is an out of band agreement, all
  mandatory attributes MUST be present in the request, and a Discovery Endpoint
  MUST reject requests that are missing such attributes.

There is no requirement that the incoming Services be processed in the
order in which they appear. However, any constraint/consistency checks
(e.g. `name` uniqueness checking) MUST only be performed after all of the
incoming Services have been processed.

The follow responses are defined by this specification:
- `200 OK` if all the specified Services were processed successfully.
  - The HTTP Response Body MUST include an array of the Services that were
    created, or updated, as a result of processing the request. The order
	of the array MUST match the order of the incoming Service array.
	Each Service in the response SHOULD include the current value for all
	attributes, even if the Discovery Endpoint added or modified some values
	during the time of processing of the request.
- `400 Bad Request` if the first error encountered is a constraint failure
- `409 Conflict` if the first error encountered is that a given `epoch` was not
  equal to the existing `epoch` value.

Other responses are allowed, but not defined by this specification.

The format of the HTTP Request MUST adhere to the following:
```
Content-Type: application/json

[
  {
    "name": "{name}",
    ... remainder of Service attributes ...
  }
  ...
]
```

The format of the `200 OK` HTTP Response MUST adhere to the following:
```
200 OK
Content-Type: application/json

[
  {
    "id": "{id}",
    "epoch": "{epoch}",
	"name": "{name},
    ... remainder of Service attributes ...
  },
  ...
]
```

#### `PUT /services/{id}`

This MUST update the Service referenced by the specified URL.
If the Service identified by the specified URL does not exist then the
request MUST fail. Upon successful processing of the request, the existing
Service MUST be completely replaced by the Service definition.

The body of the request message MUST contain a Service with an `id`
attribute matching the `{id}` in the path.

The `epoch` attribute of the Service MAY be omitted. In such cases the
discovery endpoint MUST assign a value that is greater than the existing
`epoch` value for the Service.

If an `epoch` is given in the request it MUST be equal to the `epoch` of
the existing Service, otherwise the request MUST fail.

Aside from `id` and `epoch`, unless there is an out of band agreement, all
mandatory attributes MUST be present in the request, and a Discovery Endpoint
MUST reject requests that are missing such attributes.

The follow responses are defined by this specification:
- `200 OK` if specified Service was updated.
  - The HTTP Response Body MUST include the Service values resulting from the
    successful processing of the request.
	The response SHOULD include the current value for all
	attributes, even if the Discovery Endpoint added or modified some values
	during the time of processing of the request.
- `400 Bad Request` if the `id` in the path and body are not the same or some
  other constraint failure is found.
- `404 Not Found` if there is no Service with the specified `id`.
- `409 Conflict` if the given `epoch` was not equal to the existing `epoch`
   value of the Service being updated.

Other responses are allowed, but not defined by this specification.

The format of the HTTP Request MUST adhere to the following:
```
Content-Type: application/json

{
  "url": "{url}",
  "epoch": "{id}",
  "name": "{name}",
  ... remainder of Service attributes ...
}
```

The format of the `200 OK` HTTP Response MUST adhere to the following:
```
200 OK
Content-Type: application/json

{
  "id": "{id}",
  "epoch": "{id}",
  ... remainder of Service attributes ...
}
```

#### `DELETE /services/{id}[?epoch={epoch}]`

This MUST delete the Service at the referenced URL.

The request URL MAY include an OPTIONAL `epoch` query parameter, and if
present, the Discovery Endpoint MUST reject the request if the corresponding
Service has a different `epoch` value than the query parameter.

The follow responses are defined by this specification:
- `200 OK` if the Service was deleted or does not exist.
  - The HTTP Response Body MUST include a Service definition with at least
    its `id` attribute. It SHOULD include the remaining Service attributes
	as they existed at the time of processing the request if possible.
	Note that if the Service was deleted prior to processing of this request
	the Service values might not be available to be returned.
- `409 Conflict` if the given `epoch` was not equal to the existing `epoch` of
   the Service.

Other responses are allowed, but not defined by this specification.

The format of the `200 OK` HTTP Response MUST adhere to the following:
```
200 OK
Content-Type: application/json

{
  "url": "{url}",
  "name": "{name}",
  ... remainder of Service attributes ...
}
```

#### `DELETE /services`

This MUST delete all of the Services in the Discovery Endpoint that are
contained in the request. If any of those Services cannot be deleted for any
reason then the entire request MUST fail with no effect.

If an `id` is not specified in any of the Services the entire request MUST
fail. If no Service can be found that corresponds to a specified `id`, the
processing MUST ignore that Service and not fail as a result of the Service
already being deleted. An `epoch` value MAY be omitted in the incoming Service.
If present, and does not match the Service's current `epoch` value, then the
request MUST fail.

If other service attributes are included in the request, those SHOULD be
ignored for the purposes of processing the request.

There is no requirement that the Services in the request are processed in
the order in which they appear.

The follow responses are defined by this specification:
- `200 OK` if none of the specified Services remain in the Discovery Endpoint.
  - The HTTP Response Body MUST include an array of Services that match
    the order of the array of Services specified in the request.
	The Services in the response MUST include at least the `id` attributes
	and SHOULD include the remaining Service attributes as they existed
	at the time of the request processing if possible.
	Note that if the Service was deleted prior to processing of this request
	the Service values might not be available to be returned.
- `409 Conflict` if the first error encountered is that a given `epoch` was not
  equal to the recorded `epoch` of the Service. The Response Body SHOULD
  include information about which Service caused the error.

The format of the HTTP Request MUST adhere to the following:
```
Content-Type: application/json

[
  {
    id: "{id}",      // REQUIRED
    epoch: "{epoch}" // OPTIONAL
  },
  ...
]
```

The format of the `200 OK` HTTP Response MUST adhere to the following:
```
200 OK
Content-Type: application/json

[
  {
    "id": "{id}",
    "url": "{url}",
    "name": "{name}",
    ... remainder of Service attributes ...
  }
  ...
]
```

### Discovery Endpoint Service Change Events

The discovery service MAY include itself as a Service entity that is
discoverable.

The events produced by this "self" Service describe the management requests
made to the discovery service. The events produced MUST include the operation
and path to which the management request was made as well as the request body
and the response that was given.

Receiving the complete set of these will allow a downstream mirror to exactly
materialize a consistent Service collection. A downstream mirror MAY alter
records as appropriate for its circumstances.

Any Discovery Endpoint Service entities MUST adhere to the following:
```json
{
  "id": "{id}",
  ... other service attributes ...
  "events": [
    {
      "specversions": ["1.x-wip"],
      "type" : "io.cloudevents.discovery.change",
      "dataschemacontent": { // see ../discovery/discovery.yaml#/components/schemas/change
        "type": "object",
        "properties": {
          "operation": "{operation}", // POST|DELETE
          "path": "{path}",           // /services[/{id}]
          "request": {request},       // as per path specification
          "response": {response}      // as per path specification
        }
      }
    }
  ]
}
```

### OpenAPI

See [Discovery Endpoint OpenAPI Specification](../discovery/discovery.yaml).

## Privacy and Security

The CloudDiscovery API does not place restrictions on implementation's choice of
an authentication and authorization mechanism. While the list of entities
returned from each query MAY differ, the format of the output MUST adhere to
this specification.

Additionally, implementations MAY choose different authentication schemes for
each of the APIs defined in this specifications. For example, a valid choice
might be to allow the "features" APIs to not mandate any authentication at all,
while the "discovery" APIs might be restricted to authorized users.
