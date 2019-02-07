# CloudEvents - Version 0.2

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
- [Minimum Supported Event Size](#minimum-supported-event-size)
- [Example](#example)

## Overview
Events are everywhere. However, event producers tend to describe events
differently.

The lack of a common way of describing events means developers are constantly
re-learning how to consume events. This also limits the potential for libraries,
tooling and infrastructure to aide the delivery of event data across
environments, like SDKs, event routers or tracing systems. The portability
and productivity that can be achieved from event data is hindered overall.

CloudEvents is a specification for describing event data in common formats
to provide interoperability across services, platforms and systems.

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

The CloudEvents specifications define mappings to various protocols and
encodings, and the accompanying CloudEvents SDK targets various runtimes and
languages. Some of these treat metadata elements as case-sensitive while others
do not, and a single CloudEvent might be routed via multiple hops that involve
a mix of protocols, encodings, and runtimes. Therefore, this specification
limits the available character set of all attributes such that
case-sensitivity issues or clashes with the permissible character set for
identifiers in common languages are prevented.

CloudEvents attribute names MUST consist of lower-case letters ('a' to 'z')
or digits ('0' to '9') from the ASCII character set, and MUST begin with a
lower-case letter. Attribute names SHOULD be descriptive and terse, and SHOULD
NOT exceed 20 characters in length.

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
are routed from an event producer (the source) to interested event consumers.
The routing can be performed based on information contained in the event, but
an event will not identify a specific routing destination. Events will contain
two types of information: the [Data](#data) representing the Occurrence and
[Context](#context) metadata providing contextual information about the
Occurrence.

#### Context
Context metadata will
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
- `Map` - `String`-indexed dictionary of `Any`-typed values.
- `Any` - Either a `String`, or a `Binary`, or a `Map`, or an `Integer`.
- `URI-reference` - String expression conforming to `URI-reference`
  as defined in
  [RFC 3986 §4.1](https://tools.ietf.org/html/rfc3986#section-4.1).
- `Timestamp` - String expression as defined in
  [RFC 3339](https://tools.ietf.org/html/rfc3339).

This specification does not define numeric or logical types.

The `Any` type is a variant type that can take the shape of either a
`String` or a `Binary` or a `Map`. The type system is intentionally
abstract, and therefore it is left to implementations how to represent the
variant type.

## Context Attributes
Every CloudEvent conforming to this specification MUST include context
attributes designated as REQUIRED and MAY include one or more OPTIONAL context
attributes.

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
See
[CloudEvent Attributes Extensions](primer.md#cloudevent-attribute-extensions)
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

### type
* Type: `String`
* Description: Type of occurrence which has happened. Often this
  attribute is used for routing, observability, policy enforcement, etc.
  The format of this is producer defined and might include information such
  as the version of the `eventtype` - see
  [Versioning of Attributes in the Primer](primer.md#versioning-of-attributes)
  for more information.
* Constraints:
   * REQUIRED
   * MUST be a non-empty string
   * SHOULD be prefixed with a reverse-DNS name. The prefixed domain dictates
            the organization which defines the semantics of this event type.
* Examples
   * com.github.pull.create
   * com.example.object.delete.v2

### specversion
* Type: `String`
* Description: The version of the CloudEvents specification which the event
  uses. This enables the interpretation of the context. Compliant event 
  producers MUST use a value of `0.2` when referring to this version of
  the specification.
* Constraints:
  * REQUIRED
  * MUST be a non-empty string

### source
* Type: `URI-reference`
* Description: This describes the event producer. Often this will include
  information such as the type of the event source, the organization
  publishing the event, the process that produced the event, and some unique
  identifiers. The exact syntax and semantics behind the data encoded in the URI
  is event producer defined.
* Constraints:
  * REQUIRED
* Examples
    * https://github.com/cloudevents/spec/pull/123
    * /cloudevents/spec/pull/123
    * urn:event:from:myapi/resourse/123
    * mailto:cncf-wg-serverless@lists.cncf.io

### id
* Type: `String`
* Description: ID of the event. The semantics of this string are explicitly
  undefined to ease the implementation of producers. Enables deduplication.
* Examples:
  * A database commit ID
* Constraints:
  * REQUIRED
  * MUST be a non-empty string
  * MUST be unique within the scope of the producer

### time
* Type: `Timestamp`
* Description: Timestamp of when the event happened.
* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 3339](https://tools.ietf.org/html/rfc3339)

### schemaurl
* Type: `URI`
* Description: A link to the schema that the `data` attribute adheres to.
  Incompatible changes to the schema SHOULD be reflected by a different URL.
  See
  [Versioning of Attributes in the Primer](primer.md#versioning-of-attributes)
  for more information.
* Constraints:
  * OPTIONAL
  * If present, MUST adhere to the format specified in
    [RFC 3986](https://tools.ietf.org/html/rfc3986)

### contenttype
* Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
* Description: Content type of the `data` attribute value. This attribute
  enables the `data` attribute to carry any type of content, whereby format
  and encoding might differ from that of the chosen event format. For example,
  an event rendered using the [JSON envelope](./json-format.md#3-envelope)
  format might carry an XML payload in its `data` attribute, and the
  consumer is informed by this attribute being set to "application/xml". The
  rules for how the `data` attribute content is rendered for different
  `contenttype` values are defined in the event format specifications; for
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
* Type: `Any`
* Description: The event payload. The payload depends on the `type` and
  the `schemaurl`. It is encoded into a media format
  which is specified by the `contenttype` attribute (e.g. application/json).
* Constraints:
  * OPTIONAL

# Minimum Supported Event Size

In order to increase interoperability, all CloudEvent consumers SHOULD accept
events up to a size of 64KB, measured by serializing the CloudEvent as
[JSON](./json-format.md) (minified, i.e. without white-space).

CloudEvent consumers MAY reject events above this size and MAY reject messages
that are not minified (e.g. contain unnecessary white-space).
It is RECOMMENDED for CloudEvent producers to only create events within this
size, unless they can be sure all consumers support larger sizes.

The same event serialized with a different format will likely result in a
different size. However, to aid interoperability, only the minified
[JSON](./json-format.md) is used to measure the size. As an example, an
[AMQP](./amqp-format.md) message of 70KB MUST be accepted if the contained
event serialized as JSON is below 64KB. However, an [AMQP](./amqp-format.md)
message of 60KB MAY be rejected if the contained event serialized as JSON
exceeds 64KB. Practically, an [AMQP](./amqp-format.md) consumer that wants to
protect theirself from large messages MAY simply choose to reject messagess
after a higher limit (e.g. 256KB) that comfortably fits any valid event size.
However, a middleware that wants to guarantee that the event can be forwarded
in any format SHOULD measure the size of the event independently of the format
it was received in.

# Example

The following example shows a CloudEvent serialized as JSON:

``` JSON
{
    "specversion" : "0.2",
    "type" : "com.github.pull.create",
    "source" : "https://github.com/cloudevents/spec/pull/123",
    "id" : "A234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "comexampleextension1" : "value",
    "comexampleextension2" : {
        "othervalue": 5
    },
    "contenttype" : "text/xml",
    "data" : "<much wow=\"xml\"/>"
}
```
