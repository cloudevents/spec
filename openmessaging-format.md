# OpenMessaging Event Format for CloudEvents - Version 0.1

## Abstract

The OpenMessaging Event Format for CloudEvents defines how events are expressed 
in [OpenMessaging][OpenMessaging].

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [References](#3-references)

## 1. Introduction
The [OpenMessaging][OpenMessaging] Format for CloudEvents defines how event 
attributes are expressed in the [OpenMessaging Type System][OpenMessaging-Spec].

The [Attributes](#2-attributes) section describes the naming conventions and 
data type mappings for CloudEvents attributes for use as OpenMessaging message 
properties.

This specification does not define an envelope format. The OpenMessaging type 
system's intent is primarily to provide a consistent type system for 
OpenMessaging itself and not for message payloads.


### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

## 2. Attributes

This section defines how CloudEvents attributes are mapped to OpenMessaging 
type-system . This specification does not explicitly map each attribute, but 
provides a generic mapping model that applies to all current and future 
CloudEvents attributes, including extensions.

### 2.1. Base Type System

This mapping leans on [CloudEvents specification][CE].

### 2.2. Type System Mapping

The CloudEvents type system is mapped to OpenMessaging types as follows:

| CloudEvents | OpenMessaging
|--------------|-------------------------------------------------------------
| String       | [String][OpenMessaging-Spec]
| Binary       | [Binary][OpenMessaging-Spec]
| URI          | [URI][OpenMessaging-Spec]
| Timestamp    | [String][OpenMessaging-Spec]
| Map          | [Key-Value][OpenMessaging-Spec]
| Object       | [Object][OpenMessaging-Spec]

## 3. References

- [OpenMessaging][OpenMessaging] The OpenMessaging repository
- [OpenMessaging Type System][OpenMessaging-Spec] The type system in 
OpenMessaging specification

[CE]: ./spec.md
[OpenMessaging]: https://github.com/openmessaging
[OpenMessaging-Spec]: https://github.com/openmessaging/specification/blob/master/specification-schema.md
