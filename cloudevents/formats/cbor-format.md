# Avro Event Format for CloudEvents - Version 1.0.3-wip

## Abstract

The CBOR Format for CloudEvents defines how events attributes are expressed in
the [CBOR Specification][cbor-spec].

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Data](#3-data)
4. [Examples](#4-examples)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be represented in the
Concise Binary Object Representation (CBOR) Data Interchange Format ([RFC 8949][cbor-spec]).

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes.

The [Envelope](#3-envelope) section defines a JSON container for CloudEvents
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

For clarity, extension attributes are serialized using the same rules as
core attributes. This includes their syntax and placement
within the CBOR data item. In particular, extensions are placed as top-level CBOR
key-value pairs of a map. Extensions MUST be serialized as a top-level CBOR key-value pairs.

### 2.1. Base Type System

The core [CloudEvents specification][ce] defines a minimal abstract type system,
which this mapping leans on.

### 2.2. Type System Mapping

The [CloudEvents type system][ce-types] MUST be mapped to CBOR types as follows,
with exceptions noted below.

| CloudEvents   | CBOR                                                         |
| ------------- | ------------------------------------------------------------ |
| Boolean       | [Simple value][cbor-fpnocont] number `20` for `false` and number `21` for `true` |
| Integer       | [Major type 0][cbor-major-types]                             |
| String        | [Major type 3][cbor-major-types]                             |
| Binary        | [Major type 2][cbor-major-types]                             |
| URI           | [Major type 6][cbor-major-types] [tagged][cbor-tagging] as a URI |
| URI-reference | [Major type 6][cbor-major-types] [tagged][cbor-tagging] as a URI |
| Timestamp     | [Major type 6][cbor-major-types] [tagged][cbor-tagging] as a [Standard Date/Time String][cbor-standard-datetime] |

Unset attributes MAY be encoded to the [Simple value][cbor-fpnocont] value `22` (`null`). When decoding
attributes and a `null` value is encountered, it MUST be treated as the
equivalent of unset or omitted.

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

If required, the CloudEvents type can be determined by inference using the rules
from the mapping table. The value is compatible with the respective CloudEvents type when the
mapping rules are fulfilled.

### 2.4. JSONSchema Validation

The CloudEvents [CDDL](http://json-schema.org) for the spec is located
[here](cloudevents.json) and contains the definitions for validating events in
JSON.

## 3. Envelope

Each CloudEvents event can be wholly represented as a JSON object.

Such a representation MUST use the media type `application/cloudevents+json`.

All REQUIRED and all not omitted OPTIONAL attributes in the given event MUST
become members of the JSON object, with the respective JSON object member name
matching the attribute name, and the member's type and value being mapped using
the [type system mapping](#22-type-system-mapping).

OPTIONAL not omitted attributes MAY be represented as a `null` JSON value.

### 3.1. Handling of "data"

The JSON representation of the event "data" payload is determined by the runtime
type of the `data` content and the value of the [`datacontenttype`
attribute][datacontenttype].

#### 3.1.1. Payload Serialization

Before taking action, a JSON serializer MUST first determine the runtime data
type of the `data` content.

If the implementation determines that the type of data is `Binary`, the value
MUST be represented as a [JSON string][json-string] expression containing the
[Base64][base64] encoded binary value, and use the member name `data_base64` to
store it inside the JSON representation. If present, the `datacontenttype` MUST
reflect the format of the original binary data. If a `datacontenttype` value is
not provided, no assumptions can be made as to the format of the data and
therefore the `datacontenttype` attribute MUST NOT be present in the resulting
CloudEvent.

Note: Definition of `data_base64` is a JSON-specific marshaling rule and not
part of the formal CloudEvents context attributes definition. This means the
rules governing CloudEvent attributes names do not apply to this JSON member.

If the type of data is not `Binary`, the implementation will next determine
whether the value of the `datacontenttype` attribute declares the `data` to
contain JSON-formatted content. Such a content type is defined as one having a
[media subtype][rfc2045-sec5] equal to `json` or ending with a `+json` format
extension. That is, a `datacontenttype` declares JSON-formatted content if its
media type, when stripped of parameters, has the form `*/json` or `*/*+json`.
If the `datacontenttype` is unspecified, processing SHOULD proceed as if the
`datacontenttype` had been specified explicitly as `application/json`.

If the `datacontenttype` declares the data to contain JSON-formatted content, a
JSON serializer MUST translate the data value to a [JSON value][json-value], and
use the member name `data` to store it inside the JSON representation. The data
value MUST be stored directly as a JSON value, rather than as an encoded JSON
document represented as a string. An implementation MAY fail to serialize the
event if it is unable to translate the runtime value to a JSON value.

Otherwise, if the `datacontenttype` does not declare JSON-formatted data
content, a JSON serializer MUST store a string representation of the data value,
properly encoded according to the `datacontenttype`, in the `data` member of the
JSON representation. An implementation MAY fail to serialize the event if it is
unable to represent the runtime value as a properly encoded string.

Out of this follows that the presence of the `data` and `data_base64` members is
mutually exclusive in a JSON serialized CloudEvent.

Furthermore, unlike attributes, for which value types are restricted by the
[type-system mapping](#22-type-system-mapping), the `data` member
[JSON value][json-value] is unrestricted, and MAY contain any valid JSON if the
`datacontenttype` declares the data to be JSON-formatted. In particular, the
`data` member MAY have a value of `null`, representing an explicit `null`
payload as distinct from the absence of the `data` member.

#### 3.1.2. Payload Deserialization

When a CloudEvents is deserialized from JSON, the presence of the `data_base64`
member clearly indicates that the value is a Base64 encoded binary data, which
the deserializer MUST decode into a binary runtime data type. The deserializer
MAY further interpret this binary data according to the `datacontenttype`. If
the `datacontenttype` attribute is absent, the decoding MUST NOT make an
assumption of JSON-formatted data (as described below for the `data` member).

When a `data` member is present, the decoding behavior is dependent on the value
of the `datacontenttype` attribute. If the `datacontenttype` declares the `data`
to contain JSON-formatted content (that is, its subtype is `json` or has a
`+json` format extension), then the `data` member MUST be treated directly as a
[JSON value][json-value] and decoded using an appropriate JSON type mapping for
the runtime. Note: if the `data` member is a string, a JSON deserializer MUST
interpret it directly as a [JSON String][json-string] value; it MUST NOT further
deserialize the string as a JSON document.

If the `datacontenttype` does not declare JSON-formatted data content, then the
`data` member SHOULD be treated as an encoded content string. An implementation
MAY fail to deserialize the event if the `data` member is not a string, or if it
is unable to interpret the `data` with the `datacontenttype`.

When a `data` member is present, if the `datacontenttype` attribute is absent, a
JSON deserializer SHOULD proceed as if it were set to `application/json`, which
declares the data to contain JSON-formatted content. Thus, it SHOULD treat the
`data` member directly as a [JSON value][json-value] as specified above.
Furthermore, if a JSON-formatted event with no `datacontenttype` attribute, is
deserialized and then re-serialized using a different format or protocol
binding, the `datacontenttype` in the re-serialized event SHOULD be set
explicitly to the implied `application/json` content type to preserve the
semantics of the event.

### 3.2. Examples

Example event with `Binary`-valued data:

```JSON
{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
    "source" : "/mycontext",
    "id" : "A234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "comexampleextension1" : "value",
    "comexampleothervalue" : 5,
    "datacontenttype" : "application/vnd.apache.thrift.binary",
    "data_base64" : "... base64 encoded string ..."
}
```

The above example re-encoded using [HTTP Binary Content Mode][http-binary]:

```
ce-specversion: 1.0
ce-type: com.example.someevent
ce-source: /mycontext
ce-id: A234-1234-1234
ce-time: 2018-04-05T17:31:00Z
ce-comexampleextension1: value
ce-comexampleothervalue: 5
content-type: application/vnd.apache.thrift.binary

...raw binary bytes...
```

Example event with a serialized XML document as the `String` (i.e. non-`Binary`)
valued `data`, and an XML (i.e. non-JSON-formatted) content type:

```JSON
{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
    "source" : "/mycontext",
    "id" : "B234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "comexampleextension1" : "value",
    "comexampleothervalue" : 5,
    "unsetextension": null,
    "datacontenttype" : "application/xml",
    "data" : "<much wow=\"xml\"/>"
}
```

The above example re-encoded using [HTTP Binary Content Mode][http-binary]:

```
ce-specversion: 1.0
ce-type: com.example.someevent
ce-source: /mycontext
ce-id: B234-1234-1234
ce-time: 2018-04-05T17:31:00Z
ce-comexampleextension1: value
ce-comexampleothervalue: 5
content-type: application/xml

<much wow="xml"/>
```

Example event with [JSON Object][json-object]-valued `data` and a content type
declaring JSON-formatted data:

```JSON
{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
    "source" : "/mycontext",
    "subject": null,
    "id" : "C234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "comexampleextension1" : "value",
    "comexampleothervalue" : 5,
    "datacontenttype" : "application/json",
    "data" : {
        "appinfoA" : "abc",
        "appinfoB" : 123,
        "appinfoC" : true
    }
}
```

The above example re-encoded using [HTTP Binary Content Mode][http-binary]:

```
ce-specversion: 1.0
ce-type: com.example.someevent
ce-source: /mycontext
ce-id: C234-1234-1234
ce-time: 2018-04-05T17:31:00Z
ce-comexampleextension1: value
ce-comexampleothervalue: 5
content-type: application/json

{
  "appinfoA" : "abc",
  "appinfoB" : 123,
  "appinfoC" : true
}
```

Example event with [JSON Number][json-number]-valued `data` and a content type
declaring JSON-formatted data:

```JSON
{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
    "source" : "/mycontext",
    "subject": null,
    "id" : "C234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "comexampleextension1" : "value",
    "comexampleothervalue" : 5,
    "datacontenttype" : "application/json",
    "data" : 1.5
}
```

The above example re-encoded using [HTTP Binary Content Mode][http-binary]:

```
ce-specversion: 1.0
ce-type: com.example.someevent
ce-source: /mycontext
ce-id: C234-1234-1234
ce-time: 2018-04-05T17:31:00Z
ce-comexampleextension1: value
ce-comexampleothervalue: 5
content-type: application/json

1.5
```

Example event with a literal JSON string as the non-`Binary`-valued `data` and
no `datacontenttype`. The data is implicitly treated as if the `datacontenttype`
were set to `application/json`:

```JSON
{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
    "source" : "/mycontext",
    "subject": null,
    "id" : "D234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "comexampleextension1" : "value",
    "comexampleothervalue" : 5,
    "data" : "I'm just a string"
}
```

The above example re-encoded using [HTTP Binary Content Mode][http-binary].
Note that the Content Type is explicitly set to the `application/json` value
that was implicit in JSON format. Note also that the content is quoted to
indicate that it is a literal JSON string. If the quotes were missing, this
would have been an invalid event because the content could not be decoded as
`application/json`:

```
ce-specversion: 1.0
ce-type: com.example.someevent
ce-source: /mycontext
ce-id: D234-1234-1234
ce-time: 2018-04-05T17:31:00Z
ce-comexampleextension1: value
ce-comexampleothervalue: 5
content-type: application/json

"I'm just a string"
```

Example event with a `Binary`-valued `data_base64` but no `datacontenttype`.
Even though the data happens to be a valid JSON document when interpreted as
text, no content type is inferred.

```JSON
{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
    "source" : "/mycontext",
    "id" : "D234-1234-1234",
    "data_base64" : "eyAieHl6IjogMTIzIH0="
}
```

The above example re-encoded using [HTTP Binary Content Mode][http-binary].
Note that there is no `content-type` header present.

```
ce-specversion: 1.0
ce-type: com.example.someevent
ce-source: /mycontext
ce-id: D234-1234-1234

{ "xyz": 123 }
```

## References

- [RFC 8949][cbor-spec] Concise Binary Object Representation (CBOR)
- [RFC 8610][cddl-spec]  Concise Data Definition Language (CDDL)
  - A Notational Convention to Express Concise Binary Object Representation (CBOR).


[cbor-spec]: https://www.rfc-editor.org/rfc/rfc8949.html
[cbor-fpnocont]: https://www.rfc-editor.org/rfc/rfc8949.html#fpnocont
[cbor-fpnoconttbl2]: https://www.rfc-editor.org/rfc/rfc8949.html#fpnoconttbl2
[cbor-major-types]: https://www.rfc-editor.org/rfc/rfc8949.html#name-major-types
[cbor-tagging]: https://www.rfc-editor.org/rfc/rfc8949.html#section-3.4
[cbor-standard-datetime]: https://www.rfc-editor.org/rfc/rfc8949.html#name-standard-date-time-string
[cbor-epoch-datetime]: https://www.rfc-editor.org/rfc/rfc8949.html#name-epoch-based-date-time
[cddl-spec]: https://www.rfc-editor.org/rfc/rfc8610
[ce]: ../spec.md
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986-section41]: https://tools.ietf.org/html/rfc3986#section-4.1
[rfc3986-section43]: https://tools.ietf.org/html/rfc3986#section-4.3
[rfc3339]: https://tools.ietf.org/html/rfc3339

[ce-types]: ../spec.md#type-system
[json-number]: 
