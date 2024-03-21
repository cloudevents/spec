# NATS Protocol Binding for CloudEvents - Version 1.0.3-wip

## Abstract

The [NATS][nats] Protocol Binding for CloudEvents defines how events are mapped
to [NATS messages][nats-msg-proto].

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1 [Conformance](#11-conformance)
- 1.2 [Relation to NATS](#12-relation-to-nats)
- 1.3 [Content Modes](#13-content-modes)
- 1.4 [Event Formats](#14-event-formats)
- 1.5 [Security](#15-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

- 2.1 [datacontenttype Attribute](#21-datacontenttype-attribute)
- 2.2 [data](#22-data)

3. [NATS Message Mapping](#3-nats-message-mapping)

- 3.1 [Binary Content Mode](#31-binary-content-mode)
- 3.2 [Structured Content Mode](#32-structured-content-mode)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be used in the NATS
protocol as client [produced][nats-pub-proto] and [consumed][nats-msg-proto]
messages.

### 1.1 Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2 Relation to NATS

This specification does not prescribe rules constraining transfer or settlement
of event messages with NATS; it solely defines how CloudEvents are expressed in
the NATS protocol as client messages that are [produced][nats-pub-proto] and
[consumed][nats-msg-proto].

### 1.3 Content Modes

The CloudEvents specification defines three content modes for transferring
events: _structured_, _binary_ and _batch_. The NATS protocol binding does not
currently support the batch content mode. Every compliant implementation SHOULD
support both structured and binary modes.

In the _binary_ content mode, event metadata attributes are placed in message
headers and the event data are placed in the NATS message payload. Binary mode
is supported as of [NATS 2.2][nats22], which introduced message headers.

In the _structured_ content mode, event metadata attributes and event data
are placed into the NATS message payload using an [event format](#14-event-formats).

### 1.4 Event Formats

Event formats, used with the _structured_ content mode, define how an event is
expressed in a particular data format. All implementations of this specification
MUST support the [JSON event format][json-format].

### 1.5 Security

This specification does not introduce any new security features for NATS, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][ce] event
attributes.

### 2.1 datacontenttype Attribute

The `datacontenttype` attribute is assumed to contain a media-type expression
compliant with [RFC2046][rfc2046].

### 2.2 data

`data` is assumed to contain opaque application data that is
encoded as declared by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into NATS as defined in this
specification, core NATS provides data available as a sequence of bytes.

For instance, if the declared `datacontenttype` is
`application/json;charset=utf-8`, the expectation is that the `data`
value is made available as [UTF-8][rfc3629] encoded JSON text.

## 3. NATS Message Mapping

The content mode is chosen by the sender of the event, which is either the
requesting or the responding party. Gestures that might allow solicitation
of events using a particular mode might be defined by an application, but
are not defined here.

The receiver of the event can distinguish between the two modes using two
conditions:

- If the server is a version earlier than NATS 2.2, the content mode is
always _structured_.
- If the server is version 2.2 or above and the `Content-Type` header of
`application/cloudevents` is present (matched case-insensitively),
then the message is in _structured_ mode, otherwise it is using binary mode.

If the content mode is _structured_ then the NATS message payload MUST be
the [JSON event format][json-format] serialized as specified by the
[UTF-8][rfc3629] encoded JSON text for use in NATS.

### 3.1 Binary Content Mode

The _binary_ content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1 Event Data Encoding

The [`data`](#22-data) byte-sequence is used as the message body.

#### 3.1.2 Metadata Headers

All [CloudEvents][ce] attributes, including extensions, MUST be individually
mapped to and from distinct NATS message header.

CloudEvents extensions that define their own attributes MAY define a secondary
mapping to NATS headers for those attributes, especially if specific attributes
need to align with NATS features or with other specifications that have explicit
NATS header bindings. Note that these attributes MUST also still appear in the
NATS message as NATS headers with the `ce-` prefix as noted in
[NATS Header Names](#3131-nats-header-names).

##### 3.1.3.1 NATS Header Names

Except where noted, all CloudEvents context attributes, including extensions,
MUST be mapped to NATS headers with the same name as the attribute name but
prefixed with `ce-`.

Examples:

    * `time` maps to `ce-time`
    * `id` maps to `ce-id`
    * `specversion` maps to `ce-specversion`
    * `datacontenttype` maps to `ce-datacontenttype`

Note: per the [NATS][nats-message-headers] design specification, header names are
case-insensitive.

##### 3.1.3.2 NATS Header Values

The value for each NATS header is constructed from the respective attribute
type's [canonical string representation][ce-types].

Some CloudEvents metadata attributes can contain arbitrary UTF-8 string content,
and per [RFC7230, section 3][rfc7230-section-3], NATS headers MUST only use
printable characters from the US-ASCII character set, and are terminated by a
CRLF sequence with OPTIONAL whitespace around the header value.

When encoding a CloudEvent as an NATS message, string values
represented as NATS header values MUST be percent-encoded as
described below. This is compatible with [RFC3986, section
2.1][rfc3986-section-2-1] but is more specific about what needs
encoding. The resulting string SHOULD NOT be further encoded.
(Rationale: quoted string escaping is unnecessary when every space
and double-quote character is already percent-encoded.)

When decoding an NATS message into a CloudEvent, any NATS header
value MUST first be unescaped with respect to double-quoted strings,
as described in [RFC7230, section 3.2.6][rfc7230-section-3-2-6]. A single
round of percent-decoding MUST then be performed as described
below. NATS headers for CloudEvent attribute values do not support
parenthetical comments, so the initial unescaping only needs to handle
double-quoted values, including processing backslash escapes within
double-quoted values. Header values produced via the
percent-encoding described here will never include double-quoted
values, but they MUST be supported when receiving events, for
compatibility with older versions of this specification which did
not require double-quote and space characters to be percent-encoded.

Percent encoding is performed by considering each Unicode character
within the attribute's canonical string representation. Any
character represented in memory as a [Unicode surrogate
pair][surrogate-pair] MUST be treated as a single Unicode character.
The following characters MUST be percent-encoded:

- Space (U+0020)
- Double-quote (U+0022)
- Percent (U+0025)
- Any characters outside the printable ASCII range of U+0021-U+007E
  inclusive

Attribute values are already constrained to prohibit characters in
the range U+0000-U+001F inclusive and U+007F-U+009F inclusive;
however for simplicity and to account for potential future changes,
it is RECOMMENDED that any NATS header encoding implementation treats
such characters as requiring percent-encoding.

Space and double-quote are encoded to avoid requiring any further
quoting. Percent is encoded to avoid ambiguity with percent-encoding
itself.

Steps to encode a Unicode character:

- Encode the character using UTF-8, to obtain a byte sequence.
- Encode each byte within the sequence as `%xy` where `x` is a
  hexadecimal representation of the most significant 4 bits of the byte,
  and `y` is a hexadecimal representation of the least significant 4
  bits of the byte.

Percent-encoding SHOULD be performed using upper-case for values A-F,
but decoding MUST accept lower-case values.

When performing percent-decoding (when decoding an NATS message to a
CloudEvent), values that have been unnecessarily percent-encoded MUST be
accepted, but encoded byte sequences which are invalid in UTF-8 MUST be
rejected. (For example, "%C0%A0" is an overlong encoding of U+0020, and
MUST be rejected.)

Example: a header value of "Euro &#x20AC; &#x1F600;" SHOULD be encoded as follows:

- The characters, 'E', 'u', 'r', 'o' do not require encoding
- Space, the Euro symbol, and the grinning face emoji require encoding.
  They are characters U+0020, U+20AC and U+1F600 respectively.
- The encoded NATS header value is therefore "Euro%20%E2%82%AC%20%F0%9F%98%80"
  where "%20" is the encoded form of space, "%E2%82%AC" is the encoded form
  of the Euro symbol, and "%F0%9F%98%80" is the encoded form of the
  grinning face emoji.

#### 3.1.4 Example

This example shows the _binary_ mode mapping of an event in client messages that
are [produced][nats-pub-proto] and [consumed][nats-msg-proto].

```text
------------------ Message -------------------

Subject: mySubject

------------------ header --------------------

ce-specversion: 1.0
ce-type: com.example.someevent
ce-time: 2018-04-05T03:56:24Z
ce-id: 1234-1234-1234
ce-source: /mycontext/subcontext
ce-datacontenttype: application/json


------------------ payload -------------------

{
  ... application data ...
}

-----------------------------------------------
```

### 3.2 Structured Content Mode

The chosen [event format](#14-event-formats) defines how all attributes,
including the payload, are represented.

The event metadata and data MUST then be rendered in accordance with the event
format specification and the resulting data becomes the payload.

### 3.2.1 Example

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
[ce-types]: ../spec.md#type-system
[json-format]: ../formats/json-format.md
[json-value]: https://tools.ietf.org/html/rfc7159#section-3
[nats]: https://nats.io
[nats22]: https://docs.nats.io/release-notes/whats_new/whats_new_22#message-headers
[nats-message-headers]: https://github.com/nats-io/nats-architecture-and-design/blob/main/adr/ADR-4.md#nats-message-headers
[nats-msg-proto]: https://docs.nats.io/reference/reference-protocols/nats-protocol#protocol-messages
[nats-pub-proto]: https://docs.nats.io/reference/reference-protocols/nats-protocol#pub
[rfc2046]: https://tools.ietf.org/html/rfc2046
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3629]: https://tools.ietf.org/html/rfc3629
[rfc3986-section-2-1]: https://tools.ietf.org/html/rfc3986#section-2.1
[rfc7159]: https://tools.ietf.org/html/rfc7159
[rfc7230]: https://tools.ietf.org/html/rfc7230
[rfc7230-section-3]: https://tools.ietf.org/html/rfc7230#section-3
[rfc7230-section-3-2-6]: https://tools.ietf.org/html/rfc7230#section-3.2.6
[surrogate-pair]: http://unicode.org/glossary/#surrogate_pair
