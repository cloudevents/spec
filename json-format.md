# JSON Event Format for CloudEvents - Version 0.1

## Abstract

The JSON Format for CloudEvents defines how events are expressed in
JavaScript Object Notation (JSON) Data Interchange Format ([RFC8259][RFC8259]).

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Envelope](#3-envelope)
4. [References](#4-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be represented in
the JavaScript Object Notation (JSON) Data Interchange Format
([RFC8259][RFC8259]).

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes.

The [Envelope](#3-envelope) section defines a JSON container for CloudEvents
attributes and an associated media type.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

## 2. Attributes

This section defines how CloudEvents attributes are mapped to JSON. This
specification does not explicitly map each attribute, but provides a generic
mapping model that applies to all current and future CloudEvents attributes.

### 2.1. Base Type System

The core [CloudEvents specification][CE] defines a minimal abstract type
system, which this mapping leans on.

### 2.2. Type System Mapping

The CloudEvents type system is mapped to JSON types as follows:

| CloudEvents | JSON
|--------------|-------------------------------------------------------------
| String       | [string][JSON-String]
| Binary       | [string][JSON-String], [Base64-encoded][base64] binary
| URI          | [string][JSON-String]
| Timestamp    | [string][JSON-String]
| Map          | [JSON object][JSON-Object]
| Object       | [JSON value][JSON-Value]

### 2.3. Mapping Object-typed Attributes

The CloudEvents `data` attribute is `Object`-typed, meaning that it either
holds a `String`, or a `Binary` value, or a `Map`. `Map` entry values are
also `Object` typed.

If an implementation determines that the actual type of an `Object` is a
`String`, the value MUST be represented as [JSON string][JSON-String]
expression; for `Binary`, the value MUST represented as [JSON
string][JSON-String] expression containing the [Base64][base64] encoded binary
value; for `Map`, the value MUST be represented as a [JSON object][JSON-Object]
expression, whereby the index fields become member names and the associated
values become the respective member's value.

### 2.4. Examples

The following table shows exemplary mappings:

| CloudEvents       | Type     | Exemplary JSON Value
|--------------------|----------|-------------------------------
| eventType          | String   | "com.example.someevent"
| cloudEventsVersion | String   | "0.1"
| source             | URI      | "/mycontext"
| eventID            | String   | "1234-1234-1234"
| eventTime          | Timestamp| "2018-04-05T17:31:00Z"
| contentType        | String   | "application/json"
| extensions         | Map      | { "extA" : "vA", "extB", "vB" }
| data               | String   | "<much wow=\"xml\"/>"
| data               | Binary   | "Q2xvdWRFdmVudHM="
| data               | Map      | { "objA" : "vA", "objB", "vB" }

## 3. Envelope

Each CloudEvents event can be wholly represented as a JSON object.

Such a representation uses the media type `application/cloudevents+json`

All REQUIRED and all not omitted OPTIONAL attributes in the given event MUST
become members of the JSON object, with the respective JSON object member name
matching the attribute name, and the member's type and value being mapped using
the [type system mapping](#22-type-system-mapping).

### 3.1. Special Handling of the "data" Attribute

The mapping of the `Object`-typed `data` attribute follows the rules laid out
in [Section 2.3.](#23-mapping-object-typed-attributes), with one additional
rule:

If an implementation determines that the type of the `data` attribute is
`Binary` or `String`, it MUST inspect the `contentType` attribute to determine
whether it is indicated that the data value contains JSON data.

If the `contentType` value is either ["application/json"][RFC4627] or any media type
with a [structured +json suffix][RFC6839], the implementation MUST translate
the `data` attribute value into a [JSON value][JSON-Value], and set the `data`
attribute of the envelope JSON object to this JSON value.

If the `contentType` value does not follow the [structured +json suffix][RFC6839]
but is known to use JSON encoding, the implementation MUST translate the `data` attribute
value into a [JSON value][JSON-Value], and set the `data` attribute of the envelope
JSON object to this JSON value. Its typical examples are, but not limited to,
`text/json`, [`application/json-seq`][JSON-seq] and
[`application/geo+json-seq`][JSON-geoseq].

Unlike all other attributes, for which value types are restricted to strings
per the [type-system mapping](#22-type-system-mapping), the resulting `data`
member [JSON value][JSON-Value] is unrestricted, and MAY also contain numeric
and logical JSON types.

### 3.2. Examples

Example event with `String`-valued `data`:

``` JSON
{
    "cloudEventsVersion" : "0.1",
    "eventType" : "com.example.someevent",
    "source" : "/mycontext",
    "eventID" : "A234-1234-1234",
    "eventTime" : "2018-04-05T17:31:00Z",
    "properties" : {
      "comExampleExtension" : "value"
    },
    "contentType" : "text/xml",
    "data" : "<much wow=\"xml\"/>"
}
```

Example event with `Binary`-valued data

``` JSON
{
    "cloudEventsVersion" : "0.1",
    "eventType" : "com.example.someevent",
    "source" : "/mycontext",
    "eventID" : "B234-1234-1234",
    "eventTime" : "2018-04-05T17:31:00Z",
    "properties" : {
      "comExampleExtension" : "value"
    },
    "contentType" : "application/vnd.apache.thrift.binary",
    "data" : "... base64 encoded string ..."
}
```

Example event with JSON data for the "data" member, either derived from
a `Map` or [JSON data](#31-special-handling-of-the-data-attribute) data:

``` JSON
{
    "cloudEventsVersion" : "0.1",
    "eventType" : "com.example.someevent",
    "source" : "/mycontext",
    "eventID" : "C234-1234-1234",
    "eventTime" : "2018-04-05T17:31:00Z",
    "properties" : {
      "comExampleExtension" : "value"
    },
    "contentType" : "application/json",
    "data" : {
        "appinfoA" : "abc",
        "appinfoB" : 123,
        "appinfoC" : true
    }
}
```

## 4. References

* [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
* [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
* [RFC4627][RFC4627] The application/json Media Type for JavaScript Object
  Notation (JSON)
* [RFC4648][RFC4648] The Base16, Base32, and Base64 Data Encodings
* [RFC6839][RFC6839] Additional Media Type Structured Syntax Suffixes
* [RFC8259][RFC8259] The JavaScript Object Notation (JSON) Data Interchange Format

[base64]: https://tools.ietf.org/html/rfc4648#section-4
[CE]: ./spec.md
[Content-Type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[JSON-format]: ./json-format.md
[JSON-geoseq]: https://www.iana.org/assignments/media-types/application/geo+json-seq
[JSON-Object]: https://tools.ietf.org/html/rfc7159#section-4
[JSON-seq]: https://www.iana.org/assignments/media-types/application/json-seq
[JSON-String]: https://tools.ietf.org/html/rfc7159#section-7
[JSON-Value]: https://tools.ietf.org/html/rfc7159#section-3
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC4627]: https://tools.ietf.org/html/rfc4627
[RFC4648]: https://tools.ietf.org/html/rfc4648
[RFC6839]: https://tools.ietf.org/html/rfc6839#section-3.1
[RFC8259]: https://tools.ietf.org/html/rfc8259
