# Protocol Buffers Event Format for CloudEvents  - Version 0.1

## Abstract

The Protocol Buffers Format for CloudEvents (CE) defines the encoding
of CloudEvents in the Protocol Buffers binary format.

## Status of this document

This document is a working draft.

## 1. Introduction

This specification defines how the [Context
Attributes](spec.md#context-attributes) defined in the CloudEvents
specification MUST be encoded in the protocol buffer binary
format. Transcoding to and from other formats (e.g. JSON) is out of
the scope of this document.

Protocol Buffers are a language-neutral, platform-neutral extensible
mechanism for serializing structured data. The [Google reference
implementation of Protocol
Buffers](https://github.com/protocolbuffers/protobuf) includes support
for an interface descriptor language (IDL), and this document makes
use of language level 3 IDL from Protocol Buffers v3.5.0. CloudEvents
systems using Protocol Buffers are not mandated to use the IDL or any
particular implementation of Protocol Buffers as long as they produce
messages which match the binary encoding defined by the IDL.


### 1.1. Conformance
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in
[RFC2119](https://tools.ietf.org/html/rfc2119).

## 2. Protocol Buffers format

Protocol Buffers provide a binary data serialization format which is
substantially more compact and efficient to parse when compared to XML
or JSON, along with a variety of language-specific libraries to
perform automatic serialization and deserialization. The [Protocol
Buffers specification defines a well-known encoding
format](https://developers.google.com/protocol-buffers/docs/encoding)
which is the basis of this specification. This specification is
described using the Protocol Buffers project IDL for readability, but
the ultimate basis of this specification is the Protocol Buffers
binary encoding.


### 2.1 Definition

Users of Protocol Buffers MUST use a message whose binary encoding is
identical to the one described by the [CloudEventMap
message](./cloudevent.proto):

```proto
syntax = "proto3";

package io.cloudevents;

// allows a map to appear inside `oneof`
message CloudEventMap {
  map<string, CloudEventAny> value = 1;
}

message CloudEventAny {
  oneof value {
    string string_value = 1;
    bytes binary_value = 2;
    uint32 int_value = 3;
    CloudEventMap map_value = 4;
  }
}
```

The CloudEvents type system MUST be mapped into the fields of
`CloudEventAny` as follows:


| CloudEvents  | CloudEventAny field
|--------------|-------------------------------------------------------------
| String       | string_value
| Binary       | binary_value
| URI          | string_value (string expression conforming to URI-reference as defined in [RFC 3986 §4.1](https://tools.ietf.org/html/rfc3986#section-4.1))
| Timestamp    | string_value (string expression as defined in [RFC 3339](https://tools.ietf.org/html/rfc3339))
| Map          | map_value
| Integer      | int_value
| Any          | Not applicable. Any is the enclosing CloudEventAny message itself

Protocol Buffer representations of CloudEvents MUST use the media type `application/cloudevents+proto`.

## 3. Examples

Below is an example of how to create a CloudEvent Protocol Buffer
message using the Java Google Protocol Buffers library:

```java
import com.google.common.base.Charsets;
import com.google.protobuf.ByteString;


CloudEventMap event = CloudEventMap.newBuilder()
  .putValue(
    "type",
    CloudEventAny.newBuilder()
      .setStringValue("com.example.emitter.event")
      .build())
  .putValue(
    "specversion",
    CloudEventAny.newBuilder()
      .setStringValue("0.1")
      .build())
  .putValue(
    "time",
    CloudEventAny.newBuilder()
      .setStringValue("2018-10-25T00:00:00+00:00")
      .build())
  .putValue(
    "source",
    CloudEventAny.newBuilder()
      .setStringValue("com.example.source.host1")
      .build())
  .putValue(
    "comExampleCustomextension",
    CloudEventAny.newBuilder()
      .setStringValue("some value for the extension")
      .build())
  .putValue(
    "data",
    CloudEventAny.newBuilder()
      .setBinaryValue(ByteString.copyFrom("a binary string", Charsets.UTF_8))
      .build())
  .build();
```
