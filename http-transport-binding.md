# HTTP Transport Binding for CloudEvents - Version 0.2

## Abstract

The HTTP Transport Binding for CloudEvents defines how events are mapped to
HTTP 1.1 request and response messages.

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to HTTP](#12-relation-to-http)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)
2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)
- 2.1. [contenttype Attribute](#21-contenttype-attribute)
- 2.2. [data Attribute](#22-data-attribute)
3. [HTTP Message Mapping](#3-http-message-mapping)
- 3.1. [Binary Content Mode](#31-binary-content-mode)
- 3.2. [Structured Content Mode](#32-structured-content-mode)
4. [References](#4-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be used in
[HTTP 1.1][RFC7230] requests and response messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to HTTP

This specification does not prescribe rules constraining the use or handling of
specific [HTTP methods][RFC7231-Section-4], and it also does not constrain the
[HTTP target resource][RFC7230-Section-5-1] that is used for transferring or
soliciting events.

Events can be transferred with all standard or application-defined HTTP request
methods that support payload body transfers. Events can be also be transferred
in HTTP responses and with all HTTP status codes that permit payload body
transfers.

All examples herein that show HTTP methods, HTTP target URIs, and HTTP status
codes are non-normative illustrations.

This specification also applies equivalently to HTTP/2 ([RFC7540][RFC7540]),
which is compatible with HTTP 1.1 semantics.

### 1.3. Content Modes

This specification defines two content modes for transferring events:
*structured* and *binary*. Every compliant implementation SHOULD support both
modes.

In the *structured* content mode, event metadata attributes and event data are
placed into the HTTP request or response body using an [event
format](#14-event-formats).

In the *binary* content mode, the value of the event `data` attribute is placed
into the HTTP request or response body as-is, with the `contenttype` attribute
value declaring its media type; all other event attributes are mapped to HTTP
headers.

### 1.4. Event Formats

Event formats, used with the *structured* content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][JSON-format], but MAY
support any additional, including proprietary, formats.

### 1.5. Security

This specification does not introduce any new security features for HTTP, or
mandate specific existing features to be used. This specification applies
identically to [HTTP over TLS]([RFC2818][RFC2818]).

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

Two of the event attributes, `contenttype` and `data` are handled specially
and mapped onto HTTP constructs, all other attributes are transferred as
metadata without further interpretation.

This mapping is intentionally robust against changes, including the addition
and removal of event attributes, and also accommodates vendor extensions to the
event metadata. Any mention of event attributes other than `contenttype` and
`data` is exemplary.

### 2.1. contenttype Attribute

The `contenttype` attribute is assumed to contain a [RFC2046][RFC2046]
compliant media-type expression.

### 2.2. data Attribute

The `data` attribute is assumed to contain opaque application data that is
encoded as declared by the `contenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into HTTP as defined in this
specification, the assumption is that the `data` attribute value is made
available as a sequence of bytes.

For instance, if the declared `contenttype` is
`application/json;charset=utf-8`, the expectation is that the `data` attribute
value is made available as [UTF-8][RFC3629] encoded JSON text to HTTP.

## 3. HTTP Message Mapping

The event binding is identical for both HTTP request and response messages.

The content mode is chosen by the sender of the event, which is either the
requesting or the responding party. Gestures that might allow solicitation of
events using a particular mode might be defined by an application, but are not
defined here.

The receiver of the event can distinguish between the two modes by inspecting
the `Content-Type` header value. If the value is prefixed with the CloudEvents
media type `application/cloudevents`, indicating the use of a known [event
format](#14-event-formats), the receiver uses *structured* mode, otherwise it
defaults to *binary* mode.

If a receiver detects the CloudEvents media type, but with an event format that
it cannot handle, for instance `application/cloudevents+avro`, it MAY still
treat the event as binary and forward it to another party as-is.

### 3.1. Binary Content Mode

The *binary* content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1. HTTP Content-Type

For the *binary* mode, the HTTP `Content-Type` value maps directly to the
CloudEvents `contenttype` attribute.

#### 3.1.2. Event Data Encoding

The [`data` attribute](#22-data-attribute) byte-sequence is used as the HTTP
message body.

#### 3.1.3. Metadata Headers

All [CloudEvents][CE] attributes with exception of `contenttype` and `data`
MUST be individually mapped to and from distinct HTTP message headers,
with exceptions noted below.

CloudEvents extensions that define their own attributes MAY define a 
diverging mapping to HTTP headers for those attributes, especially if 
specific attributes need to align with HTTP features or with 
other specifications that have explicit HTTP header bindings. 

An extension specification that defines a diverging mapping rule for HTTP,
and any revision of such a specification, MUST also define explicit mapping
rules for all other transport bindings that are part of the CloudEvents core at
the time of the submission or revision.

##### 3.1.3.1 HTTP Header Names

Except for attributes [explicitly handled in this specification]
(#2-use-of-cloudevents-attributes), the naming convention for the 
HTTP header mapping of well-known CloudEvents attributes is that 
each attribute name MUST be prefixed with "ce-".

Examples:

    * `time` maps to `ce-time`
    * `id` maps to `ce-id`
    * `specversion` maps to `ce-specversion`

`Map`-typed CloudEvents attributes MUST be flattened into a set
of HTTP headers, where by the name of each header carries the prefix
"ce-", an infix reflecting the map attribute followed by a dash 
("-"), and the name of the map entry key, e.g. "ce-attrib-key".

Note: per the [HTTP](https://tools.ietf.org/html/rfc7230#section-3.2)
specification, header names are case-insensitive.

##### 3.1.3.2 HTTP Header Values

The value for each HTTP header is constructed from the respective attribute's
[JSON value][JSON-value] representation, compliant with the [JSON event
format][JSON-format] specification.

Some CloudEvents metadata attributes can contain arbitrary UTF-8 string
content, and per [RFC7230 Section 3][RFC7230-Section-3], HTTP headers MUST only
use printable characters from the US-ASCII character set, and are terminated by
a CRLF sequence.

Therefore, and analog to the encoding rules for Universal character set host
names in URIs [RFC3986 3.2.2][RFC3986], the JSON value MUST be encoded as
follows:

Non-printable ASCII characters and non-ASCII characters MUST first be encoded
according to UTF-8, and then each octet of the corresponding UTF-8 sequence
MUST be percent-encoded to be represented as HTTP header characters, in
compliance with [RFC7230, sections 3, 3.2, 3.2.6][RFC7230-Section-3]. The
rules for encoding of the percent character ('%') apply as defined in 
[RFC 3986 Section 2.4.][RFC3986-Section-2-4].

JSON objects and arrays are NOT surrounded with single or double quotes.

#### 3.1.4 Examples

This example shows the *binary* mode mapping of an event with an HTTP POST
request:

``` text
POST /someresource HTTP/1.1
Host: webhook.example.com
ce-specversion: "0.2"
ce-type: "com.example.someevent"
ce-time: "2018-04-05T03:56:24Z"
ce-id: "1234-1234-1234"
ce-source: "/mycontext/subcontext"
    .... further attributes ...
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
    ... application data ...
}
```

This example shows a response containing an event:

``` text
HTTP/1.1 200 OK
ce-specversion: "0.2"
ce-type: "com.example.someevent"
ce-time: "2018-04-05T03:56:24Z"
ce-id: "1234-1234-1234"
ce-source: "/mycontext/subcontext"
    .... further attributes ...
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
    ... application data ...
}
```

### 3.2. Structured Content Mode

The *structured* content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple transports.

#### 3.2.1. HTTP Content-Type

The [HTTP `Content-Type`][Content-Type] header MUST be set to the media type of
an [event format](#14-event-formats).

Example for the [JSON format][JSON-format]:

``` text
Content-Type: application/cloudevents+json; charset=UTF-8
```

#### 3.2.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
including the `data` attribute, are represented.

The event metadata and data is then rendered in accordance with the event
format specification and the resulting data becomes the HTTP message body.

#### 3.2.3. Metadata Headers

Implementations MAY include the same HTTP headers as defined for the [binary
mode](#313-metadata-headers).

All CloudEvents metadata attributes MUST be mapped into the payload, even if
they are also mapped into HTTP headers.

#### 3.2.4 Examples

This example shows a JSON event format encoded event, sent with a PUT request:

``` text

PUT /myresource HTTP/1.1
Host: webhook.example.com
Content-Type: application/cloudevents+json; charset=utf-8
Content-Length: nnnn

{
    "specversion" : "0.2",
    "type" : "com.example.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

```

This example shows a JSON encoded event returned in a response:

``` text

HTTP/1.1 200 OK
Content-Type: application/cloudevents+json; charset=utf-8
Content-Length: nnnn

{
    "specversion" : "0.2",
    "type" : "com.example.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

```

## 4. References

- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC2818][RFC2818] HTTP over TLS
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC3986][RFC3986] Uniform Resource Identifier (URI): Generic Syntax 
- [RFC4627][RFC4627] The application/json Media Type for JavaScript Object
  Notation (JSON)
- [RFC4648][RFC4648] The Base16, Base32, and Base64 Data Encodings
- [RFC6839][RFC6839] Additional Media Type Structured Syntax Suffixes
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange Format
- [RFC7230][RFC7230] Hypertext Transfer Protocol (HTTP/1.1): Message Syntax
  and Routing
- [RFC7231][RFC7231] Hypertext Transfer Protocol (HTTP/1.1): Semantics and
  Content
- [RFC7540][RFC7540] Hypertext Transfer Protocol Version 2 (HTTP/2)

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[Content-Type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC2818]: https://tools.ietf.org/html/rfc2818
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC3986]: https://tools.ietf.org/html/rfc3986
[RFC3986-Section-2-4]: https://tools.ietf.org/html/rfc3986#section-2.4
[RFC4627]: https://tools.ietf.org/html/rfc4627
[RFC4648]: https://tools.ietf.org/html/rfc4648
[RFC6839]: https://tools.ietf.org/html/rfc6839#section-3.1
[RFC7159]: https://tools.ietf.org/html/rfc7159
[RFC7230]: https://tools.ietf.org/html/rfc7230 
[RFC7231]: https://tools.ietf.org/html/rfc7231
[RFC7230-Section-3]: https://tools.ietf.org/html/rfc7230#section-3
[RFC7231-Section-4]: https://tools.ietf.org/html/rfc7231#section-4
[RFC7230-Section-5-1]: https://tools.ietf.org/html/rfc7230#section-5.1
[RFC7540]: https://tools.ietf.org/html/rfc7540
