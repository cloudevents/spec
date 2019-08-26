# Kafka Transport Binding for CloudEvents - Version 0.4-wip

## Abstract

The [Kafka][Kafka] Transport Binding for CloudEvents defines how events are
mapped to [Kafka messages][Kafka-Message-Format].

## Status of this document

This document is a working draft.

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
- 3.1. [Key Attribute](#31-key-attribute)
- 3.2. [Binary Content Mode](#32-binary-content-mode)
- 3.3. [Structured Content Mode](#33-structured-content-mode)
4. [References](#4-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be used in the
Kafka protocol as [Kafka messages][Kafka-Message-Format] (aka Kafka records).

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to Kafka

This specification does not prescribe rules constraining transfer or settlement
of event messages with Kafka; it solely defines how CloudEvents are expressed
in the Kafka protocol as [Kafka messages][Kafka-Message-Format].

### 1.3. Content Modes

The specification defines two content modes for transferring events:
*structured* and *binary*.

The *binary* mode *only* applies to Kafka 0.11.0.0 and above, because Kafka
0.10.x.x and below lack support for message level headers.

In the *binary* content mode, the value of the event `data` MUST be
placed into the Kafka message's value section as-is, with the
`ce_datacontenttype` header value declaring its media type; all other
event attributes MUST be mapped to the Kafka message's 
[header section][Kafka-Message-Header].

In the *structured* content mode, event metadata attributes and event data are
placed into the Kafka message value section
using an [event format](#14-event-formats).



### 1.4. Event Formats

Event formats, used with the *structured* content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][JSON-format].

### 1.5. Security

This specification does not introduce any new security features for Kafka, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

### 2.1. data

`data` is assumed to contain opaque application data that is
encoded as declared by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into Kafka as defined in this
specification, core Kafka provides data available as a sequence of bytes.

For instance, if the declared `datacontenttype` is
`application/json;charset=utf-8`, the expectation is that the `data`
value is made available as [UTF-8][RFC3629] encoded JSON text.

## 3. Kafka Message Mapping

With Kafka 0.11.0.0 and above, the content mode is chosen by the sender of the 
event. Protocol usage patterns that might allow solicitation of events using a
particular content mode might be defined by an application, but are not defined
here.

The receiver of the event can distinguish between the two content modes by
inspecting the `ce_datacontenttype` [Header][Kafka-Message-Header] of the 
Kafka message. If the value is prefixed with the CloudEvents media type
`application/cloudevents`, indicating the use of a known
[event format](#14-event-formats), the receiver uses *structured* mode, otherwise
it defaults to *binary* mode.

If a receiver finds a CloudEvents media type as per the above rule, but with an
event format that it cannot handle, for instance
`application/cloudevents+avro`, it MAY still treat the event as binary and
forward it to another party as-is.

### 3.1. Key Attribute
The 'key' attribute is populated by a partitionKeyExtractor function. The 
partitionKeyExtractor is a transport specific function that contains bespoke logic 
to extract and populate the value. A default implementation of the extractor will 
use the [Partitioning](extensions/partitioning.md) extension value. 

### 3.2. Binary Content Mode

The *binary* content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.2.1. Content Type

For the *binary* mode, the header `ce_datacontenttype` property MUST be
mapped directly to the CloudEvents `datacontenttype` attribute.


#### 3.2.2. Event Data Encoding

The [`data`](#21-data) byte-sequence MUST be used as the
value of the Kafka message.

#### 3.2.3. Metadata Headers

All [CloudEvents][CE] attributes and
[CloudEvent Attributes Extensions](primer.md#cloudevent-attribute-extensions) 
with exception of `data` MUST be individually mapped to and from the Header 
fields in the Kafka message.

##### 3.2.3.1 Property Names

CloudEvent attributes are prefixed with "ce_" for use in the
[message-headers][Kafka-Message-Header] section.

Examples:

    * `time` maps to `ce_time`
    * `id` maps to `ce_id`
    * `specversion` maps to `ce_specversion`

##### 3.2.4.2 Property Values

The value for each Kafka header is constructed from the respective
header's Kafka representation, compliant with the [Kafka message
format][Kafka-Message-Format] specification.


#### 3.2.5 Example

This example shows the *binary* mode mapping of an event into the
Kafka message. All other CloudEvents attributes
are mapped to Kafka Header fields with prefix `ce_`.

Mind that `ce_` here does refer to the event `data`
content carried in the payload.

``` text
------------------ Message -------------------

Topic Name: mytopic

------------------- key ----------------------

Key: mykey

------------------ headers -------------------

ce_specversion: "0.4-wip"
ce_type: "com.example.someevent"
ce_source: "/mycontext/subcontext"
ce_id: "1234-1234-1234"
ce_time: "2018-04-05T03:56:24Z"
ce_datacontenttype: application/avro
       .... further attributes ...

------------------- value --------------------

            ... application data ...

-----------------------------------------------
```

### 3.3. Structured Content Mode

The *structured* content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple transports.

#### 3.3.1. Kafka Content-Type

The [Kafka `content-type`] property field MUST be set to the media
type of an [event format](#14-event-formats).

Example for the [JSON format][JSON-format]:

``` text
content-type: application/cloudevents+json; charset=UTF-8
```

#### 3.3.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
and `data`, are represented.

The event metadata and data are then rendered in accordance with the [event
format](#14-event-formats) specification and the resulting data becomes the
Kafka application [data][data] section.

#### 3.3.3. Metadata Headers

Implementations MAY include the same Kafka headers as defined for the
[binary mode](#32-binary-content-mode).

#### 3.3.4 Example

This example shows a JSON event format encoded event:

``` text
------------------ Message -------------------

Topic Name: mytopic

------------------- key ----------------------

Key: mykey

------------------ headers -------------------

content-type: application/cloudevents+json; charset=UTF-8

------------------- value --------------------

{
    "specversion" : "0.4-wip",
    "datacontenttype" : "com.example.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

-----------------------------------------------
```

## 4. References

- [Kafka][Kafka] The distributed stream platform
- [Kafka-Message-Format][Kafka-Message-Format] The Kafka format message
- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange
  Format

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[Kafka]: https://kafka.apache.org
[Kafka-Message-Format]: https://kafka.apache.org/documentation/#messageformat
[Kafka-Message-Header]: https://kafka.apache.org/documentation/#recordheader
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC7159]: https://tools.ietf.org/html/rfc7159
