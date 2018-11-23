# RocketMQ Transport Binding for CloudEvents

## Abstract

The [RocketMQ][RocketMQ] Transport Binding for CloudEvents defines how events are mapped to RocketMQ messages.

## Status of this document

This document is a working draft.

## Table of Contents
1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to RocketMQ](#12-relation-to-rocketmq)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats))
- 1.5. [Security](#15-security)
2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)
- 2.1. [contenttype Attribute](#21-contenttype-attribute)
- 2.2. [data Attribute](#22-data-attribute)
3. [RocketMQ Message Mapping](#3-rocketmq-message-mapping)
- 3.1. [Binary Content Mode](#31-binary-content-mode)
- 3.2. [Structured Content Mode](#32-structured-constent-mode)
4. [References](#4-references)

## 1. Introduction
[CloudEvents][CE] is a standardized and transport-neutral definition of the 
structure and metadata description of events. This specification defines how 
the elements defined in the CloudEvents specification are to be used in the 
RocketMQ Message protocol as client produced and consumed messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", 
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be 
interpreted as described in RFC2119.

### 1.2. Relation to RocketMQ

This specification does not prescribe rules constraining transfer or settlement 
of event messages with RocketMQ; it solely defines how CloudEvents are expressed 
in the RocketMQ message transport protocol as client messages that are produced and consumed.

### 1.3. Content Modes

The specification defines two content modes for transferring events:
*structured* and *binary*.

RocketMQ will only support *structured* data mode at this time. Today, the
RocketMQ protocol does not support custom message headers, necessary for
*binary* mode.

Event metadata attributes and event data are placed into the RocketMQ message
payload using an [event format](#14-event-formats).

### 1.4. Event Formats

Event formats, used with the *stuctured* content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][JSON-format].

### 1.5. Security
This specification does not introduce any new security features for RocketMQ, or mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

### 2.1. contenttype Attribute

The `contenttype` attribute is assumed to contain a media-type expression
compliant with [RFC2046][RFC2046].

### 2.2. data Attribute
The `data` attribute is assumed to contain opaque application data that is 
encoded as declared by the `contenttype` attribute.

An application is free to hold the information in any in-memory representation 
of its choosing, but as the value is transposed into RocketMQ as defined in this 
specification, core RocketMQ provides data available as a sequence of bytes.

For instance, if the declared `contenttype` is
`application/json;charset=utf-8`, the expectation is that the `data` attribute
value is made available as [UTF-8][RFC3629] encoded JSON text.

## 3. RocketMQ Message Mapping
The receiver of the event can distinguish between the two content modes by inspecting 
the `CE_contentType` property of the RocketMQ message. If the value is prefixed with the 
CloudEvents media type `application/cloudevents`, indicating the use of a known event format, 
the receiver uses structured mode, otherwise it defaults to binary mode.

If a receiver finds a CloudEvents media type as per the above rule, but with an event format 
that it cannot handle, for instance `application/cloudevents+avro`, it MAY still treat the event 
as binary and forward it to another party as-is .

### 3.1. Binary Content Mode

The [binary content mode](#31-binary-content-mode) accommodates any shape of event data, and allows for efficient 
transfer and without transcoding effort.

#### 3.1.1. Content Type

For the binary mode, the header `CE_contentType property` MUST be mapped directly to the CloudEvents 
contentType attribute.

#### 3.1.2. Event Data Encoding

The data attribute byte-sequence MUST be used as the value of the RocketMQ message.

#### 3.1.3. Metadata Headers

All CloudEvents attributes and CloudEvent Attributes Extensions with exception of data MUST be individually mapped to and from the Header fields in the RocketMQ message.

##### 3.1.3.1 Property Names

Cloud Event attributes are prefixed with `"CE_"` for use in the message section.

Examples:

    * `eventTime` maps to `CE_eventTime`
    * `eventID` maps to `CE_eventID`
    * `cloudEventsVersion` maps to `CE_cloudEventsVersion`

##### 3.1.3.2 Property Values

The value for each RocketMQ Message header is constructed from the respective header's RocketMQ 
representation, compliant with the RocketMQ message format specification.

#### 3.1.4 Example

This example shows the binary mode mapping of an event into the RocketMQ message. 
All other CloudEvents attributes are mapped to RocketMQ message property fields with prefix `CE_`.

Mind that `CE_` here does refer to the event data content carried in the payload.

``` text
------------------ Message -------------------

Topic: mytopic


-------------- user properties ---------------

CE_contentType: application/avro
CE_cloudEventsVersion: "0.1"
CE_eventType: "com.example.someevent"
CE_eventTime: "2018-11-23T03:56:24Z"
CE_eventID: "1234-1234-1234"
CE_source: "/mycontext/subcontext"
       .... further attributes ...

------------------- value --------------------

            ... application data ...

-----------------------------------------------
```

### 3.2. Structured Content Mode

The structured content mode keeps event metadata and data together in the payload, 
allowing simple forwarding of the same event across multiple routing hops, and across 
multiple transports.

#### 3.2.1. RocketMQ Content-Type

The [RocketMQ][RocketMQ] `CE_contentType` property field MUST be set to the media type of an event format.

Example for the JSON format:

```
content-type: application/cloudevents+json; charset=UTF-8

```

#### 3.2.2. Event Data Encoding
The chosen event format defines how all attributes, including the payload, are represented. 
And in RocketMQ Message Header, it describes what is the type of transport event.

The event metadata and data may then be rendered in accordance with the event format specification 
and the resulting data becomes the payload.

#### 3.2.3. Metadata Headers

Implementations MAY include the same RocketMQ headers as defined for the binary mode.

#### 3.2.4. Example
This example shows a JSON event format encoded structured data event:

``` text
------------------ Message -------------------

Topic: mytopic

------------------ user properties -------------------

CE_contentType: application/cloudevents+json; charset=UTF-8

------------------ payload -------------------

{
    "cloudEventsVersion" : "0.1",
    "eventType" : "com.example.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

-----------------------------------------------
```

## 4. References

- [RocketMQ][RocketMQ] The RocketMQ Messaging System
- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange Format

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[RocketMQ]: http://rocketmq.apache.org/
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC7159]: https://tools.ietf.org/html/rfc7159