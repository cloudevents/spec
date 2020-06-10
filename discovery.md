# CloudSubscriptions: Discovery - Version 0.1-wip

## Abstract

CloudSubscriptions Discovery API is a vendor-neutral API specification for
determining what events are available from a particular system, as well as
how to subscribe to those events.

## Status of this document

This is a working draft. Breaking changes could be made in the next minor
version.

## Table of Contents

- [Overview](#overview)
- [Notations and Terminology](#notations-and-terminology)
- [API Specification](#api-specification)
- [Protocol Bindings](#protocol-bindings)
- [Privacy & Security](#privacy-and-security)

## Overview

In order for consumers to receive events from event producers, they need
to first subscribe, or ask for, events from those producers. To do so, there
is often a process necessary that involves steps such as discovering which
event producer is of interest, what events it generates and how to create the
subscription for those events.

This specification defines a set of APIs to allow for consumers to perform
these queries against a "Discovery Endpoint". A Discovery Endpoint acts
as a catalog of:
  - [Services](#service)
  - [Event Producers](#producer-ce)
  - Event Types
overwhich consumers can query to find the Event Producer of interest, and
to which it can create a Cloud Subscription.

Which means, once the Event Producer of interest is located, additional
metadata is provided in order to consume and subscribe to events. The goal
of this API is to be such that tooling can be built where all all possible
event producers and event types aren't known in advance.

The deployment relationship of a Discovery Endpoint to the Services and
Event Producers that it advertises is out of scope of this specification.
For example, a Discovery Endpoint could choose to be implemented as part of a
Service, or Event Producer, or it could be acting as an independent aggregrator
of this metadata. This implementation detail will be transparent to consumers.

There are several discovery use cases to consider from the viewpoint of event
consumers.

1. What event producers are available, and what event types do they generate?
2. What event types are available, and from which event producers?

The second case becomes relevant if multiple producers support the same event
types. Use case 1 is likely the dominant use case. Given the example of a public
cloud provider where all producers generate events, there might be dozens of
sources (producer systems) and hundreds of event types. The discovery funnel of
producer first, then event types helps users navigate without having to see
large lists of event types. Both of these cases show the importance of using
filters in the discovery API to narrow down the selection of available events.

The CloudEvent `source` attribute is a potential cause of high fanout. For
example, consider a blob storage system where each directory constitutes a
distinct `source` attribute value. For this reason, the exact CloudEvents
`source` attribute value that might appear in a CloudEvent will not appear in
the Discovery API query result. Instead, a higher level classifier
(`service`) will be used to represent the abstract notion of the generic
event producer of those events - in the example case, the blob storage service
itself.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

### Terminology

Note: some of the terms defined below are taken from the
[CloudEvents](spec.md) specification, and are marked with a reference to
the original definition. Any difference between the definitions is accidental
and the CloudEvents version takes precendence.

This specification defines the following terms:

#### Discovery Endpoint

A compliant implementation of this specification that advertises the set
of Services, Event Types and other metadata to aid in the creation of an
Event Subcription.

#### Service

A "service" represents the entity which manages one or more event
[sources](#source-ce) and is associated with [producers](#producer-ce)
that generate events.

For example, an Object Store service might have a set of event sources
where each event source maps to a bucket.

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
event to receivers based on the information in the
event [Context](./spec.md#context).

#### Consumer [[CE](./spec.md#consumer)]

A "consumer" receives the event and acts upon it. It uses the context and data
to execute some logic, which might lead to the occurrence of new events.

#### Subscription

The request for events from an Event Producer system.


## API Specification

This API is specified as a REST API with well defined entities and
relationships between those entities.

### Services

At the core of the data model is the concept of a [Service](#service). The
API then exposes multiple ways to query over a list of Services. To help
explain the Service resource, the following non-normative pseudo yaml shows
its basic structure:

( `*` means zero or more, `+` means one or more, `?` means optional)

Service:
```
id: [unique URI]
description: [human string] ?
docsuri: [URI reference for human documentation] ?
specversion: [ce-speciversion value] ? (required?)
subscriptionuri: [URI to which the Subscribe request will be sent]
subscriptionconfig: *
authscope: [string] ?  (explain)
protocols: +
- protocol: [string]
types: *
- type: [ce-type value]
  description: [human string] ?
  datacontenttype: [ce-datacontenttype value] ?
  dataschema: [ce-dataschema URI] ?
  dataschematype: [string per RFC 2046] ?
  dataschemacontent: [schema] ?
  dataschemacontent:
  extensions: *
  - name: [CE context attribute name]
    type: [CE type string]
    spec: [URI to specification defining the extension] ?
```

An example:
```
id: example.com
subscriptionuri: https://events.example.com
protocols:
- protocol: HTTP
types:
- type: com.example.widget.create
- type: com.example.widget.delete
```

Note: the above is just a sample and implementations are free to use any
internal model they wish to store the data as long as they are compliant
with the wire format/API defined by this specification.

#### Service Attributes

The following sections define the attributes that appear on a Service
entity.

##### id

- Type: `URI`
- Description: A unique, within the scope of this Discovery Endpoint, URI
  that identifies the Service.
- Constraints:
  - REQUIRED
  - MUST be a non-empty URI
- Examples:
  - cloudstorage.com
  - github.com
  - "com.example.microservices.userlogin"

##### description (Service)

- Type: `String`
- Description: Human readable description.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string

##### docsuri

- Type: `URI`
- Description: Absolute URI that provides a link back to the producer, or
  documentation about the producer. This is intended for a developer to
  use in order to learn more about this service events produced.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty absolute URI
- Examples:
  - "http://cloud.example.com/docs/blobstorage"

###### specversion

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: CloudEvents [`specversion`](https://github.com/cloudevents/spec/blob/master/spec.md#specversion)
  that will be used for events published for this producer, event type
  combination.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string

###### subscriptionuri

- Type: `URI-reference`
- Description: URI indicating where CloudSubscriptions `subscribe` API calls
  MUST be sent to.
- Constraints:
  - REQUIRED

###### subscriptionconfig

- Type: `Map` of `String` to `String`
- Description: A map indicating supported options for the `config` parameter
  for the CloudSubscriptions subscribe() API call. Keys are the name of keys
  in the allowed config map, the values indicate the type of that parameter,
  confirming to the CloudEvents [type system](https://github.com/cloudevents/spec/blob/master/spec.md#type-system).
  TODO: Needs resolution with CloudSubscriptions API
- Constraints:
  - OPTIONAL
- Examples:

###### authscope

- Type: `String`
- Description: Authorization scope needed for creating subscriptions.
  The actual meaning of this field is determined on a per-producer basis.
- Constraints:
  - OPTIONAL
- Example:
  - "storage.read"

###### protocols

- Type: `List` of `String`
- Description: This field describes the different values that might be passed
  in the `protocol` field of the CloudSubscriptions API. The protocols with
  existing CloudEvents bindings are identified as AMQP, MQTT3, MQTT5, HTTP,
  KAFKA, and NATS. An implementation MAY add support for further
  protocols. All producers MUST support at least one delivery protocol, and MAY
  support additional protocols.
- Constraints:
  - REQUIRED
  - MUST be non-empty.
- Examples:
  - ["HTTP"]
  - ["HTTP", "AMQP", "KAFKA"]

##### type

- Type: `String`
- Description: CloudEvents [`type`](https://github.com/cloudevents/spec/blob/master/spec.md#type)
  attribute.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string, following the constraints as defined in the
    CloudEvents spec.
- Examples:
  - "com.github.pull.create"
  - "com.example.object.delete.v2"

##### description (Type)

- Type: `String`
- Description: Human readable description.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string

##### datacontenttype

- Type: `String`
- Description: CloudEvents [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#datacontenttype)
  attribute. Indicating how the `data` attribute of subscribed events will be
  encoded.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)

##### dataschema

- Type: `URI`
- Description: CloudEvents [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#dataschema)
  attribute. This identifies the canonical storage location of the schema of
  the `data` attribute of subscribed events.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI

##### dataschematype

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: If using `dataschemacontent` for inline schema storage, the
  `dataschematype` indicates the type of schema represented there.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Examples:
  - "application/json"

##### dataschemacontent

- Type: `String`
- Description: An inline representation of the schema of the `data` attribute
  encoding mechanism. This is an alternative to using the `dataschema`
  attribute.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string containing a schema compatible with
    the `datacontenttype`.
  - If `dataschama` is present, this field MUST NOT be present.

###### extensions

- Type: `Map` of `String` to `String`
- Description: Associative map of CloudEvents [Extension Context Attributes](https://github.com/cloudevents/spec/blob/master/spec.md#extension-context-attributes)
  that are used for this event `type`. Keys MUST be confirm to the extension
  context attributes naming rules and value are the type of the extension
  attribute, conforming to the CloudEvents [type system](./spec.md#type-system).
- Constraints:
  - OPTIONAL

#### Service Examples

```json
{
  "id": "com.example.storage",
  "description": "Blob storage in the cloud",
  "service_uri": "https://cloud.example.com/docs/storage",
  "types": [
    "type": "com.example.storage.object.create",
    "specversion": "1.x-wip",
    "datacontenttype": "application/json",
    "dataschema": "http://schemas.example.com/download/com.example.storage.object.create.json"
  ]
}
```


### REST Paths

Each path in the REST API represents either represents a list (or search) over
and entity class, or the retrieval of an individual entity by name. Each of
these operations MUST be supported by compliant discovery implementations.

#### Services

The following API query patterns are defined.

For each, upon succesful processing, the response MUST be a JSON array with
zero or more Service entities.

When encoded in JSON, the format MUST adhere to the following:

```
[
  {
    "id": "SERVICE-ID",
    ... remainder of Service attributes ...
  },
  ...
]
```

#### `/services`

This MUST return an array of zero or more Services. The list MUST contain
all Services that the client is authorized to see. The list MUST NOT contain
any Services that the client is not authorized to see.

##### `/services/{id}`

Same as `/services` but the array MUST be limited to at most one, the entity
whose `id` matches the value specified.

##### `/services?matching=[search term]`

Same as `/services` but the array MUST be limited to just those Services
whose `description` attribute contains the `search term` value (case
insensitive).

###### matching

* Type: `string`
* Description: Search term that provides case insensitive match against
  the Service's `description` attribute. The parameter can match any portion
  of the service's `description` value.
* Constraints:
  * OPTIONAL
  * If present, MUST be non-empty
* Examples:
  * `"storage"`
    * matches:
      * `"Awesome Cloud Storage"`
      * `"File storage system"`
      * `"storage Storage STORAGE"`


#### Types

The following API query patterns are defined.

For each, upon succesful processing, the response MUST be a JSON array with
zero or more Type values, each with the list of Service entities that
support that Type.

When encoded in JSON, the format MUST adhere to the following:

```
[
  "TYPE-VALUE": {
    "id": "SERVICE-ID",
    ... remainder of Service attributes ...
  },
  ...
]
```

##### `/types`

This MUST return an array of zero or more Types values. The list MUST contain
all Types values from all Services that the client is authorized to see. It
MUST NOT container Type values from Services that the client is not authorized
to see.

##### `/types/{type}`

Retrieves an individual type entity by exact match on the `type` value. Type
values MUST conform to the [CloudEvents type](./spec.md#type) attribute
specification.


##### `/types?matching=[search term]`

Same as `/types` but the array MUST be limited to just those Types
whose value contains the `search term` value (case insensitive).

###### matching

* Type: `string`
* Description: Search term that provides case insensitive match against
  the Type's value. The parameter can match any portion of the value.
* Constraints:
  * OPTIONAL
  * If present, MUST be non-empty
* Examples:
  * `"com.storage.object"`
    * matches:
      * `"com.storage.object.create"`
      * `"com.storage.object.delete"`
      * `"com.storage.object.update"`
  * `"storage"`
    * matches:
      * `"com.storage.object.create"`
      * `"com.storage.object.delete"`
      * `"com.storage.object.update"`
  * `"create"`
    * matches:
      * `"com.storage.object.create"`


## Protocol Bindings

The discovery API can be implemented over different API systems. We provide
API schema definitions for implementing this API using OpenAPI and gRPC as
illustrative examples.

### HTTP Binding

When using JSON, the HTTP `Content-Type` value MUST be `application/json`.

### OpenAPI

...

## Privacy and Security

The CloudDiscovery API does not place restrictions on implementation's choice
of an authentication and authorization mechanism. While the list of entities
returned from each query MAY differ, the format of the output MUST adhere
to this specification.
