# OpenMessaging Transport Binding for CloudEvents

## Abstract

The [OpenMessaging][OpenMessaging] Transport Binding for CloudEvents defines how events are mapped to [NATS messages][NATS-MSG-PROTO].

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to OpenMessaging](#12-relation-to-nats)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)
2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)
- 2.1. [contentType Attribute](#21-contenttype-attribute)
- 2.2. [data Attribute](#22-data-attribute)
3. [OpenMessaging Message Mapping](#3-mqtt-publish-message-mapping)
- 3.2. [Binary Content Mode](#31-binary-content-mode)
- 3.1. [Structured Content Mode](#32-structured-content-mode)
4. [References](#4-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be used in
[OpenMessaging][OpenMessaging]. 
### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to OpenMessaging

This specification does not prescribe rules constraining transfer or settlement
of event messages with OpenMessaging; it solely defines how CloudEvents are expressed
in the OpenMessaging protocol as client messages that are produced
and consumed.

### 1.3. Content Modes

This specification defines two content modes for transferring events:
*structured* and *binary*. Every compliant implementation SHOULD support both
modes.

In the *structured* content mode, event metadata attributes and event data are
placed into producer send message body.

In the *binary* content mode, the value of the event `data` attribute is placed
into message body, with the `contentType` attribute
value declaring its media type; all other event attributes are mapped OpenMessaging
sys headers.

### 1.4. Event Formats

Event formats, used with the *stuctured* content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][JSON-format].

### 1.5. Security

This specification does not introduce any new security features for OpenMessaging, or
mandate specific existing features to be used. This specification applies
identically to [SSL]([RFC6101][RFC6101]).

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

Two of the event attributes, `contentType` and `data` are handled specially
and mapped onto OpenMessaging constructs, all other attributes are transferred as
metadata without further interpretation.

### 2.1. contentType Attribute

The `contentType` attribute is assumed to contain a media-type expression
compliant with [RFC2046][RFC2046].

### 2.2. data Attribute

The `data` attribute is assumed to contain opaque application data that is
encoded as declared by the `contentType` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into OpenMessaging as defined in this
specification, the assumption is that the `data` attribute value is made
available as a sequence of bytes.

For instance, if the declared `contentType` is
`application/json;charset=utf-8`, the expectation is that the `data` attribute
value is made available as [UTF-8][RFC3629] encoded JSON text for use in
OpenMessaging


## 3. OpenMessaging Message Mapping

With OpenMessaging, the content mode is chosen by the sender of the event. Protocol
usage patterns that might allow solicitation of events using a particular
content mode might be defined by an application, but are not defined here.

The receiver of the event can distinguish between the two content modes by
inspecting the`Content Type` property  in the *userHeader* of the OpenMessaging PUBLISH message.
If the value of the `Content Type` property is `application/json;charset=utf-8`, 
indicating the use of a known [event format](#14-event-formats), the receiver uses *structured* mode, otherwise it
defaults to *binary* mode.

If a receiver finds a CloudEvents media type as per the above rule, but with an
event format that it cannot handle, for instance
`application/cloudevents+thrift`, it MAY still treat the event as binary and
forward it to another party as-is.


### 3.1. Binary Content Mode

The *binary* content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1. OpenMessaging Content-Type

For the *binary* mode, the  `contentType` value in *userHeaders* maps directly to the
CloudEvents `contentType` attribute.

#### 3.1.2. Event Data Encoding

The [`data` attribute](#22-data-attribute) byte-sequence is used as the OpenMessaging body

#### 3.1.3. Metadata Headers

All [CloudEvents][CE] attributes with exception of `contentType` and `data`
MUST be individually mapped to and from the *userHeader* Property fields in the OpenMessaging
message.

##### 3.1.3.1 User Property Names

CloudEvents attribute names MUST be used unchanged in each mapped User Property
in the MQTT PUBLISH message.

##### 3.1.3.2 User Property Values

The value for each OpenMessaging PUBLISH *userHeader* MUST be constructed from the
respective CloudEvents attribute's JSON type representation, compliant with the
[JSON event format][JSON-format] specification.

#### 3.1.4 Examples

This example shows the *binary* mode mapping of an event into the
OpenMessaging produce message.All 
CloudEvents attributes are mapped to OpenMessaging produce *userHeaders* Property
fields. The `Topic name` is chosen by the OpenMessaging client and not derived
from the CloudEvents event data.

Mind that `Content Type` here does refer to the event `data`
content carried in the payload.

``` text
------------------ PRODUCE -------------------

Topic Name: mytopic

------------- User Headers ----------------
contentYype: application/json; charset=utf-8
cloudEventsVersion: "0.1"
eventType: "com.example.someevent"
eventTime: "2018-04-16T08:56:24Z"
eventId: "openMessaging.io.event"
source: "io.penMessaging"
       .... further attributes ...

------------------ payload -------------------

{
    ... application data ...
}

-----------------------------------------------
```

### 3.2. Structured Content Mode

The *structured* content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple transports.

#### 3.2.1. OpenMessaging Content Type

For OpenMessaging, the  `contentType` value in *userHeaders* maps directly to the
CloudEvents `contentType` attribute.

#### 3.2.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
including the `data` attribute, are represented.

The event metadata and data MUST then be rendered in accordance with the event
format specification and the resulting data becomes the OpenMessaging payload.

#### 3.2.3. Metadata Headers

For OpenMessaging, implementations MAY include the same *userHeader* Properties
as defined for the [binary mode](#313-metadata-headers).

#### 3.2.4. Examples

The first example shows a JSON event format encoded event with OpenMessaging:

``` text
------------------ PRODUCE -------------------

Topic Name: mytopic
Content Type: application/cloudevents+json; charset=utf-8

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

- [OpenMessaging][OpenMessaging] The NATS Messaging System
- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC6101][RFC6101] HTTP over TLS
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange Format

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[OpenMessaging]: https://github.com/openmessaging
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC6101]: https://tools.ietf.org/html/rfc6101
[RFC7159]: https://tools.ietf.org/html/rfc7159