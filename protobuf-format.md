# Protobuf Event Format for CloudEvents  - Version 0.1

## Abstract

The Protocol Buffers Format for CloudEvents (CE) defines
the encoding of events in the protocol buffers binary format.

## Status of this document

This document is a working draft.

## 1. Introduction

CloudEvents is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification
defines how the [Context
Attributes](spec.md#context-attributes)defined in the CloudEvents in
the protocol buffers binary encoding MUST BE encoded. Transcoding to
and from other formats (e.g. JSON) is out of the scope of this
proposal.

Protocol buffers are a language-neutral, platform-neutral extensible
mechanism for serializing structured data. The [Google reference
implementation of protobuf](PROTO) includes support for an interface
descriptor language (IDL), and this document makes use of language
level 3 IDL from Protocol Buffers v3.5.0. CloudEvents systems using
protocol buffers are not required to use the IDL or any particular
implementation of Protocol buffers as long as they produce messages
which match the binary encoding defined by the IDL.


### 1.1. Conformance
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in RFC2119.

## 2. Protocol Buffers format

Protocol buffers provide a binary data serialization format which is
substantially more compact and efficient to parse when compared to XML
or JSON, along with a variety of language-specific libraries to
perform automatic serialization and deserialization. The [protocol
buffers specification defines a well-known encoding
format](https://developers.google.com/protocol-buffers/docs/encoding)
which is the basis of this specification. Specifications below may be
written using the protocol buffers project IDL for readability, but
the ultimate basis of this specification is the protocol buffers
binary encoding.


### 2.1 Definition

Users of protocol buffers MUST use a message whose binary encoding is
identical to the one described by the CloudEventMap message:

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

The CloudEvents type system is mapped into the fields of CloudEventAny as follows:


| CloudEvents  | CloudEventAny field
|--------------|-------------------------------------------------------------
| String       | string_value
| Binary       | binary_value
| URI          | string_value (string expression conforming to URI-reference as defined in RFC 3986 §4.1)
| Timestamp    | string_value (string expression as defined in RFC 3339.)
| Map          | map_value
| Integer      | int_value
