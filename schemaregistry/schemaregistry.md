# CNCF Schema Registry API Version 0.1-rc01s

## Abstract

This specification defines a simple API for storing, organizing, and accessing
schema documents for use with serialization and data validation frameworks such
as Apache Avro and JSON Schema.

## Status of this document

This document is a working draft.

## 1. Introduction

Schema-dependent serialization formats and related frameworks such as Apache
Avro are popular in eventing and messaging scenarios. With most of the metadata
information such as names and types of fields being held externally in schema
documents, these frameworks are able to produce very compact on-wire
representations of structured data that is carries as the payload of events and
messages. While the wire-footprint savings are often very significant, the added
cost is that of schema handling. All communicating parties who need to
deserialize the event or message payload need access to the schema used to
publish it.

For formats that do not depend on external schemas for serialization, schemas
might still be required in some scenarios to allow for consumers or inspecting
intermediaries to validate the data structure's compliance with a set of rules.

This specification defines a very simple API focused on storing, organizing, and
accessing such documents. While there are very sophisticated metadata management
solutions available as open source und under neutral governance already, the focus
of this specification is not great sophistication but straightforward simplicity.

This schema registry deals with only three top-level elements:

- Schema Group: A named collection of schemas. Each group holds a logically
  related set of schemas, typically belonging to a particular application or
  subject to shared access control rules.
- Schema: A document describing the structure, names, and types of some
  structured data payload.
- Version: A specific version of a schema document. Even though not prescribed
  in this specification, an implementation might choose to impose compatibility
  constraints on versions following the initial version of a schema.

> NOTE: There are two fundamentally different options for how we can organize
> multiple schema formats and this specification draft reflects both: 
>
> 1) In an "ideal" REST service, any data entity can be represented ("R" in
>    REST) in multiple different data formats, which a client can request in
>    prioritized order during content-type negotiation. If a service offers up
>    the same entity in JSON, Protobuf, and Avro formats, there would therefore
>    be three distinct schemas, each defining a representation of the data
>    entity for the respective format. From the same "REST" mindset perspective,
>    the ideal representation of this set of schemas, which differ with regards
>    to the format they describe, but ought to be semantically identical, is to
>    also differentiate them only by their content type and maintain them under
>    the exact same name as if they were one schema.
> 2) Since the above strategy is truly RESTful, but quite esoteric if you've not
>    grown up as a RESTafarian, the alternative strategy for concurrently
>    handling multiple schema formats is much simpler: Constrain each schema
>    group to a single format.

## 2. Schema Registry Elements

This section further describes the elements enumerated in the introduction.

### 2.1. Schema Group

A schema group is a named collection of schemas. Since a schema registry is
often a resource with a scope greater than a single application and might even
span multiple organizations, it is very useful to put a grouping construct
around sets of schemas that are related either by ownership or by a shared
subject matter context.

Implementations of this specification MAY associate access control rules with
schema groups. For instance, a user or a group of users might be given write
access only to a particular schema group that their organization owns. If trade
secret protection is required for an application or parts of it and the schema
structure would give some of those away, read access to a group of schemas might
likewise be restricted. 

Access control rules at the schema group level MUST NOT limit visibility of the
schema groups themselves to users authorized to enumerate schema groups at the
registry level or to create new schema groups in order to create unambiguous
transparency about which `id` have already been taken. An implementation MAY
withhold all details other than the `id` attribute from a user not authorized
to access the schema group.

This specification does not define management constructs for such access control
rules.

### 2.1.1. Schema group attributes

The data model for a schema group consists of three attributes:

#### id

- Type: `String`
- Description: Identifies the schema group.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST conform with RFC3986/3.3 `segment-nz-nc` syntax
  - MUST be unique within the scope of the schema registry
- Examples:
  - mygroup
  - my-group

#### format

- Type: `String`
- Description: Defines the schema format managed by this schema group. The
  formats supported by an implementation are specific to the implementation.
  This specification does not mandate support for particular formats.
- Constraints:
  - OPTIONAL. If not set, each schema in the group MAY have multiple, concurrent
    format representations. See XXXX
  - MUST be a non-empty string, if present.
- Examples:
  - "avro"
  - "json-schema"
  - "xsd11"

#### description

- Type: `String`
- Description: Explains the purpose of the schema group.
- Constraints:
  - OPTIONAL
- Examples:
  - "This group holds schemas for the fabulous example app."

## 2.2. Schema and Schema Version

Conceptually, a schema is a description of a data structure. Since data
structures evolve over time, the schema describing them will also evolve over
time. Therefore, a schema often has multiple versions.

For simple scenarios, the API allows for version management to be automatic and
transparent. Whenever a schema is updated, a new version number is assigned and
prior schema versions are retained. The latest available schema is always the
default version that is retrieved when the API is given just the schema `id`.

A newer schema version might introduce breaking changes or it might only
introduce careful changes that preserve compatibility. These strategies are not
subject of this specification, but the API provides a conflict handling
mechanism that allows an implementation to reject updates that do not comply
with a compatibility policy, if one has been implemented.

### 2.2.1. Multi-format schema sets

If the schema format has not been restricted at the schema group level, each
schema may describe the same data structure for encoding in different formats
concurrently. That implies that the schema managed by this registry is not
a single document, but MAY be a set of documents that all describe the exact
same data structure, each in their own particular syntax and using their own 
type model.

The schema version therefore relates to this abstract notion of schema and the
described data structure. All documents coexisting within the same version
SHOULD describe the exact same data structure.

### 2.2.2. Schema attributes

As per the definition above, the schema object is a collection of versions
of schema documents. It only has an identifier attribute.

#### id

- Type: `String`
- Description: Identifies the schema.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST conform with RFC3986/3.3 `segment-nz-nc` syntax
  - MUST be unique within the scope of the schema registry
- Examples:
  - myschema
  - my-schema

### 2.2.3 Schema version attributes

A schema version is a document. The "body" of a schema version MAY be a text
document or binary stream. An implementation SHOULD validate whether a
schema version is valid according to the rules of its format, for instance
whether it is a valid Avro schema document when the format is Apache Avro.

Within the scope of the schema set, the version is identified by the combination
of a version number and an optional format identifier. The schema version MAY
also have an additional, optional unique identifier within the scope of the
registry.

#### version

- Type: `Integer`
- Description: The version of the schema. This is a simple counter and tracks
  the version in the scope of this schema within the schema group. The schema
  document MAY indicate a schema that follows a different versioning scheme.
- Constraints:
  - REQUIRED
  - Assigned by server.
- Examples:
  - 1
  - 2

#### format

- Type: `String`
- Description: 
- Constraints:
  - OPTIONAL. Can be used if and only if not format has been set for the schema
    group hosting the schema.
  - MUST be a non-empty string, if present.
- Examples:
  - "avro"
  - "json-schema"
  - "xsd11"

#### id

- Type: `String`
- Description: Identifies the schema document uniquely without requiring
  other qualifiers.
- Constraints:
  - OPTIONAL
  - Assigned by the server.
- Examples:
  - { ... guid ... }  

## 3. HTTP ("REST") API 

This section informally describes the HTTP API binding of this schema registry.
The formal definition is the [OpenAPI document](./schemaregistry.yaml) that is
part of this specification.

### 3.1. Path hierarchy

Schema groups contain schemas and those contain schema versions, which are the
documents required for serialization or validation.

These dependencies are reflected in the path structure:

`/schemagroups/{group-id}/schemas/{schema-id}/versions/{version}`

The name of the first segment of the path is a suggestion and MAY differ between
implementations and the registry does not need to be anchored at the site root.
The segment names `schemas` and `versions` MUST be used.

- `{group-id}` corresponds to the schema group's [`id` attribute](#id)
- `{schema-id}` corresponds to the schema's [`id` attribute](#id-1)
- `{version}` corresponds to the schema version's [`version` attribute](#version)

### 3.2. Operations at the groups level

### 3.3 Operations at the schemas level 

### 3.4 Operations at the versions level