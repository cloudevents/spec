# Avro Event Format for CloudEvents - Version 1.0.2

## Abstract

The Avro Format for CloudEvents defines how events attributes are expressed in
the [Avro 1.9.0 Specification][avro-spec].

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Data](#3-data)
4. [Examples](#4-examples)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be represented in the
[Avro 1.9.0][avro-primitives].

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes for use as Avro message
properties.

This specification does not define an envelope format. The Avro type system's
intent is primarily to provide a consistent type system for Avro itself and not
for message payloads.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

## 2. Attributes

This section defines how CloudEvents attributes are mapped to the Avro
type-system. This specification explicitly maps each attribute.

### 2.1 Type System Mapping

The CloudEvents type system MUST be mapped to Avro types as follows.

| CloudEvents   | Avro                                                                   |
| ------------- | ---------------------------------------------------------------------- |
| Boolean       | [boolean][avro-primitives]                                             |
| Integer       | [int][avro-primitives]                                                 |
| String        | [string][avro-primitives]                                              |
| Binary        | [bytes][avro-primitives]                                               |
| URI           | [string][avro-primitives] following [RFC 3986 §4.3][rfc3986-section43] |
| URI-reference | [string][avro-primitives] following [RFC 3986 §4.1][rfc3986-section41] |
| Timestamp     | [string][avro-primitives] following [RFC 3339][rfc3339] (ISO 8601)     |

Extension specifications MAY define secondary mapping rules for the values of
attributes they define, but MUST also include the previously defined primary
mapping.

### 2.3 OPTIONAL Attributes

CloudEvents Spec defines OPTIONAL attributes. The Avro format defines that these
fields MUST use the `null` type and the actual type through the
[union][avro-unions].

Example:

```json
["null", "string"]
```

### 2.4 Definition

Users of Avro MUST use a message whose binary encoding is identical to the one
described by the [CloudEvent Avro Schema](cloudevents.avsc):

```json
{
  "namespace": "io.cloudevents",
  "type": "record",
  "name": "CloudEvent",
  "version": "1.0",
  "doc": "Avro Event Format for CloudEvents",
  "fields": [
    {
      "name": "attribute",
      "type": {
        "type": "map",
        "values": ["null", "boolean", "int", "string", "bytes"]
      }
    },
    {
      "name": "data",
      "type": [
        "bytes",
        "null",
        "boolean",
        {
          "type": "map",
          "values": [
            "null",
            "boolean",
            {
              "type": "record",
              "name": "CloudEventData",
              "doc": "Representation of a JSON Value",
              "fields": [
                {
                  "name": "value",
                  "type": {
                    "type": "map",
                    "values": [
                      "null",
                      "boolean",
                      { "type": "map", "values": "CloudEventData" },
                      { "type": "array", "items": "CloudEventData" },
                      "double",
                      "string"
                    ]
                  }
                }
              ]
            },
            "double",
            "string"
          ]
        },
        { "type": "array", "items": "CloudEventData" },
        "double",
        "string"
      ]
    }
  ]
}
```

## 3 Data

Before encoding, the AVRO serializer MUST first determine the runtime data type
of the content. This can be determined by examining the data for invalid UTF-8
sequences or by consulting the `datacontenttype` attribute.

If the implementation determines that the type of the data is binary, the value
MUST be stored in the `data` field using the `bytes` type.

For other types (non-binary data without a `datacontenttype` attribute), the
implementation MUST translate the data value into a representation of the JSON
value using the union types described for the `data` record.

## 4 Examples

The following table shows exemplary mappings:

| CloudEvents | Type   | Exemplary Avro Value                           |
| ----------- | ------ | ---------------------------------------------- |
| type        | string | `"com.example.someevent"`                      |
| specversion | string | `"1.0"`                                        |
| source      | string | `"/mycontext"`                                 |
| id          | string | `"7a0dc520-c870-4193c8"`                       |
| time        | string | `"2019-06-05T23:45:00Z"`                       |
| dataschema  | string | `"http://registry.com/schema/v1/much.json"`    |
| contenttype | string | `"application/json"`                           |
| data        | bytes  | `"{"much":{"wow":"json"}}"`                    |
|             |        |                                                |
| dataschema  | string | `"http://registry.com/subjects/ce/versions/1"` |
| contenttype | string | `"application/avro"`                           |
| data        | bytes  | `[avro-serialized-bytes]`                      |

## References

- [Avro 1.9.0][avro-spec] Apache Avro™ 1.9.0 Specification

[avro-spec]: http://avro.apache.org/docs/1.9.0/spec.html
[avro-primitives]: http://avro.apache.org/docs/1.9.0/spec.html#schema_primitive
[avro-logical-types]: http://avro.apache.org/docs/1.9.0/spec.html#Logical+Types
[avro-unions]: http://avro.apache.org/docs/1.9.0/spec.html#Unions
[ce]: ../spec.md
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986-section41]: https://tools.ietf.org/html/rfc3986#section-4.1
[rfc3986-section43]: https://tools.ietf.org/html/rfc3986#section-4.3
[rfc3339]: https://tools.ietf.org/html/rfc3339
