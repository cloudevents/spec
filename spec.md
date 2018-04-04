# CloudEvents - Version 0.1

CloudEvents is a vendor-neutral specification for defining the format
of event data.

## Table of Contents
- [Overview](#overview)
- [Design Goals](#design-goals)
- [Notations and Terminology](#notations-and-terminology)
- [Context Attributes](#context-attributes)
- [Use-Cases](about/use-cases.md)
- [Additional Topics & Questions](#additional-topics--questions)
- [References](about/references.md)

## Overview
Events are everywhere. However, event publishers tend to describe events
differently.

The lack of a common way of describing events means developers are constantly
re-learning how to receive events. This also limits the potential for libraries,
tooling and infrastructure to aide the delivery of event data across
environments, like SDKs, event routers or tracing systems. The portability
and productivity that can be achieved from event data is hindered overall.

Enter CloudEvents, a specification for describing event data in a common way.
CloudEvents seeks to ease event declaration and delivery across services,
platforms and beyond.

# Design Goals

CloudEvents are typically used in a distributed system to allow for services to
be loosely coupled during development, deployed independently, and later
can be connected to create new applications.

The goal of the CloudEvents specification is to define interoperability of event
systems that allow services to produce or consume events, where the producer and
consumer can be developed and deployed independently.  A producer can generate
events before a consumer is listening, and a consumer can express an interest in
an event or class of events that is not yet being produced.

To this end, the specification will include common metadata attributes of an
event that facilitate interoperability, where the event does not contain any
details about the consumer or transport that might be use to send the event.

## Non-Goals
The following will not be part of the specification:
* Function build and invocation process
* Language-specific runtime APIs
* Selecting a single identity/access control system

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to
be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

### Terminology

This specification defines the following terms:

#### Occurrence
An "occurrence" is the capture of a statement of fact during the operation of
a software system. This might occur because of a signal raised by the system or
a signal being observed by the system, because of a state change, because of
a timer elapsing, or any other noteworthy activity. For example, a device might
go into an alert state because the battery is low, or a virtual machine is
about to perform a scheduled reboot.

#### Event
Data representing an occurrence, a change in state, that something happened
(or did not happen).  Events include context and data.  Each occurrence MAY be
uniquely identified with data in the event. Events ought not to be confused
with messages which are used to transport or distribute data without assumptions
regarding its semantic. Events are considered to be facts that have no given
destination. Events are used to notify other systems that something has
happened.

#### Context
A set of consistent metadata attributes included with the event about the
occurrence that tools and developers can rely upon to better handle the event.
These attributes describe the event and the structure of its data, include
information about the originating system, and more.

#### Message
Events are transported from a source to a destination via messages.

#### Data
Domain-specific information about the occurrence (i.e. the payload). This
might include information about the occurrence, details about the data
that was changed, or more.

#### Protocol
Messages can be delivered through various industry standard protocol (e.g. HTTP,
AMQP, MQTT, SMTP), open-source protocols (e.g. Kafka, NATS), or
platform/vendor specific protocols (AWS Kinesis, Azure Event Grid).


## Context Attributes
Every event conforming to this specification MUST include a context.

Context is designed such that it can be delivered separately from the event
data (e.g. in protocol headers or protocol specific attributes). This allows
the context to be inspected at the destination without having to deserialize
the event data. The context might also need to be serialized with the event
data for some use cases (e.g. a JSON implementation might use one JSON object
that contains both context and data).

### namespace
* Type: String
* Description: Identifier that uniquely identifies the organization publishing
  the event.
* Constraints:
  * REQUIRED
  * MUST be a non-empty string
* Examples:
  * kafka.apache.org
  * com.microsoft.azure

### event-type
* Type: String
* Description: Type of the event `data`. Producers can specify the format of
  this, depending on their service. This enables the interpretation of `data`,
  and can be used for routing, policy and more.
* Constraints:
  * REQUIRED
  * MUST be a non-empty string
* Examples:
  * customer.created

### event-type-version
* Type: String
* Description: The version of the `event-type`. This enables the interpretation
  of `data` by eventual consumers, requires the consumer to be knowledgeable
  about the producer.
* Constraints:
  * OPTIONAL
  * If present, MUST be a non-empty string

### cloud-events-version
* Type: String
* Description: The version of the CloudEvents specification which the event
  uses. This enables the interpretation of the context.
* Constraints:
  * REQUIRED
  * MUST be a non-empty string

### source
* Type: Object
* Description: This describes the software instance that emits the event at
  runtime (i.e. the producer). It contains sub-properties (listed below)
* Constraints:
  * REQUIRED
  * MUST contain at least one non-empty sub-property.

### source-type
* Type: String
* Description: Type of the event source. Providers define list of event
  sources.
* Constraints:
  * REQUIRED
  * MUST be a non-empty string
* Examples:
  * s3

### source-id
* Type: String
* Description: ID of the event source.
* Constraints:
  * REQUIRED
  * MUST be a non-empty string
* Examples:
  * my.s3.bucket

### event-id
* Type: String
* Description: ID of the event. The semantics of this string are explicitly
  undefined to ease the implementation of producers. Enables deduplication.
* Examples:
  * A database commit ID
* Constraints:
  * REQUIRED
  * MUST be a non-empty string
  * MUST be unique within the scope of the producer

### event-time
* Type: Timestamp per [RFC 3339](https://tools.ietf.org/html/rfc3339)
* Description: Timestamp of when the event happened.
* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 3339](https://tools.ietf.org/html/rfc3339)

### schema-url
* Type: URI per [RFC 3986](https://tools.ietf.org/html/rfc3986)
* Description: A link to the schema that the `data` attribute adheres to.
* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 3986](https://tools.ietf.org/html/rfc3986)

### content-type
* Type: String per [RFC 2046](https://tools.ietf.org/html/rfc2046)
* Description: Describe the data encoding format
* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)
* For Media Type examples see [IANA Media Types](http://www.iana.org/assignments/media-types/media-types.xhtml)

### extensions
* Type: Map <String, Object>
* Description: This is for additional metadata and this does not have a
  mandated structure. This enables a place for custom fields a producer or
  middleware might want to include and provides a place to test metadata before
  adding them to the CloudEvents specification. TBD - Determine a shorter
  prefix for this (e.g. OpenAPI uses “x-”)
* Constraints:
  * OPTIONAL
  * If present, MUST contain at least one entry
* Examples:
  * authorization data

## Event Data
An event includes context and data. This "Event Data" section is the
sibling to the above "Context Attributes". This is where the original
event data info goes.

In this section, each serialization/encoding scheme of a Cloud Event should 
specify how to retrieve interoperability related information from the data
or where those information appears in the event message.

## Additional Topics & Questions

* Context Attribute Names - We decided not to spend too much time on property
  names during our working sessions. Instead the focus has been on semantics.
  We still need to revise property names.
* Event Consumer API - What does this look like?
* Routing, Batching, Failure Semantics - What do these look like?
* Authentication - Will this be included within the event?
  * Initial authN (e.g. auth at the point of event occurrence)
  * Transport level authN (e.g. auth on the event)
* What is the best way to handle encoding for event payloads?
* How to specify an action that is desired to happen based on an event
  notification (also does this violate our interpretation of events)?
* Micro batch considerations – For various streaming and asynchronous
  implementations the client might push one event at a time, but the function
  might want to process multiple events per invocation and obtain higher
  efficiency. There needs to be a mechanism to trigger a function with an
  array of events. An example implementation can be to indicate in the event
  type that it's a list type and pass a “records” list object where each
  record holds its own headers, body or attributes.
* Event Routing – Once the event structure, protocol, and API are well defined
  it becomes trivial to route from one type to another, or even route internal
  events to external clouds. It can be accomplished by simply writing a
  serverless function which listens on the source event, opens a connection to
  the destination protocol and maps every incoming event (received through
  event API) to an event message over the destination protocol.

