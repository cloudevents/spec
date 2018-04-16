# CloudEvents - Version 0.1

CloudEvents is a vendor-neutral specification for defining the format
of event data.

## Table of Contents
- [Overview](#overview)
- [Design Goals](#design-goals)
- [Notations and Terminology](#notations-and-terminology)
- [Context Attributes](#context-attributes)
- [Use-Cases](about/use-cases.md)
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

The [Serialization Profile](serialization.md) specifies how to
serialize a CloudEvent into certain encoding formats. Compliant CloudEvents
implementations that support those formats MUST adhere to the encoding rules
specified in the profile for those formats.

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
details about the consumer or transport that might be used to send the event.

## Non-Goals
The following will not be part of the specification:
* Function build and invocation process
* Language-specific runtime APIs
* Selecting a single identity/access control system

## Usage Scenarios

The list below enumerates key usage scenarios and developer perspectives
that have been considered for the development of this specification.
These usage scenarios are by no means exhaustive, and the specification
does not aim to be prescriptive about usage.

These scenarios are not normative; anyone is free to create a system that
mixes these scenarios. These cases establish a common vocabulary of event
producer, consumer, middleware, and framework.

In these scenarios, we keep the roles of event producer and event consumer
distinct. A single application context can always take on multiple roles
concurrently, including being both a producer and a consumer of events.

1) Applications produce events for consumption by other parties, for instance
   for providing consumers with insights about end-user activities, state
   changes or environment observations, or for allowing complementing the
   application's capabilities with event-driven extensions.

   Events are typically produced related to a context or a producer-chosen
   classification. For example, a temperature sensor in a room might be
   context-qualified by mount position, room, floor, and building. A sports
   result might be classified by league and team.

   The producer application could run anywhere, such as on a server or a device.

   The produced events might be rendered and emitted directly by the producer
   or by an intermediary; as example for the latter, consider event data
   transmitted by a device over payload-size-constrained networks such as
   LoRaWAN or ModBus, and where events compliant to this
   specification will be rendered by a network gateway on behalf of the
   producer.

   For example, a weather station transmits a 12-byte, proprietary event
   payload indicating weather conditions once every 5 minutes over LoRaWAN. A
   LoRaWAN gateway is then used to publish the event to an Internet destination
   in the CloudEvents format. The LoRaWAN gateway is the event producer,
   publishing on behalf of the weather station, and will set event metadata
   appropriately to reflect the source of the event.

2) Applications consume events for the purposes such as display, archival,
   analytics, workflow processing, monitoring the condition and/or providing
   transparency into the operation of a business solution and its foundational
   building blocks.

   The consumer application could run anywhere, such as on a server or a
   device.

   A consuming application will typically be interested in:
   - distinguishing events such that the exact same event is not
     processed twice.
   - identifying and selecting the origin context or the
     producer-assigned classification.
   - identifying the temporal order of the events relative to the
     originating context and/or relative to a wall-clock.
   - understanding the context-related detail information carried
     in the event.
   - correlating event instances from multiple event producers and send
     them to the same consumer context.

   In some cases, the consuming application might be interested in:
   - obtaining further details about the event's subject from the
     originating context, like obtaining detail information about a
     changed object that requires privileged access authorization.
     For example, a HR solution might only publish very limited
     information in events for privacy reasons, and any event consumer
     needing more data will have to obtain details related to the event
     from the HR system under their own authorization context.
   - interact with the event's subject at the originating context,
     for instance reading a storage blob after having been informed
     that this blob has just been created.

   Consumer interests motivate requirements for which information
   producers ought to include an event.

3) Middleware routes events from producers to consumers, or onwards
   to other middleware. Applications producing events might delegate
   certain tasks arising from their consumers' requirements to
   middleware:

   - Management of many concurrent interested consumers for one of
     multiple classes or originating contexts of events
   - Processing of filter conditions over a class or originating context
     of events on behalf of consumers.
   - Transcoding, like encoding in MsgPack after decoding from JSON
   - Transformation that changes the event's structure, like mapping from
     a proprietary format to CloudEvents, while preserving the
     identity and semantic integrity of the event.
   - Instant "push-style" delivery to interested consumers.
   - Storing events for eventual delivery, either for pick-up initiated
     by the consumer ("pull"), or initiated by the middleware ("push")
     after a delay.
   - Observing event content or event flow for monitoring or
     diagnostics purposes.

   To satisfy these needs, middleware will be interested in:
   - A metadata discriminator usable for classification or
     contextualization of events so that consumers can express interest
     in one or multiple such classes or contexts.
     For instance, a consumer might be interested in all events related
     to a specific directory inside a file storage account.
   - A metadata discriminator that allows distinguishing the subject of
     a particular event of that class or context.
     For instance, a consumer might want to filter out all events related
     to new files ending with ".jpg" (the file name being the "new file"
     event's subject) for the context describing specific directory
     inside a file storage account that it has registered interest on.
   - An indicator for the encoding of the event and its data.
   - An indicator for the structural layout (schema) for the event and
     its data.

   Whether its events are available for consumption via a middleware is
   a delegation choice of the producer.

   In practice, middleware can take on role of a producer when it changes
   the semantic meaning of an event, a consumer when it takes action based
   on an event, or middleware when it routes events without making semantic
   changes.

4) Frameworks and other abstractions make interactions with event platform
   infrastructure simpler, and often provide common API surface areas
   for multiple event platform infrastructures.

   Frameworks are often used for turning events into an object graph,
   and to dispatch the event to some specific handling user-code or
   user-rule that permits the consuming application to react to
   a particular kind of occurrence in the originating context and
   on a particular subject.

   Frameworks are most interested in semantic metadata commonality
   across the platforms they abstract, so that similar activities can
   be handled uniformly.

   For a sports application, a developer using the framework might be
   interested in all events from today's game (subject) of a team in a
   league (topic of interest), but wanting to handle reports
   of "goal" differently than reports of "substitution".
   For this, the framework will need a suitable metadata discriminator
   that frees it from having to understand the event details.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to
be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

### Attribute Naming Convention

CloudEvents attributes use "camelCasing" for the object member names, to aid
integration with common programming languages.

Attribute names that are composed of multiple words are expressed as compound
words, with the first word starting with a lower-case character and all
subsequent words starting with an upper-case character, and no separator
characters.

Words that are acronyms are written in all-caps, e.g. "ID" and "URL".

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
An "event" is a data record expressing an occurrence and its context. Events
are routed from the emitting source to interested parties for the purpose of
notifying them about the source occurrence. The routing can be performed based
on information contained in the event, but an event will not identify
a specific routing destination.

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

### eventType
* Type: String
* Description: Type of occurrence which has happened. Often this
  property is used for routing, observability, policy enforcement, etc.
* Constraints:
   * REQUIRED
   * MUST be a non-empty string
   * SHOULD be prefixed with a reverse-DNS name. The prefixed domain dictates
            the organization which defines the semantics of this event type.
* Examples
   * com.github.pull.create

### eventTypeVersion
* Type: String
* Description: The version of the `eventType`. This enables the interpretation
  of `data` by eventual consumers, requires the consumer to be knowledgeable
  about the producer.
* Constraints:
  * OPTIONAL
  * If present, MUST be a non-empty string

### cloudEventsVersion
* Type: String
* Description: The version of the CloudEvents specification which the event
  uses. This enables the interpretation of the context.
* Constraints:
  * REQUIRED
  * MUST be a non-empty string

### source
* Type: URI
* Description: This describes the event producer. Often this will include
  information such as the type of the event source, the organization
  publishing the event, and some unique idenfitiers. The exact syntax and
  semantics behind the data encoded in the URI is event producer defined.
* Constraints:
  * REQUIRED

### eventID
* Type: String
* Description: ID of the event. The semantics of this string are explicitly
  undefined to ease the implementation of producers. Enables deduplication.
* Examples:
  * A database commit ID
* Constraints:
  * REQUIRED
  * MUST be a non-empty string
  * MUST be unique within the scope of the producer

### eventTime
* Type: Timestamp per [RFC 3339](https://tools.ietf.org/html/rfc3339)
* Description: Timestamp of when the event happened.
* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 3339](https://tools.ietf.org/html/rfc3339)

### schemaURL
* Type: URI per [RFC 3986](https://tools.ietf.org/html/rfc3986)
* Description: A link to the schema that the `data` attribute adheres to.
* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 3986](https://tools.ietf.org/html/rfc3986)

### contentType
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
  See the [Extensions](extensions.md) document for a list of possible
  properties.
* Constraints:
  * OPTIONAL
  * If present, MUST contain at least one entry
* Examples:
  * authorization data

### data
* Type: Arbitrary payload
* Description: The event payload. The payload depends on the eventType,
  schemaURL and eventTypeVersion, the payload is encoded into a media format
  which is specified by the contentType attribute (e.g. application/json).
* Constraints:
  * OPTIONAL

