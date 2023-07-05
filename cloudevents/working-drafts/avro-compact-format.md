# Avro Compact Event Format for CloudEvents - Version 1.0.3-wip

## Abstract

The Avro Compact Format for CloudEvents defines how events are expressed in
the [Avro 1.9.0 Specification][avro-spec].

This differs from the [Avro format](../formats/avro-format.md) in that:

- It is optimized for performance, preferring a more compact representation.
- It only supports spec version 1.0 (any changes to spec version requires changes to the Avro schema,
  which changes the fingerprint, breaking compatibility).
- It does not natively support JSON (JSON can be straight-forwardly serialized 
  to bytes and this was therefore not considered necessary).

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Transport](#3-transport)
4. [Examples](#4-examples)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
CloudEvents are to be represented as [Avro 1.9.0][avro-primitives].

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes for use as Avro message
properties.

This specification does not define an envelope format. The Avro type system's
intent is primarily to provide a consistent type system for Avro itself and not
for message payloads.

The Avro event format does not currently define a batch mode format.

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
|---------------|------------------------------------------------------------------------|
| Boolean       | [boolean][avro-primitives]                                             |
| Integer       | [int][avro-primitives]                                                 |
| String        | [string][avro-primitives]                                              |
| Binary        | [bytes][avro-primitives]                                               |
| URI           | [string][avro-primitives] following [RFC 3986 §4.3][rfc3986-section43] |
| URI-reference | [string][avro-primitives] following [RFC 3986 §4.1][rfc3986-section41] |
| Timestamp     | [long][avro-primitives]  using `timestamp-micros` logical type         |

Extension specifications MAY define secondary mapping rules for the values of
attributes they define, but MUST also include the previously defined primary
mapping.

### 2.2 Definition

Users of Avro MUST use a message whose binary encoding is identical to the one
described by the [CloudEvent Avro Compact Schema](cloudevents-compact.avsc).

## 3 Transport

Transports that support content identification MUST use the following designation:

```text
application/cloudevents+avro-compact
```

## 4 Examples

The following table shows exemplary mappings:

| CloudEvents     | Type   | Exemplary Avro Value                      |
|-----------------|--------|-------------------------------------------|
| id              | string | `7a0dc520-c870-4193c8`                    |
| source          | string | `https://github.com/cloudevents`          |
| specversion     | N/A    | Spec version is always `1.0`.             |
| type            | string | `com.example.object.deleted.v2`           |
| datacontenttype | string | `application/octet-stream`                |
| dataschema      | string | `http://registry.com/schema/v1/much.json` |
| subject         | string | `mynewfile.jpg`                           |
| time            | long   | `1685121689691000`                        |
| data            | bytes  | `[bytes]`                                 |

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
