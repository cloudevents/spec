# HTTP Protocol Binding for CloudEvents - Version 1.0.3-wip

## Abstract

The HTTP Protocol Binding for CloudEvents defines how events are mapped to HTTP
1.1 request and response messages.

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to HTTP](#12-relation-to-http)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

- 2.1. [datacontenttype Attribute](#21-datacontenttype-attribute)
- 2.2. [data](#22-data)

3. [HTTP Message Mapping](#3-http-message-mapping)

- 3.1. [Binary Content Mode](#31-binary-content-mode)
- 3.2. [Structured Content Mode](#32-structured-content-mode)
- 3.3. [Batched Content Mode](#33-batched-content-mode)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be used in [HTTP
1.1][rfc7230] requests and response messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to HTTP

This specification does not prescribe rules constraining the use or handling of
specific [HTTP methods][rfc7231-section-4], and it also does not constrain the
[HTTP target resource][rfc7230-section-5-1] that is used for transferring or
soliciting events.

Events can be transferred with all standard or application-defined HTTP request
methods that support payload body transfers. Events can be also be transferred
in HTTP responses and with all HTTP status codes that permit payload body
transfers.

All examples herein that show HTTP methods, HTTP target URIs, and HTTP status
codes are non-normative illustrations.

This specification also applies equivalently to HTTP/2 ([RFC7540][rfc7540]),
which is compatible with HTTP 1.1 semantics.

### 1.3. Content Modes

The CloudEvents specification defines three content modes for transferring
events: _structured_, _binary_ and _batch_. The HTTP protocol binding supports
all three content modes. Every compliant implementation SHOULD
support both structured and binary modes.

In the _binary_ content mode, the value of the event `data` is placed into the
HTTP request, or response, body as-is, with the `datacontenttype` attribute
value declaring its media type in the HTTP `Content-Type` header; all other
event attributes are mapped to HTTP headers.

In the _structured_ content mode, event metadata attributes and event data are
placed into the HTTP request or response body using an
[event format](#14-event-formats) that supports
[structured-mode messages][ce-message].

In the _batched_ content mode, event metadata attributes and event data of
multiple events are batched into a single HTTP request or response body using
an [event format](#14-event-formats) that supports batching
[structured-mode messages][ce-message].

### 1.4. Event Formats

Event formats, used with the _structured_ content mode, define how an event is
expressed in a particular data format. All implementations of this specification
that support the _structured_ content mode MUST support the non-batching [JSON
event format][json-format], but MAY support any additional, including
proprietary, formats.

Event formats MAY additionally define how a batch of events is expressed. Those
can be used with the _batched_ content mode.

### 1.5. Security

This specification does not introduce any new security features for HTTP, or
mandate specific existing features to be used. This specification applies
identically to [HTTP over TLS][rfc2818].

## 2. Use of CloudEvents Attributes

This specification does not further define any of the core [CloudEvents][ce]
event attributes.

This mapping is intentionally robust against changes, including the addition and
removal of event attributes, and also accommodates vendor extensions to the
event metadata.

### 2.1. datacontenttype Attribute

The `datacontenttype` attribute is assumed to contain a [RFC2046][rfc2046]
compliant media-type expression.

### 2.2. data

`data` is assumed to contain opaque application data that is encoded as declared
by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into HTTP as defined in this
specification, the assumption is that the `data` value is made available as a
sequence of bytes.

For instance, if the declared `datacontenttype` is
`application/json;charset=utf-8`, the expectation is that the `data` value is
made available as [UTF-8][rfc3629] encoded JSON text to HTTP.

## 3. HTTP Message Mapping

The event binding is identical for both HTTP request and response messages.

The content mode is chosen by the sender of the event, which is either the
requesting or the responding party. Gestures that might allow solicitation of
events using a particular mode might be defined by an application, but are not
defined here. The _batched_ mode MUST NOT be used unless solicited, and the
gesture SHOULD allow the receiver to choose the maximum size of a batch.

The receiver of the event can distinguish between the three modes by inspecting
the `Content-Type` header value. If the value is prefixed with the CloudEvents
media type `application/cloudevents` (matched case-insensitively), indicating
the use of a known [event format](#14-event-formats), the receiver uses
_structured_ mode. If the value is prefixed with `application/cloudevents-batch`,
the receiver uses the _batched_ mode. Otherwise it defaults to _binary_ mode.

If a receiver detects the CloudEvents media type, but with an event format that
it cannot handle, for instance `application/cloudevents+avro`, it MAY still
treat the event as binary and forward it to another party as-is.

When the `Content-Type` header value is not prefixed with the CloudEvents media
type, knowing when the message ought to be parsed as a CloudEvent can be a
challenge. While this specification can not mandate that senders do not include
any of the CloudEvents HTTP headers when the message is not a CloudEvent, it
would be reasonable for a receiver to assume that if the message has all of the
mandatory CloudEvents attributes as HTTP headers then it's probably a
CloudEvent. However, as with all CloudEvent messages, if it does not adhere to
all of the normative language of this specification then it is not a valid
CloudEvent.

### 3.1. Binary Content Mode

The _binary_ content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1. HTTP Content-Type

For the _binary_ mode, the HTTP `Content-Type` header value corresponds to
(MUST be populated from or written to) the CloudEvents `datacontenttype`
attribute. Note that a `ce-datacontenttype` HTTP header MUST NOT also be
present in the message.

#### 3.1.2. Event Data Encoding

The [`data`](#22-data) byte-sequence is used as the HTTP message body.

#### 3.1.3. Metadata Headers

All other [CloudEvents][ce] attributes, including extensions, MUST be
individually mapped to and from distinct HTTP message header.

CloudEvents extensions that define their own attributes MAY define a secondary
mapping to HTTP headers for those attributes, especially if specific attributes
need to align with HTTP features or with other specifications that have explicit
HTTP header bindings. Note that these attributes MUST also still appear in the
HTTP message as HTTP headers with the `ce-` prefix as noted in
[HTTP Header Names](#3131-http-header-names).

##### 3.1.3.1. HTTP Header Names

Except where noted, all CloudEvents context attributes, including extensions,
MUST be mapped to HTTP headers with the same name as the attribute name but
prefixed with `ce-`.

Examples:

    * `time` maps to `ce-time`
    * `id` maps to `ce-id`
    * `specversion` maps to `ce-specversion`

Note: per the [HTTP](https://tools.ietf.org/html/rfc7230#section-3.2)
specification, header names are case-insensitive.

##### 3.1.3.2. HTTP Header Values

The value for each HTTP header is constructed from the respective attribute
type's [canonical string representation][ce-types].

Some CloudEvents metadata attributes can contain arbitrary UTF-8 string content,
and per [RFC7230, section 3][rfc7230-section-3], HTTP headers MUST only use
printable characters from the US-ASCII character set, and are terminated by a
CRLF sequence with OPTIONAL whitespace around the header value.

When encoding a CloudEvent as an HTTP message, string values
represented as HTTP header values MUST be percent-encoded as
described below. This is compatible with [RFC3986, section
2.1][rfc3986-section-2-1] but is more specific about what needs
encoding. The resulting string SHOULD NOT be further encoded.
(Rationale: quoted string escaping is unnecessary when every space
and double-quote character is already percent-encoded.)

When decoding an HTTP message into a CloudEvent, any HTTP header
value MUST first be unescaped with respect to double-quoted strings,
as described in [RFC7230, section 3.2.6][rfc7230-section-3-2-6]. A single
round of percent-decoding MUST then be performed as described
below. HTTP headers for CloudEvent attribute values do not support
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
it is RECOMMENDED that any HTTP header encoding implementation treats
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

When performing percent-decoding (when decoding an HTTP message to a
CloudEvent), values that have been unnecessarily percent-encoded MUST be
accepted, but encoded byte sequences which are invalid in UTF-8 MUST be
rejected. (For example, "%C0%A0" is an overlong encoding of U+0020, and
MUST be rejected.)

Example: a header value of "Euro &#x20AC; &#x1F600;" SHOULD be encoded as follows:

- The characters, 'E', 'u', 'r', 'o' do not require encoding
- Space, the Euro symbol, and the grinning face emoji require encoding.
  They are characters U+0020, U+20AC and U+1F600 respectively.
- The encoded HTTP header value is therefore "Euro%20%E2%82%AC%20%F0%9F%98%80"
  where "%20" is the encoded form of space, "%E2%82%AC" is the encoded form
  of the Euro symbol, and "%F0%9F%98%80" is the encoded form of the
  grinning face emoji.

#### 3.1.4. Examples

This example shows the _binary_ mode mapping of an event with an HTTP POST
request:

```text
POST /someresource HTTP/1.1
Host: webhook.example.com
ce-specversion: 1.0
ce-type: com.example.someevent
ce-time: 2018-04-05T03:56:24Z
ce-id: 1234-1234-1234
ce-source: /mycontext/subcontext
    .... further attributes ...
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
    ... application data ...
}
```

This example shows a response containing an event:

```text
HTTP/1.1 200 OK
ce-specversion: 1.0
ce-type: com.example.someevent
ce-time: 2018-04-05T03:56:24Z
ce-id: 1234-1234-1234
ce-source: /mycontext/subcontext
    .... further attributes ...
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
    ... application data ...
}
```

### 3.2. Structured Content Mode

The _structured_ content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple protocols.

#### 3.2.1. HTTP Content-Type

The [HTTP `Content-Type`][content-type] header MUST be set to the media type of
an [event format](#14-event-formats).

Example for the [JSON format][json-format]:

```text
Content-Type: application/cloudevents+json; charset=UTF-8
```

#### 3.2.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes, and
`data`, are represented.

The event metadata and data is then rendered in accordance with the event format
specification and the resulting data becomes the HTTP message body.

#### 3.2.3. Metadata Headers

Implementations MAY include the same HTTP headers as defined for the
[binary mode](#313-metadata-headers).

All CloudEvents metadata attributes MUST be mapped into the payload, even if
they are also mapped into HTTP headers.

#### 3.2.4. Examples

This example shows a JSON event format encoded event, sent with a PUT request:

```text

PUT /myresource HTTP/1.1
Host: webhook.example.com
Content-Type: application/cloudevents+json; charset=utf-8
Content-Length: nnnn

{
    "specversion" : "1.0",
    "type" : "com.example.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

```

This example shows a JSON encoded event returned in a response:

```text

HTTP/1.1 200 OK
Content-Type: application/cloudevents+json; charset=utf-8
Content-Length: nnnn

{
    "specversion" : "1.0",
    "type" : "com.example.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

```

### 3.3. Batched Content Mode

In the _batched_ content mode several events are batched into a single HTTP
request or response body. The chosen [event format](#14-event-formats) MUST
define how a batch is represented, including a suitable media type.

#### 3.3.1. HTTP Content-Type

The [HTTP `Content-Type`][content-type] header MUST be set to the media type of
the batch mode for the [event format](#14-event-formats).

Example for the [JSON Batch format][json-batch-format]:

```text
Content-Type: application/cloudevents-batch+json; charset=UTF-8
```

#### 3.3.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how a batch of events and
all event attributes, and `data`, are represented.

The batch of events is then rendered in accordance with the event format
specification and the resulting data becomes the HTTP message body.

#### 3.3.3. Examples

This example shows two batched CloudEvents, sent with a PUT request:

```text

PUT /myresource HTTP/1.1
Host: webhook.example.com
Content-Type: application/cloudevents-batch+json; charset=utf-8
Content-Length: nnnn

[
    {
        "specversion" : "1.0",
        "type" : "com.example.someevent",

        ... further attributes omitted ...

        "data" : {
            ... application data ...
        }
    },
    {
        "specversion" : "1.0",
        "type" : "com.example.someotherevent",

        ... further attributes omitted ...

        "data" : {
            ... application data ...
        }
    }
]

```

This example shows two batched CloudEvents returned in a response:

```text

HTTP/1.1 200 OK
Content-Type: application/cloudevents-batch+json; charset=utf-8
Content-Length: nnnn

[
    {
        "specversion" : "1.0",
        "type" : "com.example.someevent",

        ... further attributes omitted ...

        "data" : {
            ... application data ...
        }
    },
    {
        "specversion" : "1.0",
        "type" : "com.example.someotherevent",

        ... further attributes omitted ...

        "data" : {
            ... application data ...
        }
    }
]

```

## 4. References

- [RFC2046][rfc2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC2818][rfc2818] HTTP over TLS
- [RFC3629][rfc3629] UTF-8, a transformation format of ISO 10646
- [RFC3986][rfc3986] Uniform Resource Identifier (URI): Generic Syntax
- [RFC4627][rfc4627] The application/json Media Type for JavaScript Object
  Notation (JSON)
- [RFC4648][rfc4648] The Base16, Base32, and Base64 Data Encodings
- [RFC6839][rfc6839] Additional Media Type Structured Syntax Suffixes
- [RFC7159][rfc7159] The JavaScript Object Notation (JSON) Data Interchange
  Format
- [RFC7230][rfc7230] Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and
  Routing
- [RFC7231][rfc7231] Hypertext Transfer Protocol (HTTP/1.1): Semantics and
  Content
- [RFC7540][rfc7540] Hypertext Transfer Protocol Version 2 (HTTP/2)

[ce]: ../spec.md
[ce-message]: ../spec.md#message
[ce-types]: ../spec.md#type-system
[json-format]: ../formats/json-format.md
[json-batch-format]: ../formats/json-format.md#4-json-batch-format
[content-type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[json-value]: https://tools.ietf.org/html/rfc7159#section-3
[json-array]: https://tools.ietf.org/html/rfc7159#section-5
[rfc2046]: https://tools.ietf.org/html/rfc2046
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc2818]: https://tools.ietf.org/html/rfc2818
[rfc3629]: https://tools.ietf.org/html/rfc3629
[rfc3986]: https://tools.ietf.org/html/rfc3986
[rfc3986-section-2-1]: https://tools.ietf.org/html/rfc3986#section-2.1
[rfc4627]: https://tools.ietf.org/html/rfc4627
[rfc4648]: https://tools.ietf.org/html/rfc4648
[rfc6839]: https://tools.ietf.org/html/rfc6839#section-3.1
[rfc7159]: https://tools.ietf.org/html/rfc7159
[rfc7230]: https://tools.ietf.org/html/rfc7230
[rfc7230-section-3]: https://tools.ietf.org/html/rfc7230#section-3
[rfc7230-section-3-2-6]: https://tools.ietf.org/html/rfc7230#section-3.2.6
[rfc7230-section-5-1]: https://tools.ietf.org/html/rfc7230#section-5.1
[rfc7231]: https://tools.ietf.org/html/rfc7231
[rfc7231-section-4]: https://tools.ietf.org/html/rfc7231#section-4
[rfc7540]: https://tools.ietf.org/html/rfc7540
[surrogate-pair]: http://unicode.org/glossary/#surrogate_pair
