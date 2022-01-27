# NATS Protocol Binding for CloudEvents - Version 1.0.2

## Abstract

The [NATS][nats] Protocol Binding for CloudEvents defines how events are mapped
to [NATS messages][nats-msg-proto].

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to NATS](#12-relation-to-nats)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

- 2.1. [datacontenttype Attribute](#21-datacontenttype-attribute)
- 2.2. [data](#22-data)

3. [NATS Message Mapping](#3-nats-message-mapping)

- 3.1. [Event Data Encoding](#31-event-data-encoding)
- 3.2. [Example](#32-example)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be used in the NATS
protocol as client [produced][nats-pub-proto] and [consumed][nats-msg-proto]
messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to NATS

This specification does not prescribe rules constraining transfer or settlement
of event messages with NATS; it solely defines how CloudEvents are expressed in
the NATS protocol as client messages that are [produced][nats-pub-proto] and
[consumed][nats-msg-proto].

### 1.3. Content Modes

The specification defines two content modes for transferring events:
_structured_ and _binary_.

NATS will only support _structured_ data mode at this time. Today, the NATS
protocol does not support custom message headers, necessary for _binary_ mode.

Event metadata attributes and event data are placed into the NATS message
payload using an [event format](#14-event-formats).

### 1.4. Event Formats

Event formats, used with the _structured_ content mode, define how an event is
expressed in a particular data format. All implementations of this specification
MUST support the [JSON event format][json-format].

### 1.5. Security

This specification does not introduce any new security features for NATS, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][ce] event
attributes.

### 2.1. datacontenttype Attribute

The `datacontenttype` attribute is assumed to contain a media-type expression
compliant with [RFC2046][rfc2046].

### 2.2. data

`data` is assumed to contain opaque application data that is
encoded as declared by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into NATS as defined in this
specification, core NATS provides data available as a sequence of bytes.

For instance, if the declared `datacontenttype` is
`application/json;charset=utf-8`, the expectation is that the `data`
value is made available as [UTF-8][rfc3629] encoded JSON text.

## 3. NATS Message Mapping

With NATS, the content mode is always _structured_ and the NATS message payload
MUST be the [JSON event format][json-format] serialized as specified by the
[UTF-8][rfc3629] encoded JSON text for use in NATS.

The _structured_ content mode keeps event metadata and data together, allowing
simple forwarding of the same event across multiple routing hops, and across
multiple protocols.

### 3.1 Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
including the payload, are represented.

The event metadata and data MUST then be rendered in accordance with the event
format specification and the resulting data becomes the payload.

### 3.2 Example

This example shows a JSON event format encoded event in client messages that are
[produced][nats-pub-proto] and [consumed][nats-msg-proto].

```text
------------------ Message -------------------

Subject: mySubject

------------------ payload -------------------

{
    "specversion" : "1.0",
    "type" : "com.example.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

-----------------------------------------------
```

## 4. References

- [NATS][nats] The NATS Messaging System
- [NATS-PUB-PROTO][nats-pub-proto] The NATS protocol for messages published by a
  client
- [NATS-MSG-PROTO][nats-msg-proto] The NATS protocol for messages received by a
  client
- [RFC2046][rfc2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][rfc3629] UTF-8, a transformation format of ISO 10646
- [RFC7159][rfc7159] The JavaScript Object Notation (JSON) Data Interchange
  Format

[ce]: ../spec.md
[json-format]: ../formats/json-format.md
[nats]: https://nats.io
[nats-pub-proto]: https://docs.nats.io/reference/reference-protocols/nats-protocol#pub
[nats-msg-proto]: https://docs.nats.io/reference/reference-protocols/nats-protocol#protocol-messages
[json-value]: https://tools.ietf.org/html/rfc7159#section-3
[rfc2046]: https://tools.ietf.org/html/rfc2046
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3629]: https://tools.ietf.org/html/rfc3629
[rfc7159]: https://tools.ietf.org/html/rfc7159
