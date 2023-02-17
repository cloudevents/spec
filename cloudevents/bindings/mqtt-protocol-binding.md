# MQTT Protocol Binding for CloudEvents - Version 1.0.3-wip

## Abstract

The MQTT Protocol Binding for CloudEvents defines how events are mapped to MQTT
3.1.1 ([OASIS][oasis-mqtt-3.1.1]; ISO/IEC 20922:2016) and MQTT 5.0
([OASIS][oasis-mqtt-5]) messages.

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to MQTT](#12-relation-to-mqtt)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Event Formats](#14-event-formats)
- 1.5. [Security](#15-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

- 2.1. [datacontenttype Attribute](#21-datacontenttype-attribute)
- 2.2. [data](#22-data)

3. [MQTT PUBLISH Message Mapping](#3-mqtt-publish-message-mapping)

- 3.2. [Binary Content Mode](#31-binary-content-mode)
- 3.1. [Structured Content Mode](#32-structured-content-mode)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be used in MQTT PUBLISH
([3.1.1][3-publish], [5.0][5-publish]) messages.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to MQTT

This specification does not prescribe rules constraining transfer or settlement
of event messages with MQTT; it solely defines how CloudEvents are expressed as
MQTT PUBLISH messages ([3.1.1][3-publish], [5.0][5-publish]).

### 1.3. Content Modes

The CloudEvents specification defines three content modes for transferring
events: _structured_, _binary_ and _batch_. The MQTT protocol binding does not
currently support the batch content mode. Every compliant implementation SHOULD
support both structured and binary modes.

The _binary_ mode _only_ applies to MQTT 5.0, because of MQTT 3.1.1's lack of
support for custom metadata.

In the _structured_ content mode, event metadata attributes and event data are
placed into the MQTT PUBLISH message payload section using an
[event format](#14-event-formats).

In the _binary_ content mode, the value of the event `data` is placed
into the MQTT PUBLISH message's payload section as-is, with the
`datacontenttype` attribute value declaring its media type in the MQTT
PUBLISH message's [`Content Type`][5-content-type] property; all other
event attributes are mapped to User Property fields.

### 1.4. Event Formats

Event formats, used with the _structured_ content mode, define how an event is
expressed in a particular data format. All implementations of this specification
that support the _structured_ content mode MUST support the [JSON event
format][json-format].

### 1.5. Security

This specification does not introduce any new security features for MQTT, or
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

### 2.2. data

`data` is assumed to contain opaque application data that is
encoded as declared by the `datacontenttype` attribute.

An application is free to hold the information in any in-memory representation
of its choosing, but as the value is transposed into MQTT as defined in this
specification, the assumption is that the `data` value is made
available as a sequence of bytes.

For instance, if the declared `datacontenttype` is
`application/json;charset=utf-8`, the expectation is that the `data`
value is made available as [UTF-8][rfc3629] encoded JSON text for use in MQTT.

## 3. MQTT PUBLISH Message Mapping

With MQTT 5.0, the content mode is chosen by the sender of the event. Protocol
usage patterns that might allow solicitation of events using a particular
content mode might be defined by an application, but are not defined here.

The receiver of the event can distinguish between the two content modes by
inspecting the`Content Type` property of the MQTT PUBLISH message. If the value
of the `Content Type` property is prefixed with the CloudEvents media type
`application/cloudevents`, indicating the use of a known
[event format](#14-event-formats), the receiver uses _structured_ mode,
otherwise it defaults to _binary_ mode.

If a receiver finds a CloudEvents media type as per the above rule, but with an
event format that it cannot handle, for instance `application/cloudevents+avro`,
it MAY still treat the event as binary and forward it to another party as-is.

When the `Content Type` header value is not prefixed with the CloudEvents media
type, knowing when the message ought to be parsed as a CloudEvent can be a
challenge. While this specification can not mandate that senders do not include
any of the CloudEvents properties when the message is not a CloudEvent, it would
be reasonable for a receiver to assume that if the message has all of the
mandatory CloudEvents attributes as message properties then it's probably a
CloudEvent. However, as with all CloudEvent messages, if it does not adhere to
all of the normative language of this specification then it is not a valid
CloudEvent.

With MQTT 3.1.1, the content mode is always _structured_ and the message payload
MUST use the [JSON event format][json-format].

### 3.1. Binary Content Mode

The _binary_ content mode accommodates any shape of event data, and allows for
efficient transfer and without transcoding effort.

#### 3.1.1. MQTT PUBLISH Content Type

For the _binary_ mode, the MQTT PUBLISH message's
[`Content Type`][5-content-type] property MUST be mapped directly to the
CloudEvents `datacontenttype` attribute.

#### 3.1.2. Event Data Encoding

The [`data`](#22-data) byte-sequence MUST be used as the
payload of the MQTT PUBLISH message.

#### 3.1.3. Metadata Headers

All other [CloudEvents][ce] context attributes, including extensions, MUST be
individually mapped to and from the User Property fields in the MQTT
PUBLISH message.

CloudEvents extensions that define their own attributes MAY define a secondary
mapping to MQTT user properties or features for those attributes, especially if
specific attributes need to align with MQTT features, or with other
specifications that have explicit MQTT header bindings. However, they MUST
also include the previously defined primary mapping.

##### 3.1.3.1 User Property Names

CloudEvents attribute names MUST be used unchanged in each mapped User Property
in the MQTT PUBLISH message.

##### 3.1.3.2 User Property Values

The value for each MQTT PUBLISH User Property MUST be constructed from the
respective CloudEvents attribute type's [canonical string
representation][ce-types].

#### 3.1.4 Examples

This example shows the _binary_ mode mapping of an event into the MQTT 5.0
PUBLISH message. The CloudEvents `datacontenttype` attribute is mapped to the
MQTT PUBLISH `Content Type` field; all other CloudEvents attributes are mapped
to MQTT PUBLISH User Property fields. The `Topic name` is chosen by the MQTT
client and not derived from the CloudEvents event data.

Mind that `Content Type` here does refer to the event `data` content carried in
the payload.

```text
------------------ PUBLISH -------------------

Topic Name: mytopic
Content Type: application/json; charset=utf-8

------------- User Properties ----------------

specversion: 1.0
type: com.example.someevent
time: 2018-04-05T03:56:24Z
id: 1234-1234-1234
source: /mycontext/subcontext
datacontenttype: application/json; charset=utf-8
       .... further attributes ...

------------------ payload -------------------

{
    ... application data ...
}

-----------------------------------------------
```

### 3.2. Structured Content Mode

The _structured_ content mode keeps event metadata and data together in the
payload, allowing simple forwarding of the same event across multiple routing
hops, and across multiple protocols. This is the only supported mode for MQTT
3.1.1

#### 3.2.1. MQTT Content Type

For MQTT 5.0, the [MQTT PUBLISH message's `Content Type`][5-content-type]
property MUST be set to the media type of an [event format](#14-event-formats).
For MQTT 3.1.1, the media type of the [JSON event format][json-format] is always
implied:

Example for the [JSON format][json-format]:

```text
content-type: application/cloudevents+json; charset=utf-8
```

#### 3.2.2. Event Data Encoding

The chosen [event format](#14-event-formats) defines how all attributes,
and `data`, are represented.

The event metadata and data MUST then be rendered in accordance with the event
format specification and the resulting data becomes the MQTT PUBLISH payload.

#### 3.2.3. Metadata Headers

For MQTT 5.0, implementations MAY include the same MQTT PUBLISH User Properties
as defined for the [binary mode](#313-metadata-headers).

#### 3.2.4. Examples

The first example shows a JSON event format encoded event with MQTT 5.0

```text
------------------ PUBLISH -------------------

Topic Name: mytopic
Content Type: application/cloudevents+json; charset=utf-8

------------------ payload -------------------

{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
	"time" : 2018-04-05T03:56;24Z,
	"id" : 1234-1234-1234,
	"source" : "/mycontext/subcontext",
	"datacontenttype" : "application/json; charset=utf-8",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

-----------------------------------------------
```

For MQTT 3.1.1, the example looks nearly identical, but `Content Type` is absent
because not yet supported in that version of the MQTT specification and
therefore `application/cloudevents+json` is implied:

```text
------------------ PUBLISH -------------------

Topic Name: mytopic

------------------ payload -------------------

{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
	"time" : 2018-04-05T03:56;24Z,
	"id" : 1234-1234-1234,
	"source" : "/mycontext/subcontext",
	"datacontenttype" : "application/json; charset=utf-8",

    ... further attributes omitted ...

    "data" : {
        ... application data ...
    }
}

-----------------------------------------------
```

## 4. References

- [MQTT 3.1.1][oasis-mqtt-3.1.1] MQTT Version 3.1.1
- [MQTT 5.0][oasis-mqtt-5] MQTT Version 5.0
- [RFC2046][rfc2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC3629][rfc3629] UTF-8, a transformation format of ISO 10646
- [RFC4627][rfc4627] The application/json Media Type for JavaScript Object
  Notation (JSON)
- [RFC7159][rfc7159] The JavaScript Object Notation (JSON) Data Interchange
  Format

[ce]: ../spec.md
[ce-types]: ../spec.md#type-system
[json-format]: ../formats/json-format.md
[oasis-mqtt-3.1.1]: http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html
[oasis-mqtt-5]: http://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
[3-publish]: http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/errata01/os/mqtt-v3.1.1-errata01-os-complete.html#_Toc442180850
[5-content-type]: http://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html#_Toc502667341
[5-publish]: https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901100
[json-value]: https://tools.ietf.org/html/rfc7159#section-3
[rfc2046]: https://tools.ietf.org/html/rfc2046
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3629]: https://tools.ietf.org/html/rfc3629
[rfc4627]: https://tools.ietf.org/html/rfc4627
[rfc7159]: https://tools.ietf.org/html/rfc7159
