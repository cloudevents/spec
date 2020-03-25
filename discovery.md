# CloudSubscriptions: Discovery - Version 0.1-rc01

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
events and producers / aggregators / brokers of events and to facilitate the
creation of CloudSubscriptions.

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
cloud provider where all producers produce events, there may be dozens of
sources (producer systems) and hundreds of event types. The discovery funnel of
producer first, then event types helps users navigate without having to see large
lists of event types. Both of these cases require that filters can be used
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

This document structure focuses on discovery where each document has a two part
key of `provider` and `type`. This takes a denormalized view where the composite
key of documents is the `provider` and `type`. Provider is defined as an
arbitrary human readable string and `type` is the CloudEvent `type` attribute.

### Provider entity Attributes

The `Provider` entity is the main component of the discovery API. This section
covers the structure of that entity and the next section describes the
requirements for the query API.

#### provider

- Type: `String`
- Description: Identifies the provider of the event. The producer string SHOULD
  be human readable and can identify a top level producer system.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
- Examples:
  - "GitHub.com"
  - "Awesome Cloud Storage"
  - "com.example.microservices.userlogin"

#### produceruri

- Type: `URI`
- Description: Absolute URI that provides a link back to the producer, or
  documentation about the producer. This is for human consumption.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI
- Examples:
  - "http://cloud.example.com/docs/blobstorage"

#### type

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

#### specversion

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: CloudEvents [`specversion`](https://github.com/cloudevents/spec/blob/master/spec.md#specversion)
  that will be used for events published for this producer, event type
  combination.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string

#### datacontenttype

- Type: `String`
- Description: CloudEevnts [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#datacontenttype)
  attribute. Indicating how the `data` attribute of subscribed events will be
  encoded.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in [RFC 2046](https://tools.ietf.org/html/rfc2046)

#### dataschema

- Type: `URI`
- Description: CloudEevnts [`datacontenttype`](https://github.com/cloudevents/spec/blob/master/spec.md#dataschema)
  attribute. This identifies the canonical storage location of the schema of
  the `data` attribute of subscribed events.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI

#### dataschematype

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: If using `dataschemacontent` for inline schema storage, the
  `dataschematype` indicates the type of schema represented there.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Examples:
  - "application/json"
  -

#### dataschemacontent

- Type: `String`
- Description: An inline representation of the schema of the `data` attribute
  encoding mechanism. This is an alternative to using the `dataschema`
  attribute.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string containing a schema compatible with
    the `datacontenttype`.
  - If `dataschama` is present, this field MUST NOT be present.

#### protocols

- Type: `List` of `String`
- Description: This field describes the different values that may be passed
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

#### extensions

- Type: `Map` of `String` to `String`
- Description: Associative map of CloudEvents [Extension Context Attributes](https://github.com/cloudevents/spec/blob/master/spec.md#extension-context-attributes)
  that are used for this event `type`. Keys MUST be confirm to the extension
  context attributes naming rules and value are the type of the extension
  attribute, conforming to the CloudEvents [type system](https://github.com/cloudevents/spec/blob/master/spec.md#type-system).
- Constraints:
  - OPTIONAL

#### subscriptionendpoint

- Type: `URI-reference`
- Description: URI indicating where CloudSubscriptions `subscribe` API calls
  MUST be sent to.
- Constraints:
  - REQUIRED

#### subscriptionconfig

- Type: `Map` of `String` to `String`
- Description: A map indicating supported options for the `config` parameter
  for the CloudSubscriptions subscribe() API call. Keys are the name of keys
  in the allowed config map, the values indicate the type of that parameter,
  confirming to the CloudEvents [type system](https://github.com/cloudevents/spec/blob/master/spec.md#type-system).
  TODO: Needs resolution with CloudSubscriptions API
- Constraints:
  - OPTIONAL
- Examples:

#### authscope

- Type: `String`
- Description: Authorization scope required for creating subscriptions.
  The actual meaning of this field is determined on a per-producer basis.
- Constraints:
  - OPTIONAL
- Example:
  - "storage.read"

### Query API

The query operation MUST be supported by compliant Event Producers. It is used
by the Event Subscriber to get information about the events that the Event
Producer produces. To retrieve the list of events produced by an Event Producer,
the following data is to be provided. The query operation takes a key/value map
(`config`) of type `string` to `string`.

Each query parameter that is provided is an `and` operation. Each parameter
MUST support exact match and prefix matching operations. Prefix matching uses
the syntax of `prefix*` where the `*` character represents the end of the
prefix.

#### Query API keys

##### producer

- Type: `String`
- Description: The name of the [producer](#producer) that is offering this
  events.
- Constraints:
  - OPTIONAL
  - If present, must be non-empty
- Examples:
  - "Github"
  - "Awesome Cloud Storage"
  - "Awesome Cloud\*"

##### type

- Type: `String`
- Description: The specific [type](#type) to query for.
- Constraints:
  - OPTIONAL
  - If present, must be non-empty
- Examples:
  - "com.github.pull.create"
  - "com.github.pull.\*"

##### expandsources

- Type: boolean
- Description: If true, the `source` response attribute will be expanded
  for each producer entity that matches the query.
- Constraints:
  - OPTIONAL
  - If absent, a default value of `false` is used.

## Example Usage

For these examples, we'll assume discovery is being served from an events broker
that has access to events from multiple producer systems. Specifically, we will
show these producers, each with the specified event types.

* "Git Source Control"
 * `git.pullrequest`
 * `git.commit`
 * `git.newissue`
* "Cloud Storage"
 * `cloud.storage.object.create`
 * `cloud.storage.object.delete`
 * `cloud.storage.object.update`
* "Cloud RDBMS"
 * `cloud.rdbms.row.insert`
 * `cloud.rdbms.row.delete`
 * `cloud.rdbms.table.create`
 * `cloud.rdbms.table.drop`

### Query for available producers.

In order to configure a subscription, a user wants to browse available events
on this broker. We start by listing the available producers, an empty discovery
query and `expandsources` set to `false`

`/discovery?expandsources=false`

The returned data would correspond to this table. Most attributes are omitted
in the table below.

| producer           | type                          |
| ------------------ | ----------------------------- |
| Git Source Control | `git.pullrequest`             |
| Git Source Control | `git.commit`                  |
| Git Source Control | `git.newissue`                |
| Cloud Storage      | `cloud.storage.object.create` |
| Cloud Storage      | `cloud.storage.object.delete` |
| Cloud Storage      | `cloud.storage.object.update` |
| Cloud RDBMS        | `cloud.rdbms.row.insert`      |
| Cloud RDBMS        | `cloud.rdbms.row.delete`      |
| Cloud RDBMS        | `cloud.rdbms.table.create`    |
| Cloud RDBMS        | `cloud.rdbms.table.drop`      |
| Cloud RDBMS        | `cloud.rdbms.database.create` |

### More detail, based on producer

From here, the user knows they want events from the "Cloud RDBMS" producer, so
a second query is issued.

`/discovery?producer="Cloud RDBMS"`

The returned data now only shows event types from the selected producer and
could be further refined based on the type.

| producer           | type                          |
| ------------------ | ----------------------------- |
| Cloud RDBMS        | `cloud.rdbms.row.insert`      |
| Cloud RDBMS        | `cloud.rdbms.row.delete`      |
| Cloud RDBMS        | `cloud.rdbms.table.create`    |
| Cloud RDBMS        | `cloud.rdbms.table.drop`      |
| Cloud RDBMS        | `cloud.rdbms.database.create` |

## Protocol Bindings

The discovery API can be implemented over different API systems. We provide
API schema definitions for implementing this API using OpenAPI and gRPC as
illustrative examples.

### OpenAPI

**TODO**

## Privacy and Security

The CloudDiscovery API does not place restrictions on producers choice of an
authentication and authorization mechanism. Discovery output MAY be different
for different principals.
