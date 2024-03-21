# CloudEvents - Version 1.0.3-wip

## Abstract

CloudEvents is a vendor-neutral specification for defining the format of event
data.

## Table of Contents

- [Overview](#overview)
- [Notations and Terminology](#notations-and-terminology)
- [Context Attributes](#context-attributes)
- [Event Data](#event-data)
- [Size Limits](#size-limits)
- [Privacy & Security](#privacy-and-security)
- [Example](#example)

## Overview

Events are everywhere. However, event producers tend to describe events
differently.

The lack of a common way of describing events means developers are constantly
re-learning how to consume events. This also limits the potential for libraries,
tooling and infrastructure to aid the delivery of event data across
environments, like SDKs, event routers or tracing systems. The portability and
productivity that can be achieved from event data is hindered overall.

CloudEvents is a specification for describing event data in common formats to
provide interoperability across services, platforms and systems.

Event Formats specify how to serialize a CloudEvent with certain encoding
formats. Compliant CloudEvents implementations that support those encodings MUST
adhere to the encoding rules specified in the respective event format. All
implementations MUST support the [JSON format](formats/json-format.md).

For more information on the history, development and design rationale behind the
specification, see the [CloudEvents Primer](primer.md) document.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

For clarity, when a feature is marked as "OPTIONAL" this means that it is
OPTIONAL for both the [Producer](#producer) and [Consumer](#consumer) of a
message to support that feature. In other words, a producer can choose to
include that feature in a message if it wants, and a consumer can choose to
support that feature if it wants. A consumer that does not support that feature 
is free to take any action it wishes, including no action or generating an
error, as long as doing so does not violate other requirements defined by this
specification. However, the RECOMMENDED action is to ignore it. The producer
SHOULD be prepared for the situation where a consumer ignores that feature. An
[Intermediary](#intermediary) SHOULD forward OPTIONAL attributes.

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
types of information: the [Event Data](#event-data) representing the Occurrence
and [Context](#context) metadata providing contextual information about the
Occurrence. A single occurrence MAY result in more than one event.

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
changed, or more. See the [Event Data](#event-data) section for more
information.

#### Event Format

An Event Format specifies how to serialize a CloudEvent as a sequence of bytes.
Stand-alone event formats, such as the [JSON format](formats/json-format.md),
specify serialization independent of any protocol or storage medium. Protocol
Bindings MAY define formats that are dependent on the protocol.

Each Event Format MUST define a structured-mode representation, and MAY define
a batch-mode representation.

#### Message

Events are transported from a source to a destination via messages.

A "structured-mode message" is one where the entire event (attributes and data)
are encoded in the message body, according to a specific event format.

A "binary-mode message" is one where the event data is stored in the message
body, and event attributes are stored as part of message metadata.

Often, binary mode is used when the producer of the CloudEvent wishes to add
the CloudEvent's metadata to an existing event without impacting the message's
body. In most cases a CloudEvent encoded as a binary-mode message will not
break an existing receiver's processing of the event because the message's
metadata typically allows for extension attributes. In other words, a binary
formatted CloudEvent would work for both a CloudEvents enabled receiver as well
as one that is unaware of CloudEvents.

A "batch-mode message" is one where multiple (zero or more) events are
encoded in a single message body, according to a specific event format. Not
all event formats or protocol bindings support batch-mode messages.
The CloudEvents within a batch are largely independent from one another: there
is no restriction that they have the same source, producer, content type etc.
The only restriction is that all CloudEvents within the same batch MUST have
the same value for the `specversion` attribute.

#### Protocol

Messages can be delivered through various industry standard protocol (e.g. HTTP,
AMQP, MQTT, SMTP), open-source protocols (e.g. Kafka, NATS), or platform/vendor
specific protocols (AWS Kinesis, Azure Event Grid).

#### Protocol Binding

A protocol binding describes how events are sent and received over a given
protocol.

Protocol bindings MAY choose to use an [Event Format](#event-format) to map an
event directly to the transport envelope body, or MAY provide additional
formatting and structure to the envelope. For example, a wrapper around a
structured-mode message might be used, or several messages could be batched
together into a transport envelope body.

## Context Attributes

Every CloudEvent conforming to this specification MUST include context
attributes designated as REQUIRED, MAY include one or more OPTIONAL context
attributes and MAY include one or more
[extension context attributes](#extension-context-attributes). Each
context attribute MUST only appear at most once in a CloudEvent. The context
attributes defined within this specification (as opposed to extension context
attributes) are known as "core context attributes".

Context attributes, while descriptive of the event, are designed such that they
can be serialized independent of the event data. This allows for them to be
inspected at the destination without having to deserialize the event data.

### Naming Conventions

The CloudEvents specifications define mappings to various protocols and
encodings, and the accompanying CloudEvents SDK targets various runtimes and
languages. Some of these treat metadata elements as case-sensitive while others
do not, and a single CloudEvent might be routed via multiple hops that involve a
mix of protocols, encodings, and runtimes. Therefore, this specification limits
the available character set of all attributes such that case-sensitivity issues
or clashes with the permissible character set for identifiers in common
languages are prevented.

In order to maximize the likelihood of interoperability and portability across
transport protocols and messaging formats, CloudEvents attribute names MUST
consist of lower-case letters ('a' to 'z') or digits ('0' to '9') from the
ASCII character set. Attribute names SHOULD be descriptive and terse and SHOULD
NOT exceed 20 characters in length.

CloudEvent attributes MUST NOT have the name `data`; this name is reserved as it
is used in some event formats.

### Type System

The following abstract data types are available for use in attributes. Each of
these types MAY be represented differently by different event formats and in
protocol metadata fields. This specification defines a canonical
string-encoding for each type that MUST be supported by all implementations.

- `Boolean` - a boolean value of "true" or "false".
  - String encoding: a case-sensitive value of `true` or `false`.
- `Integer` - A whole number in the range -2,147,483,648 to +2,147,483,647
  inclusive. This is the range of a signed, 32-bit, twos-complement encoding.
  Event formats do not have to use this encoding, but they MUST only use
  `Integer` values in this range.
  - String encoding: Integer component of the JSON Number per
    [RFC 7159, Section 6](https://tools.ietf.org/html/rfc7159#section-6)
     optionally prefixed with a minus sign.
- `String` - Sequence of allowable Unicode characters. The following characters
  are disallowed:
  - the "control characters" in the ranges U+0000-U+001F and U+007F-U+009F (both
    ranges inclusive), since most have no agreed-on meaning, and some, such as
    U+000A (newline), are not usable in contexts such as HTTP headers.
  - code points
    [identified as noncharacters by Unicode](http://www.unicode.org/faq/private_use.html#noncharacters).
  - code points identifying Surrogates, U+D800-U+DBFF and U+DC00-U+DFFF, both
    ranges inclusive, unless used properly in pairs. Thus (in JSON notation)
    "\uDEAD" is invalid because it is an unpaired surrogate, while
    "\uD800\uDEAD" would be legal.
- `Binary` - Sequence of bytes.
  - String encoding: Base64 encoding per
    [RFC4648](https://tools.ietf.org/html/rfc4648).
- `URI` - Absolute uniform resource identifier.
  - String encoding: `Absolute URI` as defined in
    [RFC 3986 Section 4.3](https://tools.ietf.org/html/rfc3986#section-4.3).
- `URI-reference` - Uniform resource identifier reference.
  - String encoding: `URI-reference` as defined in
    [RFC 3986 Section 4.1](https://tools.ietf.org/html/rfc3986#section-4.1).
- `Timestamp` - Date and time expression using the Gregorian Calendar.
  - String encoding: [RFC 3339](https://tools.ietf.org/html/rfc3339).

All context attribute values MUST be of one of the types listed above.
Attribute values MAY be presented as native types or canonical strings.

A strongly-typed programming model that represents a CloudEvent or any extension
MUST be able to convert from and to the canonical string-encoding to the
runtime/language native type that best corresponds to the abstract type.

For example, the `time` attribute might be represented by the language's native
_datetime_ type in a given implementation, but it MUST be settable providing an
RFC3339 string, and it MUST be convertible to an RFC3339 string when mapped to a
header of an HTTP message.

A CloudEvents protocol binding or event format implementation MUST likewise be
able to convert from and to the canonical string-encoding to the corresponding
data type in the encoding or in protocol metadata fields.

An attribute value of type `Timestamp` might indeed be routed as a string
through multiple hops and only materialize as a native runtime/language type at
the producer and ultimate consumer. The `Timestamp` might also be routed as a
native protocol type and might be mapped to/from the respective
language/runtime types at the producer and consumer ends, and never materialize
as a string.

The choice of serialization mechanism will determine how the context attributes
and the event data will be serialized. For example, in the case of a JSON
serialization, the context attributes and the event data might both appear
within the same JSON object.

Attributes are often used for identification purposes. While any particular
attribute definition might include constraints on its value, in general this
specification does not mandate how those identification attributes are
constructed. For example, it might be a singleton (such as a name), or
it could be a composite made up of multiple identifying sub-values.

### REQUIRED Attributes

The following attributes are REQUIRED to be present in all CloudEvents:

#### id

- Type: `String`
- Description: Identifies the event. Producers MUST ensure that `source` + `id`
  is unique for each distinct event. If a duplicate event is re-sent (e.g. due
  to a network error) it MAY have the same `id`. Consumers MAY assume that
  Events with identical `source` and `id` are duplicates.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST be unique within the scope of the producer
- Examples:
  - An event counter maintained by the producer
  - A UUID

#### source

- Type: `URI-reference`
- Description: Identifies the context in which an event happened. Often this
  will include information such as the type of the event source, the
  organization publishing the event or the process that produced the event. The
  exact syntax and semantics behind the data encoded in the URI is defined by
  the event producer.

  Producers MUST ensure that `source` + `id` is unique for each distinct event.

  An application MAY assign a unique `source` to each distinct producer, which
  makes it easy to produce unique IDs since no other producer will have the same
  source. The application MAY use UUIDs, URNs, DNS authorities or an
  application-specific scheme to create unique `source` identifiers.

  A source MAY include more than one producer. In that case the producers MUST
  collaborate to ensure that `source` + `id` is unique for each distinct event.

- Constraints:
  - REQUIRED
  - MUST be a non-empty URI-reference
  - An absolute URI is RECOMMENDED
- Examples
  - Internet-wide unique URI with a DNS authority.
    - `https://github.com/cloudevents`
    - `mailto:cncf-wg-serverless@lists.cncf.io`
  - Universally-unique URN with a UUID:
    - `urn:uuid:6e8bc430-9c3a-11d9-9669-0800200c9a66`
  - Application-specific identifiers
    - `/cloudevents/spec/pull/123`
    - `/sensors/tn-1234567/alerts`
    - `1-555-123-4567`

#### specversion

- Type: `String`
- Description: The version of the CloudEvents specification which the event
  uses. This enables the interpretation of the context. Compliant event
  producers MUST use a value of `1.0` when referring to this version of the
  specification.

  Currently, this attribute will only have the 'major' and 'minor' version
  numbers included in it. This allows for 'patch' changes to the specification
  to be made without changing this property's value in the serialization.
  Note: for 'release candidate' releases a suffix might be used for testing
  purposes.

- Constraints:
  - REQUIRED
  - MUST be a non-empty string

#### type

- Type: `String`
- Description: This attribute contains a value describing the type of event
  related to the originating occurrence. Often this attribute is used for
  routing, observability, policy enforcement, etc. The format of this is
  producer defined and might include information such as the version of the
  `type` - see
  [Versioning of CloudEvents in the Primer](primer.md#versioning-of-cloudevents)
  for more information.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - SHOULD be prefixed with a reverse-DNS name. The prefixed domain dictates the
    organization which defines the semantics of this event type.
- Examples
  - com.github.pull_request.opened
  - com.example.object.deleted.v2

### OPTIONAL Attributes

The following attributes are OPTIONAL to appear in CloudEvents. See the
[Notational Conventions](#notational-conventions) section for more information
on the definition of OPTIONAL.

#### datacontenttype

- Type: `String` per [RFC 2046](https://tools.ietf.org/html/rfc2046)
- Description: Content type of `data` value. This attribute enables `data` to
  carry any type of content, whereby format and encoding might differ from that
  of the chosen event format. For example, an event rendered using the
  [JSON envelope](formats/json-format.md#3-envelope) format might carry an XML
  payload in `data`, and the consumer is informed by this attribute being set to
  "application/xml". The rules for how `data` content is rendered for different
  `datacontenttype` values are defined in the event format specifications; for
  example, the JSON event format defines the relationship in
  [section 3.1](formats/json-format.md#31-handling-of-data).

  For some binary mode protocol bindings, this field is directly mapped to the
  respective protocol's content-type metadata property. Normative rules for the
  binary mode and the content-type metadata mapping can be found in the
  respective protocol.

  In some event formats the `datacontenttype` attribute MAY be omitted. For
  example, if a JSON format event has no `datacontenttype` attribute, then it is
  implied that the `data` is a JSON value conforming to the "application/json"
  media type. In other words: a JSON-format event with no `datacontenttype` is
  exactly equivalent to one with `datacontenttype="application/json"`.

  When translating an event message with no `datacontenttype` attribute to a
  different format or protocol binding, the target `datacontenttype` SHOULD be
  set explicitly to the implied `datacontenttype` of the source.

  The `datacontenttype` attribute MAY appear even if there is no `data` value
  present.

  As specified in [RFC 2045](https://tools.ietf.org/html/rfc2045), the media
  type part of the content type MUST be treated in a case-insensitive manner
  by consumers, along with the attribute names in parameters. For example,
  a `datacontenttype` of `text/plain; charset=utf-8` MUST be treated in the
  same way as `TEXT/Plain; CharSet=utf-8`.

- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 2046](https://tools.ietf.org/html/rfc2046)
- For Media Type examples see
  [IANA Media Types](http://www.iana.org/assignments/media-types/media-types.xhtml)

#### dataschema

- Type: `URI`
- Description: Identifies the schema that `data` adheres to. Incompatible
  changes to the schema SHOULD be reflected by a different URI. See
  [Versioning of CloudEvents in the Primer](primer.md#versioning-of-cloudevents)
  for more information.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI

#### subject

- Type: `String`
- Description: This identifies the subject of the event in the context of the
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
- Examples:
  - A subscriber might register interest for when new blobs are created inside a
    blob-storage container. In this case, the event `source` identifies the
    subscription scope (storage container), the `type` identifies the "blob
    created" event, and the `id` uniquely identifies the event instance to
    distinguish separate occurrences of a same-named blob having been created;
    the name of the newly created blob is carried in `subject`:
      - `source`: `https://example.com/storage/tenant/container`
      - `subject`: `mynewfile.jpg`
  - A subscriber might register interest for when new updates are made to a client
    in an eCommerce system. In this case, the event `source` identifies the
    subscription scope (CRM part of an eCommerce system), the `type` identifies
    the "client updated" event, and the `id` uniquely identifies the event
    instance to distinguish separate occurrences of a same client being
    updated multiple times; the `subject` uniquely identifies the client within
    the scope of the `source` by including a "partner id" and "client id"
    (which is unique within the scope of the "partner id") separated by a colon:
      - `source`: `https://example.com/eCommerce/crm`
      - `subject`: `partnerid/5/clientid/100`

#### time

- Type: `Timestamp`
- Description: Timestamp of when the occurrence happened. If the time of the
  occurrence cannot be determined then this attribute MAY be set to some other
  time (such as the current time) by the CloudEvents producer, however all
  producers for the same `source` MUST be consistent in this respect. In other
  words, either they all use the actual time of the occurrence or they all use
  the same algorithm to determine the value used.
- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in
    [RFC 3339](https://tools.ietf.org/html/rfc3339)

### Extension Context Attributes

A CloudEvent MAY include any number of additional context attributes with
distinct names, known as "extension attributes". Extension attributes MUST
follow the same [naming convention](#naming-conventions) and use the
same [type system](#type-system) as standard attributes. Extension attributes
have no defined meaning in this specification, they allow external systems to
attach metadata to an event, much like HTTP custom headers.

Extension attributes are always serialized according to binding rules like
standard attributes. However this specification does not prevent an extension
from copying event attribute values to other parts of a message, in order to
interact with non-CloudEvents systems that also process the message. Extension
specifications that do this SHOULD specify how receivers are to interpret
messages if the copied values differ from the cloud-event serialized values.

#### Defining Extensions

See
[CloudEvent Attributes Extensions](primer.md#cloudevent-extension-attributes)
for additional information concerning the use and definition of extensions.

The definition of an extension SHOULD fully define all aspects of the
attribute - e.g. its name, type, semantic meaning and possible values. New
extension definitions SHOULD use a name that is descriptive enough to reduce the
chances of name collisions with other extensions. In particular, extension
authors SHOULD check the [documented extensions](extensions/README.md)
document for the set of known extensions - not just for possible name conflicts
but for extensions that might be of interest.

Many protocols support the ability for senders to include additional metadata,
for example as HTTP headers. While a CloudEvents receiver is not mandated to
process and pass them along, it is RECOMMENDED that they do so via some
mechanism that makes it clear they are non-CloudEvents metadata.

Here is an example that illustrates the need for additional attributes. In many
IoT and enterprise use cases, an event could be used in a serverless application
that performs actions across multiple types of events. To support such use
cases, the event producer will need to add additional identity attributes to the
"context attributes" which the event consumers can use to correlate this event
with the other events. If such identity attributes happen to be part of the
event "data", the event producer would also add the identity attributes to the
"context attributes" so that event consumers can easily access this information
without needing to decode and examine the event data. Such identity attributes
can also be used to help intermediate gateways determine how to route the
events.

## Event Data

As defined by the term [Data](#data), CloudEvents MAY include domain-specific
information about the occurrence. When present, this information will be
encapsulated within `data`.

- Description: The event payload. This specification does not place any
  restriction on the type of this information. It is encoded into a media format
  which is specified by the `datacontenttype` attribute (e.g. application/json),
  and adheres to the `dataschema` format when those respective attributes are
  present.

- Constraints:
  - OPTIONAL

## Size Limits

In many scenarios, CloudEvents will be forwarded through one or more generic
intermediaries, each of which might impose limits on the size of forwarded
events. CloudEvents might also be routed to consumers, like embedded devices,
that are storage or memory-constrained and therefore would struggle with large
singular events.

The "size" of an event is its wire-size and includes every bit that is
transmitted on the wire for the event: protocol frame-metadata, event metadata,
and event data, based on the chosen event format and the chosen protocol
binding.

If an application configuration requires for events to be routed across
different protocols or for events to be re-encoded, the least efficient
protocol and encoding used by the application SHOULD be considered for
compliance with these size constraints:

- Intermediaries MUST forward events of a size of 64 KiB or less.
- Consumers SHOULD accept events of a size of at least 64 KiB.

In effect, these rules will allow producers to publish events up to 64 KiB in size
safely. Safely here means that it is generally reasonable to expect the event to
be accepted and retransmitted by all intermediaries. It is in any particular
consumer's control, whether it wants to accept or reject events of that size due
to local considerations.

Generally, CloudEvents publishers SHOULD keep events compact by avoiding
embedding large data items into event payloads and rather use the event payload
to link to such data items. From an access control perspective, this approach
also allows for a broader distribution of events, because accessing
event-related details through resolving links allows for differentiated access
control and selective disclosure, rather than having sensitive details embedded
in the event directly.

## Privacy and Security

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

  Domain specific [event data](#event-data) SHOULD be encrypted to restrict
  visibility to trusted parties. The mechanism employed for such encryption is
  an agreement between producers and consumers and thus outside the scope of
  this specification.

- Protocol Bindings

  Protocol level security SHOULD be employed to ensure the trusted and secure
  exchange of CloudEvents.

## Example

The following example shows a CloudEvent serialized as JSON:

```JSON
{
    "specversion" : "1.0",
    "type" : "com.github.pull_request.opened",
    "source" : "https://github.com/cloudevents/spec/pull",
    "subject" : "123",
    "id" : "A234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "comexampleextension1" : "value",
    "comexampleothervalue" : 5,
    "datacontenttype" : "text/xml",
    "data" : "<much wow=\"xml\"/>"
}
```
