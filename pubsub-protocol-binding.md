# Pub/Sub Protocol Binding for CloudEvents - Version 1.0

## Abstract

The Pub/Sub Protocol Binding for CloudEvents defines how events are mapped to Pub/Sub
1.1 request and response messages.

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to Pub/Sub](#12-relation-to-pubsub)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

- 2.1. [datacontenttype Attribute](#21-datacontenttype-attribute)
- 2.2. [data Attribute](#22-data-attribute)

3. [Pub/Sub Message Mapping](#3-pub/sub-message-mapping)

- 3.1. [Binary Content Mode](#31-binary-content-mode)
- 3.2. [Structured Content Mode](#32-structured-content-mode)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be used in 
[Pub/Sub][pubsub] requests and response messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to Pub/Sub

Events can be produced using a Topic or consumed using Push or Pull based Subscriptions. 

### 1.3. Content Modes

The specification defines two content modes for transferring events:
_structured_ and _binary_.

In the _structured_ content mode, event metadata attributes and event data are
placed into the Pub/Sub message body section using an
[event format](#14-event-formats).

In the _binary_ content mode, the value of the event `data` attribute is placed
into the Pub/Sub payload data as-is, with the `datacontenttype`
attribute value declaring its media type; all other event attributes are mapped
to Pub/Sub attributes.

### 1.4. Event Formats

Event formats, used with the _structured_ content mode, define how an event is
expressed in a particular data format. All implementations of this
specification MUST support the [JSON event format][json-format], but MAY support
any additional, including proprietary, formats.

### 1.5. Security

This specification does not introduce any new security features for Pub/Sub, or
mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][ce] event
attributes.

This mapping is intentionally robust against changes, including the addition and
removal of event attributes, and also accommodates vendor extensions to the
event metadata.

### 2.1. datacontenttype Attribute

The `datacontenttype` attribute is assumed to contain a [RFC2046][rfc2046]
compliant media-type expression.

### 2.2. data Attribute

The `data` attribute is assumed to contain opaque application data that is
encoded as declared by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into a Pub/Sub message as defined 
in this specification, the assumption is that the `data` attribute value is made
available as a sequence of bytes.

For instance, if the declared `datacontenttype` is
`application/json;charset=utf-8`, the expectation is that the `data` attribute
value is made available as [UTF-8][rfc3629] encoded JSON text Pub/Sub message data.

## 3. Pub/Sub Message Mapping

With Pub/Sub, the content mode is chosen by the sender of the
event. Protocol usage patterns that might allow solicitation of events using a
particular content mode might be defined by an application, but are not defined
here.

The receiver of the event can distinguish between the two content modes by
inspecting the [Pub/Sub Attribute `Content-Type`][content-type] of the
[Pub/Sub message][pubsub-message]. If the attribute is present and its value is prefixed 
with the CloudEvents media type `application/cloudevents`, indicating the use of a known
[event format](#14-event-formats), the receiver uses _structured_ mode,
otherwise it defaults to _binary_ mode.

If a receiver finds a CloudEvents media type as per the above rule, but with an
event format that it cannot handle, for instance
`application/cloudevents+avro`, it MAY still treat the event as binary and
forward it to another party as-is.

### 3.1. Binary Content Mode

The _binary_ content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1. Content-Type

For the _binary_ mode, the [Pub/Sub Attribute `Content-Type`][content-type] of the 
[Pub/Sub message][pubsub-message] property, if present, MUST be mapped
directly to the CloudEvents `datacontenttype` attribute.

#### 3.1.2. Event Data Encoding

The [`data`](#22-data-attribute) byte-sequence MUST be used as the value of the Pub/Sub
message data payload.

#### 3.1.3. Metadata Attributes

All [CloudEvents][ce] attributes 
MUST be individually mapped to and from distinct Pub/Sub message attributes, with
exceptions noted below.

CloudEvents extensions that define their own attributes MAY define a diverging
mapping to Pub/Sub attributes for those attributes, especially if specific attributes
need to align with Pub/Sub features or with other specifications that have explicit
Pub/Sub attribute bindings.

An extension specification that defines a diverging mapping rule for Pub/Sub, and
any revision of such a specification, MUST also define explicit mapping rules
for all other transport bindings that are part of the CloudEvents core at the
time of the submission or revision.

##### 3.1.3.1 Pub/Sub Attribute Names

Except for attributes
[explicitly handled in this specification](#2-use-of-cloudevents-attributes),
the naming convention for the Pub/Sub attribute mapping of well-known CloudEvents
attributes is that each attribute name MUST be prefixed with "ce-".

Examples:

    * `time` maps to `ce-time`
    * `id` maps to `ce-id`
    * `specversion` maps to `ce-specversion`

Attribute names are case-insensitive.

##### 3.1.3.2 Pub/Sub Attribute Values

The value for each Pub/Sub attribute MUST be constructed from the respective
CloudEvents attribute type's [canonical string representation][ce-types].

#### 3.1.4 Examples

This example shows the _binary_ mode mapping of an event to a Pub/Sub Message:

```text
Publish /some-topic
--- Attributes ---
{
  "ce-specversion": "1.0",
  "ce-type": "com.example.someevent",
  "ce-time": "2020-03-10T03:56:24Z",
  "ce-id": "1234-1234-1234",
  "ce-source": "/mycontext/subcontext",
    .... further attributes ...
  "ce-datacontenttype": "application/json; charset=utf-8",
}
--- Data ---
{
    ... application data ...
}
```

### 3.2. Structured Content Mode

The _structured_ content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple transports.

#### 3.2.1. Content-Type

The [Pub/Sub Attribute `Content-Type`][content-type] MUST be set to the media type of
an [event format](#14-event-formats).

Example for the [JSON format][json-format]:

```text
"Content-Type": "application/cloudevents+json; charset=UTF-8"
```

#### 3.2.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
including the `data` attribute, are represented.

The event metadata and data is then rendered in accordance with the event format
specification and the resulting data becomes the Pub/Sub message data.

#### 3.2.3. Metadata Headers

Implementations MAY include the same Pub/sub attributes as defined for the
[binary mode](#313-metadata-headers).

All CloudEvents metadata attributes MUST be mapped into the payload, even if
they are also mapped into Pub/Sub attributes.

#### 3.2.4 Examples

This example shows the _structured_ mode mapping of an event to a Pub/Sub Message:

```text
Publish /some-topic
--- Attributes ---
{
  "Content-Type": "application/cloudevents+json; charset=utf-8",
}
--- Data ---
{
  "specversion": "0.3-wip",
  "type": "com.example.someevent",
  "time": "2018-04-05T03:56:24Z",
  "id": "1234-1234-1234",
  "source": "/mycontext/subcontext",
  "datacontenttype": "application/json; charset=utf-8",
    .... further attributes ...
  "data": {
    ... application data ...
  }
}
```

## 4. References

- [PUBSUB][pubsub] Google Cloud Pub/Sub
- [PUBSUB-MESSAGE][pubsub-message] The Google Cloud Pub/Sub message
- [RFC2046][rfc2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][rfc3629] UTF-8, a transformation format of ISO 10646
- [RFC3986][rfc3986] Uniform Resource Identifier (URI): Generic Syntax


[ce]: ./spec.md
[ce-types]: ./spec.md#type-system
[pubsub]: https://cloud.google.com/pubsub/
[pubsub-message]: https://cloud.google.com/pubsub/docs/reference/rest/v1/PubsubMessage
[json-format]: ./json-format.md
[content-type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[rfc2046]: https://tools.ietf.org/html/rfc2046
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3629]: https://tools.ietf.org/html/rfc3629
[rfc3986]: https://tools.ietf.org/html/rfc3986
