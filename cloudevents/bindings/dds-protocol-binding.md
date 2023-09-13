# Data Distribution Service Protocol Binding for CloudEvents - Version 1.0.0-wip

## Abstract

The [Data Distribution Service(DDS)][dds] Protocol Binding for CloudEvents defines how events are
mapped to [DDS messages][dds-message-format].

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to Kafka](#12-relation-to-kafka)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

- 2.1. [data](#21-data)

3. [DDS Message Mapping](#3-dds-message-mapping)

- 3.1. [Key Mapping](#31-key-mapping)
- 3.2. [Binary Content Mode](#32-binary-content-mode)
- 3.3. [Structured Content Mode](#33-structured-content-mode)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be used in the DDS
protocol as [DDS messages][dds-message-format].

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to DDS

This specification does not prescribe rules constraining transfer or settlement
of event messages with DDS; it solely defines how CloudEvents are expressed in
the DDS protocol as [DDS messages][dds-message-format].

The DDS protocol is a middleware standard for efficient and real-time data exchange
in distributed systems. It enables communication using a publish-subscribe model and
operates in conjunction with the Real-Time Publish Subscribe (RTPS) wire protocol.
DDS ensures reliable data delivery, supporting Quality of Service (QoS) parameters
like reliability, lifespan and partitioning. DDS is used for  mission-critical
applications in industries such as aerospace, healthcare, and industrial automation.

This binding specification defines how attributes and data of a CloudEvent is
mapped to a DDS message format.

Generally, the user SHOULD configure the key of the DDS message in a way that
makes most sense for their specific use case.

### 1.3. Content Modes

The CloudEvents specification defines three content modes for transferring
events: _structured_, _binary_ and _batch_. The DDS protocol binding does not
currently support the batch content mode. Every compliant implementation SHOULD
support both structured and binary modes.

The specification defines three content modes for transferring events:
_structured_, _binary_ and _batch_. The DDS protocol binding does not
currently support the _batch_ content mode.

In the _structured_ content mode, event metadata attributes and event data are
placed into the DDS message value section using an [event format](#14-event-formats).

In the _binary_ content mode, the value of the event `data` MUST be placed into
the DDS message's value section as-is, with the `content-type` header value
declaring its media type; all other event attributes MUST be mapped to the DDS
message's [header section][dds-message-header].

### 1.4. Event Formats

Event formats, used with the _structured_ content mode, define how an event is
expressed in a particular data format. All implementations of this specification
that support the _structured_ content mode MUST support the [JSON event
format][json-format].

### 1.5. Security

This specification does not introduce any new security features for DDS, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][ce] event
attributes.

### 2.1. data

`data` is assumed to contain opaque application data that is encoded as declared
by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into DDS as defined in this
specification, core DDS provides data available as a sequence of bytes.

For instance, if the declared `datacontenttype` is
`application/json;charset=utf-8`, the expectation is that the `data` value is
made available as [UTF-8][rfc3629] encoded JSON text.

## 3. DDS Message Mapping

With DDS, the content mode is chosen by the sender of the event. Usage patterns that
might require (or allow)  solicitation of events using a
particular content mode might be defined by an application, but are not defined
here.

The receiver of the event can distinguish between content modes by
inspecting the `content-type` [Header][dds-message-header] of the DDS
message. If the header is present and its value is prefixed with the CloudEvents
media type `application/cloudevents`, indicating the use of a known
[event format](#14-event-formats), the receiver uses _structured_ mode,
otherwise it defaults to _binary_ mode.

If a receiver finds a CloudEvents media type as per the above rule, but with an
event format that it cannot handle, for instance `application/cloudevents+dds`,
it MAY still treat the event as binary and forward it to another party as-is.

When the `content-type` header value is not prefixed with the CloudEvents media
type, knowing when the message ought to be parsed as a CloudEvent can be a
challenge. While this specification can not mandate that senders do not include
any of the CloudEvents headers when the message is not a CloudEvent, it would be
reasonable for a receiver to assume that if the message has all of the mandatory
CloudEvents attributes as headers then it's probably a CloudEvent. However, as
with all CloudEvent messages, if it does not adhere to all of the normative
language of this specification then it is not a valid CloudEvent.

### 3.1. Keys

The 'key' of the DDS message MAY be populated by 
which might map the key directly from one of the CloudEvent's attributes, but
might also use information from the application environment, from the
CloudEvent's data or other sources.

### 3.2. Binary Content Mode

The _binary_ content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.2.1. Content Type

For the _binary_ mode, the header `content-type` property MUST be mapped
directly to the CloudEvents `datacontenttype` attribute.

#### 3.2.2. Event Data Encoding

The [`data`](#21-data) byte-sequence MUST be used as the value of the DDS
message.

In binary mode, the DDS representation of a CloudEvent with no `data` is a
DDS message with no value.

#### 3.2.3. Metadata Headers

All [CloudEvents][ce] attributes and
[CloudEvent Attributes Extensions](../primer.md#cloudevent-extension-attributes)
with exception of `data` MUST be individually mapped to and from the Header
fields in the DDS message. Both header keys and header values MUST be encoded
as UTF-8 strings.

##### 3.2.3.1 Property Names

CloudEvent attributes are prefixed with `ce_` for use in the
[message-headers][dds-message-header] section.

Examples:

    * `time` maps to `ce_time`
    * `id` maps to `ce_id`
    * `specversion` maps to `ce_specversion`

##### 3.2.4.2 Property Values

The value for each DDS header is constructed from the respective header's
DDS representation, compliant with the [DDS message format][dds-message-format] specification.

#### 3.2.5 Example

This example shows the _binary_ mode mapping of an event into the DDS message.
All other CloudEvents attributes are mapped to DDS Header fields with prefix
`ce_`.

Mind that `ce_` here does refer to the event `data` content carried in the
payload.

```text
------------------ Message -------------------

Topic Name: mytopic

------------------- key ----------------------

Key: mykey

------------------ headers -------------------

ce_specversion: "1.0"
ce_type: "com.example.someevent"
ce_source: "/mycontext/subcontext"
ce_id: "1234-1234-1234"
ce_time: "2018-04-05T03:56:24Z"
content-type: application/binary
       .... further attributes ...

------------------- value --------------------

            ... application data encode in some binary format ...

-----------------------------------------------
```

### 3.3. Structured Content Mode

The _structured_ content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple protocols.

#### 3.3.1. DDS Content-Type

If present, the DDS message header property `content-type` MUST be set to the
media type of an [event format](#14-event-formats).

Example for the [JSON format][json-format]:

```text
content-type: application/cloudevents+json; charset=UTF-8
```

#### 3.3.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes, and
`data`, are represented.

The event metadata and data are then rendered in accordance with the
[event format](#14-event-formats) specification and the resulting data becomes
the DDS application [data](#21-data) section.

In structured mode, the DDS representation of a CloudEvent with no `data`
is a DDS message which still has a data section (containing the attributes
of the CloudEvent).

#### 3.3.3. Metadata Headers

Implementations MAY include the same DDS headers as defined for the
[binary mode](#32-binary-content-mode).

#### 3.3.4 Example

This example shows a JSON event format encoded event:

```text
------------------ Message -------------------

Topic Name: mytopic

------------------- key ----------------------

Key: mykey

------------------ headers -------------------

content-type: application/cloudevents+json

------------------- value --------------------

{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
    "source" : "/mycontext/subcontext",
    "id" : "1234-1234-1234",
    "time" : "2018-04-05T03:56:24Z",
    "datacontenttype" : "application/json",

    ... further attributes omitted ...

    "data" : {
        ... application data encoded in JSON ...
    }
}

-----------------------------------------------
```

## 4. References

- [DDS][dds]
- [DDS-Message-Format][dds-message-format] The DDS format message
- [RFC2046][rfc2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][rfc3629] UTF-8, a transformation format of ISO 10646
- [RFC7159][rfc7159] The JavaScript Object Notation (JSON) Data Interchange
  Format

[ce]: ../spec.md
[json-format]: ../formats/json-format.md
[json-value]: https://tools.ietf.org/html/rfc7159#section-3
[rfc2046]: https://tools.ietf.org/html/rfc2046
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3629]: https://tools.ietf.org/html/rfc3629
[rfc7159]: https://tools.ietf.org/html/rfc7159
