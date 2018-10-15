# MQTT Transport Binding for CloudEvents

## Abstract

The MQTT Transport Binding for CloudEvents defines how events are mapped to
MQTT 3.1.1 ([OASIS][OASIS-MQTT-3.1.1]; ISO/IEC 20922:2016) and MQTT 5.0
([OASIS][OASIS-MQTT-5]) messages.

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to MQTT](#12-relation-to-mqtt)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)
2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)
- 2.1. [contentType Attribute](#21-contenttype-attribute)
- 2.2. [data Attribute](#22-data-attribute)
3. [MQTT PUBLISH Message Mapping](#3-mqtt-publish-message-mapping)
- 3.2. [Binary Content Mode](#31-binary-content-mode)
- 3.1. [Structured Content Mode](#32-structured-content-mode)
4. [References](#4-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be used in
MQTT PUBLISH ([3.1.1][3-publish], [5.0][5-publish]) messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to MQTT

This specification does not prescribe rules constraining transfer or
settlement of event messages with MQTT; it solely defines how CloudEvents
are expressed as MQTT PUBLISH messages ([3.1.1][3-publish], [5.0][5-publish]).

### 1.3. Content Modes

The specification defines two content modes for transferring events:
*structured* and *binary*.

The *binary* mode *only* applies to MQTT 5.0, because of MQTT 3.1.1's lack of
support for custom metadata.

In the *structured* content mode, event metadata attributes and event data are
placed into the MQTT PUBLISH message payload section
using an [event format](#14-event-formats).

In the *binary* content mode, the value of the event `data` attribute is placed
into the MQTT PUBLISH message's payload section as-is, with
the `contentType` attribute value declaring its media type; all other event
attributes are mapped to the MQTT PUBLISH message's
[properties section][5-publish-properties].

### 1.4. Event Formats

Event formats, used with the *structured* content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][JSON-format].

MQTT 5.0 implementations MAY support any additional, including proprietary,
formats.

### 1.5. Security

This specification does not introduce any new security features for MQTT, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

Two of the event attributes, `contentType` and `data` are handled specially
and mapped onto MQTT constructs, all other attributes are transferred as
metadata without further interpretation.

This mapping is intentionally robust against changes, including the addition
and removal of event attributes, and also accommodates vendor extensions to the
event metadata. Any mention of event attributes other than `contentType` and
`data` is exemplary.

### 2.1. contentType Attribute

The `contentType` attribute is assumed to contain a [RFC2046][RFC2046]
compliant media-type expression.

### 2.2. data Attribute

The `data` attribute is assumed to contain opaque application data that is
encoded as declared by the `contentType` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into MQTT as defined in this
specification, the assumption is that the `data` attribute value is made
available as a sequence of bytes.

For instance, if the declared `contentType` is
`application/json;charset=utf-8`, the expectation is that the `data` attribute
value is made available as [UTF-8][RFC3629] encoded JSON text for use in
MQTT.

## 3. MQTT PUBLISH Message Mapping

With MQTT 5.0, the content mode is chosen by the sender of the event. Protocol
usage patterns that might allow solicitation of events using a particular
content mode might be defined by an application, but are not defined here.

The receiver of the event can distinguish between the two content modes by
inspecting the`Content Type` property of the MQTT PUBLISH message. If the value
of the `Content Type` property is prefixed with the CloudEvents media type
`application/cloudevents`, indicating the use of a known [event
format](#14-event-formats), the receiver uses *structured* mode, otherwise it
defaults to *binary* mode.

If a receiver finds a CloudEvents media type as per the above rule, but with an
event format that it cannot handle, for instance
`application/cloudevents+avro`, it MAY still treat the event as binary and
forward it to another party as-is.

With MQTT 3.1.1, the content mode is always *structured* and the message
payload MUST use the [JSON event format][JSON-format].

### 3.1. Binary Content Mode

The *binary* content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1. MQTT PUBLISH Content Type

For the *binary* mode, the MQTT PUBLISH message's [`Content
Type`][5-content-type] property MUST be mapped directly to the CloudEvents
`contentType` attribute.

#### 3.1.2. Event Data Encoding

The [`data` attribute](#22-data-attribute) byte-sequence MUST be used as the
payload of the MQTT PUBLISH message.

#### 3.1.3. Metadata Headers

All [CloudEvents][CE] attributes with exception of `contentType` and `data`
MUST be individually mapped to and from the User Property fields in the MQTT
PUBLISH message, with exceptions noted below.

CloudEvents extensions that define their own attributes MAY define a 
diverging mapping to MQTT user properties or features for those attributes, 
especially if specific attributes need to align with MQTT features, or with 
other specifications that have explicit MQTT header bindings.

An extension specification that defines a diverging mapping rule for MQTT,
and any revision of such a specification, MUST also define explicit mapping
rules for all other transport bindings that are part of the CloudEvents core at
the time of the submission or revision.

##### 3.1.3.1 User Property Names

CloudEvents attribute names MUST be used unchanged in each mapped User Property
in the MQTT PUBLISH message.

##### 3.1.3.2 User Property Values

The value for each MQTT PUBLISH User Property MUST be constructed from the
respective CloudEvents attribute's JSON type representation, compliant with the
[JSON event format][JSON-format] specification.

#### 3.1.4 Examples

This example shows the *binary* mode mapping of an event into the
MQTT 5.0 PUBLISH message. The CloudEvents `contentType` attribute
is mapped to the MQTT PUBLISH `Content Type` field; all other
CloudEvents attributes are mapped to MQTT PUBLISH User Property
fields. The `Topic name` is chosen by the MQTT client and not derived
from the CloudEvents event data.

Mind that `Content Type` here does refer to the event `data`
content carried in the payload.

``` text
------------------ PUBLISH -------------------

Topic Name: mytopic
Content Type: application/json; charset=utf-8

------------- User Properties ----------------

cloudEventsVersion: "0.1"
eventType: "com.example.someevent"
eventTime: "2018-04-05T03:56:24Z"
eventId: "1234-1234-1234"
source: "/mycontext/subcontext"
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
hops, and across multiple transports. This is the only supported mode for
MQTT 3.1.1

#### 3.2.1. MQTT Content Type

For MQTT 5.0, the [MQTT PUBLISH message's `Content Type`][5-content-type]
property MUST be set to the media type of an [event format](#14-event-formats). For
MQTT 3.1.1, the media type of the [JSON event format][JSON-format] is always
implied:

Example for the [JSON format][JSON-format]:

``` text
content-type: application/cloudevents+json; charset=utf-8
```

#### 3.2.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
including the `data` attribute, are represented.

The event metadata and data MUST then be rendered in accordance with the event
format specification and the resulting data becomes the MQTT PUBLISH payload.

#### 3.2.3. Metadata Headers

For MQTT 5.0, implementations MAY include the same MQTT PUBLISH User Properties
as defined for the [binary mode](#313-metadata-headers).

#### 3.2.4. Examples

The first example shows a JSON event format encoded event with MQTT 5.0

``` text
------------------ PUBLISH -------------------

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

For MQTT 3.1.1, the example looks nearly identical, but `Content Type`
is absent because not yet supported in that version of the MQTT specification
and therefore `application/cloudevents+json` is implied:

``` text
------------------ PUBLISH -------------------

Topic Name: mytopic

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

- [MQTT 3.1.1][OASIS-MQTT-3.1.1] MQTT Version 3.1.1
- [MQTT 5.0][OASIS-MQTT-5] MQTT Version 5.0
- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC4627][RFC4627] The application/json Media Type for JavaScript Object
  Notation (JSON)
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange Format

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[OASIS-MQTT-3.1.1]: http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html
[OASIS-MQTT-5]: http://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
[5-content-type]: http://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html#_Toc502667341 
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC4627]: https://tools.ietf.org/html/rfc4627