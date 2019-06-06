# CloudEvents - Version 0.3-wip

=======

## Abstract

CloudEvents is a vendor-neutral specification for defining the format of event
data.

## Status of this document

This document is a working draft.

## Table of Contents

- [Overview](#overview)
- [Notations and Terminology](#notations-and-terminology)
- [Type System](#type-system)
- [Context Attributes](#context-attributes)
- [Data Attribute](#data-attribute)
- [Size Limits](#size-limits)
- [Privacy & Security](#privacy-and-security)
- [Example](#example)

## Overview

Events are everywhere. However, event producers tend to describe events
differently.

The lack of a common way of describing events means developers are constantly
re-learning how to consume events. This also limits the potential for libraries,
tooling and infrastructure to aide the delivery of event data across
environments, like SDKs, event routers or tracing systems. The portability and
productivity that can be achieved from event data is hindered overall.

CloudEvents is a specification for describing event data in common formats to
provide interoperability across services, platforms and systems.

Event Formats specify how to serialize a CloudEvent with certain encoding
formats. Compliant CloudEvents implementations that support those encodings MUST
adhere to the encoding rules specified in the respective event format. All
implementations MUST support the [JSON format](json-format.md).

For more information on the history, development and design rationale behind the
specification, see the [CloudEvents Primer](primer.md) document.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

For clarity, when a feature is marked as "OPTIONAL" this means that it is
OPTIONAL for both the sender and receiver of a message to support that feature.
In other words, a sender can choose to include that feature in a message if it
wants, and a receiver can choose to support that feature if it wants. A receiver
that does not support that feature will then silently ignore that part of the
message. The sender needs to be prepared for the situation where a receiver
ignores that feature.

### Attribute Naming Convention

The CloudEvents specifications define mappings to various protocols and
encodings, and the accompanying CloudEvents SDK targets various runtimes and
languages. Some of these treat metadata elements as case-sensitive while others
do not, and a single CloudEvent might be routed via multiple hops that involve a
mix of protocols, encodings, and runtimes. Therefore, this specification limits
the available character set of all attributes such that case-sensitivity issues
or clashes with the permissible character set for identifiers in common
languages are prevented.

CloudEvents attribute names MUST consist of lower-case letters ('a' to 'z') or
digits ('0' to '9') from the ASCII character set, and MUST begin with a
lower-case letter. Attribute names SHOULD be descriptive and terse, and SHOULD
NOT exceed 20 characters in length.

### Terminology

This specification defines the following terms:

#### Occurrence

An "occurrence" is the capture of a statement of fact during the operation of a
software system. This might occur because of a signal raised by the system or a
signal being observed by the system, because of a state change, because of a
timer elapsing, or any other noteworthy activity. For example, a device might go
into an alert state because the battery is low, or a virtual machine is about to
perform a scheduled reboot.

#### Event

An "event" is a data record expressing an occurrence and its context. Events are
routed from an event producer (the source) to interested event consumers. The
routing can be performed based on information contained in the event, but an
event will not identify a specific routing destination. Events will contain two
types of information: the [Data](#data) representing the Occurrence and
[Context](#context) metadata providing contextual information about the
Occurrence.

#### Producer

The "producer" is a specific instance, process or device that creates the data
structure describing the CloudEvent.

#### Source

The "source" is the context in which the occurrence happened. In a distributed
system it might consist of multiple [Producers](#producer). If a source is not
aware of CloudEvents, an external producer creates the CloudEvent on behalf of
the source.

#### Consumer

A "consumer" receives the event and acts upon it. It uses the context and data
to execute some logic, which might lead to the occurrence of new events.

#### Intermediary

An "intermediary" receives a message containing an event for the purpose of
forwarding it to the next receiver, which might be another intermediary or a
[Consumer](#consumer). A typical task for an intermediary is to route the event
to receivers based on the information in the [Context](#context).

#### Context

Context metadata will be encapsulated in the
[Context Attributes](#context-attributes). Tools and application code can use
this information to identify the relationship of Events to aspects of the system
or to other Events.

#### Data

Domain-specific information about the occurrence (i.e. the payload). This might
include information about the occurrence, details about the data that was
changed, or more. See the [Data Attribute](#data-attribute) section for more
information.

#### Message

Events are transported from a source to a destination via messages.

#### Protocol

Messages can be delivered through various industry standard protocol (e.g. HTTP,
AMQP, MQTT, SMTP), open-source protocols (e.g. Kafka, NATS), or platform/vendor
specific protocols (AWS Kinesis, Azure Event Grid).

## Type System

The following abstract data types are available for use in attributes.

- `Integer` - A whole number in the range -2,147,483,648 to +2,147,483,647
  inclusive. This is the range of a signed, 32-bit, twos-complement encoding.
  Event formats do not have to use this encoding, but they MUST only use
  `Integer` values in this range.
- `String` - Sequence of printable Unicode characters.
- `Binary` - Sequence of bytes.
- `Map` - `String`-indexed dictionary of `Any`-typed values.
- `Any` - Either a `Binary`, `Integer`, `Map` or `String`.
- `URI-reference` - String expression conforming to `URI-reference` as defined
  in [RFC 3986 §4.1](https://tools.ietf.org/html/rfc3986#section-4.1).
- `Timestamp` - String expression as defined in
  [RFC 3339](https://tools.ietf.org/html/rfc3339).

The `Any` type is a variant type that can take the shape of either a `Binary`,
`Integer`, `Map` or `String`. The type system is intentionally abstract, and
therefore it is left to implementations how to represent the variant type.

## Context Attributes

Every CloudEvent conforming to this specification MUST include context
attributes designated as REQUIRED and MAY include one or more OPTIONAL context
attributes.

These attributes, while descriptive of the event, are designed such that they
can be serialized independent of the event data. This allows for them to be
inspected at the destination without having to deserialize the event data.

The choice of serialization mechanism will determine how the context attributes
and the event data will be materialized. For example, in the case of a JSON
serialization, the context attributes and the event data might both appear
within the same JSON object.

### REQUIRED Attributes

The following attributes are REQUIRED to be present in all CloudEvents:

#### id

- Type: `String`
- Description: Identifies the event.
  Producers MUST ensure that `source` + `id` is unique for each
  distinct event.  If a duplicate event is re-sent (e.g. due to a
  network error) it MAY have the same `id`.  Consumers MAY assume that
  Events with identical `source` and `id` are duplicates.
- Examples:
  - An event counter maintained by the producer
  - A UUID
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST be unique within the scope of the producer

#### source

- Type: `URI-reference`
- Description: Identifies the context in which an event
  happened. Often this will include information such as the type of
  the event source, the organization publishing the event or the
  process that produced the event. The exact syntax and semantics
  behind the data encoded in the URI is defined by the event producer.

  Producers MUST ensure that `source` + `id` is unique for each
  distinct event.

  An application MAY assign a unique `source` to each distinct
  producer, which makes it easy to produce unique IDs since no other
  producer will have the same source. The application MAY use UUIDs,
  URNs, DNS authorities or an application-specific scheme to create
  unique `source` identifiers.

  A source MAY include more than one producer. In that case the
  producers MUST collaborate to ensure that `source` + `id` is unique
  for each distinct event.

- Constraints:
  - REQUIRED
- Examples
  - Internet-wide unique URI with a DNS authority.
    - https://github.com/cloudevents
    - mailto:cncf-wg-serverless@lists.cncf.io
  - Universally-unique URN with a UUID:
    -  urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66
  - Application-specific identifiers
    - /cloudevents/spec/pull/123
    - /sensors/tn-1234567/alerts
    - 1-555-123-4567

#### specversion

- Type: `String`
- Description: The version of the CloudEvents specification which the event
  uses. This enables the interpretation of the context. Compliant event
  producers MUST use a value of `0.3-wip` when referring to this version of the
  specification.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string

#### type

- Type: `String`
- Description: Type of occurrence which has happened. Often this attribute is
  used for routing, observability, policy enforcement, etc. The format of this
  is producer defined and might include information such as the version of the
  `type` - see
  [Versioning of Attributes in the Primer](primer.md#versioning-of-attributes)
  for more information.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - SHOULD be prefixed with a reverse-DNS name. The prefixed domain dictates the
    organization which defines the semantics of this event type.
- Examples
  - com.github.pull.create
  - com.example.object.delete.v2

### OPTIONAL Attributes

The following attribtues are OPTIONAL to appear in CloudEvents. See the
[Notational Conventions](#notational-conventions) section for more information
on the definition of OPTIONAL.

#### datacontentencoding

- Type: `String` per
  [RFC 2045 Section 6.1](https://tools.ietf.org/html/rfc2045#section-6.1)
- Description: Describes the content encoding for the `data` attribute for when
  the `data` field MUST be encoded as a string, like with structured transport
  binding modes using the JSON event format, but the `datacontenttype` indicates
  a non-string media type. When the `data` field's effective data type is not
  `String`, this attribute MUST NOT be set and MUST be ignored when set.

  The "Base64" value for the Base64 encoding as defined in
  [RFC 2045 Section 6.8](https://tools.ietf.org/html/rfc2045#section-6.8) MUST
  be supported. When set, the event-format-encoded value of the `data` attribute
  is a base64 string, but the effective data type of the `data` attribute
  towards the application is the base64-decoded binary array.

  All other RFC2045 schemes are undefined for CloudEvents.

- Constraints:
  - The attribute MUST be set if the `data` attribute contains string-encoded
    binary data. Otherwise the attribute MUST NOT be set.
  - If present, MUST adhere to
    [RFC 2045 Section 6.1](https://tools.ietf.org/html/rfc2045#section-6.1)

#### datacontenttype

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: Content type of the `data` attribute value. This attribute
  enables the `data` attribute to carry any type of content, whereby format and
  encoding might differ from that of the chosen event format. For example, an
  event rendered using the [JSON envelope](./json-format.md#3-envelope) format
  might carry an XML payload in its `data` attribute, and the consumer is
  informed by this attribute being set to "application/xml". The rules for how
  the `data` attribute content is rendered for different `datacontenttype`
  values are defined in the event format specifications; for example, the JSON
  event format defines the relationship in
  [section 3.1](./json-format.md#31-special-handling-of-the-data-attribute).

  When this attribute is omitted, the `data` attribute simply follows the event
  format's encoding rules. For the JSON event format, the `data` attribute value
  can therefore be a JSON object, array, or value.

  For the binary mode of some of the CloudEvents transport bindings, where the
  `data` content is immediately mapped into the payload of the transport frame,
  this field is directly mapped to the respective transport or application
  protocol's content-type metadata property. Normative rules for the binary mode
  and the content-type metadata mapping can be found in the respective transport
  mapping specifications.

- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)
- For Media Type examples see
  [IANA Media Types](http://www.iana.org/assignments/media-types/media-types.xhtml)

#### schemaurl

- Type: `URI-reference`
- Description: A link to the schema that the `data` attribute adheres to.
  Incompatible changes to the schema SHOULD be reflected by a different URL. See
  [Versioning of Attributes in the Primer](primer.md#versioning-of-attributes)
  for more information.
- Constraints:
  - OPTIONAL

#### subject

- Type: `String`
- Description: This describes the subject of the event in the context of the
  event producer (identified by `source`). In publish-subscribe scenarios, a
  subscriber will typically subscribe to events emitted by a `source`, but the
  `source` identifier alone might not be sufficient as a qualifier for any
  specific event if the `source` context has internal sub-structure.

  Identifying the subject of the event in context metadata (opposed to only in
  the `data` payload) is particularly helpful in generic subscription filtering
  scenarios where middleware is unable to interpret the `data` content. In the
  above example, the subscriber might only be interested in blobs with names
  ending with '.jpg' or '.jpeg' and the `subject` attribute allows for
  constructing a simple and efficient string-suffix filter for that subset of
  events.

- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string
- Example:
  - A subscriber might register interest for when new blobs are created inside a
    blob-storage container. In this case, the event `source` identifies the
    subscription scope (storage container), the `type` identifies the "blob
    created" event, and the `id` uniquely identifies the event instance to
    distinguish separate occurrences of a same-named blob having been created;
    the name of the newly created blob is carried in `subject`:
    - `source`: https://example.com/storage/tenant/container
    - `subject`: mynewfile.jpg

#### time

- Type: `Timestamp`
- Description: Timestamp of when the event happened.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 3339](https://tools.ietf.org/html/rfc3339)

### Extension Context Attributes

CloudEvents producers MAY include additional context attributes in the event
that might be used in ancillary actions related to the processing of the event.
See
[CloudEvent Attributes Extensions](primer.md#cloudevent-attribute-extensions)
for additional information concerning the use and definition of extensions.

This specification places no restriction on the type or semantics of the
extension attributes. Each definition of an extensions SHOULD fully define all
aspects of the attribute - e.g. its name, semantic meaning and possible values
or even to indicate that it places no restrictions on its values. New extension
definitions SHOULD use a name that is descriptive enough to reduce the chances
of name collisions with other extensions. In particular, extension authors
SHOULD check the [documented extensions](documented-extensions.md) document for
the set of known extensions - not just for possible name conflicts but for
extensions that might be of interest.

Each specification that defines how to serialize a CloudEvent will define how
extension attributes will appear.

Here is an example that illustrates the need for additional attributes. In many
IoT and enterprise use cases, an event could be used in a serverless application
that performs actions across multiple types of events. To support such use
cases, the event producer will need to add additional identity attributes to the
"context attributes" which the event consumers can use to correlate this event
with the other events. If such identity attributes happen to be part of the
event "data", the event producer SHOULD also add the identity attributes to the
"context attributes" so that event consumers can easily access this information
without needing to decode and examine the event data. Such identity attributes
can also be used to help intermediate gateways determine how to route the
events.

## Data Attribute

As defined by the term [Data](#data), CloudEvents MAY include domain-specific
information about the occurrence. When present, this information will be
encapsulated within the `data` attribute.

### data

- Type: `Any`
- Description: The event payload. The payload depends on the `type` and the
  `schemaurl`. It is encoded into a media format which is specified by the
  `datacontenttype` attribute (e.g. application/json).
- Constraints:
  - OPTIONAL

# Size Limits

In many scenarios, CloudEvents will be forwarded through one or more
generic intermediaries, each of which might impose limits on the size of
forwarded events. CloudEvents might also be routed to consumers, like
embedded devices, that are storage or memory-constrained and therefore
would struggle with large singular events.

The "size" of an event is its wire-size, and includes every bit that is
transmitted on the wire for the event: transport frame-metadata, event
metadata, and event data, based on the chosen event format and the chosen
protocol binding.

If an application configuration requires for events to be routed across
different transports or for events to be re-encoded, the least efficient
transport and encoding used by the application SHOULD be considered for
compliance with these size constraints:

- Intermediaries MUST forward events of a size of 64 KByte or less.
- Consumers SHOULD accept events of a size of at least 64 KByte.

In effect, these rules will allow producers to publish events up to 64KB in
size safely. Safely here means that it is generally reasonable to expect the
event to be accepted and retransmitted by all intermediaries. It is in any
particular consumer's control, whether it wants to accept or reject events
of that size due to local considerations.

Generally, CloudEvents publishers SHOULD keep events compact by avoiding to
embed large data items into event payloads and rather use the event payload
to link to such data items. From an access control perspective, this approach
also allows for a broader distribution of events, because accessing
event-related details through resolving links allows for differentiated access
control and selective disclosure, rather than having sensitive details embedded
in the event directly.

# Privacy and Security

Interoperability is the primary driver behind this specification, enabling such
behavior requires some information to be made available _in the clear_ resulting
in the potential for information leakage.

Consider the following to prevent inadvertent leakage especially when leveraging
3rd party platforms and communication networks:

- Context Attributes

  Sensitive information SHOULD NOT be carried or represented in context
  attributes.

  CloudEvent producers, consumers, and intermediaries MAY introspect and log
  context attributes.

- Data

  Domain specific [data](#data) SHOULD be encrypted to restrict visibility to
  trusted parties. The mechanism employed for such encryption is an agreement
  between producers and consumers and thus outside the scope of this
  specification.

- Transport Bindings

  Transport level security SHOULD be employed to ensure the trusted and secure
  exchange of CloudEvents.

# Example

The following example shows a CloudEvent serialized as JSON:

```JSON
{
    "specversion" : "0.3-wip",
    "type" : "com.github.pull.create",
    "source" : "https://github.com/cloudevents/spec/pull",
    "subject" : "123",
    "id" : "A234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "comexampleextension1" : "value",
    "comexampleextension2" : {
        "othervalue": 5
    },
    "datacontenttype" : "text/xml",
    "data" : "<much wow=\"xml\"/>"
}
```
