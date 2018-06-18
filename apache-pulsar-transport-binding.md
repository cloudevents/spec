# Pulsar Transport Binding for CloudEvents

## Abstract

The [Apache Pulsar][PULSAR] Transport Binding for CloudEvents defines how events
are mapped to [Apache Pulsar messages][PULSAR-MSG-PROTO].

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to Apache Pulsar](#12-relation-to-apache-pulsar)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)
2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)
- 2.1. [contentType Attribute](#21-contenttype-attribute)
- 2.2. [data Attribute](#22-data-attribute)
3. [Apache Pulsar Message Mapping](#3-apache-pulsar-message-mapping)
- 3.1. [Binary Content Mode](#31-binary-content-mode)
- 3.2. [Structured Content Mode](#32-structured-content-mode)
4. [References](#4-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be used in
[Apache Pulsar messages][PULSAR-MSG-PROTO].

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to Apache Pulsar

This specification does not prescribe rules constraining transfer or settlement
of event messages with Apache Pulsar; it solely defines how CloudEvents are
expressed in the Apache Pulsar protocol as client messages that are produced
and consumed.

### 1.3. Content Modes

The specification defines two content modes for transferring events:
*structured* and *binary*. Each compliant implementation SHOULD support both modes.

In the *structured* content mode, event metadata attributes and event data are
placed into the Apache Pulsar message payload using an
[event format](#14-event-formats).

In the *binary* content mode, the value of the event `data` attribute is placed
into the Apache Pulsar message payload as-is; all event metadata attributes are
mapped to Apache Pulsar application-defined properties section.

### 1.4. Event Formats

Event formats, used with the *structured* content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][JSON-format].

### 1.5. Security

This specification does not introduce any new security features for
Apache Pulsar, or mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][CE] event
attributes.

One event attribute, `data` is handled specially and mapped onto Apache Pulsar
constructs, all other attributes are transferred as application-specific
properties without future interpretation.

This mapping is intentionally robust against changes, including the addition
and removal of event attributes, and also accommodates vendor extensions to
the event metadata. Any mention of event attributes other than `data` is
exemplary.

### 2.1. contentType Attribute

The `contentType` attribute is assumed to contain a media-type expression
compliant with [RFC2046][RFC2046].

### 2.2. data Attribute

The `data` attribute is assumed to contain opaque application data that is
encoded as declared by the `contentType` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into Apache Pulsar as defined
in this specification, the assumption is that the `data` attribute value is
made available as a sequence of bytes.

For instance, if the declared `contentType` is
`application/json;charset=utf-8`, the expectation is that the `data` attribute
value is made available as [UTF-8][RFC3629] encoded JSON text.

## 3. Apache Pulsar Message Mapping
The content mode is chosen by the sender of the event, which is either the
requesting or the responding party. Protocol interaction patterns that might
allow solicitation of events using a particular content mode might be defined
by an application, but are not defined here.

The receiver of the event can distinguish between the two modes by inspecting
the `CE-ContentType` property value. If the value exists and is prefixed with
the CloudEvents media type `application/cloudevents`, indicating the use of a
known [event format](#14-event-formats), the receiver uses *structured* mode,
otherwise it defaults to *binary* mode.

If a receiver detects the CloudEvents media type, but with an event format that
it cannot handle, for instance `application/cloudevents+avro`, it MAY still
treat the event as binary and forward it to another party as-is.

The *structured* content mode keeps event metadata and data together, allowing
simple forwarding of the same event across multiple routing hops, and across
multiple transports.

### 3.1 Binary Content Mode

The *binary* content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1 Event Data Encoding

The `data` attribute byte-sequence is used as the Apache Pulsar message payload.

#### 3.1.2 Application Properties

All [CloudEvents][CE] attributes with exception of `data` are individually
mapped to and from the application properties section in Apache Pulsar messages.

##### 3.1.2.1 Property Names

The naming convention for the Pulsar application property mapping of attributes
is:
```
* Each attribute name MUST be prefixed with "CE-"
```

Examples:
```
* `eventID` maps to `CE-EventID`
* `cloudEventsVersion` maps to `CE-CloudEventsVersion`
* `schemaURI` maps to `CE-SchemaURI`
```

For the `extensions` attribute, each entry of the `extensions` map is mapped to
a separate application property. The `extensions` attribute itself is not mapped
to an application property.

The naming convention for the `extensions` application property mapping of
attributes is:
```
* Each property name MUST be prefixed with "CE-X-"
```

Examples:
```
* `example` maps to `CE-X-Example`
* `testExtension` maps to `CE-X-TestExtension`
```
Note: per Apache Pulsar protocol, property names are case-sensitive.

##### 3.1.2.2 Property Values

The value for each Pulsar property is constructed from the respective
attribute's [JSON value][RFC7159] representation, compliant with the
[JSON event format][JSON-format] specification.

#### 3.1.3 Examples

This example shows the *binary* mode mapping of an event with an Apache Pulsar
message:

``` text
--------------- message metadata ------------------

properties: {
    "CE-CloudEventsVersion": "0.1"
    "CE-EventType": "org.apache.pulsar.someevent"
    "CE-EventTime": "2018-04-05T03:56:24Z"
    "CE-EventID": "adcd-abcd-abcd"
    "CE-Source": "/mycontext/subcontext"
}
... other pulsar message metadata fields

--------------- payload ---------------------------

{
    ... application data ...
}

```

### 3.2 Structured Content Mode

The *structured* content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple transports.

#### 3.2.1 Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
including the `data` attribute, are represented.

The event metadata and data MUST then be rendered in accordance with the event
format specification and the resulting data becomes the payload.

#### 3.2.2 Application Properties

Implementations MAY include the same Apache Pulsar application properties as
defined for the [binary mode][#312-application-properties].

#### 3.2.3 Example

This example shows a JSON event format encoded event:.

``` text
--------------- message metadata ------------------

... pulsar message metadata fields

--------------- payload ---------------------------

{
    "cloudEventsVersion" : "0.1",
    "eventType" : "org.apache.pulsar.someevent",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

-----------------------------------------------
```

## 4. References

- [Apache Pulsar][PULSAR] A distributed pub-sub messaging system
- [PULSAR-MSG-PROTO][PULSAR-MSG-PROTO] The Apache Pulsar messaging protocol
- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange
  Format

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[PULSAR]: https://pulsar.incubator.apache.org/
[PULSAR-MSG-PROTO]: https://pulsar.incubator.apache.org/docs/latest/project/BinaryProtocol/#Messagemetadata-9cce0q
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC7159]: https://tools.ietf.org/html/rfc7159
