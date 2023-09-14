# Data Distribution Service (DDS) Event Format for CloudEvents - Version 1.0.0-wip

## Abstract

The Data Distribution Service (DDS) Format for CloudEvents defines how event attributes are
expressed using the data types defined in the [Object Management Group (OMG)][omg]
[Interface Definition Language (IDL) Specification][idl-spec].

The [OMG DDS Specification][dds-spec] is closely related to the IDL specification as
messages transmitted over the DDS protocol are defined via the IDL type system.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Data](#3-data)
4. [Examples](#4-examples)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be represented in IDL
primitive types.

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes for use as DDS message
properties.

This specification does not define an envelope format.

The DDS event format does not currently define a batch mode format.

An eXtensible Markup Language (XML) reprsentation of the [DDS Event Format][dds-event-format]
is provided in conjunction with this document.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

## 2. Attributes

This section defines how CloudEvents attributes are mapped to the IDL
type-system used by DDS. This specification explicitly maps each attribute.

### 2.1 Type System Mapping

The CloudEvents type system MUST be mapped to DDS types as follows.

| CloudEvents   | DDS                                                                   |
| ------------- | ---------------------------------------------------------------------- |
| Boolean       | Boolean                                             |
| Integer       | Int32                                                 |
| String        | String (255)                                              |
| Binary        | Bytes (100)                                               |
| URI           | String (255) following [RFC 3986 §4.3][rfc3986-section43] |
| URI-reference | String (255) following [RFC 3986 §4.1][rfc3986-section41] |
| Timestamp     | seconds: Int64 nanoseconds: UInt32     |

Extension specifications MAY define secondary mapping rules for the values of
attributes they define, but MUST also include the previously defined primary
mapping.

## 3 Data

Before encoding, the DDS serializer MUST first determine the runtime data type
of the content. This can be determined by examining by consulting the `datacontenttype`
and 'dataencoding' attributes.

If the implementation determines that the type of the data is binary, the value
MUST be stored in the `body` field using the `bytes` type.

For other types, the implementation MUST translate the data value into a text or JSON
representation of the value using the union types described for the message body.

## 4 Examples

The following table shows exemplary mappings:

| CloudEvents | Type   | Exemplary DDS Value                           |
| ----------- | ------ | ---------------------------------------------- |
| type        | string | `"org.cncf.cloudevents.example"`                      |
| specversion | string | `"1.0"`                                        |
| source      | string | `"urn:event:from:myapi/resource/123"`                                 |
| id          | string | `"b46cf653-d48a-4b90-8dfa-355c01061361"`                       |
| time        | string | `"sec: 1694707005, nanosec: 996000000"`                       |
| dataschema  | string | `"http://cloudevents.io/schema.json'"`    |
| contenttype | string | `"cloudevent/json"`                           |
| data        | string  | `"{"color":"red","x":120,"y":42,"shapesize":20}"`                    |
| contenttype | string | `"application/cloudevent+dds"`                           |
| data        | bytes  | `"data_base64":"anVzdCBub3JtYWwgdGV4dA=="`                      |

## References
- [OMG][omg] Object Management Group (OMG)
- [idl-spec] OMG Interface Definition Language (IDL) Specification 
- [DDS][dds-spec] OMG Data Distribution Service (DDS) Specification
- [dds-event-format] XML representation of DDS event format
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels


[ce]: ../spec.md
[omg]: https://www.omg.org/
[idl-spec]: https://www.omg.org/spec/IDL/4.2/PDF
[dds-spec]: https://www.omg.org/spec/DDS/1.4/PDF
[dds-event-format]: ./dds-format.xml
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986-section41]: https://tools.ietf.org/html/rfc3986#section-4.1
[rfc3986-section43]: https://tools.ietf.org/html/rfc3986#section-4.3
[rfc3339]: https://tools.ietf.org/html/rfc3339
