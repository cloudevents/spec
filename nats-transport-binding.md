# NATS Transport Binding for CloudEvents

## Abstract

The [NATS][NATS] Transport Binding for CloudEvents defines how events are mapped to [NATS messages][NATS-MSG-PROTO].

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to NATS](#12-relation-to-nats)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)
2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)
- 2.1. [contentType Attribute](#21-contenttype-attribute)
- 2.2. [data Attribute](#22-data-attribute)
3. [NATS Message Mapping](#3-nats-message-mapping)
- 3.1. [Event Data Encoding](#31-event-data-encoding)
- 3.2. [Example](#32-example)
4. [References](#4-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be used in the
NATS protocol as client [produced][NATS-PUB-PROTO] and [consumed][NATS-MSG-PROTO]
messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to NATS

This specification does not prescribe rules constraining transfer or settlement
of event messages with NATS; it solely defines how CloudEvents are expressed
in the NATS protocol as client messages that are [produced][NATS-PUB-PROTO] 
and [consumed][NATS-MSG-PROTO].

### 1.3. Content Modes

The specification defines two content modes for transferring events:
*structured* and *binary*.

NATS will only support *structured* data mode at this time.  Today, the
NATS protocol does not support custom message headers, necessary for
*binary* mode.

Event metadata attributes and event data are placed into the NATS message
payload using an [event format](#14-event-formats).

### 1.4. Event Formats

Event formats, used with the *stuctured* content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][JSON-format].

### 1.5. Security

This specification does not introduce any new security features for NATS, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

### 2.1. contentType Attribute

The `contentType` attribute is assumed to contain a media-type expression
compliant with [RFC2046][RFC2046].

### 2.2. data Attribute

The `data` attribute is assumed to contain opaque application data that is
encoded as declared by the `contentType` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into NATS as defined in this
specification, core NATS provides data available as a sequence of bytes.

For instance, if the declared `contentType` is
`application/json;charset=utf-8`, the expectation is that the `data` attribute
value is made available as [UTF-8][RFC3629] encoded JSON text.

## 3. NATS Message Mapping

With NATS, the content mode is always *structured* and the NATS message
payload MUST be the [JSON event format][JSON-format] serialized as
specified by the [UTF-8][RFC3629] encoded JSON text for use in NATS.

The *structured* content mode keeps event metadata and data together,
allowing simple forwarding of the same event across multiple routing
hops, and across multiple transports.

### 3.1 Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
including the payload, are represented.

The event metadata and data MUST then be rendered in accordance with the event
format specification and the resulting data becomes the payload.

### 3.2 Example

This example shows a JSON event format encoded event in client
messages that are [produced][NATS-PUB-PROTO] and [consumed][NATS-MSG-PROTO].

``` text
------------------ Message -------------------

Subject: mySubject

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

- [NATS][NATS] The NATS Messaging System
- [NATS-PUB-PROTO][NATS-PUB-PROTO] The NATS protocol for messages published by a client
- [NATS-MSG-PROTO][NATS-MSG-PROTO] The NATS protocol for messages received by a client
- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange Format

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[NATS]: https://nats.io
[NATS-PUB-PROTO]: https://nats.io/documentation/internals/nats-protocol/#PUB
[NATS-MSG-PROTO]: https://nats.io/documentation/internals/nats-protocol/#MSG
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC7159]: https://tools.ietf.org/html/rfc7159