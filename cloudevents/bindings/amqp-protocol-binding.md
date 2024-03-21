# AMQP Protocol Binding for CloudEvents - Version 1.0.3-wip

## Abstract

The AMQP Protocol Binding for CloudEvents defines how events are mapped to
OASIS AMQP 1.0 ([OASIS][oasis-amqp-1.0]; ISO/IEC 19464:2014) messages.

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to AMQP](#12-relation-to-amqp)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

3. [AMQP Message Mapping](#3-amqp-message-mapping)

- 3.2. [Binary Content Mode](#31-binary-content-mode)
- 3.1. [Structured Content Mode](#32-structured-content-mode)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be used in
[AMQP][oasis-amqp-1.0] messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to AMQP

This specification does not prescribe rules constraining transfer or settlement
of event messages with AMQP; it solely defines how CloudEvents are expressed as
AMQP 1.0 messages.

AMQP-based messaging and eventing infrastructures often provide higher-level
programming-level abstractions that do not expose all AMQP protocol elements, or
map AMQP protocol elements or names to proprietary constructs. This
specification uses AMQP terminology, and implementers can refer to the
respective infrastructure's AMQP documentation to determine the mapping into a
programming-level abstraction.

This specification assumes use of the default AMQP [message
format][message-format].

### 1.3. Content Modes

The CloudEvents specification defines three content modes for transferring
events: _structured_, _binary_ and _batch_. The AMQP protocol binding does not
currently support the batch content mode. Every compliant implementation SHOULD
support both structured and binary modes.

In the _structured_ content mode, event metadata attributes and event data are
placed into the AMQP message's [application data][data] section using an
event format as defined in the CloudEvents [spec][ce].

In the _binary_ content mode, the value of the event `data` is placed into the
AMQP message's [application data][data] section as-is, with the
`datacontenttype` attribute value declaring its media type mapped to the AMQP
`content-type` message property; all other event attributes are mapped to the
AMQP [application-properties][app-properties] section.

### 1.4. Event Formats

Event formats, used with the _structured_ content mode, define how an event is
expressed in a particular data format. All implementations of this specification
that support the _structured_ content mode MUST support the [JSON event
format][json-format].

### 1.5. Security

This specification does not introduce any new security features for AMQP, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][ce] event
attributes.

One event attribute, `datacontenttype` is handled specially in _binary_ content
mode and mapped onto the AMQP content-type message property. All other
attributes are transferred as metadata without further interpretation.

This mapping is intentionally robust against changes, including the addition and
removal of event attributes, and also accommodates vendor extensions to the
event metadata. Any mention of event attributes other than `datacontenttype`
is exemplary.

## 3. AMQP Message Mapping

The content mode is chosen by the sender of the event, which is either the
requesting or the responding party. Protocol interaction patterns that might
allow solicitation of events using a particular content mode might be defined by
an application, but are not defined here.

The receiver of the event can distinguish between the two modes by inspecting
the `content-type` message property field. If the value is prefixed with the
CloudEvents media type `application/cloudevents` (matched case-insensitively),
indicating the use of a known [event format](#14-event-formats), the receiver
uses _structured_ mode, otherwise it defaults to _binary_ mode.

If a receiver detects the CloudEvents media type, but with an event format that
it cannot handle, for instance `application/cloudevents+avro`, it MAY still
treat the event as binary and forward it to another party as-is.

When the `content-type` message property is not prefixed with the CloudEvents
media type, being able to know when the message ought to be attempted to be
parsed as a CloudEvent can be a challenge. While this specification can not
mandate that senders do not include any of the CloudEvents message properties
when the message is not a CloudEvent, it would be reasonable for a receiver
to assume that if the message has all of the mandatory CloudEvents attributes
as message properties then it's probably a CloudEvent. However, as with all
CloudEvent messages, if it does not adhere to all of the normative language of
this specification then it is not a valid CloudEvent.

### 3.1. Binary Content Mode

The _binary_ content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1. AMQP content-type

For the _binary_ mode, the AMQP `content-type` property field value maps
directly to the CloudEvents `datacontenttype` attribute.

#### 3.1.2. Event Data Encoding

Event data is assumed to contain opaque application data that is
encoded as declared by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as it is transposed into AMQP as defined in this
specification, the assumption is that the event data is made available as a
sequence of bytes. The byte sequence is used as the AMQP
[application-data][data] section.

Example:

If the declared `datacontenttype` is `application/json;charset=utf-8`, the
expectation is that the event data is made available as [UTF-8][rfc3629] encoded
JSON text for use in AMQP.

#### 3.1.3. Metadata Headers

All [CloudEvents][ce] attributes with exception of `datacontenttype` MUST be
individually mapped to and from the AMQP
[application-properties][app-properties] section.

CloudEvents extensions that define their own attributes MAY define a secondary
mapping to AMQP properties for those attributes, also in different message
sections, especially if specific attributes or their names need to align with
AMQP features or with other specifications that have explicit AMQP header
bindings. However, they MUST also include the previously defined primary
mapping.

An extension specification that defines a secondary mapping rule for AMQP, and
any revision of such a specification, MUST also define explicit mapping rules
for all other protocol bindings that are part of the CloudEvents core at the
time of the submission or revision.

##### 3.1.3.1 AMQP Application Property Names

CloudEvent attributes MUST be prefixed with either "cloudEvents_" or
"cloudEvents:" for use in the application-properties section.

The '\_' separator character SHOULD be preferred in the interest of
compatibility with JMS 2.0 clients and JMS message selectors where the ':'
separator is not permitted for property identifiers (see section 3.8.1.1 of
[JMS2.0][JMS20]). Any single message MUST use the same separator for all
CloudEvents attributes, but a single queue MAY contain messages which use
different separators.

CloudEvents AMQP consumers SHOULD understand the "cloudEvents" prefix with both
the '\_' and the ':' separators as permitted within the constraints of the
client model. JMS 2.0 AMQP consumers MUST understand the '\_' separator; they
cannot understand the ':' separator as per the cited JMS constraints.

Examples:

    * `time` maps to `cloudEvents_time`
    * `id` maps to `cloudEvents_id`
    * `specversion` maps to `cloudEvents_specversion`

##### 3.1.3.2 AMQP Application Property Values

The value for each AMQP application property is constructed from the respective
attribute's AMQP type representation.

The CloudEvents type system MUST be mapped to AMQP types as follows, with
additional notes below.

| CloudEvents   | AMQP                        |
| ------------- | --------------------------- |
| Boolean       | [boolean][amqp-boolean]     |
| Integer       | [long][amqp-long]           |
| String        | [string][amqp-string]       |
| Binary        | [binary][amqp-binary]       |
| URI           | [string][amqp-string]       |
| URI-reference | [string][amqp-string]       |
| Timestamp     | [timestamp][amqp-timestamp] |

All attribute values in an AMQP binary message MUST either be represented using
the native AMQP types above or the canonical string form.

An implementation

- MUST be able to interpret both forms on an incoming AMQP message
- MAY further relax the requirements for incoming messages (for example
  accepting numeric types other than AMQP long), but MUST be strict for outgoing
  messages.
- SHOULD use the native AMQP form on outgoing AMQP messages when it is efficient
  to do so, but MAY forward values as canonical strings

#### 3.1.4 Examples

This example shows the _binary_ mode mapping of an event into the [bare
message][message-format] sections of AMQP:

```text
--------------- properties ------------------

to: myqueue
content-type: application/json; charset=utf-8

----------- application-properties -----------

cloudEvents:specversion: 1.0
cloudEvents:type: com.example.someevent
cloudEvents:time: 2018-04-05T03:56:24Z
cloudEvents:id: 1234-1234-1234
cloudEvents:source: /mycontext/subcontext
       .... further attributes ...

------------- application-data ---------------

{
    ... application data ...
}

----------------------------------------------
```

### 3.2. Structured Content Mode

The _structured_ content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple protocols.

#### 3.2.1. AMQP Content-Type

The [AMQP `content-type`][content-type] property field is set to the media type
of an [event format](#14-event-formats).

Example for the [JSON format][json-format]:

```text
content-type: application/cloudevents+json; charset=UTF-8
```

#### 3.2.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes
and `data` are represented.

The event metadata and data is then rendered in accordance with the event format
specification and the resulting data becomes the AMQP application [data][data]
section.

#### 3.2.3. Metadata Headers

Implementations MAY include the same AMQP application-properties as defined for
the [binary mode](#313-metadata-headers).

#### 3.2.4 Examples

This example shows a JSON event format encoded event:

```text
--------------- properties ------------------------------

to: myqueue
content-type: application/cloudevents+json; charset=utf-8

----------- application-properties ----------------------

------------- application-data --------------------------

{
    "specversion" : "1.0",
    "type" : "com.example.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

---------------------------------------------------------
```

## 4. References

- [RFC2046][rfc2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][rfc3629] UTF-8, a transformation format of ISO 10646
- [RFC4627][rfc4627] The application/json Media Type for JavaScript Object
  Notation (JSON)
- [RFC7159][rfc7159] The JavaScript Object Notation (JSON) Data Interchange
  Format
- [OASIS-AMQP-1.0][oasis-amqp-1.0] OASIS Advanced Message Queuing Protocol
  (AMQP) Version 1.0
- [JMS20][JMS20] JSR-343 Java Message Service 2.0

[ce]: ../spec.md
[json-format]: ../formats/json-format.md
[content-type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[json-value]: https://tools.ietf.org/html/rfc7159#section-3
[rfc2046]: https://tools.ietf.org/html/rfc2046
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3629]: https://tools.ietf.org/html/rfc3629
[rfc4627]: https://tools.ietf.org/html/rfc4627
[rfc6839]: https://tools.ietf.org/html/rfc6839#section-3.1
[rfc7159]: https://tools.ietf.org/html/rfc7159
[oasis-amqp-1.0]: http://docs.oasis-open.org/amqp/core/v1.0/amqp-core-overview-v1.0.html
[message-format]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#section-message-format
[data]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-data
[app-properties]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-application-properties
[amqp-boolean]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-boolean
[amqp-long]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-long
[amqp-binary]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-binary
[amqp-string]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-string
[amqp-timestamp]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-timestamp
[jms20]: https://jcp.org/aboutJava/communityprocess/final/jsr343/index.html
