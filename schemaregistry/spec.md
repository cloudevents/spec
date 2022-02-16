# CNCF Schema Registry API Version 0.2-wip

## Abstract

This specification defines a simple API for storing, organizing, and accessing
schema documents for use with serialization and data validation frameworks such
as Apache Avro and JSON Schema.

It also defines a set of CloudEvent event type definitions and topology models
for synchronizing schemas across different schema registries.

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
might still be needed in some scenarios to allow for consumers or inspecting
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
secret protection is needed for an application or parts of it and the schema
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

#### `id` (schema group id)

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

#### `format` (schema group format)

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

#### `description` (schema group description)

- Type: `String`
- Description: Explains the purpose of the schema group.
- Constraints:
  - OPTIONAL
- Examples:
  - "This group holds schemas for the fabulous example app."

#### `createdtimeutc` (schema group created time)

- Type: `Timestamp`
- Description: Instant when the schema group was added to the registry.
- Constraints:
  - OPTIONAL
  - Assigned by the server.

#### `updatedtimeutc` (schema group updated time)

- Type: `Timestamp`
- Description: Instant when the schema group was last updated
- Constraints:
  - OPTIONAL
  - Assigned by the server.

## 2.2. Schema and Schema Version

Conceptually, a schema is a description of a data structure. Since data
structures evolve over time, the schema describing them will also evolve over
time. Therefore, a schema often has multiple versions.

In this specification, the ["schema version"](#225-schema-version-attributes)
refers to an individual schema document. The ["schema"](#224-schema-attributes)
is a management bracket for those documents that helps enforcing consistency
across versions, including compatibility policies.

A newer schema version might introduce breaking changes or it might only
introduce careful changes that preserve compatibility. These strategies are not
subject of this specification, but the API provides a conflict handling
mechanism that allows an implementation to reject updates that do not comply
with a compatibility policy, if one has been implemented.

For simple scenarios, the API allows for version management to be automatic and
transparent. Whenever a schema is updated, a new version number is assigned and
prior schema versions are retained. This specification does not mandate a
retention policy, but implementations MAY retire and remove outdated schema
versions.

The latest available schema MUST always the default version that is retrieved
when the URI to the schema is used without the version having been specified.

### 2.2.1 Schema authority

Every schema has an implicit or explicit "authority". Abstractly, the authority
is a person or group of people or system that controls the schema. For the most
common cases, the authority is whoever manages the schemas in a registry.

For the [replication model](#4-replication-model-and-state-change-events), the
authority information MUST be used to disambiguate schemas from different
origins that need to be consolidated in central schema registries or in caches.

In complex business systems, the authority might be centralized and schemas are
explicitly designed, reviewed and approved for use. In simpler scenarios, the
authority might simply lay with any producer of events, and schemas might be
inferred from code artifacts without developers being aware.

The [authority](#authority-schema-authority) attribute of the Schema object
reflects the controlling entity. The [authority](#authority-schema-authority)
attribute MAY be set to any URI and the URI does not have to correspond to a
resolvable network endpoint, even if a URI scheme like "http" is used in order
to borrow its generally well-understood structure. If the URI does not
correspond to an active network endpoint, ownership rights of corresponding DNS
domain name owners SHOULD nevertheless be respected.

For centralized governance scenarios, the `authority` SHOULD be set to a URI
reflecting the governing entity, like `https://schemas.corp.example.com`.

### 2.2.2. Schema version URI

For use with the [dataschema](../cloudevents/spec.md#dataschema) attribute in CloudEvents,
and with any other use case where we need to refer to a specific schema
document, unambiguous references to specific [schema
versions](#22-schema-and-schema-version) are needed. These references can be
resolved into schema documents with the help of a registry.

The schema version URI is composed from the
[authority](#authority-schema-authority) (as the base URI) and the [schema
version id](#id-schema-version-id).

In the default case, with the schema [authority](#authority-schema-authority)
and the [schema version id](#id-schema-version-id) not being explicitly set for
schema and schema version, this URI corresponds directly to the URI of the
["getSchemaVersion"](#342-get-a-specific-schema-version) API operation, which is
convenient for simple usage scenarios.

In [replication scenarios](#4-replication-model-and-state-change-events) where
those attributes are set, the URI might not correspond to a resolvable network
address, as permitted for the authority URI in the previous section.

In those scenarios, an event consumer SHOULD be configured with a fixed schema
registry endpoint for it to use, and obtain schemas identified, for example, in
the [dataschema](../cloudevents/spec.md#dataschema) attribute, using the
["getSchemaVersionByURI"](#342-get-a-specific-schema-version) API operation on
that endpoint, rather than trying to resolve the URI directly.

The following table shows some examples for a registry hosted at `https://example.com/registry`:

| [authority](#authority-schema-authority) | [id](#id-schema-version-id) | Schema URI
|------------------------------------------|-----------------------------|--------------------|
| (empty, therefore implied)               | `342`          | `https://example.com/registry/342`
| `https://example.com/registry`           | `342`          | `https://example.com/registry/342`
| `http://schemas.example.com/`            | `/mygroup/schemas/myschema/versions/2`  | `http://schemas.example.com/mygroup/schemas/myschema/versions/2`
| `http://schemas.example.org/`            | `http://schemas.example.org/41751` | `http://schemas.example.org/41751`
| `urn:example:schemas`                    | `a1b2c3d4`          | `urn:example:schemas:a1b2c3d4`

### 2.2.3. Multi-format schema groups

If the schema format has not been restricted at the schema group level, each
schema MAY have its own format. This choice is mutually exclusive. If a format
has been defined for the group, schemas in the group MUST use that format.

### 2.2.4. Schema attributes

As per the definition above, the schema object is a collection of versions
of schema documents. An implementation MAY add further attributes.

#### `id` (schema id)

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

#### `authority` (schema authority)

- Type: `URI`
- Description: Identifies the authority for this schema. See [Section 4.1](#41-producer-authority-or-central-authority).
- Constraints:
  - OPTIONAL. If the attribute is absent or empty, its implied default value is the base
    URI of the API endpoint.
  - MUST be a valid URI.
  - For schemas imported from other registries in replication scenarios, the
    attribute is REQUIRED to be not empty. If the value is empty or absent
    during import, it MUST be explicitly set to its implied default value.
- Examples:
  - `urn:com-example-schemas`
  - `https://schemas.example.com`

#### `format` (schema formats)

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

#### `description` (schema description)

- Type: `String`
- Description: Explains the purpose of the schema.
- Constraints:
  - OPTIONAL
- Examples:
  - "This schema describes the toppings for a Pizza."

#### `createdtimeutc` (schema created time)

- Type: `Timestamp`
- Description: Instant when the schema was added to the registry.
- Constraints:
  - OPTIONAL
  - Assigned by the server.

#### `updatedtimeutc` (schema updated time)

- Type: `Timestamp`
- Description: Instant when the schema was last updated
- Constraints:
  - OPTIONAL
  - Assigned by the server.

### 2.2.5 Schema version attributes

A schema version is a document. The "body" of a schema version MAY be a text
document or binary stream. An implementation SHOULD validate whether a
schema version is valid according to the rules of its format, for instance
whether it is a valid Avro schema document when the format is Apache Avro.

The schema version MAY also have an additional, OPTIONAL unique identifier
within the scope of the registry.

#### `version` (schema version)

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

#### `id` (schema version id)

- Type: `URI-reference`
- Description: Identifies the schema document uniquely, within the scope of this
  registry, without requiring other qualifiers.
- Constraints:
  - OPTIONAL. If the attribute is absent or empty, its implied default value is
    constructed as a relative URI based on the [path
    hierarchy](#31-path-hierarchy) for the
    ["getSchemaVersion"](#342-get-a-specific-schema-version) API operation.
  - MUST be a valid URI-reference.
  - MUST be unique within the scope of the registry.
  - For schema versions imported from other registries in [replication
    scenarios](#4-replication-model-and-state-change-events), this attribute is
    REQUIRED to be not empty. It MUST be set to the absolute [schema version
    URI](#222-schema-version-uri) of the imported schema version.
- Examples:
  - `123`
  - `https://example.org/456`
  - `/schemagroups/mygroup/schemas/2/version/3`

#### `description` (schema version description)

- Type: `String`
- Description: Explains details of the schema version.
- Constraints:
  - OPTIONAL
- Examples:
  - "This version adds support for different types of Pizza crust."  

#### `createdtimeutc`(schema version created time)

- Type: `Timestamp`
- Description: Instant when the schema version was added to the registry.
- Constraints:
  - OPTIONAL
  - Assigned by the server.

## 3. HTTP ("REST") API

This section informally describes the HTTP API binding of this schema registry.
The formal definition is the [OpenAPI document](schemaregistry.yaml) that is
part of this specification.

This section is therefore non-normative.

### 3.1. Path hierarchy

Schema groups contain schemas and those contain schema versions, which are the
documents needed for serialization or validation.

These dependencies are reflected in the path structure:

`/schemagroups/{group-id}/schemas/{schema-id}/versions/{version}`

- `{group-id}` corresponds to the schema group's [`id` attribute](#id-schema-group-id)
- `{schema-id}` corresponds to the schema's [`id` attribute](#id-schema-id)
- `{version}` corresponds to the schema version's [`version` attribute](#version-schema-version)

### 3.2. Operations at the `schemagroups` level

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

### 3.3 Operations at the `schemas` level

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

### 3.4 Operations at the `versions` level

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

#### 3.4.3. Get a specific schema version by schema version URI

Each schema version has a URI as a unique identifier, as defined in
[2.2.2](#222-schema-version-uri). This URI can be used as a lookup key on any
schema registry that holds a copy of that schema version.

As discussed in 2.2.2, the URI might not be network resolvable or the network
location might not be reachable from everywhere. That is a key motivation for
replication.

The operation to obtain a schema version is a GET on `/schema?uri={uri}`, with
the REQUIRED parameter being the schema version URI.

The returned payload is the schema document. Further attributes such as the
`description` and the `format` indicator are returned as HTTP headers.

The returned ´Content-Type´ is the same that was passed when the schema version
was registered.

The HEAD method SHOULD also be implemented.

## 4. Replication Model and State Change Events

Many eventing scenarios require that events cross from private networks into
public networks (and possibly back into a different private network) and it is
quite common that event producers and event consumers do not share the same
network scope.

In complex systems made up of subsystems owned by different organizations, the
subsystem owners might also want to decouple the systems such that they are not
dependent on the other system's availability wherever possible, and therefore
introduce redundant footprint for metadata stores such as a schema registry.

We therefore cannot assume that an event consumer has access to the same
endpoints accessible to the producer. The producer might use a schema registry
endpoint to publish schemas that is different from the endpoint from which the
consumer will need to fetch those schemas, and schemas will be synchronized
between these distinct registries, parallel to the event flow.

For the discussion in this section, we will use the term "source" for a registry
from which schemas originate and "target" for a registry into which those
schemas will be added.

The synchronization is accomplished by a combination of two mechanisms:

1. The Schema Registry API explained in [section 3](#3-http-rest-api) and
   formally defined in the [OpenAPI spec](schemaregistry.yaml) allows for
   schema information to be read from a source and written imperatively to a
   target: A target can pull changes or a source can push changes.
2. A set of change events, defined in this section, can be emitted by the source
   whenever any aspect of its state changes, and the target can update the
   replica of said state by subscribing to these events.

### 4.1 Producer authority or central authority

[Section 2.2.1](#221-schema-authority) discusses the concept of schema
authorities. For the replication model, authority matters because it influences
the shape of the replication topology.

In scenarios where registries are just a tool to share schemas between producers
and consumers, producers will generally be the controlling authorities and the
replication of schemas flows from registries near the producers to registries
near the consumers.

When schema governance is handled centrally, the replication of schemas might
flow from a central registry to registries near the producers to registries
near the consumers.

These two models mights also be mixed. Schemas representing event data that is
used throughout a greater system might stem from a centrally managed registry
and event data schemas that are local to a subsystem might be controlled by the
respective producers. 

### 4.2 Replication topologies

A peer-to-peer replication topology copies schemas between a source and target
registry directly. For a mutual synchronization of schemas between registries, a
second replication path is established with reversed roles.

A hub replication topology copies schemas from a source to the target through an
intermediary hub. The hub acts as an intermediary store, but with the authority
over the schemas still being with the producers. Hubs might also be used by
services that cannot host their own service registry endpoints.

A star replication topology uses hubs central hubs into which all sources
contribute schemas and to which all targets subscribe. If the hub is a centrally
governed registry, it might not accept inbound replications.

### 4.3 Push replication

In an imperative "push" replication model, a registry might push any updates of
its state to one of more configured target registry by forwarding all changes to
the respective schema registry API calls on that target registry.

The pushing registry might be configured to copy changes of the full registry, of
a specific schema group, or just of a specific schema.

This replication model uses the registry API as defined above on the target
registry and the configuration of what aspects of the registry are pushed are
implementation specific.

The names of the schema groups and of the schemas MAY mirror those from the
source registry, but they MAY also differ. Each schema version is always
accessible under both [its local path a given
registry](#342-get-a-specific-schema-version) and under its globally unique
[schema version URI](#343-get-a-specific-schema-version-by-schema-version-uri).

### 4.4 Pull replication

In an imperative "pull" replication model, a target registry will once or periodically
traverse the source registry contents and apply differences between the source
state and its own state.

The names of the schema groups and of the schemas MAY mirror those from the
source registry, but they MAY also differ.

The pulling registry might be configured to copy changes of the full registry, of
a specific schema group, or just of a specific schema.

This replication model uses the registry API as defined above on the source
registry and the configuration of what aspects of the registry are pulled are
implementation specific.

### 4.5. Event-driven replication

Event-driven replication uses CloudEvents to notify interested parties of
changes in the source registry such that those parties can
[pull](#44-pull-replication) changes immediately and as they become available.

Each registry SHOULD offer a [Subscription API](../subscriptions/spec.md)
endpoint, either directly or using some middleware, to allow interested parties
to subscribe to these change events.

The subscription's `source` MUST be the root of the schema registry. A [prefix
filter](../subscriptions/spec.md#prefix-filter-dialect) on the `subject`
attribute MAY be used to scope the subscription to a particular schema group or
schema.

The subscribing party registers a notification sink of its choosing.

```HTTP
POST https://source.example.com/subscriptions HTTP/1.1
Content-Type: application/cloudevents-subscription+json

{
  "source": "https://source.example.com",
  "protocol" : "HTTPS",
  "sink" : "https://target.example.com/notifications",
  "filter" : {
    "prefix" : {
       "subject" : "/schemagroups/5"
    }
  }
}
```

#### io.cloudevents.schemaregistry.updated.v1

This event notifies the subscriber of an element of the registry having been
created or updated. Because schema documents might be very large, and because
schema information might be subject to special authorization since it might
disclose trade secrets, the event carries no data, but requires the consumer to
fetch the indicated change from the registry.

* **source**: Base URI of the schema registry
* **type**: `io.cloudevents.schemaregistry.updated.v1`
* **subject**: [API path](#31-path-hierarchy) of the object that has been created or updated
* **time**: Time of the change, exactly as recorded in `updatedtimeutc` (or
  `createdtimeutc`for schema versions)

`id` MUST be set to a unique value relative to the scope formed by the `source`,
`type`, and `subject` attributes. The event `data` MUST be empty.

```JSON
{
    "specversion" : "1.0",
    "type" : "io.cloudevents.schemaregistry.updated.v1",
    "source" : "https://source.example.com",
    "subject" : "/schemagroups/5/schemas/1/version/3",
    "id" : "A234-1234-1234",
    "time" : "2020-10-30T17:31:00Z"
}
```

#### io.cloudevents.schemaregistry.deleted.v1

This event notifies the subscriber of an element of the registry having been
deleted.

* **source**: Base URI of the schema registry
* **type**: `io.cloudevents.schemaregistry.deleted.v1`
* **subject**: [API path](#31-path-hierarchy) of the object that has been deleted
* **time**: Time of the deletion

`id` MUST be set to a unique value relative to the scope formed by by the `source`, 
`type`, and `subject` attributes. The event `data` MUST be empty.

```JSON
{
    "specversion" : "1.0",
    "type" : "io.cloudevents.schemaregistry.deleted.v1",
    "source" : "https://source.example.com",
    "subject" : "/schemagroups/5/schemas/78",
    "id" : "A234-1234-1234",
    "time" : "2020-10-30T17:31:00Z"
}
```
