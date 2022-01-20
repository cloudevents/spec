# CNCF Message and Event Catalog API

## Abstract

This specification defines a simple API for storing, organizing, and accessing
catalogs of message definitions for use with event and messaging infrastructures
using common, standardized event and message information models like those of
CNCF CloudEvents, CNCF NATS, OASIS AMQP, OASIS MQTT and others.

## Status of this document

This document is a working draft.

## Terminology

A message is a data structure for transferring and dispatching
metadata-annotated information through some asynchronous communication framework
or infrastructure. An event is a kind of message.

A producer produces messages and publishes them. A subscriber subscribes to
published messages based on some criteria. A consumer is the delivery
destination for such subscriptions and handles the delivered information.

## 1. Introduction

Message and event catalogs are useful tools at design and development time
because they allow explorative discovery of the kinds of messages that are
available for subscription from a system and to find out, for instance, which
event sources raise them. A chosen message definition catalog entry can serve as
the basis for generating strongly typed representations of the message or other
handling code.

The message catalog defined here contains groups of abstract message
definitions. A group is typically associated with a kind of producer. The
message definitions belonging to the group describe messages that the
producer(s) might send. The catalog can store multiple versions of a message
definition.

The message definition entries in the catalog contain some fixed metadata
information. That fixed information MUST uniquely identify the type of message
and depends on the particular message information model. For example, for CNCF
CloudEvents message definitions, the "type" attribute is required as fixed
information for each entry.

- Message definition group: A named collection of message definitions. Each
  group holds a logically related set of message definitions, typically managed
  by a single entity, belonging to a particular application and/or having a
  shared access control management scope.

- Message definition: A document describing the metadata and structure of
  messages and events. 

- Message definition version: A specific version of such a definition. All documents
  that are stored and retrieved through the API are such versions. The
  identifying criteria of a definition MUST be identical across versions.

A message definition MAY refer to a CNCF Schema Registry endpoint for describing
structured message payloads and/or the structure of complex metadata fields
where required.

Structurally and functionally, this message catalog API is very similar to the
CNCF Schema Registry API, and it is reasonable and desirable for those APIs to
be collocated in the same service and on the same endpoint.

## 2. Message Catalog Elements

This section further describes the elements enumerated in the introduction.

All data types used in this section are defined in the CNCF CloudEvents
specification and MUST follow the respective formatting and syntax rules unless
specified otherwise.

### 2.1. Message definition group

Since message definitions are often used across several applications and in
conjunction with related message definitions like commands and command replies,
and those definitions might even be shared by multiple organizations, it is very
useful to put a grouping construct around sets of message definitions that are
related either by ownership or by a shared subject matter context.

Implementations of this specification MAY associate access control rules with
message definition groups. For instance, a user or a group of users might be
given write access only to a particular message definition group that their
organization owns. If trade secret protection is required for an application or
parts of it and the definition structure would give some of those away, read
access to a group of definitions might likewise be restricted.

This specification does not define management constructs for access control
rules.

### 2.1.1. Message definition group attributes

The data model for a message definition group consists of these attributes:

#### `id` (message definition group)

- Type: `String`
- Description: Identifies the message definition group.
- Constraints:
  - REQUIRED. IMMUTABLE.
  - MUST be a non-empty string
  - MUST conform with RFC3986/3.3 `segment-nz-nc` syntax. This allows for "dot
    notation", e.g. `org.example.myapp.module` for logical organization of
    message definition groups, even though the namespace is flat.
  - MUST be unique within the scope of the message catalog
- Examples:
  - mygroup
  - my-group
  - org.example.myapp.module
  - events\@example.com

#### `format` (message definition group)

- Type: `String`
- Description: Defines the message definition format managed by this message
  definition group. The format MAY be one of formats defined in this
  specification (CloudEvents, NATS, AMQP, MQTT) or a custom format. All
  definitions in this group MUST conform with the rules of the chosen format.
- Constraints:
  - REQUIRED. IMMUTABLE.
  - MUST NOT be modified if at least one definition exists in the group.
  - "CloudEvents", "NATS", "AMQP", "MQTT" for the definition formats defined in
    this specification, or another format defined elsewhere. If one of the names
    of definition formats defined in this specification is used, those
    definitions MUST be conformant with this specification.
- Examples:
  - "CloudsEvents"
  - "AMQP"
  - "MQTT"

#### `description` (message definition group)

- Type: `String`
- Description: Concisely explains the purpose of the message definition group.
- Constraints:
  - OPTIONAL
- Examples:
  - "This group holds Message definitions for the fabulous example app."

#### `documentation` (message definition group)

- Type: `String`
- Description: Documents the purpose of the message definition group in greater
  detail than the `description`. The text MAY have rich formatting in a format
  indicated by the `documentationformat` parameter.
- Constraints:
  - OPTIONAL

#### `documentationformat` (message definition group)

- Type: `String`
- Description: Indicates the format of the `documentation` content.  Well-known
  values are `HTML` and `Markdown` as well as `URL` if the documentation
  attribute contains a URL pointing to external content.
- Constraints:
  - OPTIONAL

#### `tags` (message definition group)

- Type: `String`
- Description: A single string containing a comma-separated list of tags
  describing the message definition group for search indexing.
- Constraints:
  - OPTIONAL
- Examples:
  - "exampleapp,examplecorp"

#### `createdtimeutc` (message definition group)

- Type: `Timestamp`
- Description: Instant when the message definition group was added to the
  catalog.
- Constraints:
  - OPTIONAL
- Assigned by the server.

#### `updatedtimeutc` (message definition group)

- Type: `Timestamp`
- Description: Instant when the message definition group was last updated
- Constraints:
  - OPTIONAL
- Assigned by the server.

## 2.2. Message definition and message definition version

A message definition is a description of a message data structure constrained by
a format rule. A message definition MAY have multiple versions.

In this specification, the "message definition" is an abstract collection object
that helps enforcing consistency across versions and the "message definition
version" is the concrete object handled by the API. A "message definition"
cannot exist without at least one "message definition version". All versions
share the common properties of the message definition and the immutable
properties of the definition, specifically `id` and `format`, cannot be
overridden by versions added later.

The API is created such that a message definition can only be created by
posting an initial version and that the message definition can only be changed
by posting a new version. Existing versions can be individually retrieved and
deleted, but not modified.

A newer message definition version might introduce breaking changes or it might
only introduce careful changes that preserve compatibility. These strategies are
not subject of this specification, but the API provides a conflict handling
mechanism that allows an implementation to reject updates that do not comply
with a compatibility policy, if one has been implemented.

For simple scenarios, the API allows for version management to be automatic and
transparent. Whenever a message definition is updated, a new version number is
assigned and prior definition versions are retained. This specification does not
mandate a retention policy, but implementations MAY retire and remove outdated
definition versions.

The latest available definition MUST always the default version that is
retrieved when the URI to the Message definition is used without the version
having been specified.

### 2.2.1 Authority

Every message definition has an implicit or explicit "authority". Abstractly,
the authority is a person or group of people or a system that controls the
message definition. For the most common cases, the authority is whoever manages
the message definition in the catalog.

For the replication model, the authority information MUST be used to
disambiguate message definitions from different origins that need to be
consolidated in central catalogs or in caches.

In complex business systems, the authority might be centralized and message
definitions are explicitly designed, reviewed and approved for use. In simpler
scenarios, the authority might simply lay with any producer of events, and
message definitions might be inferred from code artifacts without developers
being aware.

The [authority](#authority-definition-authority) attribute of the message
definition object reflects the controlling entity. The
[authority](#authority-definition-authority) attribute MAY be set to any URI.
The URI does not have to correspond to a resolvable network endpoint, even if a
URI scheme like "http" is used in order to borrow its generally well-understood
structure. If the URI does not correspond to an active network endpoint,
ownership rights of corresponding DNS domain name owners SHOULD nevertheless be
respected.

For centralized governance scenarios, the `authority` SHOULD be set to a URI
reflecting the governing entity, like `https://messagecatalog.corp.example.com`.

### 2.2.2. Message definition version URI

To refer to a specific message definition object, unambiguous references to
specific [definition versions](#22-schema-and-schema-version) are needed. These
references can be resolved into definition documents with the help of a catalog.

The message definition version URI is composed from the
[authority](#authority-definition-authority) (as the base URI) and the
[message definition version id](#id-definition-version-id).

In the default case, this URI corresponds directly to the URI of the
["getMessage definitionVersion"](#342-get-a-specific-schema-version) API
operation, which is convenient for simple usage scenarios.

In [replication scenarios](#4-replication-model-and-state-change-events), the
URI might not correspond to a resolvable network address, as permitted for the
authority URI in the previous section. A consumer SHOULD then be configured with
a fixed message catalog endpoint for it to use, and obtain definitions
identified by a URI using the
["getMessage definitionVersionByURI"](#342-get-a-specific-schema-version) API
operation on that endpoint, rather than trying to resolve the URI directly.

The following table shows some examples for a catalog hosted at
`https://example.com/messagecatalog`:

| [authority](#authority-definition-authority) | [id](#id-definition-version-id)                               | Message definition URI                                                                         |
| -------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| (empty, therefore implied)                   | `342`                                                         | <https://example.com/messagecatalog/342>                                                       |
| <https://example.com/messagecatalog>         | `342`                                                         | `https://example.com/messagecatelog/342`                                                       |
| `http://messagecatalog.example.com/`         | `/mygroup/messagedefinitions/myMessage definition/versions/2` | <http://messagecatalog.example.com/mygroup/messagedefinitions/myMessage definition/versions/2> |
| `http://messagecatalog.example.org/`         | `http://messagedefinitions.example.org/41751`                 | <http://messagecatalog.example.org/41751>                                                      |
| `urn:example:messagecatalog`                 | `a1b2c3d4`                                                    | `urn:example:messagecatalog:a1b2c3d4`                                                          |

### 2.2.4. Message definition attributes

The message definition object holds a collection of message definition versions.
An implementation MAY add further attributes.

#### `id` (message definition)

- Type: `String`
- Description: Identifies the message definition.
- Constraints:
  - REQUIRED. IMMUTABLE.
  - MUST be a non-empty string
  - MUST conform with RFC3986/3.3 `segment-nz-nc` syntax
  - MUST be unique within the scope of the message definition group
- Examples:
  - myMessage definition
  - my-Message definition

#### `authority` (message definition)

- Type: `URI`
- Description: Identifies the authority for this message definition. See
  [Section 4.1](#41-producer-authority-or-central-authority).
- Constraints:
  - OPTIONAL. IMMUTABLE. If the attribute is absent or empty, its implied default value is
    the base URI of the API endpoint.
  - MUST be a valid URI.
  - For Message definitions imported from other catalogs in replication
    scenarios, the attribute is REQUIRED to be not empty. If the value is empty
    or absent during import, it MUST be explicitly set to its implied default
    value.
- Examples:
  - `urn:com-example-message definitions`
  - `https://messagedefinitions.example.com`

#### `format` (message definition)

- Type: `String`
- Description: Reflects the message definition group format. If set by a client,
  the value MUST match the message definition group format.
- Constraints:
  - REQUIRED to be returned by the server. OPTIONAL for clients. IMMUTABLE.
  - MUST be a non-empty string, if present.
- For examples refer to the format attribute of the message definition group.

#### `description` (message definition)

- Type: `String`
- Description: Explains the purpose of the message definition.
- Constraints:
  - OPTIONAL
- Examples:
  - "Food order"

#### `tags` (message definition group)

- Type: `String`
- Description: A single string containing a comma-separated list of tags
  describing the message definition group for search indexing.
- Constraints:
  - OPTIONAL
- Examples:
  - "exampleapp,examplecorp"

#### `documentation` (message definition group)

- Type: `String`
- Description: Documents the purpose of the message definition group in greater
  detail than the `description`. The text MAY have rich formatting in a format
  indicated by the `documentationformat` parameter.
- Constraints:
  - OPTIONAL

#### `documentationformat` (message definition group)

- Type: `String`
- Description: Indicates the format of the `documentation` content.  Well-known
  values are `HTML` and `Markdown` as well as `URL` if the documentation
  attribute contains a URL pointing to external content.
- Constraints:
  - OPTIONAL

#### `createdtimeutc` (message definition)

- Type: `Timestamp`
- Description: Instant when the Message definition was added to the catalog.
- Constraints:
  - OPTIONAL
  - Assigned by the server.

#### `updatedtimeutc` (message definition)

- Type: `Timestamp`
- Description: Instant when the Message definition was last updated
- Constraints:
  - OPTIONAL
- Assigned by the server.

### 2.2.5 Message definition version

A message definition version is an object that defines the concrete shape of a
message in said version. The message definition version inherits all attributes
of the containing message definition object.

#### `version` (message definition version)

- Type: `Integer`
- Description: The version of the Message definition. This is a simple counter
  and tracks the version in the scope of this Message definition within the
  message definition group. The Message definition document content MAY indicate
  a different versioning scheme.
- Constraints:
  - REQUIRED
  - Assigned by server.
- Examples:
  - 1
  - 2

#### `createdtimeutc` (message definition version)

- Type: `Timestamp`
- Description: Instant when the Message definition version was added to the
  catalog.
- Constraints:
  - OPTIONAL
  - Assigned by the server.

## 3. Message definition formats

This section defines metaschemas for several well-known message and event
formats and/or protocols. These meta-schemas are meant to be used as the body
content of a message definition version.

A metaschema is a JSON document containing an object with an object-typed
property for each logical section of the event/message to be described. For
instance, for CNCF CloudEvents, there is only an "attributes" section. The AMQP
metaschema reflects the various sections of the AMQP data model.

The metaschemas use the RFC6570 URI template expression language to indicate
whether and what content is expected for metadata field/attribute/property
values. An empty string value permits any content. A 'null' value is equivalent
to the metadata field/attribute/property not being listed.

### 3.1. CNCF CloudEvents

#### 3.1.1. 'attributes' object

The `attributes` object MAY contain any number of uniquely named attribute fields,
whereby any name MUST conform with CloudEvents naming rules.

Whenever the name of an attribute field matches that of a well-known CloudEvents
attribute, its value or the constraints for the value expressed with the regular
expression MUST match the constraint rules of the CloudEvents attribute.

- A definition for the `type` field is REQUIRED and its value MUST follow all
  constraints of the `type` attribute of CloudEvents. The `id` of a message
  definition version using this metaschema MUST match the `type` field value.

- If the event carries a body, a definition for the `datacontenttype` field is
  RECOMMENDED and its value MUST, if present, follow all constraints of the
  `datacontenttype` attribute of CloudEvents.

- If the event carries a body, a definition for the `dataschema` field is
  RECOMMENDED and its value MUST, if present, follow all constraints of the
  `dataschema` attribute of CloudEvents.

#### 3.1.3. Examples

Message catalog object deleted event:

```
{
    "id" : "io.cloudevents.messagecatalog.deleted.v1",
    "description" : "Raised when an object has been deleted from the catalog",
    "format" : "CloudEvents",
    "version" : 1,
    "definition" : {
      "attributes" : {
        "specversion" : "1.0",
        "type" : "io.cloudevents.messagecatalog.deleted.v1",
      }
    }
}
```

Fictitious storage service "storage object created" event:

```
{
    "id" : "com.example.storage.object.created",
    "description" : "Raised when an object has been created",
    "format" : "CloudEvents",
    "version" : 1,
    "definition": {
      "attributes" : {
        "specversion" : "1.0",
        "type" : "com.example.storage.object.created",
        "subject" : "/{container}/{filepath}",
        "dataschema" : "http://schemas.example.com/schemagroups/storage/schema/objectcreated/version/1"
        "datacontenttype" : "application/json"
      }
    }
}
```

### 3.2. OASIS AMQP

The AMQP metaschema describes the content of an AMQP message.

#### 3.2.1. `header` object

The `header` object has a set of well-known fields defined by the AMQP 1.0
specification that are not extensible. For detailed descriptions refer to
section 3.2.1. in the AMQP 1.0 specification. The fields `first-acquirer` and
`delivery-count`of the AMQP header and not supported for definitions since they
depend on runtime state of the AMQP node.

- `durable` : Boolean
- `priority` : Integer
- `ttl` : Integer

#### 3.2.2. `deliveryannotations` object

The `deliveryannotations` object MAY contain any number of uniquely named
`delivery-annotation` fields, whereby any name MUST conform with AMQP `symbol`
type rules.

#### 3.2.3. `messageannotations` object

The `deliveryannotations` object MAY contain any number of uniquely named
`message-annotation` fields, whereby any name MUST conform with AMQP `symbol`
type rules.

#### 3.2.4. `properties` object

The `properties` object has a set of well-known fields defined by the AMQP 1.0
specification that are not extensible. For detailed descriptions refer to
section 3.2.4. in the AMQP 1.0 specification.

- `messageid` : String
- `userid` : Binary
- `to` : String
- `subject` : String
- `replyto` : String
- `correlationid` : String
- `contenttype` : String
- `contentencoding` : String
- `absoluteexpirytime` : TimeStamp
- `creationtime` : TimeStamp
- `groupid` : String
- `groupsequence` : String
- `replytogroupid` : String

#### 3.2.5. `applicationproperties` object

The `applicationproperties` object MAY contain any number of uniquely named
`application-properties` fields, whereby any name MUST conform with AMQP
`symbol` type rules.

#### 3.2.7. `applicationdata` object

The `applicationdata` object complements the `contentencoding` and `contenttype`
fields of the `properties` object with an optional reference to a schema
document and an indicator for how the data is encoded in the message.

- `dataschema` : optional URI reference to a schema object
- `amqpencoding` : "Data", "Value", "Sequence" (defaults to "Data")

#### 3.2.7. `footer` object

The `footer` object MAY contain any number of uniquely named `footer` fields,
whereby any name MUST conform with AMQP `symbol` type rules.

#### 3.2.8. Examples

(TBD)

### 3.3. OASIS MQTT

The MQTT metaschema describes the content of a MQTT 3.1.1. or MQTT 5.0 PUBLISH
packet. 

#### 3.3.1. `publish` object

The `publish` object has a set of well-known fields defined by the MQTT 3.1.1
and MQTT 5.0 specifications that are not extensible. For detailed descriptions
refer to section 3.3.2.3. in the MQTT 5.0 specification.

- `mqttversion` : String, either "3.1.1" or "5.0". Defaults to "5.0".
- `qos` : Integer. QoS level 0, 1, or 2.
- `retain` : Boolean
- `topicname` : String
- `payloadformat` : Integer (MQTT 5.0 only)
- `expiryinterval` : Integer (MQTT 5.0 only)
- `responsetopic` : String (MQTT 5.0 only)
- `correlationdata` : Binary (MQTT 5.0 only)
- `contenttype` : String (MQTT 5.0 only)

#### 3.3.2 `userproperty` object

The `userproperty` object MAY contain any number of uniquely named
`userproperty` fields, whereby any name MUST conform with MQTT naming rules.

#### 3.3.3 `payload` object

The `payload` object complements the `payloadformat` and `contenttype`
fields of the `publish` object with an optional reference to a schema
document and an indicator for how the data is encoded in the message.

- `dataschema` : optional URI reference to a schema object


### 3.4. CNCF NATS

The NATS metaschema describes the content of a NATS PUB message.

#### 3.3.1. `pub` object

The `pub` object has a set of well-known fields defined by the NATS client
specification that are not extensible. For detailed descriptions refer to
the NATS protocol documentation.

- `subject` : String
- `replyto` : String
#### 3.3.2 `payload` object

Optional reference to a schema document and an indicator for how the data is
encoded in the message.

- `dataschema` : optional URI reference to a schema object

## 4. HTTP ("REST") API

This section informally describes the HTTP API binding of this message catalog.
The formal definition is the [OpenAPI
document](messagecatalog.yaml)
that is part of this specification.

This section is therefore non-normative.

### 4.1. Path hierarchy

Message definition groups contain message definitions and those contain message
definition versions, which are the documents required for serialization or
validation.

These dependencies are reflected in the path structure:

`/messagecatalog/{group-id}/messagedefinitions/{Message definition-id}/versions/{version}`

- `{group-id}` corresponds to the message definition group's
  [id attribute](#id-message-definition-group-id)

- `{Message definition-id}` corresponds to the message definition's
  [id attribute](#id-definition-id)

- `{version}` corresponds to the message definition version's
  [version attribute](#version-definition-version)

### 4.2. Operations at the `messagecatalog` level

#### 4.2.1. List message definition groups

Message definition groups are enumerated with a GET on the root of the catalog
hierarchy, in the exemplary structure above identified as `/messagecatalog`.

The result is a JSON encoded array of strings enumerating the `id` values of the
message definition groups.

#### 4.2.2. Get message definition group

The details of a message definition group are retrieved with a GET on the
group's path in the message definition groups collection, for instance
`/messagecatalog/mygroup`.

The result is a JSON object that contains the attributes of the Message
definition group.

#### 4.2.3. Create message definition group

A message definition group is created with a PUT on the desired group's path in
the message definition groups collection, for instance
`/messagecatalog/mygroup`.

The payload is a JSON object that contains the attributes of the Message
definition group.

The operation returns the effective attributes as a JSON object when the Message
definition group has been created or updated.

#### 4.2.4. Delete message definition group

A message definition group is deleted with a DELETE on the desired group's path
in the message definition groups collection, for instance
`/messagecatalog/mygroup`.

### 4.3 Operations at the `messagedefinitions` level

#### 4.3.1. List message definitions for the group

Message definitions within a group are enumerated with a GET on the
`messagedefinitions` collection of the group, for instance
`/messagecatalog/mygroup/messagedefinitions`.

The result is a JSON encoded array of strings enumerating the `id` values of the
Message definitions within the group.

#### 4.3.2. Delete all message definitions from the group

All message definitions of a group can be deleted DELETE on the
`messagedefinitions` collection of the group, for instance
`/messagecatalog/mygroup/messagedefinitions`.

#### 4.3.3. Add a new message definition version

A new Message definition or a new version of a Message definition is added to
the version collection with a POST on the message definition collection
`/messagecatalog/mygroup/messagedefinitions/`.

This operation will either create a new message definition and store the
document under the version identifier assigned by the server or will
update the message definition by assigning a new version to the given document
and storing it.

The payload of the request is the message definition version object.

#### 4.3.4. Get the latest version of a Message definition

The latest version of a Message definition is retrieved via a GET on Message
definition's path in the Message definitions collection, for instance
`/messagecatalog/myGroup/messagedefinitions/myMessageDefinition`.

The returned payload is the Message definition version object.

The HEAD method SHOULD also be implemented.

#### 4.3.4. Delete a message definition

A Message definition including all its versions is deleted with a DELETE on
Message definition's path in the Message definitions collection, for instance
`/messagecatalog/mygroup/messagedefinitions/myMessageDefinition`

### 4.4 Operations at the `versions` level

#### 4.4.1. List all versions of the message definition

Versions of a message definition within a message definition group are
enumerated with a GET on the `versions` collection of the Message definition,
for instance
`/messagecatalog/mygroup/messagedefinitions/myMessageDefinition/versions`.

The result is a JSON encoded array of integers enumerating the `version` values
of the Message definitions within the group.

#### 4.4.2. Get a specific message definition version

A specific version of a message definition is retrieved via a GET on Message
definition version's path in the `versions` collection, for instance
`/messagecatalog/mygroup/messagedefinitions/myMessageDefinition/versions/myversion`.

The HEAD method SHOULD also be implemented.

#### 4.4.3. Get a specific message definition version by message definition version URI

Each Message definition version has a URI as a unique identifier, as defined in
[2.2.2](#222-schema-version-uri). This URI can be used as a lookup key on any
Message Catalog that holds a copy of that Message definition version.

As discussed in 2.2.2, the URI might not be network resolvable or the network
location may not be reachable from everywhere. That is a key motivation for
replication.

The operation to obtain a Message definition version is a GET on
`/messagedefinition?uri={uri}`, with the required parameter being the Message
definition version URI.

The returned payload is the Message definition document. 

The HEAD method SHOULD also be implemented.

## 4. Replication Model and State Change Events

Many eventing scenarios require that events cross from private networks into
public networks (and possibly back into a different private network) and it is
quite common that event producers and event consumers do not share the same
network scope.

In complex systems made up of subsystems owned by different organizations, the
subsystem owners might also want to decouple the systems such that they are not
dependent on the other system's availability wherever possible, and therefore
introduce redundant footprint for metadata stores such as a Message Catalog.

We therefore cannot assume that an event consumer has access to the same
endpoints accessible to the producer. The producer might use a Message Catalog
endpoint to publish Message definitions that is different from the endpoint from
which the consumer will need to fetch those Message definitions, and Message
definitions will be synchronized between these distinct catalogs, parallel to
the event flow.

For the discussion in this section, we will use the term "source" for a catalog
from which Message definitions originate and "target" for a catalog into which
those Message definitions shall be added.

The synchronization is accomplished by a combination of two mechanisms:

1. The Message Catalog API explained in [section 3](#3-http-rest-api) and
   formally defined in the
   [OpenAPI spec](../schemaregistry/schemaregistry.yaml)
   allows for Message definition information to be read from a source and
   written imperatively to a target: A target can pull changes or a source can
   push changes.

2. A set of change events, defined in this section, can be emitted by the source
   whenever any aspect of its state changes, and the target can update the
   replica of said state by subscribing to these events.

### 4.1 Producer authority or central authority

[Section 2.2.1](#221-schema-authority) discusses the concept of authorities. For
the replication model, authority matters because it influences the shape of the
replication topology.

In scenarios where catalogs are just a tool to share Message definitions between
producers and consumers, producers will generally be the controlling authorities
and the replication of Message definitions flows from catalogs near the
producers to catalogs near the consumers.

When Message definition governance is handled centrally, the replication of
Message definitions might flow from a central catalog to catalogs near the
producers to catalogs near the consumers.

These two models mights also be mixed. Message definitions representing event
data that is used throughout a greater system might stem from a centrally
managed catalog and event data Message definitions that are local to a subsystem
might be controlled by the respective producers.

### 4.2 Replication topologies

A peer-to-peer replication topology copies Message definitions between a source
and target catalog directly. For a mutual synchronization of Message definitions
between catalogs, a second replication path is established with reversed roles.

A hub replication topology copies Message definitions from a source to the
target through an intermediary hub. The hub acts as an intermediary store, but
with the authority over the Message definitions still being with the producers.
Hubs might also be used by services that cannot host their own service catalog
endpoints.

A star replication topology uses hubs central hubs into which all sources
contribute Message definitions and to which all targets subscribe. If the hub is
a centrally governed catalog, it might not accept inbound replications.

### 4.3 Push replication

In an imperative "push" replication model, a catalog might push any updates of
its state to one of more configured target catalog by forwarding all changes to
the respective Message Catalog API calls on that target catalog.

The pushing catalog might be configured to copy changes of the full catalog, of
a specific message definition group, or just of a specific Message definition.

This replication model uses the catalog API as defined above on the target
catalog and the configuration of what aspects of the catalog are pushed are
implementation specific.

The names of the message definition groups and of the Message definitions MAY
mirror those from the source catalog, but they MAY also differ. Each Message
definition version is always accessible under both
[its local path a given catalog](#442-get-a-specific-message-definition-version) and under
its globally unique
[Message definition version URI](#443-get-a-specific-message-definition-version-by-message-definition-version-uri).

### 4.4 Pull replication

In an imperative "pull" replication model, a target catalog will once or
periodically traverse the source catalog contents and apply differences between
the source state and its own state.

The names of the message definition groups and of the Message definitions MAY
mirror those from the source catalog, but they MAY also differ.

The pulling catalog might be configured to copy changes of the full catalog, of
a specific message definition group, or just of a specific Message definition.

This replication model uses the catalog API as defined above on the source
catalog and the configuration of what aspects of the catalog are pulled are
implementation specific.

### 4.5. Event-driven replication

Event-driven replication uses CloudEvents to notify interested parties of
changes in the source catalog such that those parties can
[pull](#44-pull-replication) changes immediately and as they become available.

Each catalog SHOULD offer a [Subscription API](../subscriptions/spec.md)
endpoint, either directly or using some middleware, to allow interested parties
to subscribe to these change events.

The subscription's `source` MUST be the root of the Message Catalog. A [prefix
filter](../subscriptions/spec.md#prefix-filter-dialect) on the `subject`
attribute MAY be used to scope the subscription to a particular message
definition group or Message definition.

The subscribing party registers a notification sink of its choosing.

```
POST https://source.example.com/subscriptions HTTP/1.1
Content-Type: application/cloudevents-subscription+json

{
  "source": "https://source.example.com",
  "protocol" : "HTTPS",
  "sink" : "https://target.example.com/notifications",
  "filter" : {
    "prefix" : {
       "subject" : "/messagecatalog/5"
    }
  }
}
```

#### io.cloudevents.messagecatalog.updated.v1

This event notifies the subscriber of an element of the catalog having been
created or updated. Because Message definition documents might be very large,
and because Message definition information might be subject to special
authorization since it might disclose trade secrets, the event carries no data,
but requires the consumer to fetch the indicated change from the catalog.

- **source**: Base URI of the Message Catalog

- **type**: `io.cloudevents.messagecatalog.updated.v1`

- **subject**: [API path](#31-path-hierarchy) of the object that has been
  created or updated

- **time**: Time of the change, exactly as recorded in `updatedtimeutc` (or
  `createdtimeutc`for Message definition versions)

`id` MUST be set to a unique value relative to the scope formed by the `source`,
`type`, and `subject` attributes. The event `data` MUST be empty.

```
{
    "specversion" : "1.0",
    "type" : "io.cloudevents.messagecatalog.updated.v1",
    "source" : "https://source.example.com",
    "subject" : "/messagecatalog/5/messagedefinitions/1/version/3",
    "id" : "A234-1234-1234",
    "time" : "2020-10-30T17:31:00Z"
}
```

#### io.cloudevents.messagecatalog.deleted.v1

This event notifies the subscriber of an element of the catalog having been
deleted.

- **source**: Base URI of the Message Catalog

- **type**: `io.cloudevents.messagecatalog.deleted.v1`

- **subject**: [API path](#31-path-hierarchy) of the object that has been
  deleted

- **time**: Time of the deletion

`id` MUST be set to a unique value relative to the scope formed by by the
`source`, `type`, and `subject` attributes. The event `data` MUST be empty.

```
{
    "specversion" : "1.0",
    "type" : "io.cloudevents.messagecatalog.deleted.v1",
    "source" : "https://source.example.com",
    "subject" : "/messagecatalog/5/messagedefinitions/78",
    "id" : "A234-1234-1234",
    "time" : "2020-10-30T17:31:00Z"
}
```
