# OpenMessaging Transport Binding for CloudEvents

## Abstract

The [OpenMessaging][OpenMessaging] Transport Binding for CloudEvents defines how
events are mapped to [OpenMessaging Specification][OpenMessaging-Spec].


## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to OpenMessaging](#12-relation-to-openmessaging)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)
2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)
- 2.1. [contentType Attribute](#21-contenttype-attribute)
- 2.2. [data Attribute](#22-data-attribute)
3. [OpenMessaging Message Mapping](#3-openmessaging-message-mapping)
- 3.2. [Binary Content Mode](#31-binary-content-mode)
- 3.1. [Structured Content Mode](#32-structured-content-mode)
4. [References](#4-references)

## 1. Introduction

This specification defines how
the elements defined in the CloudEvents specification are to be used in
[OpenMessaging][OpenMessaging]. 

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to OpenMessaging

This specification does not prescribe rules constraining transfer or settlement
of event messages with [OpenMessaging][OpenMessaging]; it solely defines how 
CloudEvents are expressed with [OpenMessaging 
Specification][OpenMessaging-Spec].    

OpenMessaging-based messaging and eventing infrastructures may provide
higher-level programming-level abstractions although OpenMessaging provides 
optional core APIs, but they all follow the schema of the messages
provided by OpenMessaging Specification. This specification uses OpenMessaging
terminology, and implementers can refer the respective infrastructure's 
OpenMessaging documentation to determine the mapping into a programming-level 
abstraction.


### 1.3. Content Modes

This specification defines two content modes for transferring events:
*structured* and *binary*. Every compliant implementation SHOULD support both
modes.

In the *structured* content mode, event metadata attributes and event data are
placed into the OpenMessaging message's application data section using an 
[event format](#14-event-formats).

In the *binary* content mode, the value of the event `data` attribute is placed
into message body, with the `contentType` attribute
value declaring its media type; all other event attributes are 
mapped [OpenMessaging properties][OpenMessaging-Spec]

### 1.4. Event Formats

Event formats, used with the *stuctured* content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][JSON-format], as well as 
the [OpenMessaging event format][OpenMessaging-format] for the 
[properties][OpenMessaging-Spec]
section, but MAY support any additional, including proprietary, formats.

### 1.5. Security

This specification does not introduce any new security features for 
OpenMessaging, or mandate specific existing features to be used. This 
specification applies identically to [SSL]([RFC6101][RFC6101]).

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

Two of the event attributes, `contentType` and `data` are handled specially
and mapped onto OpenMessaging constructs, all other attributes are transferred
as metadata without further interpretation.

This mapping is intentionally robust against changes, including the addition 
and removal of event attributes, and also accommodates vendor extensions to the 
event metadata. Any mention of event attributes other than contentType and data 
is exemplary.


### 2.1. contentType Attribute

The `contentType` attribute is assumed to contain a media-type expression
compliant with [RFC2046][RFC2046].

### 2.2. data Attribute

The `data` attribute is assumed to contain opaque application data that is
encoded as declared by the `contentType` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into OpenMessaging as defined 
in this specification, the assumption is that the `data` attribute value is made
available as a sequence of bytes.

For instance, if the declared `contentType` is
`application/json;charset=utf-8`, the expectation is that the `data` attribute
value is made available as [UTF-8][RFC3629] encoded JSON text for use in
OpenMessaging.


## 3. OpenMessaging Message Mapping

With OpenMessaging, the content mode is chosen by the sender of the event. 
Protocol usage patterns that might allow solicitation of events using a 
particular content mode might be defined by an application, but are not 
defined here.

The receiver of the event can distinguish between the two content modes by
inspecting the`contentType` property  in the *properties* of the OpenMessaging 
message. If the value is prefixed with the CloudEvents media type 
application/cloudevents, 
indicating the use of a known event format, the receiver uses structured mode, 
otherwise it defaults to binary mode.

If a receiver detects the CloudEvents media type, but with an event format that 
it cannot handle, for instance application/cloudevents+avro, it MAY still treat 
the event as binary and forward it to another party as-is.


### 3.1. Binary Content Mode

The *binary* content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1. OpenMessaging contentType

For the *binary* mode, the  `contentType`  property field value maps directly to
the CloudEvents `contentType` attribute.

#### 3.1.2. Event Data Encoding

The [`data` attribute](#22-data-attribute) byte-sequence is used as the 
[OpenMessaging data][OpenMessaging-Spec] section.

#### 3.1.3. Metadata Headers

All [CloudEvents][CE] attributes with exception of `contentType` and `data`
MUST be individually mapped to and from the *properties* section.

##### 3.1.3.1 OpenMessaging Properties Names


Cloud Event attributes are prefixed with "cloudEvents:" for use in the
[properties][OpenMessaging-Spec] section.

Examples:

* `eventTime` maps to `cloudEvents:eventTime`
* `eventID` maps to `cloudEvents:eventID`
* `cloudEventsVersion` maps to `cloudEvents:cloudEventsVersion`

##### 3.1.3.2 OpenMessaging Properties Values

The value for each OpenMessaging *properties* is constructed from the 
respective attribute's OpenMessaging type representation, compliant with the
[OpenMessaging event format][OpenMessaging-format] specification.

#### 3.1.4 Examples

This example shows the *binary* mode mapping of an event into the
OpenMessaging message. All CloudEvents attributes are mapped to OpenMessaging
*properties* section fields. Mind that `contentType` here does refer to the 
event `data` content carried in the payload.

``` text
------------- headers -------------------
destination: mytopic

------------- properties ----------------
contentType: application/json; charset=utf-8
cloudEvents:cloudEventsVersion: "0.1"
cloudEvents:eventType: "com.example.someevent"
cloudEvents:eventTime: "2018-09-05T03:56:24Z"
cloudEvents:eventID: "1234-1234-1234"
cloudEvents:source: "/mycontext/subcontext"
       .... further attributes ...

------------------ data -------------------

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

The OpenMessaging `contentType` field in *properties* section is set to the 
media type of an [event format](#14-event-formats).


Example for the [JSON format][JSON-format]:

``` text
content-type: application/cloudevents+json; charset=UTF-8
```

#### 3.2.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
including the `data` attribute, are represented.

The event metadata and data MUST then be rendered in accordance with the event
format specification and the resulting data becomes the OpenMessaging payload.

#### 3.2.3. Metadata Headers

For OpenMessaging, implementations MAY include the same *properties* as defined 
for the [binary mode](#313-metadata-headers).

#### 3.2.4. Examples

The first example shows a JSON event format encoded event with OpenMessaging:

``` text
------------------ headers -------------------
destination: mytopic

------------- properties ----------------
contentType: application/cloudevents+json; charset=utf-8

------------------ data -------------------

{
    "cloudEventsVersion" : "0.1",
    "eventType" : "io.openMessaging.event",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

-----------------------------------------------
```


## 4. References

- [OpenMessaging][OpenMessaging] The OpenMessaging System
- [OpenMessaging-Specification][OpenMessaging-Spec] OpenMessaging Specification
- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC6101][RFC6101] HTTP over TLS
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange Format

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[OpenMessaging-format]: ./openmessaging-format.md
[OpenMessaging]: https://github.com/openmessaging
[OpenMessaging-Spec]: https://github.com/openmessaging/specification/blob/master/specification-schema.md
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC6101]: https://tools.ietf.org/html/rfc6101
[RFC7159]: https://tools.ietf.org/html/rfc7159
