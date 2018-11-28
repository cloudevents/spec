# AMQP Event Format for CloudEvents

## Abstract

The AMQP Format for CloudEvents defines how event attributes are expressed in
the [AMQP 1.0 Type System][type-system].

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [References](#3-references)

## 1. Introduction

[CloudEvents][CE] is a standardized and transport-neutral definition of the
structure and metadata description of events. This specification defines how
the elements defined in the CloudEvents specification are to be represented in
the [AMQP 1.0 Type System][amqp-types].

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes for use as AMQP message
properties.

This specification does not define an envelope format. The AMQP type system's
intent is primarily to provide a consistent type system for AMQP itself and
not for message payloads.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

## 2. Attributes

This section defines how CloudEvents attributes are mapped to the AMQP
type-system. This specification does not explicitly map each attribute, but
provides a generic mapping model that applies to all current and future
CloudEvents attributes, including extensions.

### 2.1. Base Type System

The core [CloudEvents specification][CE] defines a minimal abstract type
system, which this mapping leans on.

### 2.2. Type System Mapping

The CloudEvents type system MUST be mapped to AMQP types as follows,
with exceptions noted below.

| CloudEvents   | AMQP
|---------------|-------------------------------------------------------------
| String        | [string][AMQP-String]
| Integer       | [long][AMQP-Long]
| Binary        | [binary][AMQP-Binary]
| URI-reference | [string][AMQP-String]
| Timestamp     | [timestamp][AMQP-Timestamp]
| Map           | [map][AMQP-Map]
| Any           | See 2.3.

Extension specifications MAY define diverging mapping rules for the values of
attributes they define.

For instance, the attribute value may be a data structure
defined in a standard outside of CloudEvents, with a formal AMQP mapping, and
there might be risk of translation errors or information loss when the original
format is not preserved.

An extension specification that defines a diverging mapping rule for AMQP,
and any revision of such a specification, MUST also define explicit mapping
rules for all other event formats that are part of the CloudEvents core at
the time of the submission or revision.

### 2.3. Mapping Any-typed Attributes

`Any`-typed CloudEvents values can either hold a `String`, or a `Binary`
value, or a `Map`. `Map` entry values are also `Any` typed. AMQP's type
system natively represents dynamic typing in its [type system
encoding][type-system-encoding], and therefore immediately allows for the required
variant type representation.

## 3. References

* [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two:
  Media Types
* [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
* [OASIS-AMQP-1.0][OASIS-AMQP-1.0] OASIS Advanced Message Queuing Protocol (AMQP) Version 1.0

[CE]: ./spec.md
[Content-Type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[type-system]: https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html
[type-system-encoding]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#section-encodings
[AMQP-String]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-string
[AMQP-Long]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-long
[AMQP-Binary]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-binary
[AMQP-Timestamp]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-timestamp
[AMQP-Map]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#type-map
[AMQP-DescribedType]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-types-v1.0-os.html#doc-idp38080
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC4627]: https://tools.ietf.org/html/rfc4627
[RFC4648]: https://tools.ietf.org/html/rfc4648
[RFC6839]: https://tools.ietf.org/html/rfc6839#section-3.1
[RFC8259]: https://tools.ietf.org/html/rfc8259
