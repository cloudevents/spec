# CloudSubscriptions: Discovery - Version 0.1-wip

## Abstract

CloudSubscriptions Discovery API is a vendor-neutral API specification for
determining what events an Event Producer or Aggregator / Broker
has available, as well as how to subscribe to those events.

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

The goal of the CloudDiscovery API is to enable connections between consumers of
events and Event providers / producers / aggregators / brokers of events and to
facilitate the creation of CloudSubscriptions.

Discovery allows for an event producer or intermediary component to
advertise the event types that are available, provide the necessary information
to consume that event (schema / delivery protocol options), and the necessary
information to create a subscription. The output of the API ought to be such
that tooling can be built where all possible event producers and types aren’t
known in advance.

There are several discovery use cases to consider from the viewpoint of event
consumers.

1. What providers are available, and what event types do they produce?
2. What event types are available, and from which providers?

The second case becomes relevant if multiple providers support the same event
types. Use case 1 is likely the dominant use case. Given the example of a public
cloud provider where all producers produce events, there might be dozens of
sources (producer systems) and hundreds of event types. The discovery funnel of
producer first, then event types helps users navigate without having to see large
lists of event types. Both of these cases show the importance of using filters
in the discovery API to narrow down the selection of available events.

The CloudEvent `source` attribute is a potential cause of high fanout. For
example consider a blob storage system where each directory constitutes a
distinct `source` attribute value. For this reason, `source` is not part of the
discovery system.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

### Terminology

This specification defines the following terms:

#### Event Provider

An "Event Provider" is a grouping terminology used to aid in the discovery
process. It is a human readable name that developers can use to narrow in on
the origin system that produces the events they are interested in.

#### Producer

The "producer" is a specific instance, process or device that creates the data
structure describing the CloudEvent.

#### Intermediary

An "intermediary" receives a message containing an event for the purpose of
forwarding it to the next receiver, which might be another intermediary or a
consumer. A typical task for an intermediary is to route the event to receivers
based on the information in the event context.

#### Source

The "source" is the context in which the occurrence happened. In a distributed
system it might consist of multiple Producers. If a source is not aware of
CloudEvents, an external producer creates the CloudEvent on behalf of the
source.

#### Consumer

A "consumer" receives the event and acts upon it. It uses the context and data
to execute some logic, which might lead to the occurrence of new events.

#### Subscription

The request for events from an Event Producer system.

#### Event Subscriber

The entity managing the lifecycle of a Subscription on behalf of an Event
Consumer. In some instances this might be the same entity as the Event Consumer.

For example, a UI for connecting eventing producers to event consumers would
be considered an event subscriber and a target user of this API.

## API Specification

This API is specified as a REST API with well defined entities and relationships
between those entities.

### Entities in the API

1. `eventprovider`
2. `type`
3. `producer`

The `EventProvider` and `Type` entities form the basis of the directory and can
be used to build user experiences around discovery. The `Producer` entity is
keyed off of `{EventProvider.Name, Type.Name}` and provides the necessary
details to create a subscription for events of that `ce-type` from the selected
`EventProvider`.

### Entity Specifications

This section details the fields that make up each of the entities referenced
earlier in this document.

#### `eventprovider` entity

Used in discovery for enumerating the different providers represented in this
discovery system.

##### `eventprovider` entity attributes

###### name

- Type: `String`
- Description: The `name` attribute SHOULD be human readable and can identify a
  top level event provider system.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
- Examples:
  - "GitHub.com"
  - "Awesome Cloud Storage"
  - "com.example.microservices.userlogin"

###### description

- Type: `String`
- Description: Human readable description .
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string

###### provider_uri

- Type: `URI`
- Description: Absolute URI that provides a link back to the producer, or
  documentation about the producer. This is intended for a developer to
  use in order to learn more about this provider events produced.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty absolute URI
- Examples:
  - "http://cloud.example.com/docs/blobstorage"


##### `eventprovider` entity examples

```json
{
  "name": "Cloud Storage Provider",
  "description": "Blob storage in the cloud",
  "provider_uri": "https://cloud.example.com/docs/storage"
}
```

And a list of valid `provider` entities.

```json
[
  {
    "name": "Cloud Storage Provider",
    "description": "Blob storage in the cloud",
    "provider_uri": "https://cloud.example.com/docs/storage"
  },
  {
    "name": "Cloud MySQL"
  },
  {
    "name": "Cloud OtherSQL",
    "description": "Highly scalable SQL service"
  }
]
```

#### `type` entity

Used in discovery for enumerating the different CloudEvent `type`s represented
in this discovery system.

##### `type` entity attributes

###### type

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

###### datacontenttype

- Type: `String`
- Description: CloudEevnts [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#datacontenttype)
  attribute. Indicating how the `data` attribute of subscribed events will be
  encoded.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in [RFC 2046](https://tools.ietf.org/html/rfc2046)

###### dataschema

- Type: `URI`
- Description: CloudEevnts [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#dataschema)
  attribute. This identifies the canonical storage location of the schema of
  the `data` attribute of subscribed events.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI

###### dataschematype

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: If using `dataschemacontent` for inline schema storage, the
  `dataschematype` indicates the type of schema represented there.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Examples:
  - "application/json"
  -

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

##### `type` entity examples

A single `type` entity.

```json
{
  "type": "com.example.storage.object.create",
  "specversion": "1.x-wip",
  "datacontenttype": "application/json",
  "dataschema": "http://schemas.example.com/download/com.example.storage.object.create.json"
}
```

#### `producer` entity

Once discovery narrows down to a specific event `type` that we want to subscribe
to from a specific `provider`, the appropriate `producer` entity can be
retrieved by key. The key is a composite key of the `provider` and `type` names.

##### `producer` entity Attributes

The `Provider` entity is the main component of the discovery API. This section
covers the structure of that entity and the next section describes the
requirements for the query API.

###### eventprovider

- Type: `String`
- Description: Identifies the provider of the event. The `eventprovider` string
  SHOULD be human readable and can identify a top level producer system.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
- Examples:
  - "GitHub.com"
  - "Awesome Cloud Storage"
  - "com.example.microservices.userlogin"

###### produceruri

- Type: `URI`
- Description: Absolute URI that provides a link back to the producer, or
  documentation about the producer. This is for human consumption.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI
- Examples:
  - "http://cloud.example.com/docs/blobstorage"

###### type

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

###### specversion

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: CloudEvents [`specversion`](https://github.com/cloudevents/spec/blob/master/spec.md#specversion)
  that will be used for events published for this producer, event type
  combination.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string

###### datacontenttype

- Type: `String`
- Description: CloudEevnts [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#datacontenttype)
  attribute. Indicating how the `data` attribute of subscribed events will be
  encoded.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in [RFC 2046](https://tools.ietf.org/html/rfc2046)

###### dataschema

- Type: `URI`
- Description: CloudEevnts [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#dataschema)
  attribute. This identifies the canonical storage location of the schema of
  the `data` attribute of subscribed events.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI

###### dataschematype

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: If using `dataschemacontent` for inline schema storage, the
  `dataschematype` indicates the type of schema represented there.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Examples:
  - "application/json"
  -

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

###### extensions

- Type: `Map` of `String` to `String`
- Description: Associative map of CloudEvents [Extension Context Attributes](https://github.com/cloudevents/spec/blob/master/spec.md#extension-context-attributes)
  that are used for this event `type`. Keys MUST be confirm to the extension
  context attributes naming rules and value are the type of the extension
  attribute, conforming to the CloudEvents [type system](./spec.md#type-system).
- Constraints:
  - OPTIONAL

###### subscriptionendpoint

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

### REST Paths

Each path in the REST API represents either represents a list (or search) over
and entity class, or the retrieval of an individual entity by name. Each of
these operations MUST be supported by compliant discovery providers.

#### `/providers?matching=[search term]`

Returns a list of all providers in the discovery system, optionally filtering on
a provided search term (`matching`).

##### matching

* Type: `string`
* Description: Search term that provides case insensitive match against
  `provider` names. The parameter can match any portion of the provider name.
* Constraints:
  * OPTIONAL
  * If present, MUST be non-empty
* Examples:
  * `"storage"`
    * matches:
      * `"Awesome Cloud Storage"`
      * `"File storage system"`
      * `"storage Storage STORAGE"`

##### Returns

Upon successful processing, the response MUST be a JSON array of `provider`
entities.

#### `/providers/{name}`

Retrieves an individual provider entity by exact match on the `provider` name.

##### Returns

Upon successful processing, the response MUST be a JSON object that is a single
`provider` entity.

#### `/providers/{name}/types`

Retrieves the details about the types that are offered by the specified
`provider`.

##### Returns

Upon successful processing, the response MUST be a JSON array of `type` entity
objects.

#### `/types?matching=[search term]`

MUST return a list of all Types in the discovery system. If the matching query
parameter is specified then the returned list MUST only include Types that match
the search term value.

##### matching

* Type: `string`
* Description: Search term that provides case insensitive match against `type`
  names. The parameter can match any portion of the type name.
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

##### Returns

A JSON array of `type` entities.

#### `/types/{name}`

Retrieves an individual type entity by exact match on the `type` name. Type
names MUST conform to the [CloudEvents type](./spec.md#type)
attribute specification.

##### Returns

A `type` entity as a JSON object.

#### `/types/{name}/providers`

Retrieves the details about providers that offer the specified `type`.

##### Returns

A JSON array of `provider` entities.

#### `/producer/{provider.name}/{type.name}`

Retrieves the `producer` entity that specifies the information necessary to
create subscriptions and to consume the events. The `provider.name` and
`type.name` items in the request path make up the composite key for the
information that can be obtained via the `/provider` and `/type` API calls.

##### Returns

A `producer` entity as a JSON object.


## Protocol Bindings

The discovery API can be implemented over different API systems. We provide
API schema definitions for implementing this API using OpenAPI and gRPC as
illustrative examples.

### REST, JSON HTTP API

All responses will have a content-type of `application/json` and are either
a single JSON encoded object or an array of objects.

### OpenAPI

**TODO**

## Privacy and Security

The CloudDiscovery API does not place restrictions on producers choice of an
authentication and authorization mechanism. Discovery output MAY be different
for different principals.
