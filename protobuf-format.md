# Protobuf Event Format for CloudEvents  - Version 0.1

## Abstract

The Protocol Buffers (protobuf) Format for CloudEvents defines how
events are to be expressed in protobuf version 3.

## Status of this document

This document is a working draft

## 1. Introduction

CloudEvents is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification
defines how the elements defined in the CloudEvents specification are
to be represented in the Protocol buffers version 3.

Protocol buffers are a language-neutral, platform-neutral extensible
mechanism for serializing structured data. A message is defined once
using the protobuf interface description language (IDL), and the
protobuf compiler generates the language specific libraries for
serializing to and deserializing from the binary representation. The
protobuf version 3 library can also convert a protobuf message into
its [standard JSON form][PROTO_JSON].

Some built in message types in protobuf 3 (`google.protobuf.Value`,
`google.protobuf.Any`, etc) have special runtime support from the
protobuf library. These built in messages are given special treatment
when transcoding to and from JSON. Tools in the protobuf ecosystem
also give special treatment to these messages. For example, the
[Common Expression Language tool (CEL)][CEL] automatically converts a
`google.protobuf.Any` into its contained message when performing data
queries.


### 1.1. Conformance
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in RFC2119.

## 2. Protobuf format

Users of protobuf MUST use the official message definition when
expressing a CloudEvent as a protobuf message. Users SHOULD NOT change
the language specific options in order to have consistent code
generation output. Users MUST NOT change the protobuf package
name. Users MUST NOT use any protobuf options that change the protobuf
wire compatibility such as message_set_wire_format.

```proto
syntax = "proto3";

package io.cloudevents.v0;

import "google/protobuf/any.proto";
import "google/protobuf/struct.proto";
import "google/protobuf/timestamp.proto";

option go_package = "cloudevents.io/protobuf/";
option java_package = "io.cloudevents";
option java_multiple_files = true;

message CloudEvent {
  string event_type = 1;
  string event_type_version = 2;
  string cloud_events_version = 3;
  string source = 4;
  string event_id = 5;
  google.protobuf.Timestamp timestamp = 6;
  string schema_url = 7;
  string content_type = 8;
  google.protobuf.Value data = 9;
  google.protobuf.Struct extensions = 11;
}
```

In general, the CloudEvents attribute names are converted into
protobuf fields in lower_snake_case, and the the CloudEvents type
system is mapped into protobuf types as follows:


| CloudEvents | Protobuf
|--------------|-------------------------------------------------------------
| String       | string
| Binary       | bytes
| URI          | string
| Timestamp    | google.protobuf.Timestamp
| Map          | google.protobuf.Struct
| Object       | google.protobuf.Value
| Integer      | int32

By default, lower_case_names in the protobuf IDL field names are
represented as lowerCamelCase in the protobuf standard JSON format. If
the field has a different styled casing, the `json_name` protobuf
option MUST be used:

```
string arbitrary_casing_attr = 12 [json_name = "aRbItRaRy_casing_ATTR_"];
```

### 2.1 Note on cloud_events_version:

The protobuf `package` keyword defines a package name that includes
the CloudEvents major version number. The package name and message
name together form a fully qualified name for a protobuf
message. Messages with the same name but different package names are
independent messages with no relation to one another. The
`cloud_events_version` field’s major version number MUST match the
major version of the protobuf package.

### 2.2 Special handling of `data` attribute:

#### 2.2.1 Background knowledge on special built in protobuf types

`google.protobuf.Value` ([more info][PROTO_JSON]) is used to express a
JSON structure. Its fields are composed of special wrapper value types
such as `google.protobuf.BytesValue`. The protobuf runtime library
provides JSON conversion support for these special built in message
types.

`google.protobuf.Any` ([more info][PROTO_ANY]) is used in protobuf to
express a field whose type is not known to the enclosing message. It
contains the binary representation of the embedded message and a URL
string that identifies the type of the embedded message.


#### 2.2.2 Handling instructions

If the `contentType` is `application/json` or any media type with the
structured `+json` suffix, the implementation MUST store the JSON
payload in the `data` field.

If the payload is binary, the implementation MUST store the bytes in
the `bytes_data` field.

If the payload is a protobuf, the implementation MUST store the
payload in the `proto_data` field and the `contentType` MUST be
`application/protobuf`.

### 2.3 Extensions:

`google.protobuf.Struct` ([more info][PROTO_STRUCT]) represents an
arbitrary JSON structure. The keys of the `Struct` are the names of
the extensions. The values of the `google.protobuf.Struct` are
`com.protobuf.Value` ([more info][PROTO_VALUE]) fields whose contents
correspond to the value of the extension mapped into JSON using the
[JSON mapping rules][CE_JSON_ENCODING]. All extensions attributes MUST
be put into this bag because they are not a part of the CloudEvents
spec.

Well known extensions can not be given a top level field because they
have no official standing, therefore the protobuf definition can not
commit to a strongly typed representation of the value. The protobuf
binding must be able to map an extension name to different value
types, e.g. a "exampleExtension" with CE type "Object" in one message
and another "exampleExtension" with CE type "Integer" in another
message.

When a new CloudEvent spec version is released, promoted extensions
move from the extensions bag to a strongly typed top level field.

For example, consider an extension for CloudEvents 1.0:

```java
CloudEvent.newBuilder()
  .setCloudEventsVersion("1.0")
  .setExtensions(
    Struct.newBuilder()
    .putFields(
      "vendorExtension",
      Value.newBuilder().setStringValue("myvalue").build()))
  .build();
```

In the next CloudEvents minor release, the extension is promoted to an
official field. The protobuf message definition is updated for
CloudEvents 1.1:

```java
CloudEvent.newBuilder()
  .setCloudEventsVersion("1.1")
  .setComExampleMyextension("myvalue")
  // During the upgrade process producers SHOULD continue setting
  // exts bag to maintain backwards compat
  .setExtensions(
    Struct.newBuilder()
      .putFields(
        "comExampleMyextension",
        Value.newBuilder().setStringValue("myvalue").build()))
  .build();
```

#### 2.3.1 CloudEvents upgrade process

If a field moves from the extensions bag to a top level field, then
the producers and consumers of a CloudEvents system SHOULD coordinate
in the upgrade process:

1. Initially, the producers and consumers are using CloudEvents 1.0
   and the extension is expressed in the “extensions” bag.
1. CloudEvents 1.1 is released.
1. The producers write the extension to both the extensions bag and
   the type safe top level field. The messages will have
   "cloudEventsVersion" set to "1.1", but the extension is still
   readable by 1.0 consumers.
1. All consumers upgrade to 1.1 and stop reading from the extensions
   bag and switch to reading from only the type safe top level field.
1. The producers stop writing to the extensions bag, and only write to
   the type safe top level field.


### 2.4 Relation to CloudEvents JSON format:

All proto3 messages have a standard JSON form.

Note: at the time of writing, extensions are in a separate extensions
bag. The standard JSON is the same as the CloudEvents JSON.

Below are a few examples of the proto message and its JSON
representation.

A CloudEvent whose payload is a JSON may be constructed as follows:
```java
CloudEvent.newBuilder()
  .setEventType("com.example.usercreated")
  .setEventTypeVersion("1.0")
  .setCloudEventsVersion("0.1")
  .setSource("producer1")
  .setEventId("100")
  .setTimestamp(ts)
  .setContentType("application/json")
  .setSchemaUrl("https://com.example.schema/usercreated")
  .setData(
    Value.newBuilder().setStructValue(Struct.newBuilder()
    .putFields(
        "username",
        Value.newBuilder().setStringValue("theusername").build())
    .putFields(
        "email",
        Value.newBuilder().setStringValue("user@example.com").build())
    .build()))
  .setExtensions(
    Struct.newBuilder()
      .putFields(
        "vendorExtension1",
        Value.newBuilder().setStringValue("value1").build())
      .putFields(
        "vendorExtension2",
        Value.newBuilder().setStringValue("value2").build()))
  .build();
```

It has the following proto3 standard JSON representation:
```json
{
  "eventType": "com.example.usercreated",
  "eventTypeVersion": "1.0",
  "cloudEventsVersion": "0.1",
  "source": "producer1",
  "eventId": "100",
  "timestamp": "2018-08-22T15:47:00.951Z",
  "schemaUrl": "https://com.example.schema/usercreated",
  "contentType": "application/json",
  "data": {
    "username": "theusername",
    "email": "user@example.com"
  },
  "extensions": {
    "vendorExtension1": "value1",
    "vendorExtension2": "value2"
  }
}
```

A CloudEvent whose data payload is bytes may be constructed as follows:
```java
CloudEvent.newBuilder()
  .setEventType("com.example.somebytes")
  .setEventTypeVersion("1.0")
  .setCloudEventsVersion("0.1")
  .setSource("producer1")
  .setEventId("100")
  .setTimestamp(ts)
  .setContentType("application/json")
  .setSchemaUrl("https://com.example.schema/usercreated")
  .setData(
    Value.newBuilder()
        .setStringValue(Base64.encode(new byte[] {1, 2, 3, 4})))
  .setExtensions(
    Struct.newBuilder()
      .putFields(
        "vendorExtension1",
        Value.newBuilder().setStringValue("value1").build())
      .putFields(
        "vendorExtension2",
        Value.newBuilder().setStringValue("value2").build()))
  .build();
```

It has the following proto3 standard JSON representation.
```json
{
  "eventType": "com.example.somebytes",
  "eventTypeVersion": "1.0",
  "cloudEventsVersion": "0.1",
  "source": "producer1",
  "eventId": "100",
  "timestamp": "2018-08-23T17:24:34.226Z",
  "schemaUrl": "https://com.example.schema/usercreated",
  "contentType": "application/json",
  "data": "AQIDBA==",
  "extensions": {
    "vendorExtension1": "value1",
    "vendorExtension2": "value2"
  }
}
```

## 3. References:

* [google.protobuf.Any][PROTO_ANY]
* [google.protobuf.Struct][PROTO_STRUCT]
* [google.protobuf.Value][PROTO_VALUE]
* [Protobuf and JSON][PROTO_JSON]
* [Common Expression Language][CEL]


[PROTO_ANY]: https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#any
[PROTO_STRUCT]: https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#struct
[PROTO_VALUE]: https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#google.protobuf.Value
[PROTO_JSON]: https://developers.google.com/protocol-buffers/docs/proto3#json
[CEL]: https://github.com/google/cel-spec/blob/master/doc/langdef.md
[CE_JSON_ENCODING]: ./json-format.md
[CE_SPEC]: ./spec.md
