# Data Distribution Service Protocol Binding for CloudEvents - Version 1.0.3-wip

## Abstract

The [Data Distribution Service(DDS)][dds] Protocol Binding for CloudEvents
defines how events are mapped to [DDS messages][dds-message-format].

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to DDS](#12-relation-to-dds)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

- 2.1. [data](#21-data)

3. [DDS Message Mapping](#3-dds-message-mapping)

- 3.1. [Keys](#31-keys)
- 3.2. [Binary Content Mode](#32-binary-content-mode)
- 3.3. [Structured Content Mode](#33-structured-content-mode)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are implemented in the DDS protocol
and transmitted as [DDS messages][dds-message-format].

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to DDS

This specification does not prescribe rules constraining transfer or settlement
of event messages with DDS; it solely defines how CloudEvents are expressed in
the DDS protocol as [DDS messages][dds-message-format].

The DDS protocol is an [Object Management Group (OMG)][omg] middleware standard
for efficient and real-time data exchange in distributed systems.
It enables communication using a publish-subscribe model and
operates in conjunction with the [Real-Time Publish Subscribe (RTPS)][rtps]
wire protocol.
DDS ensures reliable data delivery for latency-sensitive payloads,
supporting Quality of Service (QoS) parameters like reliability, lifespan
and partitioning. DDS is most commonly used for mission-critical applications
in industries such as aerospace, healthcare, and industrial automation.

This binding specification defines how attributes and data of a CloudEvent is
mapped to a DDS message format.

### 1.3. Content Modes

The CloudEvents specification defines three content modes for transferring
events: _structured_, _binary_ and _batch_. 

Every compliant implementation of the CloudEvent specification SHOULD support
both structured and binary modes. The DDS protocol binding supports both these modes.

The DDS protocol binding does not currently support the _batch_ content mode.

In the _structured_ content mode, event metadata attributes and event data are
placed into the DDS message using an [event format](#14-event-formats).

In the _binary_ content mode, the value of the event `data` is placed into
the DDS message's `data` section as-is; all other event attributes are
mapped to the DDS message's event metadata fields.

### 1.4. Event Formats

Event formats define how an event is expressed in a particular data format.
All implementations of this specification that support the _structured_
content mode MUST support the [JSON event format][json-format].

The DDS protocol binding additionally supports the
[DDS event format][dds-message-format].

### 1.5. Security

This specification does not introduce any new security features for DDS, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][ce] event
attributes.

### 2.1. data

`data` is assumed to contain opaque application data that is encoded as declared
by the `datacontenttype` attribute. 

There are two values of `datacontenttype` currently supported:
- `cloudevent/json` for JSON data
- `application/cloudevent+dds` for binary and plain text data types

If the `datacontenttype` attribute is set to `application/cloudevent+dds`, the
`datacontentencoding` attribute defines the encoding of the message body. 

The `content-type` field in the message header MUST be consistent with the
`datacontenttype` attribute.

## 3. DDS Message Mapping

The content type is chosen by the sender of the event. The receiver of the
event can distinguish between content modes by inspecting the `content-type`
header of the DDS message.

If the header is present and its value is `cloudevent/json`, the receiver
decodes the message as JSON data.

If the header is present and its value is `application/cloudevent+dds`, the
receiver decodes the message into the DDS message format, using the
`datacontentencoding` attribute to determine the encoding of the message body.
There are three valid values of the `datacontentencoding` attribute
currently supported:
- `text` for ASCII text
- `binary` for binary data

The `content-type` of the DDS message is REQUIRED to be consistent with the
`datacontenttype` attribute.

If a receiver finds a CloudEvents type as per the above rule, but with a
`datacontentencoding` that it cannot handle, it MAY treat the event as binary
and forward it to another party as-is.

When the `content-type` header value is not set, knowing when the message ought
to be parsed as a CloudEvent can be a challenge. While this specification
can not mandate that senders do not include any of the CloudEvents headers
when the message is not a CloudEvent, it would be reasonable for a receiver
to assume that if the message has all of the mandatory CloudEvents attributes
as headers then it`s probably a CloudEvent. However, as with all CloudEvent
messages, if it does not adhere to all of the normative language of this
specification then it is not a valid CloudEvent.

### 3.1. Keys

The `datakey` of the DDS message MAY be populated. A _key field_ in DDS is way
to uniquely identify individual instances of data being published to a topic. For
example, if you are publishing data to a Temperature Topic dealing with
temperature readings from different sensors, the sensor ID could be a key field.

Key fields in DDS are used to enable numerous data-centric communications
capabilities that are central to the protocol. These include:
- Keyed Access: Subscribers can express interest in receiving data samples with
specific key values.
- Filtering and Matching: Publishers use key values to categorize data samples, and
subscribers use key-based filters to specify which data samples they are
interested in. This reduces the amount of data that is sent over the wire in a
DDS-based system.
- Reliability and Durability: These Quality of Service (QoS) settings control
how DDS handles reliable message delivery of data samples with the same key, and
when to overwrite locally available data samples with the same key.

While it is not necessary to set the `datakey` field for a DDS CloudEvent message,
setting this value will enable many of the more powerful features of the DDS
protocol.

### 3.2. Binary Content Mode

The _binary_ content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.2.1. Content Type

For the _binary_ mode, the header `content-type` property MUST be mapped
directly to the CloudEvents `datacontenttype` attribute and the
`datacontentencoding` attribute MUST be set to `binary`.

#### 3.2.2. Event Data Encoding

The [`data`](#21-data) byte-sequence MUST be used as the body ("Data" field)
of the DDS message.

In binary mode, the DDS representation of a CloudEvent with no `data` is a
DDS message with no body. Transmission such a DDS message is allowable.

#### 3.2.3. Metadata Headers

All [CloudEvents][ce] attributes and [CloudEvent Attributes Extensions]
(../primer.md#cloudevent-extension-attributes)
with exception of `data` MUST be individually mapped to and from the Header
fields in the DDS message.

### 3.3. Structured Content Mode

The _structured_ content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple protocols.

#### 3.3.1. Content-Type

If present, the DDS message header property `content-type` MUST be set to the
media type of an [event format](#14-event-formats).

Example for the [JSON format][json-format]:

```text
content-type: cloudevent/json
```
Example for the [DDS event format][dds-message-format]:

```text
content-type: application/cloudevent+dds
```

For both of the above cases, the `content-type` property MUST be mapped
directly to the CloudEvents `datacontenttype` attribute and the
`datacontentencoding` attribute MUST be set to either `text` or `json`
depending on the type of structured data being transmitted.


#### 3.3.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes, and
`data`, are represented.

The event metadata and data are then rendered in accordance with the
[event format](#14-event-formats) specification and the resulting data becomes
the DDS application [data](#21-data) section.

Similar to binary mode, the DDS representation of a structured CloudEvent with
no `data` is a DDS message with no body, and transmission of such a message
is allowable.

#### 3.3.3. Metadata Headers

Implementations include the same DDS headers as defined for the
[binary mode](#32-binary-content-mode). No additional metadata header attributes
are defined for structured data.

## 4. References

- [OMG][omg] Object Management Group (OMG) 
- [DDS][dds] OMG Data Distribution Service (DDS) Specification
- [RTPS][rtps] OMG Real-Time Publish Subscribe Wire Protocol
- [DDS-Message-Format][dds-message-format] The DDS message format
- [RFC2046][rfc2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][rfc3629] UTF-8, a transformation format of ISO 10646
- [RFC7159][rfc7159] The JavaScript Object Notation (JSON) Data Interchange
  Format

[ce]: ../spec.md
[omg]: https://www.omg.org/
[dds]: https://www.omg.org/spec/DDS/1.4/PDF
[rtps]: https://www.omg.org/spec/DDSI-RTPS/2.3/PDF
[dds-message-format]: ./dds-format.md
[json-format]: ../formats/json-format.md
[json-value]: https://tools.ietf.org/html/rfc7159#section-3
[rfc2046]: https://tools.ietf.org/html/rfc2046
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3629]: https://tools.ietf.org/html/rfc3629
[rfc7159]: https://tools.ietf.org/html/rfc7159
