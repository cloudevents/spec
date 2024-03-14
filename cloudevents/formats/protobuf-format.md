# Protobuf Event Format for CloudEvents - Version 1.0.3-wip

## Abstract

[Protocol Buffers][proto-home] is a mechanism for marshalling structured data,
this document defines how CloudEvents are represented using [version 3][proto-3]
of that specification.

In this document the terms *Protocol Buffers*, *protobuf*, and *proto* are used
interchangeably.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Data](#3-data)
4. [Transport](#4-transport)
5. [Batch Format](#5-batch-format)
6. [Examples](#6-examples)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are represented using
a protobuf schema.

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvent attributes for use as protobuf message
properties.

The [Data](#3-data) section describes how the event payload is carried.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2 Content-Type

There is no official IANA *media-type* designation for protobuf, as such this
specification uses 'application/protobuf' to identify such content.

## 2. Attributes

This section defines how CloudEvents attributes are represented in the protobuf
[schema][proto-schema].

## 2.1 Type System

The CloudEvents type system is mapped to protobuf as follows :

| CloudEvents   | protobuf |
| ------------- | ---------------------------------------------------------------------- |
| Boolean       | [boolean][proto-scalars] |
| Integer       | [int32][proto-scalars] |
| String        | [string][proto-scalars] |
| Binary        | [bytes][proto-scalars] |
| URI           | [string][proto-scalars] following [RFC 3986 §4.3][rfc3986-section43]|
| URI-reference | [string][proto-scalars] following [RFC 3986 §4.1][rfc3986-section41] |
| Timestamp     | [Timestamp][proto-timestamp]  |

## 2.3 REQUIRED Attributes

REQUIRED attributes are represented explicitly as protobuf fields.

## 2.4 OPTIONAL Attributes & Extensions

OPTIONAL and extension attributes are represented using a map construct enabling
direct support of the CloudEvent [type system][ce-types].

```proto
map<string, CloudEventAttributeValue> attributes = 1;

message CloudEventAttributeValue {

    oneof attr {
      bool ce_boolean = 1;
      int32 ce_integer = 2;
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

This approach allows attributes to be represented and transported
with no loss of *type* information.

## 3. Data

The specification allows for data payloads of the following types to be explicitly represented:

* string
* bytes
* protobuf object/message

```proto
oneof data {

    // Binary data
    bytes binary_data = 2;

    // String data
    string text_data = 3;

    // Protobuf Message data
    google.protobuf.Any proto_data = 4;
}
```

* Where the data is a protobuf message it MUST be stored in the `proto_data` property.
  * `datacontenttype` MAY be populated with `application/protobuf`
  * `dataschema` SHOULD be populated with the type URL of the protobuf data message.

* When the type of the data is text, the value MUST be stored in the `text_data` property.
  * `datacontenttype` SHOULD be populated with the appropriate media-type.

* When the type of the data is binary the value MUST be stored in the `binary_data` property.
  * `datacontenttype` SHOULD be populated with the appropriate media-type.

## 4. Transport

Transports that support content identification MUST use the following designation:

```text
   application/cloudevents+protobuf
```

## 5. Batch Format

In the _Protobuf Batch Format_ several CloudEvents are batched into a single Protobuf
message. The message contains a repeated field filled with independent CloudEvent messages
in the structured mode Protobuf event format.

### 5.1 Envelope

The enveloping container is a _CloudEventBatch_ protobuf message containing a
repeating set of _CloudEvent_ message(s):

```proto
message CloudEventBatch {
  repeated CloudEvent events = 1;
}
```

### 5.2 Batch Media Type

A compliant protobuf batch representation is identifed using the following media-type

```text
   application/cloudevents-batch+protobuf
```

## 6. Examples

The following code-snippets show how proto representations might be constructed
assuming the availability of some convenience methods.

### 6.1 Plain Text event data

```java
public static CloudEvent plainTextExample() {
  CloudEvent.Builder ceBuilder = CloudEvent.newBuilder();

  ceBuilder
    //-- REQUIRED Attributes.
    .setId(UUID.randomUUID().toString())
    .setSpecVersion("1.0")
    .setType("io.cloudevent.example")
    .setSource("producer-1")

    //-- Data.
    .setTextData("This is a plain text message");

  //-- OPTIONAL Attributes
  withCurrentTime(ceBuilder, "time");
  withAttribute(ceBuilder, "datacontenttype", "text/plain");

  // Build it.
  return ceBuilder.build();
}

```

### 6.2 Proto message as event data

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
  CloudEvent.Builder ceBuilder = Spec.CloudEvent.newBuilder();

  ceBuilder
    .setId(UUID.randomUUID().toString())
    .setSpecVersion("1.0")
    .setType("io.cloudevent.example")
    .setSource("producer-2")

    // Add the proto data into the CloudEvent envelope.
    .setProtoData(Any.pack(dataBuilder.build()));

  // Add the protto type URL
  withAttribute(ceBuilder, "dataschema", ceBuilder.getProtoData().getTypeUrl());

  // Set Content-Type (OPTIONAL)
  withAttribute(ceBuilder, "datacontenttype", "application/protobuf");

  //-- Done.
  return ceBuilder.build();

}
```

## References

* [Protocol Buffer 3 Specification][proto-3]
* [CloudEvents Protocol Buffers format schema][proto-schema]

[proto-3]: https://developers.google.com/protocol-buffers/docs/reference/proto3-spec
[proto-home]: https://developers.google.com/protocol-buffers
[proto-scalars]: https://developers.google.com/protocol-buffers/docs/proto3#scalar
[proto-wellknown]: https://developers.google.com/protocol-buffers/docs/reference/google.protobuf
[proto-timestamp]: https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Timestamp
[proto-schema]: ./cloudevents.proto
[ce]: ../spec.md
[ce-types]: ../spec.md#type-system
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986-section41]: https://tools.ietf.org/html/rfc3986#section-4.1
[rfc3986-section43]: https://tools.ietf.org/html/rfc3986#section-4.3
[rfc3339]: https://tools.ietf.org/html/rfc3339
