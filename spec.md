<!--
---
linkTitle: "Common Metadata"
weight: 30
icon: "fas fa-info-circle"
hide_summary: true
description: >
    Introduction to CDEvents and specification of common metadata
---
-->
# CDEvents

## Abstract

CDEvents is a common specification for Continuous Delivery events.

## Table of Contents

<!-- toc -->
- [Overview](#overview)
- [Notations and Terminology](#notations-and-terminology)
  - [Notational Conventions](#notational-conventions)
  - [Terminology](#terminology)
    - [Event](#event)
    - [Subject](#subject)
    - [Predicate](#predicate)
  - [Types](#types)
- [CDEvent context](#cdevent-context)
  - [REQUIRED Context Attributes](#required-context-attributes)
    - [id (context)](#id-context)
    - [type (context)](#type-context)
    - [source (context)](#source-context)
    - [timestamp](#timestamp)
    - [specversion](#specversion)
  - [OPTIONAL Context  Attributes](#optional-context-attributes)
    - [chainId](#chainId)
    - [links](#links)
  - [Context example](#context-example)
- [CDEvent subject](#cdevent-subject)
  - [REQUIRED Subject Attributes](#required-subject-attributes)
    - [id (subject)](#id-subject)
    - [content](#content)
  - [OPTIONAL Subject Attributes](#optional-subject-attributes)
    - [source (subject)](#source-subject)
  - [Subject example](#subject-example)
- [CDEvents custom data](#cdevents-custom-data)
  - [OPTIONAL Custom Data attributes](#optional-custom-data-attributes)
    - [customData](#customdata)
    - [customDataContentType](#customdatacontenttype)
  - [Examples](#examples)
    - [JSON Data](#json-data)
    - [Generic Data](#generic-data)
- [Vocabulary](#vocabulary)
  - [Vocabulary Stages](#vocabulary-stages)
<!-- /toc -->

## Overview

Each CDEvent is structured into two mandatory parts:

- The [*context*](#cdevent-context): its structure is common to all CDEvents
- The [*subject*](#cdevent-subject): part of its root structure is common to all
  CDEvents, some of its content may vary from event to event, as described in
  the *vocabulary*

plus two optional attributes `customData` and `customDataEncoding`, that host
[*CDEvents custom data*](#cdevents-custom-data).

The specification is structured in two main parts:

- [This](#cdevents) document describes the part of the spec that are common to
  __all__ events:
  - The [*context*](#cdevent-context), made of mandatory and optional
    *attributes*
  - The common part of the [*subject*](#cdevent-subject)
  - How to include custom / additional [*data*](#cdevents-custom-data) in a CDEvent

- The [*vocabulary*](#vocabulary) describes *event types*, with their event
  specific mandatory and optional attributes. These attributes are all located
  in the [*subject*](#cdevent-subject) object within the event. The
  [*vocabulary*](#vocabulary) is organized in *stages*, each specified in a
  dedicated document in the spec.

For an introduction see the [CDEvents README](README.md) and for more background
information please see our [CDEvents primer](https://cdevents.dev/docs/primer/).

## Spelling

CDEvents adopt american english ("en_US") as dictionary for spelling both in the
specification as well as in the documentation.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

For clarity, when a feature is marked as "OPTIONAL" this means that it is
OPTIONAL for both the [Producer][producer] and [Consumer][consumer] of a
message to support that feature. In other words, a producer can choose to
include that feature in a message if it wants, and a consumer can choose to
support that feature if it wants. A consumer that does not support that feature
will then silently ignore that part of the message. The producer needs to be
prepared for the situation where a consumer ignores that feature. An
[Intermediary][intermediary] SHOULD forward OPTIONAL attributes.

### Terminology

__Note__: CDEvents adopts, wherever applicable, the terminology used by
[CloudEvents](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#notational-conventions).
Specifically, the following terms are borrowed from the CloudEvents spec:

- [*Occurrence*][occurrence]
- [*Producer*][producer]
- [*Source*][source]
- [*Consumer*][consumer]
- [*Intermediary*][intermediary]

The CDEvents specification additionally defines the following terms:

#### Event

An "event" is a data record expressing an occurrence and its context. Events are
routed from an event producer (the source) to interested event consumers. The
routing can be performed based on information contained in the event, but an
event will not identify a specific routing destination.

#### Subject

The "subject" is the entity with which the occurrence in a software system
is concerned. For instance when a software build is started, the build is the
subject of the occurrence, or when a service is deployed, the subject is the
service. Subjects have a list of *attributes* associated, defined in the
[vocabulary](#vocabulary). Subjects belong to two main categories:

- long running, which stay in a running state until they're purposely stopped or
  encounter a failure or a condition that prevents them from running - for
  example a service, an environment, an artifact or a source change
- run to completion, which independently stop after they accomplished (or
  failed to) a specific task, or encounter a failure or a condition that
  prevents them from continuing - for example a task run, a build or a test

#### Predicate

A "predicate" is what happened to a subject in an occurrence.
For instance in case of a software build, started is a valid predicate in the
occurrence, or in case of a service, deployed in a valid predicate. Valid
predicate are defined in the [vocabulary](#vocabulary).

### Types

Attributes in CDEvents are defined with as typed. We use a the
[types system](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type-system)
defined by the CloudEvents project, plus some CDEvents specific types

- `Enum`: an attribute of type `String`, constrained to a fixed set of options
- `List`: a list of values of the same type
- `Object`: a map of (key, value) tuples
  - Keys are of type `String`. Valid keys can be defined by this spec
  - Values can be any of the other kind
  - An object key is referred to as an "attribute"
- `Purl`: a string in [package-url][purl-spec] format

  Object key names are by convention defined in [CamelCase](https://en.wikipedia.org/wiki/Camel_case).

## CDEvent context

### REQUIRED Context Attributes

The following context attributes are REQUIRED to be present in all the Events
defined in the [vocabulary](#vocabulary):

#### id (context)

- Type: [`String`][typesystem]
- Description: Identifier for an event.
  Subsequent delivery attempts of the same event MAY share the same
  [`id`](#id-context). This attribute matches the syntax and semantics of the
  [`id`](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id)
  attribute of CloudEvents.

- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST be unique within the given [`source`](#source-context) (in the scope of
    the producer)
- Examples:
  - A [UUID version 4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random))

#### type (context)

- Type: [`String`][typesystem]
- Description: defines the type of event, as combination of a *subject*,
  *predicate* and *version*. Valid event types are defined in the [vocabulary](#vocabulary).

  All event types should be prefixed with `dev.cdevents.`. One occurrence may
  have multiple events associated, as long as they have different event types.
  *Versions* are semantic in the *major.minor.patch* format (`M.m.p`). For more details about versions
  see the the see [versioning](https://cdevents.dev/docs/primer/#versioning) documentation.

  In addition to `dev.cdevents.`, event types prefixed with `dev.cdeventsx.` can be defined in
  specifications outside of CDEvents. Events that use these event types can be partly produced
  and validated by CDEvents SDKs and are known a ["custom events"](custom/README.md).
  External specifications can be registered in this repository in the
  [custom events registry](custom/registry.md).

- Constraints:
  - REQUIRED
  - `dev.cdevents.` types MUST be defined in the [vocabulary](#vocabulary)
  - `dev.cdeventsx.` types SHOULD be defined in a third party specification

- Examples:
  - `dev.cdevents.taskrun.started.0.2.0`
  - `dev.cdevents.environment.created.0.2.0`
  - `dev.cdevents.<subject>.<predicate>.M.m.p`
  - `dev.cdeventsx.mytool-process.finished.0.1.0`
  - `dev.cdeventsx.<tool>-<subject>.<predicate>.M.m.p`

#### source (context)

- Type: [`URI-Reference`][typesystem]
- Description: defines the context in which an event happened. The main purpose
  of the source is to provide global uniqueness for [`source`](#source-context) +
  [`id`](#id-context).

  The source MAY identify a single producer or a group of producer that belong
  to the same application.

  When selecting the format for the source, it may be useful to think about how
  clients may use it. Using the [root use cases](https://cdevents.dev/docs/primer/#use-cases) as
  reference:

  - A client may want to react only to events sent by a specific service, like
    the instance of Tekton that runs in a specific cluster or the instance of
    Jenkins managed by team X
  - A client may want to collate all events coming from a specific source for
    monitoring, observability or visualization purposes

- Constraints:
  - REQUIRED
  - MUST be a non-empty URI-reference
  - An absolute URI is RECOMMENDED

- Examples:

  - If there is a single "context" (cloud, cluster or platform of some kind)
    - `/tekton`
    - `https://www.jenkins.io/`

  - If there are multiple "contexts":
    - `/cloud1/spinnaker-A`
    - `/cluster2/keptn-A`
    - `/teamX/knative-1`

#### timestamp

- Type: [timestamp][typesystem]
- Description: defines the time of the occurrence. When the time of the
  occurrence is not available, the time when the event was produced MAY be used.

  In case the transport layer should require a re-transmission of the event,
  the timestamp SHOULD NOT be updated, i.e. it should be the same for the same
  [`source`](#source-context) + [`id`](#id-context) combination.

- Constraints:
  - REQUIRED
  - MUST adhere to the format specified in [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339)

#### specversion

- Type: `String`
- Description: The version of the CDEvents specification which the event
  uses. This enables the interpretation of the context. Compliant event
  producers MUST use a value of `0.1.1` when referring to this version of the
  specification. For more details see [versioning](https://cdevents.dev/docs/primer/#versioning).

- Constraints:
  - REQUIRED
  - MUST be a non-empty string

### OPTIONAL Context Attributes

#### schemaUri

- Type: [`URI`][typesystem]
- Description: link to a `jsonschema` schema that further refines the event schema
  as defined by CDEvents.

  The schema provided by the `schemaUri` MUST be stricter than the CDEvents one,
  and thus MUST NOT allow elements that would not be allowed by the CDEvents schema.
  For example, the schema at `schemaUri` could define the content of `customData`
  or restrict a `string` field to a specific `Enum`.

  Versioning of the schema provided in `schemaUri` is up to the maintainer, there
  is no specific requirement from CDEvents side.

  Consumers of events that specify a `schemaUri` SHOULD validate the event against
  the CDEvents schema as well as the additional schema provided. If the consumer
  does not have access to the URI specified, it SHOULD fail to validate the event.

- Constraints:
  - OPTIONAL
  - When specified, it MUST be a non-empty URI
  - An absolute URI is REQUIRED

- Examples:

  - If there is a single "context" (cloud, cluster or platform of some kind)
    - `https://myorg.com/cdevents/schema/artifact-published-0-1-0`

#### chainId

- Type: [`String`][typesystem]
- Description: Identifier for a chain as defined in the [links spec](links.md).

- Constraints:
  - A [UUID version 4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random))

#### links

- Type: [`List`][typesystem]
- Description: A list of link objects as defined in the [links spec](links.md).

- Examples:
  - A path link which is used to indicate a direct connection between two
    events

    ```json
    [
      {
        "linkType": "PATH",
        "from": {
          "contextId": "271069a8-fc18-44f1-b38f-9d70a1695819"
        }
      }
    ]
    ```
  - A relation link where the `contextId` is was some trigger for this event

    ```json
    [
      {
        "linkType": "RELATION",
        "linkKind": "TRIGGER",
        "target": {
          "contextId": "5328c37f-bb7e-4bb7-84ea-9f5f85e4a7ce"
        }
      }
    ]
    ```
  - An end link signaling the end of a chain

    ```json
    [
      {
        "linkType": "END",
        "from": {
          "contextId": "fb455028-a876-430e-a5ff-4b2ece77e827"
        }
      }
    ]
    ```

### Context example

This is an example of a full CDEvent context, rendered in JSON format:

```json
{
    "context": {
    "specversion": "0.6.0-draft",
    "id" : "A234-1234-1234",
    "source" : "/staging/tekton/",
    "type" : "dev.cdevents.taskrun.started.0.2.0",
    "timestamp" : "2018-04-05T17:31:00Z",
    "schemaUri":  "https://myorg.com/cdevents/schema/taskrun-started-1-1-0"
  }
}
```

## CDEvent subject

### REQUIRED Subject Attributes

The following subject attributes are REQUIRED to be present in all the event
defined in the [vocabulary](#vocabulary):

#### id (subject)

- Type: [`String`][typesystem]
- Description: Identifier for a subject.
  Subsequent events associated to the same subject MUST use the same subject
  [`id`](#id-subject).

- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST be unique within the given [`source`](#source-subject) (in the scope of
    the producer)
- Examples:
  - A [UUID version 4](https://en.wikipedia.org/wiki/Universally_unique_identifier#Version_4_(random))

#### content

- Type: [`Object`](#types)
- Description: This provides all the relevant details of the
  [`content`](#content). The format of the [`content`](#content) depends on the
  event [`type`](#type-context). All attributes in the subject
  [`content`](#content), REQUIRED and OPTIONAL ones, MUST comply with the
  specification from the [vocabulary](#vocabulary). The [`content`](#content)
  may be empty.

- Constraints:
  - REQUIRED

- Example:
  - Considering the event type `dev.cdevents.taskrun.started.0.2.0`, an example of
    subject, serialized as JSON, is:

    ```json
        "content" : {
          "task": "my-task",
          "uri": "/apis/tekton.dev/v1beta1/namespaces/default/taskruns/my-taskrun-123"
        }
    ```

### OPTIONAL Subject Attributes

#### source (subject)

- Type: [`URI-Reference`][typesystem]
- Description: defines the context in which the subject originated. In most
  cases the [`source`](#source-subject) of the subject matches the
  [`source`](#source-context) of the event. This field should be used only in
  cases where the [`source`](#source-subject) of the *subject* is different from
  the [`source`](#source-context) of the event.

  The format and semantic of the *subject* [`source`](#source-subject) are the
  same of those of the *context* [`source`](#source-context).

### Subject example

The following example shows `context` and `subject` together, rendered as JSON.

```json
{
   "context": {
      "specversion": "0.6.0-draft",
      "id" : "A234-1234-1234",
      "source" : "/staging/tekton/",
      "type" : "dev.cdevents.taskrun.started.0.2.0",
      "timestamp" : "2018-04-05T17:31:00Z"
   },
   "subject" : {
      "id": "my-taskrun-123",
      "content": {
         "task": "my-task",
         "uri": "/apis/tekton.dev/v1beta1/namespaces/default/taskruns/my-taskrun-123",
         "pipelineRun": {
            "id": "my-distributed-pipelinerun",
            "source": "/tenant1/tekton/"
         }
      }
   }
}
```

## CDEvents custom data

The `customData` and `customDataContentType` fields can be used to carry
additional data in CDEvents.

### OPTIONAL Custom Data attributes

#### customData

- Type: This specification does not place any restriction on the type of this
  information.
- Description: custom data. The content of the `customData` field is not
  specified in CDEvent and typically require tool specific knowledge
  to be parsed.

- Constraints:
  - OPTIONAL

- Examples:
  - `{"mydata1": "myvalue1"}`
  - `"VGhlIHZvY2FidWxhcnkgZGVmaW5lcyAqZXZlbnQgdHlwZXMqLCB3aGljaCBhcmUgbWFkZSBvZiAqc3ViamVjdHMqCg=="`

#### customDataContentType

The `customDataContentType` is modelled after the [CloudEvents datacontenttype][datacontenttype].

- Type: [`String`][typesystem]
- Description: Content type of `customData` value. This attribute enables data
  to carry any type of content, whereby format and encoding might differ from
  that of the chosen event format. For example, an event rendered using the
  [CloudEvents](cloudevents-binding.md) format might carry an XML payload in
  data, and the consumer is informed by this attribute being set to
  "application/xml". The rules for how data content is rendered for different
  `customDataContentType` values are defined in the specific binding
  specification

- Default value: "application/json"

- Constraints:
  - OPTIONAL
  - If present, MUST adhere to the format specified in [RFC 2046][rfc2406]

### Examples

#### JSON Data

Data with the default "application/json" content-type can be included directly
in the `customData` field, as in the following example:

```json
{
  "context": {
    (...)
  },
  "subject" : {
    (...)
  },
  "customData": {
    "mydata1": {
      "f1": "f1",
      "f2": "f2"
    },
    "mydata2": "myvalue1"
  }
}
```

#### Generic Data

Generic (non-JSON) data, must be base64 encoded:

```json
{
  "context": {
    (...)
  },
  "subject" : {
    (...)
  },
  "customData": "PGRhdGE+VkdobElIWnZZMkZpZFd4aGNua2daR1ZtYVc1bGN5QXFaWFpsYm5RZ2RIbHdaWE1xTENCM2FHbGphQ0JoY21VZ2JXRmtaU0J2WmlBcWMzVmlhbVZqZEhNcUNnPT08L2RhdGE+Cg==",
  "customDataContentType": "application/xml"
}
```

## Vocabulary

The vocabulary defines *event types*, which are made of *subjects*, and
*predicates*. An example of *subject* is a `build`. The `build` can be `started`
or `finished`, which are the predicates. The `build` is of type `Object` and
has several *attributes* associated; the *event type* schema defines which ones
are mandatory and which ones are optional. *Subjects* can represent the core
context of an event, but may also be referenced to in other areas of the
protocol.

The *subjects* are grouped, to help browsing the spec, in different *stages*,
which are associated to different parts of a Continuous Delivery process where
they are expected to be *produced*.

These *subjects*, with their associated *predicates* and *attributes*, are
agnostic from any specific tool and are designed to fit a wide range of
scenarios. The CDEvents project collaborates with the
[SIG Interoperability](https://github.com/cdfoundation/sig-interoperability) to
identify a the common terminology to be used and how it maps to different terms
in different platforms.

### Vocabulary Stages

The [*vocabulary*](#vocabulary) is organized in *stages*, each specified in a
dedicated document in the spec:

- __[Core](core.md)__: includes core events related to core activities and
  orchestration that needs to exist to be able to deterministically and
  continuously being able to delivery software to users.
- __[Source Code Version Control](source-code-version-control.md)__: Events
  emitted by changes in source code or by the creation, modification or
  deletion of new repositories that hold source code.
- __[Continuous Integration](continuous-integration.md)__:
  includes events related to building software artifacts and packaging, releasing
  and managing software artifacts.
- __[Testing](testing.md)__:
  includes events related to testing. Sometimes part of continuous
  integration, testing may take place in different stages of the workflow.
- __[Continuous Deployment](continuous-deployment.md)__:
  include events related with environments where the artifacts produced by the
  integration pipelines actually run. These are usually services running in a
  specific environment (dev, QA, production), or embedded software running in
  a specific hardware.
- __[Continuous Operations](continuous-operations.md)__: include events related
  to the health of the services deployed and running in a specific environment.
  Health may refer to different aspects such as performance, availability,
  response time and more.

The grouping may serve in future as a reference for different CDEvents
compliance profiles, which can be supported individually by implementing
platforms.

[source]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source
[producer]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#producer
[consumer]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#consumer
[intermediary]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#intermediary
[occurrence]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#occurrence
[typesystem]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type-system
[datacontenttype]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#datacontenttype
[rfc2406]: https://tools.ietf.org/html/rfc2046
[purl-spec]: https://github.com/package-url/purl-spec/blob/master/PURL-SPECIFICATION.rst
