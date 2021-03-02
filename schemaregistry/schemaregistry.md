# CNCF Schema Registry API Version 0.1-wip

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
representations of structured data that is carried as the payload of events and
messages. While the wire-footprint savings are often very significant, the added
cost is that of schema handling. All communicating parties who need to
deserialize the event or message payload need access to the schema used to
publish it.

For formats that do not depend on external schemas for serialization, schemas
might still be required in some scenarios to allow for consumers or inspecting
intermediaries to validate the data structure's compliance with a set of rules.

This specification defines a very simple API focused on storing, organizing, and
accessing such documents. While there are very sophisticated metadata management
solutions available as open source and under neutral governance already, the focus
of this specification is not great sophistication but straightforward simplicity.

This schema registry deals with only three top-level elements:

- Schema Group: A named collection of schemas. Each group holds a logically
  related set of schemas, typically managed by a single entity, belonging to a
  particular application and/or having a shared access control management scope.
- Schema: A document describing the structure, names, and types of some
  structured data payload.
- Version: A specific version of a schema document. Even though not prescribed
  in this specification, an implementation might choose to impose compatibility
  constraints on versions following the initial version of a schema.

## 2. Schema Registry Elements

This section further describes the elements enumerated in the introduction. All
data types used in this section are defined in the core CloudEvents
specification and MUST follow the respective formatting and syntax rules unless
specified otherwise.

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

The data model for a schema group consists of these attributes:

#### id

- Type: `String`
- Description: Identifies the schema group.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST conform with RFC3986/3.3 `segment-nz-nc` syntax. This allows for "dot
    notation", e.g. `org.example.myapp.module` for logical organization of
    schema groups, even though the namespace is flat.
  - MUST be unique within the scope of the schema registry
- Examples:
  - mygroup
  - my-group
  - org.example.myapp.module
  - events@example.com

#### format

- Type: `String`
- Description: Defines the schema format managed by this schema group. The
  formats supported by an implementation are specific to the implementation. If
  the format is omitted for the schema group, the format MUST be specified at
  the schema-level. This specification does not mandate support for particular
  formats.
- Constraints:
  - OPTIONAL.
  - MUST be a non-empty string, if present.
  - MUST NOT be modified if at least one schema exists in the group.
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

#### createdtimeutc

- Type: `Timestamp`
- Description: Instant when the schema group was added to the registry.
- Constraints:
  - OPTIONAL
  - Assigned by the server.

#### updatedtimeutc

- Type: `Timestamp` 
- Description: Instant when the schema group was last updated
- Constraints:
  - OPTIONAL
  - Assigned by the server.

## 2.2. Schema and Schema Version

Conceptually, a schema is a description of a data structure. Since data
structures evolve over time, the schema describing them will also evolve over
time. Therefore, a schema often has multiple versions.

For simple scenarios, the API allows for version management to be automatic and
transparent. Whenever a schema is updated, a new version number is assigned and
prior schema versions are retained. This specification does not mandate a
retention policy, but implementations MAY retire and remove outdated schema
versions.

The latest available schema is always the default version that is retrieved when
the URL to the schema is given without the version specified.

A newer schema version might introduce breaking changes or it might only
introduce careful changes that preserve compatibility. These strategies are not
subject of this specification, but the API provides a conflict handling
mechanism that allows an implementation to reject updates that do not comply
with a compatibility policy, if one has been implemented.

### 2.2.1. Multi-format schema groups

If the schema format has not been restricted at the schema group level, each
schema MAY have its own format. This choice is mutually exclusive. If a format
has been defined for the group, schemas in the group MUST use that format. 

### 2.2.2. Schema attributes

As per the definition above, the schema object is a collection of versions
of schema documents. An implementation MAY add further attributes.

#### id

- Type: `String`
- Description: Identifies the schema.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST conform with RFC3986/3.3 `segment-nz-nc` syntax
  - MUST be unique within the scope of the schema group
- Examples:
  - myschema
  - my-schema

#### format

- Type: `String`
- Description: Defines the format of this schema. The formats supported by an
  implementation are specific to the implementation. If the format has been omitted
  for the schema group, the format MUST be specified at the schema-level. This
  specification does not mandate support for particular formats.
- Constraints:
  - REQUIRED if not set at the schema group level.
  - MUST be null (not present) if set at the schema group level.
  - MUST be a non-empty string, if present.
- Examples:
  - "avro"
  - "json-schema"
  - "xsd11"

#### description

- Type: `String`
- Description: Explains the purpose of the schema.
- Constraints:
  - OPTIONAL
- Examples:
  - "This schema describes the toppings for a Pizza."

#### createdtimeutc

- Type: `Timestamp`
- Description: Instant when the schema was added to the registry.
- Constraints:
  - OPTIONAL
  - Assigned by the server.

#### updatedtimeutc

- Type: `Timestamp`
- Description: Instant when the schema was last updated
- Constraints:
  - OPTIONAL
  - Assigned by the server.

### 2.2.3 Schema version attributes

A schema version is a document. The "body" of a schema version MAY be a text
document or binary stream. An implementation SHOULD validate whether a
schema version is valid according to the rules of its format, for instance
whether it is a valid Avro schema document when the format is Apache Avro.

The schema version MAY also have an additional, optional unique identifier
within the scope of the registry.

#### version

- Type: `Integer`
- Description: The version of the schema. This is a simple counter and tracks
  the version in the scope of this schema within the schema group. The schema
  document content MAY indicate a different versioning scheme.
- Constraints:
  - REQUIRED
  - Assigned by server.
- Examples:
  - 1
  - 2

#### id

- Type: `String`
- Description: Identifies the schema document uniquely without requiring
  other qualifiers.
- Constraints:
  - OPTIONAL
  - Assigned by the server.
- Examples:
  - { ... guid ... }

#### description

- Type: `String`
- Description: Explains details of the schema version.
- Constraints:
  - OPTIONAL
- Examples:
  - "This version adds support for different types of Pizza crust."  

#### createdtimeutc

- Type: `Timestamp`
- Description: Instant when the schema version was added to the registry.
- Constraints:
  - OPTIONAL
  - Assigned by the server.

## 3. HTTP ("REST") API 

This section informally describes the HTTP API binding of this schema registry.
The formal definition is the [OpenAPI document](./schemaregistry.yaml) that is
part of this specification.

This section is therefore non-normative.

### 3.1. Path hierarchy

Schema groups contain schemas and those contain schema versions, which are the
documents required for serialization or validation.

These dependencies are reflected in the path structure:

`/schemagroups/{group-id}/schemas/{schema-id}/versions/{version}`

The name of the first segment of the path ("/schemagroups") is an illustrative
suggestion and MAY differ between implementations and the registry does not need
to be anchored at the site root. The segment names `schemas` and `versions` MUST
be used.

- `{group-id}` corresponds to the schema group's [`id` attribute](#id)
- `{schema-id}` corresponds to the schema's [`id` attribute](#id-1)
- `{version}` corresponds to the schema version's [`version` attribute](#version)

### 3.2. Operations at the groups level

#### 3.2.1. List schema groups

Schema groups are enumerated with a GET on the root of the registry hierarchy,
in the exemplary structure above identified as `/schemagroups`.

The result is a JSON encoded array of strings enumerating the `id` values of the
schema groups.

#### 3.2.2. Get schema group

The details of a schema group are retrieved with a GET on the group's path in
the schema groups collection, for instance `/schemagroups/mygroup`. 

The result is a JSON object that contains the attributes of the schema group.

#### 3.2.3. Create schema group

A schema group is created with a PUT on the desired group's path in
the schema groups collection, for instance `/schemagroups/mygroup`.

The payload is a JSON object that contains the attributes of the schema group.

The operation returns the effective attributes as a JSON object when the schema
group has been created or updated.

#### 3.2.4. Delete schema group

A schema group is deleted with a DELETE on the desired group's path in
the schema groups collection, for instance `/schemagroups/mygroup`.

### 3.3 Operations at the schemas level 

#### 3.3.1. List schemas for the group

Schemas within a schema group are enumerated with a GET on the `schemas`
collection of the group, for instance `/schemagroups/mygroup/schemas`.

The result is a JSON encoded array of strings enumerating the `id` values of the
schemas within the group.

#### 3.3.2. Delete all schemas from the group

All schemas of a schema group can be deleted DELETE on the `schemas`
collection of the group, for instance `/schemagroups/mygroup/schemas`.

#### 3.3.3. Add a new schema version

A new schema or a new version of a schema is added to the version collection
with a POST on the desired schema's path in the schemas collection, for instance
`/schemagroups/mygroup/schemas/myschema`.

This operation will either create a new schema and store the document under the
first version identifier assigned by the server or will update the schema by
assigning a new version to the given document and storing it.

The payload of the request is the schema document. All further attributes such
as the `description` or the `format` indicator are passed either via the query
string or as HTTP headers.  

The ´Content-Type´ for the payload MUST be preserved by the registry and
returned when the schema is requested, independent of the format identifier. 

#### 3.3.4. Get the latest version of a schema

The latest version of a schema is retrieved via a GET on schema's path in the
schemas collection, for instance `/schemagroups/mygroup/schemas/myschema`. 

The returned payload is the schema document. Further attributes such as the
`description` and the `format` indicator are returned as HTTP headers.

The returned ´Content-Type´ is the same that was passed when the schema version
was registered.

The HEAD method SHOULD also be implemented.

#### 3.3.4. Delete a schema

A schema including all its versions is deleted with a DELETE on schema's path in the
schemas collection, for instance `/schemagroups/mygroup/schemas/myschema`

### 3.4 Operations at the versions level

#### 3.4.1. List all versions of the schema

Versions of a schema within a schema group are enumerated with a GET on the
`versions` collection of the schema, for instance
`/schemagroups/mygroup/schemas/myschemas/versions`.

The result is a JSON encoded array of integers enumerating the `version` values of the
schemas within the group.

#### 3.4.2. Get a specific schema version

A specific version of a schema is retrieved via a GET on schema version's path in the
`versions` collection, for instance `/schemagroups/mygroup/schemas/myschema/versions/myversion`.

The returned payload is the schema document. Further attributes such as the
`description` and the `format` indicator are returned as HTTP headers.

The returned ´Content-Type´ is the same that was passed when the schema version
was registered.

The HEAD method SHOULD also be implemented.
