# Kafka Protocol Binding for CloudEvents - Version 1.0.3-wip

## Abstract

The [Kafka][kafka] Protocol Binding for CloudEvents defines how events are
mapped to [Kafka messages][kafka-message-format].

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to Kafka](#12-relation-to-kafka)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

- 2.1. [data](#21-data)

3. [Kafka Message Mapping](#3-kafka-message-mapping)

- 3.1. [Key Mapping](#31-key-mapping)
- 3.2. [Binary Content Mode](#32-binary-content-mode)
- 3.3. [Structured Content Mode](#33-structured-content-mode)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be used in the Kafka
protocol as [Kafka messages][kafka-message-format] (aka Kafka records).

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to Kafka

This specification does not prescribe rules constraining transfer or settlement
of event messages with Kafka; it solely defines how CloudEvents are expressed in
the Kafka protocol as [Kafka messages][kafka-message-format].

The Kafka documentation uses "message" and "record" somewhat interchangeably and
therefore the terms are to be considered synonyms in this specification as well.

Conceptually, Kafka is a log-oriented store for records, each holding a singular
key/value pair. The store is commonly partitioned, and the partition for a
record is typically chosen based on the key's value. Kafka clients accomplish
this by using a hash function.

This binding specification defines how attributes and data of a CloudEvent is
mapped to the value and headers sections of a Kafka record.

Generally, the user SHOULD configure the key and/or the partition of the Kafka
record in a way that makes more sense for his/her use case (e.g. streaming
applications), in order to co-partition values, define relationships between
events, etc. This spec provides an OPTIONAL definition to map the key section of
the Kafka record, without constraining the user to implement it nor use it. An
example use case of this definition is when the sink of the event is a Kafka
topic, but the source is another transport (e.g. HTTP), and the user needs a way
to key the record. As a counter example, it doesn't make sense to use it when
the sink and source are Kafka topics, because this might cause the re-keying of
the records.

### 1.3. Content Modes

The CloudEvents specification defines three content modes for transferring
events: _structured_, _binary_ and _batch_. The Kafka protocol binding does not
currently support the batch content mode. Every compliant implementation SHOULD
support both structured and binary modes.

The specification defines three content modes for transferring events:
_structured_, _binary_ and _batch_. The Kafka protocol binding does not
currently support the _batch_ content mode.

In the _structured_ content mode, event metadata attributes and event data are
placed into the Kafka message value section using an
[event format](#14-event-formats).

In the _binary_ content mode, the value of the event `data` MUST be placed into
the Kafka message's value section as-is, with the `content-type` header value
declaring its media type; all other event attributes MUST be mapped to the Kafka
message's [header section][kafka-message-header].

Implementations that use Kafka 0.11.0.0 and above MAY use either _binary_ or
_structured_ modes. Implementations that use Kafka 0.10.x.x and below MUST only
use _structured_ mode. This is because older versions of Kafka lacked
support for message level headers.

### 1.4. Event Formats

Event formats, used with the _structured_ content mode, define how an event is
expressed in a particular data format. All implementations of this specification
that support the _structured_ content mode MUST support the [JSON event
format][json-format].

### 1.5. Security

This specification does not introduce any new security features for Kafka, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][ce] event
attributes.

### 2.1. data

`data` is assumed to contain opaque application data that is encoded as declared
by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into Kafka as defined in this
specification, core Kafka provides data available as a sequence of bytes.

For instance, if the declared `datacontenttype` is
`application/json;charset=utf-8`, the expectation is that the `data` value is
made available as [UTF-8][rfc3629] encoded JSON text.

## 3. Kafka Message Mapping

With Kafka 0.11.0.0 and above, the content mode is chosen by the sender of the
event. Protocol usage patterns that might allow solicitation of events using a
particular content mode might be defined by an application, but are not defined
here.

The receiver of the event can distinguish between the two content modes by
inspecting the `content-type` [Header][kafka-message-header] of the Kafka
message. If the header is present and its value is prefixed with the CloudEvents
media type `application/cloudevents` (matched case-insensitively),
indicating the use of a known [event format](#14-event-formats), the receiver
uses _structured_ mode, otherwise it defaults to _binary_ mode.

If a receiver finds a CloudEvents media type as per the above rule, but with an
event format that it cannot handle, for instance `application/cloudevents+avro`,
it MAY still treat the event as binary and forward it to another party as-is.

When the `content-type` header value is not prefixed with the CloudEvents media
type, knowing when the message ought to be parsed as a CloudEvent can be a
challenge. While this specification can not mandate that senders do not include
any of the CloudEvents headers when the message is not a CloudEvent, it would be
reasonable for a receiver to assume that if the message has all of the mandatory
CloudEvents attributes as headers then it's probably a CloudEvent. However, as
with all CloudEvent messages, if it does not adhere to all of the normative
language of this specification then it is not a valid CloudEvent.

### 3.1. Key Mapping

Every implementation MUST, by default, map the user provided record key to the
Kafka record key.

The 'key' of the Kafka message MAY be populated by a "Key Mapper" function,
which might map the key directly from one of the CloudEvent's attributes, but
might also use information from the application environment, from the
CloudEvent's data or other sources.

The shape and configuration of the "Key Mapper" function is implementation
specific.

Every implementation SHOULD provide an opt-in "Key Mapper" implementation that
maps the [Partitioning](../extensions/partitioning.md) `partitionkey` attribute
value to the 'key' of the Kafka message as-is, if present.

A mapping function MUST NOT modify the CloudEvent. This means that the
aforementioned `partitionkey` attribute MUST still be included with the
transmitted event, if present. It also means that a mapping function that uses
key information from an out-of-band source, like a parameter or configuration
setting, MUST NOT add an attribute to the CloudEvent.

### 3.2. Binary Content Mode

The _binary_ content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.2.1. Content Type

For the _binary_ mode, the header `content-type` property MUST be mapped
directly to the CloudEvents `datacontenttype` attribute.

#### 3.2.2. Event Data Encoding

The [`data`](#21-data) byte-sequence MUST be used as the value of the Kafka
message.

In binary mode, the Kafka representation of a CloudEvent with no `data` is a
Kafka message with no value. In a topic with log compaction enabled, any such
message will represent a _tombstone_ record, as described in the
[Kafka compaction documentation][kafka-log-compaction].

#### 3.2.3. Metadata Headers

All [CloudEvents][ce] attributes and
[CloudEvent Attributes Extensions](../primer.md#cloudevent-extension-attributes)
with exception of `data` MUST be individually mapped to and from the Header
fields in the Kafka message. Both header keys and header values MUST be encoded
as UTF-8 strings.

##### 3.2.3.1 Property Names

CloudEvent attributes are prefixed with `ce_` for use in the
[message-headers][kafka-message-header] section.

Examples:

    * `time` maps to `ce_time`
    * `id` maps to `ce_id`
    * `specversion` maps to `ce_specversion`

##### 3.2.4.2 Property Values

The value for each Kafka header is constructed from the respective header's
Kafka representation, compliant with the [Kafka message
format][kafka-message-format] specification.

#### 3.2.5 Example

This example shows the _binary_ mode mapping of an event into the Kafka message.
All other CloudEvents attributes are mapped to Kafka Header fields with prefix
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
content-type: application/avro
       .... further attributes ...

------------------- value --------------------

            ... application data encoded in Avro ...

-----------------------------------------------
```

### 3.3. Structured Content Mode

The _structured_ content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple protocols.

#### 3.3.1. Kafka Content-Type

If present, the Kafka message header property `content-type` MUST be set to the
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
the Kafka application [data](#21-data) section.

In structured mode, the Kafka representation of a CloudEvent with no `data`
is a Kafka message which still has a data section (containing the attributes
of the CloudEvent). Such a message does _not_ represent a tombstone record in
a topic with log compaction enabled, unlike the representation in binary mode.

#### 3.3.3. Metadata Headers

Implementations MAY include the same Kafka headers as defined for the
[binary mode](#32-binary-content-mode).

#### 3.3.4 Example

This example shows a JSON event format encoded event:

```text
------------------ Message -------------------

Topic Name: mytopic

------------------- key ----------------------

Key: mykey

------------------ headers -------------------

content-type: application/cloudevents+json; charset=UTF-8

------------------- value --------------------

{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
    "source" : "/mycontext/subcontext",
    "id" : "1234-1234-1234",
    "time" : "2018-04-05T03:56:24Z",
    "datacontenttype" : "application/xml",

    ... further attributes omitted ...

    "data" : {
        ... application data encoded in XML ...
    }
}

-----------------------------------------------
```

## 4. References

- [Kafka][kafka] The distributed stream platform
- [Kafka-Message-Format][kafka-message-format] The Kafka format message
- [RFC2046][rfc2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][rfc3629] UTF-8, a transformation format of ISO 10646
- [RFC7159][rfc7159] The JavaScript Object Notation (JSON) Data Interchange
  Format

[ce]: ../spec.md
[json-format]: ../formats/json-format.md
[kafka]: https://kafka.apache.org
[kafka-message-format]: https://kafka.apache.org/documentation/#messageformat
[kafka-message-header]: https://kafka.apache.org/documentation/#recordheader
[kafka-log-compaction]: https://kafka.apache.org/documentation/#design_compactionbasics
[json-value]: https://tools.ietf.org/html/rfc7159#section-3
[rfc2046]: https://tools.ietf.org/html/rfc2046
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3629]: https://tools.ietf.org/html/rfc3629
[rfc7159]: https://tools.ietf.org/html/rfc7159
