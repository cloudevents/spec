# CBOR Event Format for CloudEvents - Version 1.0.3-wip

## Abstract

This specifications defines how to serialize CloudEvents in the 
[Concise Binary Object Representation (CBOR)][cbor-spec] data format.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Envelope](#3-envelope)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be represented in the
Concise Binary Object Representation (CBOR) Data Interchange Format 
([RFC 8949][cbor-spec]).

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes.

The [Envelope](#3-envelope) section defines a CBOR container for CloudEvents
attributes and an associated media type.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

## 2. Attributes

This section defines how CloudEvents attributes are mapped to CBOR. This
specification does not explicitly map each attribute, but provides a generic
mapping model that applies to all current and future CloudEvents attributes,
including extensions.

For clarity, extension attributes are encoded using the same rules as core 
attributes. This includes their syntax and placement within the CBOR data item. 
In particular, extensions are placed as top-level CBOR key-value pairs of a map. 
Extensions MUST be encoded as a top-level CBOR key-value pairs.

### 2.1. Base Type System

The core [CloudEvents specification][ce] defines a minimal abstract type system,
which this mapping leans on.

### 2.2. Type System Mapping

The [CloudEvents type system][ce-types] MUST be mapped to CBOR types as follows,
with exceptions noted below.

| CloudEvents   | CBOR                                                         |
| ------------- | ------------------------------------------------------------ |
| Boolean       | CBOR [simple value][cbor-simple-value] `true` (21) or CBOR simple value `false` (20) |
| Integer       | [Major type 0][cbor-major-types] for positive integers and [Major type 1][cbor-major-types] for negative integers                         |
| String        | [Major type 3][cbor-major-types]                             |
| Binary        | [Major type 2][cbor-major-types]                             |
| URI           | [Major type 6][cbor-major-types] [tagged][cbor-tagging] as a URI (tag number `32`) or a [Major type 3][cbor-major-types] (string) following [RFC 3986][rfc3986]|
| URI-reference | [Major type 6][cbor-major-types] [tagged][cbor-tagging] as a URI (tag number `32`) or a [Major type 3][cbor-major-types] (string) following [RFC 3986][rfc3986]|
| Timestamp     | [Major type 6][cbor-major-types] [tagged][cbor-tagging] as a [Standard Date/Time String][cbor-standard-datetime] (tag number `0`)  or a [Major type 3][cbor-major-types] (string) following [RFC 3339][rfc3339] (ISO 8601)  |

Unset attributes MAY be encoded to the CBOR [simple value][cbor-simple-value] 
`null` (22). When decoding attributes and a `null` value is encountered, 
it MUST be treated as the equivalent of unset or omitted.

The reason [major types][cbor-major-types] 0 and 1 were chosen to represent the 
`Integer` type is because CBOR does not have a single type for positive and 
negative numbers, but rather a type for positive numbers (0) and a type 
for negative numbers (1).  

Extension specifications MAY define secondary mapping rules for the values of
attributes they define, but MUST also include the previously defined primary
mapping.

For instance, the attribute value might be a data structure defined in a
standard outside of CloudEvents, with a formal CBOR mapping, and there might be
risk of translation errors or information loss when the original format is not
preserved.

An extension specification that defines a secondary mapping rule for CBOR, and
any revision of such a specification, MUST also define explicit mapping rules
for all other event formats that are part of the CloudEvents core at the time of
the submission or revision.

If needed, the CloudEvents attribute type can be determined by inference using 
the rules from the mapping table. The value is compatible with the respective 
CloudEvents type when the mapping rules are fulfilled.

### 2.4. CDDL Schema Validation

The CloudEvents [CDDL][cddl-spec] for the spec is defined under
[cloudevents.cddl](cloudevents.cddl) and contains the definitions for 
validating events in CBOR.

## 3. Envelope

Each CloudEvent event MAY be wholly represented as a CBOR map 
([major type 5][cbor-major-types]).

Such a representation MUST use the media type `application/cloudevents+cbor`.

All REQUIRED and all not omitted OPTIONAL attributes in the given event MUST 
become key-value pairs of the CBOR map, with the respective CBOR item key 
acting as the attribute name and encoded as a CBOR text 
([major type 3][cbor-major-types]), and the items's type and value being mapped 
using the [type system mapping](#22-type-system-mapping).

OPTIONAL not omitted attributes MAY be represented as a CBOR 
[simple value][cbor-simple-value] `null` (22).

### 3.1. Handling of "data"

The CBOR representation of the event "data" payload is determined by the runtime
type of the `data` content and the value of the [`datacontenttype`
attribute][datacontenttype].

#### 3.1.1. Payload Encoding

Before taking action, a [CBOR encoder][cbor-encoder] MUST first determine 
the runtime data type of the `data` content.

If the implementation determines that the type of data is `Binary`, the value
MUST be represented as a [Major type 2][cbor-major-types] value. If present, 
the `datacontenttype` MUST reflect the format of the original binary data.

If the type of data is not `Binary`, the implementation will next determine
whether the value of the `datacontenttype` attribute declares the `data` to
contain CBOR-formatted content. Such a content type is defined as one having a
[media subtype][rfc2045-sec5] equal to `cbor` or ending with a `+cbor` format
extension. That is, a `datacontenttype` declares CBOR-formatted content if its
media type, when stripped of parameters, has the form `*/cbor` or `*/*+cbor`.
If the `datacontenttype` is unspecified, processing SHOULD proceed as if the
`datacontenttype` had been specified explicitly as `application/cbor`.

If the `datacontenttype` declares the data to contain CBOR-formatted content, a
[CBOR encoder][cbor-encoder] MUST translate the data value to a 
[CBOR data item][cbor-data-item], and use the member name `data` to store it 
inside the CBOR representation. The data value MUST be stored directly as a 
CBOR data item, rather than as an encoded CBOR buffer (tagged or un-tagged).
An implementation MAY fail to encode the event if it is unable to translate 
the runtime value to a [CBOR data item][cbor-data-item].

Otherwise, if the `datacontenttype` does not declare CBOR-formatted data
content, a [CBOR encoder][cbor-encoder] MUST store the data value, 
properly encoded according to the `datacontenttype`, in the `data` member of the
CBOR representation. An implementation MAY fail to encode the event if it is 
unable to represent the runtime value as a properly encoded CBOR data item.

Furthermore, unlike attributes, for which value types are restricted by the
[type-system mapping](#22-type-system-mapping), the `data` member
[CBOR data item][cbor-data-item] is unrestricted, and MAY contain any valid 
CBOR if the `datacontenttype` declares the data to be CBOR-formatted. 
In particular, the `data` member MAY have a simple value of `null`, 
representing an explicit `null` payload as distinct from the absence of 
the `data` member.

#### 3.1.2. Payload Decoding

When a `data` member is present, the decoding behavior is dependent on the value
of the `datacontenttype` attribute. If the `datacontenttype` declares the `data`
to contain CBOR-formatted content (that is, its subtype is `cbor` or has a
`+cbor` format extension), then the `data` member MUST be treated directly as a
[CBOR data item][cbor-data-item] and decoded using an appropriate CBOR type 
mapping for the runtime. Note: if the `data` member is a string, bytes or 
[encoded cbor data item][cbor-encoded-data-item], a [CBOR decoder][cbor-decoder] 
MUST interpret it directly as a the given value; it MUST NOT further
decode the value as a [CBOR data item][cbor-data-item].

If the `datacontenttype` does not declare CBOR-formatted data content, then the
`data` member SHOULD be treated as an encoded content string. An implementation
MAY fail to decode the event if the `data` member is not a string or bytes 
value, or if it is unable to interpret the `data` with the `datacontenttype`.

When a `data` member is present, if the `datacontenttype` attribute is absent, a
[CBOR decoder][cbor-decoder] SHOULD proceed as if it were set to 
`application/cbor`, which declares the data to contain CBOR-formatted content. 
Thus, it SHOULD treat the `data` member directly as a 
[CBOR data item][cbor-data-item] as specified above. Furthermore, 
if a CBOR-formatted event with no `datacontenttype` attribute, is decoded and 
then re-encoded using a different format or protocol binding, the 
`datacontenttype` in the re-encoded event SHOULD be set explicitly to the 
implied `application/cbor` content type to preserve the semantics of the event.

## References

- [RFC 8949][cbor-spec] Concise Binary Object Representation (CBOR)
- [RFC 8610][cddl-spec]  Concise Data Definition Language (CDDL)
  - A Notational Convention to Express 
  Concise Binary Object Representation (CBOR).


[cbor-spec]: https://www.rfc-editor.org/rfc/rfc8949.html
[cbor-simple-value]: https://www.rfc-editor.org/rfc/rfc8949.html#fpnocont
[cbor-major-types]: https://www.rfc-editor.org/rfc/rfc8949.html#name-major-types
[cbor-tagging]: https://www.rfc-editor.org/rfc/rfc8949.html#section-3.4
[cbor-standard-datetime]: https://www.rfc-editor.org/rfc/rfc8949.html#name-standard-date-time-string
[cbor-encoded-data-item]: https://www.rfc-editor.org/rfc/rfc8949.html#section-3.4.5.1
[cddl-spec]: https://www.rfc-editor.org/rfc/rfc8610
[cbor-encoder]: https://www.rfc-editor.org/rfc/rfc8949.html#name-terminology
[cbor-decoder]: https://www.rfc-editor.org/rfc/rfc8949.html#name-terminology
[cbor-data-item]: https://www.rfc-editor.org/rfc/rfc8949.html#section-1.2
[ce]: ../spec.md
[rfc2119]: https://tools.ietf.org/html/rfc2119
[ce-types]: ../spec.md#type-system
[datacontenttype]: ../spec.md#datacontenttype
[rfc2045-sec5]: https://tools.ietf.org/html/rfc2045#section-5
[rfc3339]: https://www.ietf.org/rfc/rfc3339.txt
[rfc3986]: https://tools.ietf.org/html/rfc3986