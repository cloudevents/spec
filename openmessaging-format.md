# OpenMessaging Event Format for CloudEvents - Version 0.1

## Abstract

The OpenMessaging Format for CloudEvents defines how events are expressed in
Open Messaging.

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
the [OpenMessaging][OpenMessaging].

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes.

The [Envelope](#3-envelope) section defines a OpenMessaging container for CloudEvents
attributes and an associated media type.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

## 2. Attributes

This section defines how CloudEvents attributes are mapped to OpenMessaging. This
specification does not explicitly map each attribute, but provides a generic
mapping model that applies to all current and future CloudEvents attributes.

### 2.1. Base Type System

The core [CloudEvents specification][CE] defines a minimal abstract type
system, which this mapping leans on.

### 2.2. Type System Mapping

The CloudEvents type system is mapped to JSON types as follows:

| CloudEvents | JSON
|--------------|-------------------------------------------------------------
| String       | [String][String]
| Binary       | [Binary][binary], unicode binary
| URI          | [String][String]
| Timestamp    | [String][String]
| Map          | [Map][map]
| Object       | see2.3

### 2.3. Mapping Object-typed Attributes

`Object`-typed CloudEvents values can either hold a `String`, or a `Binary`
value, or a `Map`. `Map` entry values are also `Object` typed. OpenMessaging's type
system natively represents dynamic typing in its [type system
encoding][type-system-encoding], and therefore immediately allows for the required
variant type representation.

### 2.4. Examples

The following table shows exemplary mappings:

| CloudEvents       | Type     | Exemplary OpenMessaging Value
|--------------------|----------|-------------------------------
| eventType          | String   | "openMessaging"
| eventTypeVersion   | String   | "1.0"
| cloudEventsVersion | String   | "0.1"
| source             | URI      | "openMessaging.io.event"
| eventID            | String   | "1234-1234-1234"
| eventTime          | Timestamp| "2018-04-05T17:31:00Z"
| contentType        | String   | "text/json"
| extensions         | Map      | { "extA" : "vA", "extB", "vB" }
| data               | String   | "test openMessaging"
| data               | Binary   | "156,134,111"
| data               | Map      | { "objA" : "vA", "objB", "vB" }

## 3. Envelope
Each CloudEvents event can be wholly represented as a OpenMessaging object.

Such a representation uses the *userHeader* in the OpenMessaging,
If the property "cloudEvent" existed, it represented it's a cloud event message.
All REQUIRED and all not omitted OPTIONAL attributes in the given event MUST
become members of the OpenMessaging object, with the respective OpenMessaging object member name
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

Unlike all other attributes, for which value types are restricted to strings
per the [type-system mapping](#22-type-system-mapping), the resulting `data`
member [JSON value][JSON-Value] is unrestricted, and if `contentType` value is either "binary/thrift",it represented
that the data should be interpreted by the thrift protocol. so for the binary, users can customize 
the serialization protocol. 


## 4. References

- [OpenMessaging][OpenMessaging] The NATS Messaging System
- [RFC4627][RFC4627] The application/json Media Type for JavaScript Object Notation (JSON)
- [RFC6839][RFC6839] additional Media Type Structured Syntax Suffixes

[base64]: https://tools.ietf.org/html/rfc4648#section-4
[CE]: ./spec.md
[OpenMessaging]: https://github.com/openmessaging
[RFC4627]: https://tools.ietf.org/html/rfc4627
[RFC6839]: https://tools.ietf.org/html/rfc6839#section-3.1
