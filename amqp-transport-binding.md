# AMQP Transport Binding for CloudEvents

## Abstract

The AMQP Transport Binding for CloudEvents defines how events are mapped to
OASIS AMQP 1.0 ([OASIS][OASIS-AMQP-1.0]; ISO/IEC 19464:2014) messages.

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to AMQP](#12-relation-to-amqp)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)
2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)
- 2.1. [contenttype Attribute](#21-contenttype-attribute)
- 2.2. [data Attribute](#22-data-attribute)
3. [AMQP Message Mapping](#3-amqp-message-mapping)
- 3.2. [Binary Content Mode](#31-binary-content-mode)
- 3.1. [Structured Content Mode](#32-structured-content-mode)
4. [References](#4-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be used in
[AMQP][OASIS-AMQP-1.0] messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to AMQP

This specification does not prescribe rules constraining transfer or
settlement of event messages with AMQP; it solely defines how CloudEvents
are expressed as AMQP 1.0 messages.

AMQP-based messaging and eventing infrastructures often provide higher-level
programming-level abstractions that do not expose all AMQP protocol elements,
or map AMQP protocol elements or names to proprietary constructs. This
specification uses AMQP terminology, and implementers can refer the the
respective infrastructure's AMQP documentation to determine the mapping into
a programming-level abstraction.

This specification assumes use of the default AMQP [message format][message-format].

### 1.3. Content Modes

The specification defines two content modes for transferring events:
*structured* and *binary*. Every compliant implementation SHOULD support both
modes.

In the *structured* content mode, event metadata attributes and event data are
placed into the AMQP message's [application data][data] section
using an [event format](#14-event-formats).

In the *binary* content mode, the value of the event `data` attribute is placed
into the AMQP message's [application data][data] section as-is, with
the `contenttype` attribute value declaring its media type; all other event
attributes are mapped to the AMQP [application-properties][app-properties] section.

### 1.4. Event Formats

Event formats, used with the *stuctured* content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][JSON-format] as well as the
[AMQP event format][AMQP-format] for the [application-properties][app-properties]
section, but MAY support any additional, including proprietary, formats.

### 1.5. Security

This specification does not introduce any new security features for AMQP, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

Two of the event attributes, `contenttype` and `data` are handled specially
and mapped onto AMQP constructs, all other attributes are transferred as
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
of its choosing, but as the value is transposed into AMQP as defined in this
specification, the assumption is that the `data` attribute value is made
available as a sequence of bytes.

For instance, if the declared `contenttype` is
`application/json;charset=utf-8`, the expectation is that the `data` attribute
value is made available as [UTF-8][RFC3629] encoded JSON text for use in
AMQP.

## 3. AMQP Message Mapping

The content mode is chosen by the sender of the event, which is either the
requesting or the responding party. Protocol interaction patterns that might
allow solicitation of events using a particular content mode might be defined
by an application, but are not defined here.

The receiver of the event can distinguish between the two modes by inspecting
the `content-type` message property field. If the value is prefixed with the
CloudEvents media type `application/cloudevents`, indicating the use of a
known [event format](#14-event-formats), the receiver uses *structured* mode,
otherwise it defaults to *binary* mode.

If a receiver detects the CloudEvents media type, but with an event format that
it cannot handle, for instance `application/cloudevents+avro`, it MAY still
treat the event as binary and forward it to another party as-is.

### 3.1. Binary Content Mode

The *binary* content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1. AMQP content-type

For the *binary* mode, the AMQP `content-type` property field value maps
directly to the CloudEvents `contenttype` attribute.

#### 3.1.2. Event Data Encoding

The [`data` attribute](#22-data-attribute) byte-sequence is used as the AMQP
[application-data][data] section.

#### 3.1.3. Metadata Headers

All [CloudEvents][CE] attributes with exception of `contenttype` and `data`
are individually mapped to and from the AMQP
[application-properties][app-properties] section.

##### 3.1.3.1 AMQP Application Property Names

Cloud Event attributes are prefixed with "cloudEvents:" for use in the
[application-properties][app-properties] section.

Examples:

    * `eventtime` maps to `cloudEvents:eventtime`
    * `eventid` maps to `cloudEvents:eventid`
    * `cloudeventsversion` maps to `cloudEvents:cloudeventsversion`

##### 3.1.3.2 AMQP Application Property Values

The value for each AMQP application property is constructed from the respective
attribute's AMQP type representation, compliant with the [AMQP event
format][AMQP-format] specification.

#### 3.1.4 Examples

This example shows the *binary* mode mapping of an event into the 
[bare message][message-format] sections of AMQP:

``` text
--------------- properties ------------------

to: myqueue
content-type: application/json; charset=utf-8

----------- application-properties -----------

cloudEvents:cloudeventsversion: "0.1"
cloudEvents:eventtype: "com.example.someevent"
cloudEvents:eventtime: "2018-04-05T03:56:24Z"
cloudEvents:eventid: "1234-1234-1234"
cloudEvents:source: "/mycontext/subcontext"
       .... further attributes ...

------------- application-data ---------------

{
    ... application data ...
}

----------------------------------------------
```

### 3.2. Structured Content Mode

The *structured* content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple transports.

#### 3.2.1. AMQP Content-Type

The [AMQP `content-type`][content-type] property field is set to the media type
of an [event format](#14-event-formats).

Example for the [JSON format][JSON-format]:

``` text
content-type: application/cloudevents+json; charset=UTF-8
```

#### 3.2.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
including the `data` attribute, are represented.

The event metadata and data is then rendered in accordance with the event
format specification and the resulting data becomes the AMQP application 
[data][data] section.

#### 3.2.3. Metadata Headers

Implementations MAY include the same AMQP application-properties as defined for
the [binary mode](#313-metadata-headers).

#### 3.2.4 Examples

This example shows a JSON event format encoded event:

``` text
--------------- properties ------------------------------

to: myqueue
content-type: application/cloudevents+json; charset=utf-8

----------- application-properties ----------------------

------------- application-data --------------------------

{
    "cloudeventsversion" : "0.1",
    "eventtype" : "com.example.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

---------------------------------------------------------
```

## 4. References

- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC4627][RFC4627] The application/json Media Type for JavaScript Object
  Notation (JSON)
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange Format
- [OASIS-AMQP-1.0][OASIS-AMQP-1.0] OASIS Advanced Message Queuing Protocol (AMQP) Version 1.0

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[AMQP-format]: ./amqp-format.md
[data-section]: 3.2.6
[Content-Type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC4627]: https://tools.ietf.org/html/rfc4627
[RFC6839]: https://tools.ietf.org/html/rfc6839#section-3.1
[RFC7159]: https://tools.ietf.org/html/rfc7159
[OASIS-AMQP-1.0]: http://docs.oasis-open.org/amqp/core/v1.0/amqp-core-overview-v1.0.html
[message-format]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#section-message-format
[data]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-data
[app-properties]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-application-properties