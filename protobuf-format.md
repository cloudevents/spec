# Protobuf Event Format for CloudEvents - Version 1.0

## Abstract

[Protocol Buffers][proto-home] is a mechanism for marshalling structured data,
this document defines how CloudEvents are represented using [version 3][proto-3]
of that specification.

In this document the terms *Protocol Buffers*, *protobuf*, and *proto* are used
interchangeably.

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Data](#3-data)
4. [Transport](#4-transport)
5. [Examples](#5-examples)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are are represented using
a protobuf schema.

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes for use as protobuf message
properties.

The [Data](#3-data) section describes how the event payload is carried.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2 Content-Type

There is no official IANA *media-type* designation for protobuf, as such this
specification uses 'application/x-protobuf' to identify such content.

## 2. Attributes

This section defines how CloudEvents attributes are represented in the protobuf
[schema][proto-schema].

## 2.1 Type System

The CloudEvents type system is mapped to protobuf as follows :

| CloudEvents   | protobuf |
| ------------- | ---------------------------------------------------------------------- |
| Boolean       | [boolean][proto-scalars] |
| Integer       | [sint32][proto-scalars] |
| String        | [string][proto-scalars] |
| Binary        | [bytes][proto-scalars] |
| URI           | [string][proto-scalars] following [RFC 3986 §4.3][rfc3986-section43]|
| URI-reference | [string][proto-scalars] following [RFC 3986 §4.1][rfc3986-section41] |
| Timestamp     | [Timestamp][proto-timestamp]  |

## 2.3 Required Attributes

Required attributes are represented explicitly as protobuf fields.

## 2.4 Optional Attributes & Extensions

Optional and extension attributes are represented using a map construct enabling
direct support of the CloudEvent [type system][ce-types].

```proto
map<string, CloudEventAttribute> attributes = 1;

message CloudEventAttribute {

    oneof attr_oneof {
      bool ce_boolean = 1;
      sfixed32 ce_integer = 2;
      string ce_string = 3;
      bytes ce_binary = 4;
      string ce_uri = 5;
      string ce_uri_reference = 6;
      google.protobuf.Timestamp ce_timestamp = 7;
    }
}
```

In this model an attribute's name is used as the map *key* and is
associated with its *value* stored in the appropriately typed property.

This approach allows for attributes to be represented and transported
with no loss of *type* information.

## 3. Data

The specification allows for data payloads of the following types to be explicitly represented:

* string
* bytes
* protobuf object/message

```proto
oneof data_oneof {

    // Binary data
    bytes binary_data = 2;

    // String data
    string text_data = 3;

    // Protobuf Message data
    google.protobuf.Any proto_data = 4;
}
```

Before encoding, a protobuf serializer MUST first determine the runtime data type
of the content. This can be determined by examining the data for invalid UTF-8
sequences or by consulting the `datacontenttype` attribute.

* Where the data is a protobuf message it MUST be stored in the `proto_data`
property.
* If the implementation determines that the type of the data is text, the value
MUST be stored in the `text_data` property.
* If the implementation determines that the type of the data is binary, the value
MUST be stored in the `binary_data` property.

## 4. Transport

Transports that support content identification MUST use the following designation:

```text
   application/cloudevents+x-protobuf
```

## 5. Examples

The following code-snippets show how proto representations might be constucted asuming the availability of some convenience methods ...

### 5.1 Plain Text event data

```java
public static Spec.CloudEvent plainTextExample() {
  Spec.CloudEvent.Builder ceBuilder = Spec.CloudEvent.newBuilder();

  ceBuilder
    //-- Required Attributes.
    .setId(UUID.randomUUID().toString())
    .setSpecVersion("1.0")
    .setType("io.cloudevent.example")
    .setSource("producer-1")

    //-- Data.
    .setTextData("This is a plain text message");

    //-- Optional Attributes
    withCurrentTime(ceBuilder, "time");
    withAttribute(ceBuilder, "datacontenttype", "text/plain");

    // Build it.
    return ceBuilder.build();
}

```

### 5.2 Proto message as event data

Where the event data payload is itself a protobuf message (with its own schema)
a protocol buffer idiomatic method can be used to carry the data.

```java
private static Spec.CloudEvent protoExample() {

  //-- Build an event data protobuf object.
  Test.SomeData.Builder dataBuilder = Test.SomeData.newBuilder();

  dataBuilder
    .setSomeText("this is an important message")
    .setIsImportant(true);

  //-- Build the CloudEvent.
  Spec.CloudEvent.Builder ceBuilder = Spec.CloudEvent.newBuilder();

    ceBuilder
      .setId(UUID.randomUUID().toString())
      .setSpecVersion("1.0")
      .setType("io.cloudevent.example")
      .setSource("producer-2")

      // Add the proto data into the CloudEvent envelope
      .setProtoData(Any.pack(dataBuilder.build()));

      //-- Done.
      return ceBuilder.build();

   }
```

## References

* [Protocol Buffer 3 Specification][proto-3]
* [CloudEvents Protocol Buffers format schema][proto-schema]

[Proto-3]: https://developers.google.com/protocol-buffers/docs/reference/proto3-spec
[proto-home]: https://developers.google.com/protocol-buffers
[proto-scalars]: https://developers.google.com/protocol-buffers/docs/proto3#scalar
[proto-wellknown]: https://developers.google.com/protocol-buffers/docs/reference/google.protobuf
[proto-timestamp]: https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Timestamp
[proto-schema]: ./spec.proto
[json-format]: ./json-format.md
[ce]: ./spec.md
[ce-types]: ./spec.md#type-system
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986-section41]: https://tools.ietf.org/html/rfc3986#section-4.1
[rfc3986-section43]: https://tools.ietf.org/html/rfc3986#section-4.3
[rfc3339]: https://tools.ietf.org/html/rfc3339
