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

This sections defines the resource model of a Discovery Endpoint.

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

  Typically, this value is defined by the Discovery Endpoint, or one of the
  components behind it. However, there might be cases where the value is
  provided to the Discovery Endpoint, for example, during an "import" type of
  operation.

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
  - REQUIRED
  - MUST be a valid UUID per RFC4122.
- Examples:
  - `bf5ff5cc-d059-4c79-a89a-2513e45a1340`

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

All of the APIs specified below MUST be supported by compliant Discovery
Endpoint implementations.

Note: the relative paths specified below are NOT REQUIRED to be at the root of
the `fpath` (per RFC1738). However, they are REQUIRED to match the end of it.
For example, the follow are valid URLs/paths:

```
https://example.com/services
https://example.com/myAggregator/services
```

If a Discovery Endpoint can perform authorization checks to determine
which client can see which Service, and the requesting client is not allowed
access to a particular Service, then the Discovery Endpoint MUST respond
as if that Service did does exist. For example, it would be excluded from
any array of Services returned and it would result in a `404 Not Found`
error for a request to that Service directly.

Unless there is some out-of-band agreement, all APIs MUST use JSON encoding,
which means when there is an HTTP Body the HTTP `Content-Type` Header MUST
be `application/json`.

#### Services

#### `GET /services`

This MUST return an array of zero or more Services. The array MUST contain all
Services available via this Discovery Enpoint.

When encoded in JSON, the response format MUST adhere to the following:

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

##### `GET /services/{id}`

If this refers to a valid Service, then this MUST return that single Service
entity.

The following responses are defined by this specification:
- `200 OK` and the new Service representation in the HTTP Response Body.
- `204 No Content` to indicate that the Service is in the process of being
  created but has not yet completed.  The HTTP Response Body MAY be empty.
- `404 Not Found` if there is no Service with the specified `id`.
- `406 Not Acceptable` to indicate that the Service at this endpoint has
  failed to be created due to the creation request being syntactically invalid.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.
- `409 Conflict` to indicate that the Service at this endpoint has failed
  to be created due to the value of one or more of the attributes of the
  creation request being invalid.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.

TODO: Define the shape of errors in the Body

Other responses are allowed, but not defined by this specification.

In the case of `200 OK`, the response format MUST adhere to the following:

```
200 OK
Content-Type: application/json

{
  "id": "{id}",
  "url": "{url}",
  "name": "{name}",
  ... remainder of Service attributes ...
}
```

Note: in the case of `406 Not Acceptable` or `409 Conflict`, it is an
implementation choice as to how long these responses will be returned. But it
is expected that a `404 Not Found` will eventually be returned.

#### `POST /services`

This MUST add a Service to the list of Services available at this Discovery
Endpoint. The Body of the request message MUST contain a valid single Service
definition, with the exception that it MUST NOT include an `id` attribute.
The `id` MUST be generated by the Discovery Enpoint.

An error MUST be generated if the request can not be fulfilled.

The follow responses are defined by this specification:
- `201 Created` if the new Service was added. The response MUST include
  an HTTP `Location` Header with a value that points to the new Service.
  The HTTP Response Body MUST include the JSON represenation of the
  newly created Service.
- `202 Accepted` to indicate that the request has been accepted but not
  processed yet. The response MUST include an HTTP `Location` Header with
  a value that can be used to determine the status of the request. The
  HTTP Response Body MAY be empty.
- `406 Not Acceptable` to indicate that the request message is syntactically
  invalid.  For example, if it contains an `id` attribute.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.
- `409 Conflict` to indicate that the request message is syntactically valid,
  but the value of one or more of the attributes are invalid - for example, the
  `name` is not unique.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.

Other responses are allowed, but not defined by this specification.

If a `202 Accepted` was returned, an HTTP `GET` to the `Location` endpoint
can be used to determine the status of the original request.
This specification defines the following responses:
- `200 OK` and the new Service representation in the HTTP Response Body -
  meaning that this URL is the final URL of the newly added Service. Note:
  in this case the URL MUST adhere to the normal `/services/{id}` format.
- `204 No Content` to indicate that the `POST` request is not completed yet.
  The HTTP Response Body MAY be empty.
- `301 Moved Permanently` to indicate that the Service was successfully
  added and can be found at the URL in the REQUIRED `Location` header of the
  response.
- `406 Not Acceptable` to indicate that the original request message was
  syntactically invalid.  For example, if it contains an `id` attribute.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.
- `409 Conflict` to indicate that the original request message is
  syntactically valid, but the value of one or more of the attributes are
  invalid - for example, the `name` is not unique.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.

Other responses are allowed, but not defined by this specification, however
they are related to the `GET` itself and not the original add request.

How long the Discovery Endpoint will support the original `Location` URL is
an implementation choice, however, it MUST be available immediately upon
return of the `202 Accepted`. Meaning, a `404 Not Found` MUST NOT be returned
in response to a `GET` to the `Location` URL during the time the creation
request is being processed.

##### `PUT /services/{id}`

This operation is used to either add or update a Service in a Discovery
Endpoint. If a Service already exists with the specified `id` then this
MUST attempt to update that Service. If not, then a new Service MUST be
added with that `id`.

The Body of the request message MUST contain a single Service
definition. Unlike the `POST` operation, the Service MUST contain an `id`
attribute that matches the `{id}` in the `PUT` URL.

An error MUST be generated if the request can not be fulfilled.

The follow responses are defined by this specification:
- `200 OK` if an existing Service was updated.
  The HTTP Response Body MUST include the JSON represenation of the
  newly created Service.
- `201 Created` if a new Service was added.
  The HTTP Response Body MUST include the JSON represenation of the
  newly created Service.
- `202 Accepted` to indicate that the request has been accepted but not
  processed yet. The response MUST include an HTTP `Location` Header with
  a URL that can be used to determine the status of the request. The
  HTTP Response Body MAY be empty.
  Note: in the case of updating an existing Service, the URL MUST NOT be the
  same as the Service's URL.
- `403 Forbidden` if this Discovery Endpoint does not support creation of
  new Services with pre-defined `id` values. This means that the client
  would need to use the `POST` method above instead.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.
- `406 Not Acceptable` to indicate that the request message is syntactically
  invalid.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.
- `409 Conflict` to indicate that the request message is syntactically valid,
  but the value of one or more of the attributes are invalid - for example, the
  `name` is not unique.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.

Other responses are allowed, but not defined by this specification.

If a `202 Accepted` was returned, an HTTP `GET` to the `Location` endpoint
can be used to determine the status of the original request. This specification
defines the following responses:
- `200 OK` indicates that the `PUT` was successful. The HTTP Response Body
  MAY be empty - thus clients are expected to use the Service's true URL
  to retrieve the current version of the Service.
- `204 No Content` to indicate that the `PUT` request is not completed yet.
  The HTTP Response Body MAY be empty.
- `406 Not Acceptable` to indicate that the request message is syntactically
  invalid.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.
- `409 Conflict` to indicate that the original request message is
  syntactically valid, but the value of one or more of the attributes are
  invalid - for example, the `name` is not unique.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.

Other responses are allowed, but not defined by this specification, however
they are related to the `GET` itself and not the original `PUT` request.

How long the Discovery Endpoint will support the original `Location` URL is
an implementation choice, however, it MUST be available immediately upon
return of the `202 Accepted`. Meaning, a `404 Not Found` MUST NOT be returned
in response to a `GET` to the `Location` URL during the time the creation
request is being processed.

##### `DELETE /services/{id}`

This MUST delete the Service at the referenced URL. If the Service can not
be deleted then an error MUST be generated.

If an error is not generated, the Discovery Endpoint MUST return one of:
- `200 OK` if the new Service was deleted
- `202 Accepted` to indicate that the request has been accepted but not
  processed yet

Other responses are allowed, but not defined by this specification.

In the case of `202 Accepted` the Discovery Endpoint MUST include an
HTTP `Location` Header in the response pointing to an endpoint that the
client can use to determine the status of the delete.

A successful HTTP `GET` to the `Location` endpoint MUST either return:
- `200 OK` meaning the the original Service was successfully deleted
- `204 No Content` to indicate that the `DELETE` request is not completed yet
- `409 Conflict` to indicate that the original `DELETE` request message failed.
  The HTTP Response Body SHOULD contain information as to why the create
  failed.

Note that any other failure response indicates that the `GET` to the
`Location` URL itself failed and not the original delete request.

How long the Discovery Endpoint will support the `Location` URL is an
implementation choice.

If the Service is successfully deleted any HTTP `GET` to the Service's
original URL MUST return an HTTP `404 Gone` unless that URL happens to be
reused in the future (e.g. the Service was restored from a backup).

##### `GET /services?name={name}`

This returns a single Service entity whose `name` attribute exactly matches the
`name` query parameter value specified (case insensitive).

When encoded in JSON, the response format MUST adhere to the following:

```
200 OK
Content-Type: application/json

{
  "id": "{id}",
  "url": "{url}",
  "name": "{name}",
  ... remainder of Service attributes ...
}
```

### OpenAPI

...

## Privacy and Security

The CloudDiscovery API does not place restrictions on implementation's choice of
an authentication and authorization mechanism. While the list of entities
returned from each query MAY differ, the format of the output MUST adhere to
this specification.
