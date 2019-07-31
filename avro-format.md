# Avro Event Format for CloudEvents - Version 0.4-wip

## Abstract

The Avro Format for CloudEvents defines how events attributes are expressed
in the [Avro 1.9.0 Specification][avro-spec].

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Examples](#3-examples)

## 1. Introduction

[CloudEvents][ce] is a standardized and transport-neutral definition of the
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
| Integer       | [int][avro-primitives]                                                 |
| String        | [string][avro-primitives]                                              |
| Binary        | [bytes][avro-primitives]                                               |
| Map           | [map][avro-primitives]                                                 |
| URI-reference | [string][avro-primitives] following [RFC 3986 §4.1][rfc3986-section41] |
| Timestamp     | [string][avro-primitives] following [RFC 3339][rfc3339] (ISO 8601)     |
| Any           | See [2.2](#22-mapping-any-typed-attributes)                            |

Extension specifications MAY define diverging mapping rules for the values of
attributes they define.

### 2.2 Mapping Any-typed Attributes

`Any`-typed CloudEvents values can either hold a `String`, or a `Binary` value,
or a `Map`, or any of all other types. Avro type system satisfies this requirement by employing a recursive reference,
where a `record` type is referenced as a value inside of its own `map`.

Example:

```json
{
  "type":"record",
  "name":"MyRecord",
  "fields":[
    {
      "name":"wow",
      "type":{
        "type":"map",
        "values":[
          "null",
          "string",
          "MyRecord"
        ]
      }
    }
  ]
}
```

### 2.3 OPTIONAL Attributes

CloudEvents Spec defines OPTIONAL attributes. The Avro format defines that
these fields MUST use the `null` type and the actual type through
the [union][avro-unions].

Example:

```json
[
  "null",
  "string"
]
```

### 2.4 Definition

Users of Avro MUST use a message whose binary encoding is identical
to the one described by the [CloudEvent Avro Schema](./spec.avsc):

```json
{
  "namespace":"io.cloudevents",
  "type":"record",
  "name":"CloudEvent",
  "version":"0.4-wip",
  "doc":"Avro Event Format for CloudEvents",
  "fields":[
    {
      "name":"attribute",
      "type":{
        "type":"map",
        "values":[
          "null",
          "int",
          "string",
          "bytes",
          "CloudEvent"
        ]
      }
    }
  ]
}
```

## 3 Examples

The following table shows exemplary mappings:

| CloudEvents     | Type      | Exemplary Avro Value                           |
| --------------- | --------- | ---------------------------------------------- |
| type            | string    | `"com.example.someevent"`                      |
| specversion     | string    | `"0.4-wip`                                      |
| source          | string    | `"/mycontext"`                                 |
| id              | string    | `"7a0dc520-c870-4193c8"`                       |
| time            | string    | `"2019-06-05T23:45:00Z"`                       |
| dataschemaurl   | string    | `"http://registry.com/schema/v1/much.json"`    |
| contenttype     | string    | `"application/json"`                           |
| data            | string    | `"{"much":{"wow":"json"}}"`                    |
||||
| dataschemaurl   | string    | `"http://registry.com/subjects/ce/versions/1"` |
| contenttype     | string    | `"application/avro"`                           |
| data            | string    | `"Q2xvdWRFdmVudHM="`                           |

## References

- [Avro 1.9.0][avro-spec] Apache Avro™ 1.9.0 Specification

[avro-spec]: http://avro.apache.org/docs/1.9.0/spec.html
[avro-primitives]: http://avro.apache.org/docs/1.9.0/spec.html#schema_primitive
[avro-logical-types]: http://avro.apache.org/docs/1.9.0/spec.html#Logical+Types
[avro-unions]: http://avro.apache.org/docs/1.9.0/spec.html#Unions

[ce]: ./spec.md

[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986-section41]: https://tools.ietf.org/html/rfc3986#section-4.1
[rfc3339]: https://tools.ietf.org/html/rfc3339
