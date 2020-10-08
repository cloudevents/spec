# CloudSubscriptions: Discovery - Version 0.1-wip

## Abstract

CloudSubscriptions Discovery API is a vendor-neutral API specification for
determining what events are available from a particular service, as well as how
to subscribe to those events.

## Status of this document

This is a working draft. Breaking changes could be made in the next minor
version.

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

Note: some of the terms defined below are taken from the [CloudEvents](spec.md)
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

#### Source [[CE](./spec.md#source)]

The "source" is the context in which the occurrence happened. In a distributed
system it might consist of multiple Producers. If a source is not aware of
CloudEvents, an external producer creates the CloudEvent on behalf of the
source.

#### Producer [[CE](./spec.md#producer)]

The "producer" is a specific instance, process or device that creates the data
structure describing the CloudEvent.

#### Intermediary [[CE](./spec.md#intermediary)]

An "intermediary" receives a message containing an event for the purpose of
forwarding it to the next receiver, which might be another intermediary or a
[Consumer](#consumer-ce). A typical task for an intermediary is to route the
event to receivers based on the information in the event
[Context](./spec.md#context).

#### Consumer [[CE](./spec.md#consumer)]

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
  "id": "[a globally unique UUID]",
  "epoch": "[discovery entry epoch value]",
  "url": "[unique URL to this service]",
  "name": "[unique name for this services]",
  "description": "[human string]", ?
  "docsurl": "[URL reference for human documentation]", ?
  "specversions": [ "[ce-specversion value]" + ],
  "subscriptionurl": "[URL to which the Subscribe request will be sent]",
  "subscriptionconfig": { ?
    "[key]": "[value]", *
  },
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
  "epoch": 1,
  "url": "https://example.com/services/widgetService",
  "name": "widgets",
  "specversions": ["1.0"],
  "subscriptionurl": "https://events.example.com",
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
- Description: A unique identifier for this Service. This value MUST be globally
  unique. While other metadata about this Service MAY change, this value MUST
  NOT so that clients can use this attribute to know whether a Service returned
  by a query is the same Service returned by a previous query.

  Whether a change to a Service would result in changing of the Service's
  metadata (except `id`) and thus be just an update of an existing Service, or
  whether the change would result in a brand new Service (with a new `id`) is
  not defined by this specification.

  For example, if a Service's implementation is upgraded to a new version then
  whether this would result in a new Service (and `id`) or is an update to the
  existing Service's metadata, is an implementation choice. Likewise, this
  specification makes no statement, or guarantees, as to the forwards or
  backwards compatibility a Service as it changes over time.

  Note, unlike the `name` attribute which only needs to be unique within the
  scope of a single Discovery Endpoint, the global uniqueness aspect of this
  attribute allows for the discovery of the same Service across multiple
  Discovery Endpoints.

  See the Primer for more information.

- Constraints:
  - REQUIRED in responses from the Discovery Endpoint.
  - MUST be a valid UUID per RFC4122.
- Examples:
  - `bf5ff5cc-d059-4c79-a89a-2513e45a1340`

##### epoch

- Type: `Integer`
- Description: The Discovery Endpoint's epoch value for this Service Entry.
  This specification does not mandate any particular semantic meaning to
  the value used. For example, implementations are free to use a value that
  represents a timestamp or could choose to simply use a monotomically
  increasing number. The only requirement is that the value MUST always
  increase each time the Service Entry is updated. This allows for a quick
  integer comparision to determine which version of this Service Entry is the
  latest - meaning, the one with the larger integer value.

- Constraints:
  - REQUIRED in responses from the Discovery Endpoint.
- Examples:
  - `42`
  - `915148800`

##### name

- Type: `String`
- Description: A unique human readable identifier for this Service. This value
  MUST be unique (case insensitive) within the scope of this Discovery Endpoint.
  Note, this differs from the `id` attribute which is globally unique.
- Constraints:
  - REQUIRED
- Examples:
  - `my storage service`
  - `cool git offering`

##### url

- Type: `URL`
- Description: An absolute URL that references this Service. This value MUST be
  usable in subsequent requests, by authorized clients, to retrieve this Service
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

- Type: Array of `Strings` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: CloudEvents
  [`specversions`](https://github.com/cloudevents/spec/blob/master/spec.md#specversion)
  that can be used for events published for this service.
- Constraints:
  - REQUIRED
  - MUST be a non-empty array or non-empty strings

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
  allowed config map, the values indicate the type of that parameter, confirming
  to the CloudEvents
  [type system](https://github.com/cloudevents/spec/blob/master/spec.md#type-system).
  TODO: Needs resolution with CloudSubscriptions API
- Constraints:
  - OPTIONAL
- Examples:
  - ??

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

##### type

- Type: `String`
- Description: CloudEvents
  [`type`](https://github.com/cloudevents/spec/blob/master/spec.md#type)
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
  [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#datacontenttype)
  attribute. Indicating how the `data` attribute of subscribed events will be
  encoded.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)

###### dataschema

- Type: `URI`
- Description: CloudEvents
  [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#dataschema)
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
  - If `dataschama` is present, this field MUST NOT be present.

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
  [Extension Context Attributes](https://github.com/cloudevents/spec/blob/master/spec.md#extension-context-attributes)
  that are used for this event `type`. The structure contains the following
  attributes:
  - `name` - the CloudEvents context attribute name used by this extension. It
    MUST adhere to the CloudEvents context attribute naming rules
  - `type` - the data type of the extension attribute. It MUST adhere to the
    CloudEvents [type system](./spec.md#type-system)
  - `specurl` - an attribute pointing to the specification that defines the
    extension
- Constraints:
  - OPTIONAL
  - if present, the `name` attribute in the structure is REQUIRED
  - if present, the `type` attribute in the structure is REQUIRED
  - if present, the `specurl` attribute in the structure is OPTIONAL
- Examples:
  - `{ "name": "dataref", "type": "URI-reference", "specurl": "https://github.com/cloudevents/spec/blob/master/extensions/dataref.md" }`

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

## API Specification

The endpoints defined by this specification are broken into two categories:
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

Unless there is some out-of-band agreement, all APIs MUST use JSON encoding,
which means when there is an HTTP Body the HTTP `Content-Type` Header MUST
be `application/json`.

### Discovery APIs

All of the API endpoints specified in this section MUST be supported by
compliant Discovery Endpoint implementations.

#### `GET /services`

This MUST return an array of zero or more Services. The array MUST contain all
Services available via this Discovery Enpoint.

In the case of `200 OK`, the response format MUST adhere to the following:

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

Implementations MAY use the [pagination](pagination.md) specification
if the number of Services returned is large. Clients SHOULD be
prepared to support paginated responses.

#### `GET /services/{id}`

If this refers to a valid Service, then this MUST return that single Service
entity.

The following responses are defined by this specification:
- `200 OK` and the Service representation in the HTTP Response Body.
- `404 Not Found` if there is no Service with the specified `id`.

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

#### `GET /services?name={name}`

This returns a single Service whose `name` attribute exactly matches the
`name` query parameter value specified (case insensitive).

The following responses are defined by this specification:
- `200 OK` and the Service representation in the HTTP Response Body.
- `404 Not Found` if there is no Service with the specified `id`.

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

This MUST add the specified Services to the list of Services available at this
Discovery Endpoint. The Body of the request message MUST contain an array of
zero or more Service Entries. For convinience to clients, each Service in the
array MAY include the `id` or `epoch` attributes but they MUST be ignored by
the Discovery Endpoint. Both of these attributes' values MUST be defined by
the Discovery Endpoint.

If any Service specified in the request matches the `name` of any existing
Service, or the same `name` is used more than once within the request, then
an error MUST be generated.

If the Discovery Endpoint is unable to successully add all of the Services
in the incoming request then an error MUST be generated and none of the
specified Services are to be added to the Discovery Endpoint.

The follow responses are defined by this specification:
- `201 Created` if all the specified Services were processed successfully.
  - If there was only one Service in the incoming request, then the response
    MUST include an HTTP `Location` Header with a value that points to the
	correspdonding Service.
  - If the request contained more than one Service, then the HTTP `Location`
    Header MUST NOT appear in the response.
  - The HTTP Response Body MUST include an array of `id` values whose order
    and values MUST match the list of Services in the request.

Other responses are allowed, but not defined by this specification.

The format of the HTTP Request MUST adhere to the following:
```
Content-Type: application/json

[
  {
    "url": "{url}",
    "name": "{name}",
    ... remainder of Service attributes ...
  }
  ...
]
```

The format of the HTTP Response MUST adhere to the following:
```
Content-Type: application/json

[
  "id": "{id}"
  ...
]
```

#### `POST /services?import`

This MUST add, or update, the specified Services to the list of Services
available at this Discovery Endpoint. The Body of the request message MUST
contain an array of zero or more Service Entries. For convinience to clients,
the presence of the `id` and `epoch` attributes are OPTIONAL. If `id` is
present then it MUST be retained as a result of this operation and any existing
Service with that `id` MUST be replaced. If `epoch` is present then the
`epoch` value of the resulting Service MUST be larger than the maximum of
the incoming Service and any existing Service with that same `id`. If either
attribute is not present then the Discovery Endpoint MUST assign appropriate
value to the missing attribute.

If the Discovery Endpoint is unable to successully add all of the Services
in the incoming request then an error MUST be generated and none of the
specified Services are to be added, or updated, in the Discovery Endpoint.

The Services in the request message MUST be processed in the order in which
they appear. While any error in the overall process MUST rollback any changes
made due to the request, the processing of each Service in the request MUST be
applied as if all previous Services in the request were already completed.
This means that attribute uniqueness checking, such as on the `name`
attribute, MUST be done on the new state of all Services as if all previously
specified Services in the incoming request were already successfully processed.

For example, if a Discovery Endpoint has a Service called `MyService`, it is
possible to rename that Service to `YourService` and then to add, or update,
another Service to use `MyService` as its `name`. But this is only true if
the rename of the first Service happens first the request message.

Likewise, while it might be less than optimal, it is technically possible for
a request to update a Service multiple times if the same `id` is used more
than once within a request.

The follow responses are defined by this specification:
- `201 Created` if all the specified Services were processed successfully.
  - If there was only one Service in the incoming request, then the response
    MUST include an HTTP `Location` Header with a value that points to the
	correspoding Service.
  - If the request contained more than one Service, then the HTTP `Location`
    Header MUST NOT appear in the response.
  - The HTTP Response Body MUST include an array of `id` values whose order
    and values MUST match the list of Services in the request.

Other responses are allowed, but not defined by this specification.

The format of the HTTP Request MUST adhere to the following:
```
Content-Type: application/json

[
  {
    "url": "{url}",
    "name": "{name}",
    ... remainder of Service attributes ...
  }
  ...
]
```

The format of the HTTP Response MUST adhere to the following:
```
Content-Type: application/json

[
  "id": "{id}"
  ...
]
```

#### `PUT /services/{id}`

This MUST update an existing Service in a Discovery Endpoint. The Body of the
request message MUST contain a single Service definition. The Service MUST
contain an `id` attribute that matches the `{id}` in the `PUT` URL.

The request MAY include the `epoch` attribute. If present then the Discovery
Endpoint MUST ensure that the value on the incoming request matches the
current value on the Service. If they do not match then an error MUST be
generated and the Service MUST NOT be updated. However, if the incoming
request does not include this attribute then this verification MUST NOT
be done.

Additionally, if the incoming request did contain the `epoch` attribute, then
its value MUST be updated by the Discovery Endpint to a larger value,
indicating that the Service has been updated.

The follow responses are defined by this specification:
- `200 OK` if Service was updated.
  The HTTP Response Body MUST include the JSON represenation of the updated
  Service.
- `404 Not Found` if there is no Service with the specified `id`.

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

The format of the HTTP Response MUST adhere to the following:
```
Content-Type: application/json

{
  "url": "{url}",
  "epoch": "{id}",
  "name": "{name}",
  ... remainder of Service attributes ...
}
```
#### `PUT /services/{id}?import`

This MUST create or update a Service in a Discovery Endpoint. The Body of the
request message MUST contain a single Service definition, however the presence
of the `epoch` attribute is OPTIONAL. The Service MUST contain an `id`
attribute that matches the `{id}` in the `PUT` URL.

If `epoch` attribute is present then the resulting value of this attribute
MUST result in a value that is larger than both the incoming `epoch` value and
any existing Service's `epoch` value.  If it is not present then the Discovery
Endpoint MUST assign a value that is larger than any existing Service's
`epoch` value.

The follow responses are defined by this specification:
- `200 OK` if an existing Service was updated.
  The HTTP Response Body MUST include the JSON represenation of the updated
  Service.
- `201 Created` if a new Service was added.
  The HTTP Response Body MUST include the JSON represenation of the
  newly created Service.

Other responses are allowed, but not defined by this specification.

The format of the HTTP Request MUST adhere to the following:
```
Content-Type: application/json

{
  "url": "{url}",
  "name": "{name}",
  ... remainder of Service attributes ...
}
```

The format of the HTTP Response MUST adhere to the following:
```
Content-Type: application/json

{
  "url": "{url}",
  "epoch": "{int}",
  "name": "{name}",
  ... remainder of Service attributes ...
}
```
#### `DELETE /services/{id}`

This MUST delete the Service at the referenced URL.

The follow responses are defined by this specification:
- `200 OK` if the new Service was deleted.
- `404 Not Found` if there is no Service with the specified `id`.

Other responses are allowed, but not defined by this specification.

If the Service is successfully deleted any HTTP `GET` to the Service's
original URL MUST return an HTTP `404 Not Found` unless that URL happens to be
reused in the future (e.g. the Service was restored from a backup).

### OpenAPI

...

## Privacy and Security

The CloudDiscovery API does not place restrictions on implementation's choice of
an authentication and authorization mechanism. While the list of entities
returned from each query MAY differ, the format of the output MUST adhere to
this specification.
