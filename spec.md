# CloudEvents - Version 0.1

## Abstract

CloudEvents is a vendor-neutral specification for defining the format
of event data.

## Status of this document

This document is a working draft.

## Table of Contents
- [Overview](#overview)
- [Notations and Terminology](#notations-and-terminology)
- [Type System](#type-system)
- [Context Attributes](#context-attributes)
- [Data Attribute](#data-attribute)
- [Example](#example)

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

Event Formats specify how to serialize a CloudEvent with certain encoding
formats. Compliant CloudEvents implementations that support those encodings
MUST adhere to the encoding rules specified in the respective event format.
All implementations MUST support the [JSON format](json-format.md).

For more information on the history, development and design rationale
behind the specification, see the [CloudEvents Primer](primer.md) document.

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
a specific routing destination. Events will contain two pieces of information:
the [Data](#data) representing the Occurrence and extra [Context](#context)
metadata providing additional information about the Occurrence.

#### Context
As described in the Event definition, an Event contains two parts, the
[data](#data) representing the occurrence and additional metadata
that provides other circumstantial information about the occurrence
(e.g. information about the originating system). This additional metadata will
be encapsulated in the [Context Attributes](#context-attributes).
Tools and application code can use this information to identify the
relationship of Events to aspects of the system or to other Events.

#### Data
Domain-specific information about the occurrence (i.e. the payload). This
might include information about the occurrence, details about the data
that was changed, or more. See the [Data Attribute](#data-attribute) section
for more information.

#### Message
Events are transported from a source to a destination via messages.

#### Protocol
Messages can be delivered through various industry standard protocol (e.g. HTTP,
AMQP, MQTT, SMTP), open-source protocols (e.g. Kafka, NATS), or
platform/vendor specific protocols (AWS Kinesis, Azure Event Grid).

## Type System

The following abstract data types are available for use in attributes.

- `Integer` - A 32-bit whole number.
- `String` - Sequence of printable Unicode characters.
- `Binary` - Sequence of bytes.
- `Map` - `String`-indexed dictionary of `Object`-typed values.
- `Object` - Either a `String`, or a `Binary`, or a `Map`, or an `Integer`.
- `URI` - String expression conforming to `URI-reference`
  as defined in
  [RFC 3986 §4.1](https://tools.ietf.org/html/rfc3986#section-4.1).
- `Timestamp` - String expression as defined in
  [RFC 3339](https://tools.ietf.org/html/rfc3339).

This specification does not define numeric or logical types.

The `Object` type is a variant type that can take the shape of either a
`String` or a `Binary` or a `Map`. The type system is intentionally
abstract, and therefore it is left to implementations how to represent the
variant type.

## Context Attributes
Every CloudEvent conforming to this specification MUST include one or more
of the following context attributes.

These attributes, while descriptive of the event, are designed such that they
can be serialized independent of the event data. This allows for them to be
inspected at the destination without having to deserialize the event data.

The choice of serialization mechanism will determine how the context
attributes and the event data will be materialized. For example, in the case
of a JSON serialization, the context attributes and the event data might
both appear within the same JSON object.

### Extension Attributes
CloudEvents producers MAY include additional context attributes in the event
that might be used in ancillary actions related to the processing of the event.
See [CloudEvent Attributes Extensions](primer.md#cloudevent-attribute-extensions)
for additional information concerning the use and definition of extensions.

This specification places no restriction on the type or semantics of the
extension attributes. Each definition of an extensions SHOULD fully
define all aspects of the attribute - e.g. its name, semantic meaning
and possible values or even to indicate that it places no restrictions on
its values.  New extension definitions SHOULD use a name that is
descriptive enough to reduce the chances of name collisions with other
extensions. In particular, extension authors SHOULD check the
[documented extensions](documented-extensions.md) document for the
set of known extensions - not just for possible name conflicts but
for extensions that might be of interest.

Each specification that defines how to serialize a CloudEvent will
define how extension attributes will appear.

Here is an example that illustrates the need for additional attributes.
In many IoT and enterprise use cases, an event could be used in
a serverless application that performs actions across multiple types of events.
To support such use cases, the event producer will need to add additional
identity attributes to the "context attributes" which the event consumers can
use to correlate this event with the other events. If such identity attributes
happen to be part of the event "data", the event producer SHOULD also add
the identity attributes to the "context attributes" so that
event consumers can easily access this information without needing to decode
and examine the event data. Such identity attributes can also be used to
help intermediate gateways determine how to route the events.

### eventType
* Type: `String`
* Description: Type of occurrence which has happened. Often this
  attribute is used for routing, observability, policy enforcement, etc.
* Constraints:
   * REQUIRED
   * MUST be a non-empty string
   * SHOULD be prefixed with a reverse-DNS name. The prefixed domain dictates
            the organization which defines the semantics of this event type.
* Examples
   * com.github.pull.create

### cloudEventsVersion
* Type: `String`
* Description: The version of the CloudEvents specification which the event
  uses. This enables the interpretation of the context.
* Constraints:
  * REQUIRED
  * MUST be a non-empty string

### source
* Type: `URI`
* Description: This describes the event producer. Often this will include
  information such as the type of the event source, the organization
  publishing the event, and some unique identifiers. The exact syntax and
  semantics behind the data encoded in the URI is event producer defined.
* Constraints:
  * REQUIRED

### eventID
* Type: `String`
* Description: ID of the event. The semantics of this string are explicitly
  undefined to ease the implementation of producers. Enables deduplication.
* Examples:
  * A database commit ID
* Constraints:
  * REQUIRED
  * MUST be a non-empty string
  * MUST be unique within the scope of the producer

### eventTime
* Type: `Timestamp`
* Description: Timestamp of when the event happened.
* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 3339](https://tools.ietf.org/html/rfc3339)

### schemaURL
* Type: `URI`
* Description: A link to the schema that the `data` attribute adheres to.
Incompatible changes to the schema SHOULD be reflected by a different URL.
* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 3986](https://tools.ietf.org/html/rfc3986)

### contentType
* Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
* Description: Content type of the `data` attribute value. This attribute
  enables the `data` attribute to carry any type of content, whereby format
  and encoding might differ from that of the chosen event format. For example,
  an event rendered using the [JSON envelope](./json-format.md#3-envelope)
  format might carry an XML payload in its `data` attribute, and the
  consumer is informed by this attribute being set to "application/xml". The
  rules for how the `data` attribute content is rendered for different
  `contentType` values are defined in the event format specifications; for
  example, the JSON event format defines the relationship in
  [section 3.1](./json-format.md#31-special-handling-of-the-data-attribute).

  When this attribute is omitted, the "data" attribute simply follows the
  event format's encoding rules. For the JSON event format, the "data"
  attribute value can therefore be a JSON object, array, or value.

  For the binary mode of some of the CloudEvents transport bindings,
  where the "data" content is immediately mapped into the payload of the
  transport frame, this field is directly mapped to the respective transport
  or application protocol's content-type metadata property. Normative rules
  for the binary mode and the content-type metadata mapping can be found
  in the respective transport mapping specifications.

* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)
* For Media Type examples see [IANA Media Types](http://www.iana.org/assignments/media-types/media-types.xhtml)

## Data Attribute

As defined by the term [Data](#data), CloudEvents MAY include domain-specific
information about the occurrence. When present, this information will be
encapsulated within the `data` attribute.

### data
* Type: `Object`
* Description: The event payload. The payload depends on the eventType and
  the schemaURL. It is encoded into a media format
  which is specified by the contentType attribute (e.g. application/json).
* Constraints:
  * OPTIONAL

# Example

The following example shows a CloudEvent serialized as JSON:

``` JSON
{
    "cloudEventsVersion" : "0.1",
    "eventType" : "com.example.someevent",
    "source" : "/mycontext",
    "eventID" : "A234-1234-1234",
    "eventTime" : "2018-04-05T17:31:00Z",
    "comExampleExtension1" : "value",
    "comExampleExtension2" : {
        "otherValue": 5
    },
    "contentType" : "text/xml",
    "data" : "<much wow=\"xml\"/>"
}
```
