# Registry Service - Version 0.5-wip

## Abstract

A Registry Service exposes resources, and their metadata, for the purposes
of enabling discovery of those resources for either end-user consumption or
automation and tooling.

## Table of Contents

- [Overview](#overview)
- [Notations and Terminology](#notations-and-terminology)
  - [Notational Conventions](#notational-conventions)
  - [Terminology](#terminology)
- [Registry Formats and APIs](#registry-formats-and-apis)
  - [Attributes and Extensions](#attributes-and-extensions)
  - [Registry APIs](#registry-apis)
    - [Registry Model](#registry-model)
    - [Registry Collections](#registry-collections)
    - [Retrieving the Registry](#retrieving-the-registry)
    - [Managing Groups](#managing-groups)
    - [Managing Resources](#managing-resources)
    - [Managing versions of a Resource](#managing-versions-of-a-resource)
- [CloudEvents Registry](#cloudevents-registry)
  - [Schema Registry](#schema-registry)
    - [Schema Groups](#group-schemagroups)
    - [Schemas](#resource-schemas)
  - [Message Definitions Registry](#message-definitions-registry)
    - [Message Definition Groups](#message-definition-groups)
    - [Message Definitions](#message-definitions)
  - [Endpoint Registry](#endpoint-registry)
    - [Endpoints](#endpoints-endpoints)

## Overview

A Registry Service is one that manages metadata about resources. At its core,
the management of an individual resource is simply a REST-based interface for
creating, modifying and deleting the resource. However, many resource models
share a common pattern of grouping resources by their "format" and can
optionally support versioning of the resources. This specification aims to
provide a common interaction pattern for these types of services with the goal
of providing an interoperable framework that will enable common tooling and
automation to be created.

The first section of this specification, ["Registry Formats and
APIs"](#registry-formats-and-apis), is meant to be a framework from which
additional specifications can be defined that expose model specific resources
and metadata.

The second section of this specification ["CloudEvents
Registry"](#cloudevents-registry) defines a set of concrete resource types and
metadata for the purpose of describing messaging and eventing endpoints, message
and event metadata definitions, and the payload schemas they use. The name
"CloudEvents Registry" reflects the specification coming from the CNCF
CloudEvents project, but the specification is intended to be generic enough to
be used with any messaging and eventing format and protocol and the registry
section does thus define metadata formats for the native message formats of
several other messaging and eventing protocols.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

For clarity, when a feature is marked as "OPTIONAL" this means that it is
OPTIONAL for both the sender and receiver of a message to support that
feature. In other words, a sender can choose to include that feature in a
message if it wants, and a receiver can choose to support that feature if it
wants. A receiver that does not support that feature is free to take any
action it wishes, including no action or generating an error, as long as
doing so does not violate other requirements defined by this specification.
However, the RECOMMENDED action is to ignore it. The sender SHOULD be prepared
for the situation where a receiver ignores that feature. An
Intermediary SHOULD forward OPTIONAL attributes.

In the pseudo JSON format snippets `?` means the preceding attribute is
OPTIONAL, `*` means the preceding attribute MAY appear zero or more times,
and `+` means the preceding attribute MUST appear at least once.

### Terminology

This specification defines the following terms:

#### Group

An entity that acts as a collection of related Resources.

#### Registry

An implementation of this specification. Typically, the implementation would
include model specific Groups, Resources and extension attributes.

#### Resource

A Resource is the main entity that is stored within a Registry Service. It
MAY be versioned and grouped as needed by the Registry's model.

## Registry Formats and APIs

This section defines common Registry metadata elements and APIs. It is an
explicit goal for this specification that metadata can be created and managed in
files in a file system, for instance in a Git repository, and also managed in a
Registry service that implements the API described here.

For instance, during development of a module, the metadata about the events
raised by the modules will best be managed in a file that resides alongside the
module's source code. When the module is ready to be deployed into a concrete
system, the metadata about the events will be registered in a Registry service
along with the endpoint where those events can be subscribed to or consumed
from, and which allows discovery of the endpoint and all related metadata by
other systems at runtime.

Therefore, the hierarchical structure of the Registry model is defined in such a
way that it can be represented in a single file, including but not limited to
JSON or YAML, or via the resource graph of a REST API.

### Attributes and Extensions

The following attributes are used by one or more entities defined by this
specification. They are defined here once rather than repeating them
throughout the specification.

Attributes:

- `"id": "STRING"`
- `"name": "STRING"`
- `"description": "STRING"`
- `"tags": { "STRING": "STRING" * }`
- `"versionId": STRING`
- `"epoch": UINT`
- `"self": "URL"`
- `"createdBy": "STRING"`
- `"createdOn": "TIME"`
- `"modifiedBy": "STRING"`
- `"modifiedOn": "TIME"`
- `"docs": "URI"`

Implementations of this specification MAY define additional (extension)
attributes, and they MAY appear at any level of the model. However they MUST
adhere to the following rules:

- it is STRONGLY RECOMMENDED that they be named in such a way as to avoid
  potential conflicts with future Registry Service attributes. For example,
  use of a model specific prefix.
- they MUST differ from sibling attributes irrespective of case. This avoids
  potential conflicts if the attributes are serialized in a case-insensitive
  situation, such as HTTP headers.

In situations where an attribute is serialized in a case-sensitive situation,
then the case specified by this specification, or the defining extension
specification, MUST be adhere to.

TODO: Add `format`
  - MUST be of the form document-type[/version]
  - children MUST NOT be looser than parent (can't do parent xx/3, child xx)
  - format group level is OPTIONAL, if present all resources/versions MUST
    match its previs
  - REQUIRED on resources and versions
    - format prefix MUST be consistent
    - but format version number can differe

#### `id`

- Type: String   # SHOULD this be a URI-Reference?
- Description: An immutable unique identifier of the entity.
- Constraints:
  - MUST be a non-empty string
  - MUST be immutable
  - MUST be case-insensitive unique within the scope of the entity's parent.
    In the case of the `id` for the Registry itself, the uniqueness scope will
    be based on where the Registry is used. For example, a publicly accessible
    Registry might want to consider using a UUID, while a private Registry
    does not need to be so widely unique.
- Examples:
  - A UUID

#### `name`

- Type: String
- Description: A human readable name of the entity.
  Note that implementations MAY choose to enforce constraints on this value.
  For example, they could mandate that `id` and `name` be the same value.
  How any such requirement is shared with all parties is out of scope of this
  specification.
- Constraints:
  - MUST be a non-empty string
- Examples:
  - `My Endpoints`

#### `description`

- Type: String
- Description: A human readable summary of the purpose of the entity.
- Constraints:
  - When this attribute has no value it MUST be serialized by either an empty
    string or by being excluded from the serialization of the owning entity
- Examples:
  - `A queue of the sensor generated messages`

#### `tags`

- Type: Map of name/value string pairs
- Description: A mechanism in which additional metadata about the entity can
  be stored without changing the schema of the entity.
- Constraints:
  - if present, MUST be a map of zero or more name/value string pairs
  - each name MUST be a non-empty string consisting of only alphanumeric
    characters, `-`, `_` or a `.`; be no longer than 63 characters;
    start with an alphanumeric character and be unique within the scope of
    this map. Values MAY be empty strings
- Examples:
  - `{ "owner": "John", "verified": "" }`

#### `versionId`

- Type: String
- Description: The ID of a specific version of an entity.
  Note that versions of an entity can be modified without changing the
  `versionId` value. Often this value is controlled by a user of the Registry.
  This specification makes no statement as to the format or versioning scheme
  used by implementations of this specification. However, it is assumed that
  newer versions of an entity will have a "higher" versionId value than older
  versions.  Also see `epoch`.
- Constraints:
  - MUST be a non-empty string.
  - MUST be unique across all versions of the entity
- Examples:
  - `1`, `2.0`, `v3-rc1`

#### `epoch`

- Type: Unsigned Integer
- Description: A numeric value used to determine whether an entity has been
  modified. Each time the associated entity is updated, this value MUST be
  set to a new value that is greater than the current one.
  Note that unlike `versionId`, this attribute is most often managed by
  the Registry itself. Additionally, if an entity is created that is based
  on another entity (e.g. a new version of an entity is created), then the
  new entity's `epoch` value can be reset (e.g. to zero) since the scope of
  its values is the entity.
- Constraints:
  - MUST be an unsigned integer equal to or greater than zero
  - MUST be unique within the scope of a version of an entity. If the entity
    is not versioned then the scope is just the entity itself
- Examples:
  - `1`, `2`, `3`

#### `self`

- Type: URL
- Description: A unique URL for the entity. The URL MUST be a combination of
  the base URL for the list of resources of this type of entity appended with
  the `id` of the entity.
- Constraints:
  - MUST be a non-empty URL
- Examples:
  - `https://example.com/registry/endpoints/123`

#### `createdBy`

- Type: String
- Description: A reference to the user or component that was responsible for
  the creation of this entity. This specification makes no requirement on
  the semantics or syntax of this value.
- Constraints:
  - When this attribute has no value it MUST be serialized by either an empty
    string or by being excluded from the serialization of the owning entity
- Examples:
  - `John Smith`
  - `john.smith@example.com`

#### `createdOn`

- Type: Timestamp
- Description: The date/time of when the entity was created.
- Constraints:
  - MUST be a [RFC3339](https://tools.ietf.org/html/rfc3339) timestamp
- Examples:
  - `2030-12-19T06:00:00Z"

#### `modifiedBy`

- Type: String
- Description: A reference to the user or component that was responsible for
  the the latest update of this entity. This specification makes no requirement
  on the semantics or syntax of this value.
- Constraints:
  - When this attribute has no value it MUST be serialized by either an empty
    string or by being excluded from the serialization of the owning entity
- Examples:
  - `John Smith`
  - `john.smith@example.com`

#### `modifiedOn`

- Type: Timestamp
- Description: The date/time of when the entity was last updated.
- Constraints:
  - MUST be a [RFC3339](https://tools.ietf.org/html/rfc3339) timestamp
- Examples:
  - `2030-12-19T06:00:00Z"

#### `docs`

- Type: URI-Reference
- Description: A URI-Reference to additional documentation about this entity.
  This specification does not place any constraints on the data returned from
  an HTTP GET to this value.
- Constraints:
  - if present, MUST be a non-empty URI-Reference
  - if present with a scheme, it MUST use either `http` or `https`
  - MUST support an HTTP GET to this URI-Reference
- Examples:
  - `https://example.com/docs/myQueue`

### Registry APIs

This specification defines the following API patterns:

``` meta
/model                              # Manage the registry model
/                                   # Show all Groups
/GROUPs                             # Manage a Group Type
/GROUPs/gID                         # Manage a Group
/GROUPs/gID/RESOURCEs               # Manage a Resource Type
/GROUPs/gID/RESOURCEs/rID           # Manage the latest Resource version
/GROUPs/gID/RESOURCEs/rID?meta      # Metadata about the latest Resource version
/GROUPs/gID/RESOURCEs/rID/versions  # Show version strings for a Resource
/GROUPs/gID/RESOURCEs/rID/versions/vID         # Manage a Resource version
/GROUPs/gID/RESOURCEs/rID/versions/vID?meta    # Metadata about a version
```

Where:
- `GROUPs` is a grouping name (plural). E.g. `endpoints`
- `gID` is the unique identifier of a single Group
- `RESOURCEs` is the type of resources (plural). E.g. `definitions`
- `rID` is the unique identifier of a single Resource
- `vID` is the unique identifier of a version of a Resource

While these APIs are shown to be at the root path of a Registry Service,
implementation MAY choose to prefix them as necessary. However, the same
prefix MUST be used consistently for all APIs in the same Registry Service.

The following sections define the APIs in more detail.

#### Registry Model

The Registry model defines the Groups and Resources supported by the Registry
Service. This information will usually be used by tooling that does not have
advanced knowledge of the data stored within the Registry.

The Registry model can be retrieved two ways:

1. as a stand-alone resource. This is useful when management of the Registry's
   model is needed independently from the resources within the Registry.
2. as part of the Registry resources. This is useful when it is desirable to
   view the entire Registry as a single document - such as an "export" type
   of scenario. See the [Retrieving the Registry](#retrieving-the-registry)
   section (the `?model` flag) for more information on this option.

Regardless of how the model is retrieved, the overall format is as follows:

``` meta
{
  "schema": "URI-Reference", ?         # Schema doc for the entire Registry
  "groups": [
    { "singular": "STRING",            # eg. "endpoint"
      "plural": "STRING",              # eg. "endpoints"
      "schema": "URI-Reference", ?     # Schema doc for the group

      "resources": [
        { "singular": "STRING",        # eg. "definition"
          "plural": "STRING",          # eg. "definitions"
          "versions": UINT ?           # Num versions(>=1). Def=1, 0=unlimited
        } +
      ] ?
    } +
  ] ?
}
```

The following describes the attributes of Registry model:

- `groups`
  - REQUIRED if there are any Groups defined for the Registry
  - The set of Groups supported by the Registry
- `groups.singular`
  - REQUIRED
  - The singular name of a Group. E.g. `endpoint`
  - MUST be unique across all Groups in the Registry
- `groups.plural`
  - REQUIRED
  - The plural name of a Group. E.g. `endpoints`
  - MUST be unique across all Groups in the Registry
- `groups.schema`
  - OPTIONAL
  - A URI-Reference to a schema document for the Group
- `groups.resources`
  - REQUIRED if there are any Resources defined for the Group
  - The set of Resource entities defined for the Group
- `groups.resources.singular`
  - REQUIRED
  - The singular name of the Resource. E.g. `definition`
- `groups.resources.plural`
  - REQUIRED
  - The plural name of the Resource. E.g. `definitions`
- `groups.resources.versions`
  - OPTIONAL
  - Number of versions per Resource that will be stored in the Registry
  - The default value is zero (`0`), meaning no old versions will be stored
  - A value of negative one (`-1`) indicates there is no stated limit, and
    implementation MAY prune old versions at any time. Implementation MUST
    NOT delete a version without also deleting all older versions.


Below describes how to retrieve the model as an independent resource.

The request MUST be of the form:

``` meta
GET /model
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "schema": "URI-Reference", ?         # Schema doc for the entire Registry
  "groups": [
    { "singular": "STRING",            # eg. "endpoint"
      "plural": "STRING",              # eg. "endpoints"
      "schema": "URI-Reference", ?     # Schema doc for the group

      "resources": [
        { "singular": "STRING",        # eg. "definition"
          "plural": "STRING",          # eg. "definitions"
          "versions": UINT ?           # Num versions. Def=1, 0=unlimited
        } +
      ] ?
    } +
  ] ?
}
```

**Example:**

Request:

``` meta
GET /model
```

Response:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "model": {
    "groups": [
      { "singular": "endpoint",
        "plural": "endpoints",

        "resources": [
          { "singular": "definitionGroup",
            "plural": "definitionGroups",
            "versions": 1
          }
        ]
      }
    ]
  }
}
```

#### Registry Collections

The Registry collections (groupings of same-typed resources) that are defined
by the Registry Model discussed in the previous section follow a consistent
pattern with respect to how they are represented in the serialization of the
Registry.

Each collection MUST be serialized as 2 REQUIRED properties and 1 OPTIONAL
one - as shown in the following example for a GROUP:
```
  "GROUPsUrl": "URL,
  "GROUPsCount": UINT,
  "GROUPs": { ... map of entities in the group, key is the "id" of each ... } ?
```

Each property MUST start with the plural name of the entity type. For example,
`endpointsUrl`, not `endpointUrl`. The `xxxsUrl` property MUST always be
present and MUST contain an absolute URL that can be used to retrieve the
latest set of entities in the collection via an HTTP `GET`. The `xxxsCount`
property MUST always be present and MUST containe the number of entities in
the collection after any filtering might have been applied. The `xxxs`
property is OPTIONAL and MUST only be included if the Registry request included
the `inline` flag and it included this collection's plural name. This property
MUST be a map with the key equal to the `id` of each entity in the collection.
When filtering is applied then this property MUST only include entities that
satisfy the filter criteria.

The set of entitie returned in the `xxxs` property is a point-in-time view
of the Registry. There is no guarantee that a `GET` to the `xxxsUrl` will
return the exact same collection since the contents of the Registry might
have changed.

When the number of entities in the collection is zero, the `xxxs` property
MAY be excluded from the serialization, even if `inline` is specified.

For clarity, these rules MUST apply to the `GROUPs`, `RESOURCEs` and
`versions` collections.

#### Retrieving the Registry

This returns the Groups in the Registry along with metadata about the
Registry itself.

The request MUST be of the form:

``` meta
GET /[?model]
```

The presence of the `model` query parameter indicates that the response
MUST include the Registry model as an additional top-level property.

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING", ?
  "description": "STRING", ?  # Description of Registry
  "specVersion": "STRING",    # Registry spec version
  "self": "URL",
  "tags": { "STRING": "STRING" * }, ?
  "docs": "URL", ?

  "model": { ... } ?          # if ?model is present

  # Repeat for each Group
  "GROUPsUrl": "URL",         # eg. "endpointsUrl" - repeated for each GROUP
  "GROUPsCount": INT          # eg. "endpointsCount"
}
```

**Example:**

Request:

``` meta
GET /
```

Response:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "123",
  "specVersion": "0.1",
  "self": "http://example.com/",

  "endpointsURL": "https://example.com/endpoints",
  "endpointsCount": 42,

  "definitionGroupsURL": "https://example.com/groups",
  "definitionGroupsCount": 3
}
```

Another example asking for the model to be included:

Request:

``` meta
GET /?model
```

Response:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "123",
  "specVersion": "0.1",
  "self": "http://example.com/",

  "model": {
    "groups": [
      { "singular": "endpoint",
        "plural": "endpoints",

        "resources": [
          { "singular": "definitionGroup",
            "plural": "definitionGroups",
            "versions": 1
          }
        ]
      }
    ]
  },

  "endpointsUrl": "https://example.com/endpoints",
  "endpointsCount": 42,

  "definitionGroupsUrl": "https://example.com/groups",
  "definitionGroupsCount": 3
}
```

##### Retrieving all Registry Contents

This returns the Groups and all nested data in the Registry along with
metadata about the Registry itself. This is designed for cases where the
entire Registry's contents are to be represented as a single document.

The request MUST be of the form:

``` meta
GET /[?inline[=PATH,...]][&model]
```

Where `PATH` is a string indicating which collections of GROUPs, RESOURCEs
and `versions` to include in the response. The PATH MUST be of the form
`GROUPs[.RESOURCEs[.versions]]` where `GROUPs` is replaced with the plural
name of a Group, and `RESOURCEs` is replaced with the plural name of a nested
Resource. There MAY be mulitple PATHs specified, either as comma separated
values or via mulitple `inline` query parameters. Absence of a value, or a
value of an empty string, indicates that all nested collections MUST be inlined.

Presence of the `model` query parameter indicates that the response MUST
include the Registry model definition as a top-level property.

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "name": "STRING", ?
  "description": "STRING", ?  # Description of Registry
  "specVersion": "STRING",    # Registry spec version
  "tags": { "STRING": "STRING" * }, ?
  "docs": "URL", ?

  "model": { ... } ?          # Only if ?model is present

  # Repeat for each Group
  "GROUPsUrl": "URL",         # eg. "endpointsUrl"
  "GROUPsCount": INT,         # eg. "endpointsCount"
  "GROUPs": {                 # eg. "endpoints" - only if ?inline is present
    "ID": {                   # The Group ID
      "id": "STRING",
      "name": "STRING",
      "epoch": UINT,          # What other common fields?
                              # type? createdBy/On? modifiedBy/On? docs? tags?
                              # description? self?

      # Repeat for each RESOURCE in the Group
      "RESOURCEsUrl": "URL",  # URL to retrieve all nested Resources
      "RESOURCEsCount": INT,  # Total number of resources
      "RESOURCEs": {          # eg. "definitions" - only if ?inline is present
        "ID": {               # MUST match the "id" on the next line
          "id": "STRING",
          ... remaining RESOURCE ?meta and RESOURCE itself ...

          "versionsUrl": "URL",
          "versionsCount": INT,
          "versions": {       # Only when ?inline is present
            "ID": {
              "id": "STRING",
              ... remaining VERSION ?meta and VERSION itself ...
            }
          } ?
        } *
      } ?                     # OPTIONAL if RESOURCEsCount is zero
    } *
  } ?                         # OPTIONAL if GROUPsCount is zero
}
```

Note: If the Registry can not return all expected data in one response then it
MUST generate an error. In those cases, the client will need to query the
individual Groups via the `/GROUPsUrl` API so the Registry can leverage
pagination of the response.

TODO: define the error / add filtering / pagination

**Example:**

Request:

``` meta
GET /?inline
```

Response:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ TODO }
```

#### Managing Groups

##### Retrieving all Groups

This returns all entities that are in a Group.

The request MUST be of the form:

``` meta
GET /GROUPs[?inline[=PATH,...]]
```

Where `PATH` is a string indicating which collections of RESOURCEs and
`versions` to include in the response. The PATH MUST be of the form
`RESOURCEs[.versions]` where `RESOURCEs` is replaced with the plural name of
a Resource. There MAY be mulitple PATHs specified, either as comma separated
values or via mulitple `inline` query parameters. Absence of a value
indicates that all nested collections MUST be inlined.

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Link: <URL>;rel=next;count=INT  # If pagination is needed

{
  "ID": {                   # The Group ID
    "id": "STRING",         # Group attributes
    "name": "STRING",
    "epoch": UINT,          # Server controlled

    # Repeat for each RESOURCE in the Group
    "RESOURCEsUrl": "URL",  # URL to retrieve all nested Resources
    "RESOURCEsCount": INT,  # Total number resources
    "RESOURCEs": {          # Only when ?inline is present
      "ID": {               # MUST match the "id" on the next line
        "id": "STRING",
        ... remaining RESOURCE ?meta and RESOURCE itself ...

        "versionsUrl": "URL",
        "versionsCount": INT,
        "versions": {       # Only when ?inline is present
          "ID": {
            "id": "STRING",
            ... remaining VERSION ?meta and VERSION itself ...
          } ?
        } ?
      } *
    } ?                     # OPTIONAL if RESOURCEsCount is zero
  } *
}
```

Note: If the `inline` query parameter is present and the presence of the
`RESOURCEs` map results in even a single Group being too large to return in
one response then an error MUST be generated. In those cases the client will
need to query the individual Resources via the `RESOURCEsUrl` so the Registry
can leverage pagination of the response data.

**Example:**

Request:

``` meta
GET /endpoints
```

Response:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Link: <http://example.com/endpoints&page=2>;rel=next;count=100

{
  "123": {
    "id": "123",
    "name": "A cool endpoint",
    "epoch": 1,

    "definitionsUrl": "https://example.com/endpoints/123/definitions",
    "definitionsCount": 5
  },
  "124": {
    "id": "124",
    "name": "Redis Queue",
    "epoch": 3,

    "definitionsUrl": "https://example.com/endpoints/124/definitions",
    "definitionsCount": 1
  }
}
```

TODO: add filtering and define error

##### Creating a Group

This will add a new Group to the Registry.

The request MUST be of the form:

``` meta
POST /GROUPs

{
  "id": "STRING", ?       # If absent then it's server defined
  "name": "STRING",
}
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Location: URL             # .../GROUPs/ID

{                         # MUST be full representation of new Group
  "id": "STRING",
  "name": "STRING",
  "epoch": UINT,

  # Repeat for each RESOURCE type in the Group
  "RESOURCEsUrl": "URL",  # URL to retrieve all nested Resources
  "RESOURCEsCount": INT   # Total number resources
}
```

**Example:**

Request:

``` meta
POST /endpoints

{ TODO }
```

Response:

``` meta
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Location: https://example.com/endpoints/ID

{ TODO }
```

##### Retrieving a Group

This will return a single Group.

The request MUST be of the form:

``` meta
GET /GROUPs/ID[?inline[=PATH,...]]
```

Where `PATH` is a string indicating which collections of RESOURCEs and
`versions` to include in the response. The PATH MUST be of the form
`RESOURCEs[.versions]` where `RESOURCEs` is replaced with the plural name of
a Resource. There MAY be mulitple PATHs specified, either as comma separated
values or via mulitple `inline` query parameters. Absence of a value, or a
value of an empty string, indicates that all nested collections MUST be inlined.

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",         # Group attributes
  "name": "STRING",
  "epoch": UINT,           # Server controlled

  # Repeat for each RESOURCE type in the Group
  "RESOURCEsUrl": "URL",  # URL to retrieve all nested Resources
  "RESOURCEsCount": INT,  # Total number resources
  "RESOURCEs": {          # Only when ?inline is present
    "ID": {
      "id": "STRING",
      ... remaining RESOURCE ?meta and RESOURCE itself ...

      "versionsUrl": "URL",
      "versionsCount": INT,
      "versions": {       # Only when ?inline is present
        "ID": {
          "id": "STRING",
          ... remaining VERSION ?meta and VERSION itself ...
        } ?
      } ?
    } *
  } ?                     # OPTIONAL if RESOURCEsCount is zero
}
```

**Example:**

Request:

``` meta
GET /endpoints/123
```

Response:

``` meta
HTTP/1.1 ...
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "123",
  "name": "A cool endpoint",
  "epoch": 1,

  "definitionsUrl": "https://example.com/endpoints/123/definitions",
  "definitionsCount": 5
}
```

##### Updating a Group

This will update the attributes of a Group.

The request MUST be of the form:

``` meta
PUT /GROUPs/ID[?epoch=EPOCH]

{
  # Missing attributes are deleted from Group
  "id": "STRING",            # MUST match URL if present
  "name": "STRING",
  "epoch": UINT ?            # OPTIONAL - MUST be current value if present

  # Presence of the RESOURCEs attributes are OPTIONAL and MUST be ignored
}
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "epoch": UINT,          # MUST be greater than previous value

  # Repeat for each RESOURCE type in the Group
  "RESOURCEsUrl": "URL",
  "RESOURCEsCount": INT
}
```

**Example:**

Request:

``` meta
PUT /endpoints/123

{
  "id": "123",
  "name": "A cooler endpoint",
  "epoch": 1
}
```

Response:

``` meta
HTTP/1.1 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "123",
  "name": "A cooler endpoint",
  "epoch": 2,

  "definitionsUrl": "https://example.com/endpoints/123/definitions",
  "definitionsCount": 5,
}
```

##### Deleting Groups

To delete a single Group the following API can be used.

The request MUST be of the form:

``` meta
DELETE /GROUPs/ID[?epoch=EPOCH]
```

If `epoch` is present then it MUST match the current value.

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{                       # RECOMMENDED, last known state of entity
  "id": "STRING",
  "name": "STRING",
  "epoch": UINT,
  ...
} ?
```

To delete multiple Groups the following API can be used.

The request MUST be of the form:

``` meta
DELETE /GROUPs

[
  {
    "id": "STRING",
    "epoch": UINT ?     # If present it MUST match current value
  } *
]
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ "ID": { ... } * } ?   # RECOMMENDED
```

If any of the individual deletes fails then the entire request MUST fail
and none of the Groups are deleted.

A `DELETE /GROUPs` without a body MUST delete all Groups.

#### Managing Resources

##### Retrieving all Resources

This will retrieve the Resources from a Group.

The request MUST be of the form:

``` meta
GET /GROUPs/ID/RESOURCEs[?inline[=versions]]
```

Where `inline` indicates whether to include the `versions` collection
in the response. In this case the "versions" value is OPTIONAL since it is the
only collection within the RESOURCE that might be shown. Absence of a value, or
a value of an empty string, indicates that the `versions` collection MUST
be inlined.

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Link: <URL>;rel=next;count=INT  # If pagination is needed

{
  "ID": {
    "id": "STRING",
    "name": "STRING",
    "versionId": "STRING",
    "epoch": UINT,
    "self": "URL",                   # URL to specific version

    "RESOURCEUri": "URI", ?          # If not locally stored (singular)
    "RESOURCE": {} ?,                # If ?inline present & JSON (singular)
    "RESOURCEBase64": "STRING" ?     # If ?inline present & ~JSON (singular)

    "versionsUrl": "URL",
    "versionsCount": INT,
    "versions": {                    # Only when ?inline is present
      "ID": {
        "id": "STRING",
        ... remaining VERSION ?meta and VERSION itself ...
      } ?
    } ?
  } *
}
```

Note: If the `inline` query parameter is present and the presence of the
`versions` map results in even a single Resource being too large to return in
one response then an error MUST be generated. In those cases the client will
need to query the individual Versions via the `versionUrl` so the Registry
can leverage pagination of the response data.

**Example:**

Request:

``` meta
GET /endpoints/123/definitions
```

Response:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Link: <http://example.com/endpoints/123/definitions&page=2>;rel=next;count=100

{
  "456": {
    "id": "456",
    "name": "Blob Created",
    "format": "CloudEvents/1.0",
    "versionId": "3.0",
    "epoch": 1,
    "self": "https://example.com/endpoints/123/definitions/456/version/3"
  }
}
```

##### Creating Resources

This will create a new Resources in a particular Group.

The request MUST be of the form:

``` meta
POST /GROUPs/ID/RESOURCEs
Registry-name: STRING ?          # If absent, default to the ID?
Registry-type: STRING ?
Registry-RESOURCEURI: URI ?      # If present body MUST be empty (singular)

{ ...Resource entity... } ?
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING            # URL to the specific version
Registry-RESOURCEURI: URI ?      # If present body MUST be empty (singular)
Location: URL                    # Points to "latest" URL
Content-Location: URL            # Same as Registry-self value

{ ...Resource entity... } ?
```

**Example:**

Request:

``` meta
TODO
```

##### Retrieving a Resource

This will retrieve the latest version of a Resource. This can be considered an
alias for `/GROUPs/gID/RESOURCEs/rID/versions/vID` where `vID` is the latest
versionId value.

The request MUST be of the form:

``` meta
GET /GROUPs/ID/RESOURCEs/ID[?inline[=versions]]
```

Where `inline` indicates whether to include the `versions` collection
in the response. In this case the "versions" value is OPTIONAL since it is the
only collection within the RESOURCE that might be shown. Absence of a value, or
a value of an empty string, indicates that the `versions` collection MUST
be inlined.

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK  or 307 Temporary Redirect    # 307 if RESOURCEURI is present
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING            # URL to the specific version
Registry-RESOURCEURI: URI ?      # If present body MUST be empty (singular)
Content-Location: URL            # Same as Registry-self value
Location: URL                    # If 307. Same a Registry-RESOURCEURI

{ ...Resource entity... } ?
```

**Example:**

Request:

``` meta
TODO
```

##### Retrieving a Resource's Metadata

This will retrieve the metadata for the latest version of a Resource. This can
be considered an alias for
`/GROUPs/ID/RESOURCEs/RESOURCEID/versions/VERSIONID?meta` where `VERSIONID` is
the latest versionId value.

The request MUST be of the form:

``` meta
GET /GROUPs/ID/RESOURCEs/ID?meta
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "versionId": "STRING",
  "epoch": UINT,
  "self": "URL",
  "RESOURCEUri": "URI" ?     # singular
}
```

**Example:**

Request:

``` meta
TODO
```

##### Updating a Resource

This will update the latest version of a Resource. Missing Registry HTTP
headers MUST NOT be interpreted as deleting the attribute. However, a Registry
HTTP headers with an empty string for its value MUST be interpreted as a
request to delete the attribute.

The request MUST be of the form:

``` meta
PUT /GROUPs/ID/RESOURCEs/ID[?epoch=EPOCH]
Registry-id: STRING ?            # If present it MUST match URL
Registry-name: STRING ?
Registry-type: STRING ?
Registry-version: STRING ?       # If present it MUST match current value
Registry-epoch: UINT ?           # If present it MUST match current value & URL
Registry-self: STRING ?          # If present it MUST be ignored?
Registry-RESOURCEURI: URI ?      # If present body MUST be empty (singular)

{ ...Resource entity... } ?      # If empty then content is erased
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT             # MUST be incremented
Registry-self: STRING
Registry-RESOURCEURI: URI ?      # singular
Content-Location: URL

{ ...Resource entity... } ?
```

Note: if some of the Registry attributes are shared with the Resource itself
then those values MUST appear in both the Registry HTTP headers as well as in
the Resource itself when retrieving the Resource. However, in this "update"
case, if the attribute only appears in the HTTP body and the corresponding
Registry HTTP header is missing then the Registry attribute MUST be updated to
match the Resource's attribute. If both are present on the request and do not
have the same value then an error MUST be generated.

**Example:**

Request:

``` meta
TODO
```

Response:

``` meta
TODO
```

TODO: make a note that empty string and attribute missing are the same thing.
Which error is to be returned?

##### Updating a Resource's metadata

This will update the metadata of the latest version of a Resource without
creating a new version.

The request MUST be of the form:

``` meta
PUT /GROUPs/ID/RESOURCEs/ID?meta[&epoch=EPOCH]

{
  "id": "STRING",
  "name": "STRING",
  "versionId": "STRING", ?     # If present it MUST match current value
  "epoch": UINT, ?             # If present it MUST match current value & URL
  "self": "URL", ?             # If present it MUST be ignored
  "RESOURCEUri": "URI" ?       # singular
}
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "versionId": "STRING",
  "epoch": UINT,               # MUST be incremented
  "self": "URL",
  "RESOURCEUri": "URI" ?       # singular
}
```

**Example:**

Request:

``` meta
TODO
```

Response:

``` meta
TODO
```

##### Deleting Resources

To delete a single Resource the following API can be used.

The request MUST be of the form:

``` meta
DELETE /GROUPs/ID/RESOURCEs/ID[?epoch=EPOCH]
```

If `epoch` is present then it MUST match the current value.

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING
Registry-RESOURCEURI: URI ?        # singular
Content-Location: URL              # Does this make sense if it's been deleted?

{ ...Resource entity... } ?
```

**Example:**

Request:

``` meta
TODO
```

To delete multiple Resources the following API can be used.

The request MUST be of the form:

``` meta
DELETE /GROUPs/ID/RESOURCEs

[
  {
    "id": "STRING",
    "epoch": UINT ?     # If present it MUST match current value
  } *
]
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ "ID": { ... } * } ?   # RECOMMENDED
```

If any of the individual deletes fails then the entire request MUST fail
and none of the Resources are deleted.

A `DELETE /GROUPs/ID/RESOURCEs` without a body MUST delete all Resources in the
Group.

#### Managing versions of a Resource

##### Retrieving all versions of a Resource

This will retrieve all versions of a Resource.

The request MUST be of the form:

``` meta
GET /GROUPs/ID/RESOURCEs/ID/versions
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Link: <URL>;rel=next;count=INT  # If pagination is needed

{
  "ID": {                            # Versions ID/string
    "id": "STRING",
    "name": "STRING",
    "versionId": "STRING",
    "epoch": UINT,
    "self": "URL",
    "RESOURCEUri": "URI", ?          # If not locally stored (singular)
    "RESOURCE": {} ?,                # If ?inline present & JSON (singular)
    "RESOURCEBase64": "STRING" ?     # If ?inline present & ~JSON (singular)
  } *
}
```

**Example:**

Request:

``` meta
TODO
```

##### Creating a new version of a Resource

This will create a new version of a Resource. Any metadata not present will be
inherited from latest version. To delete any metadata include its HTTP Header
with an empty value.

The request MUST be of the form:

``` meta
POST /GROUPs/ID/RESOURCEs/ID[?epoch=EPOCH]
Registry-id: STRING ?            # If present it MUST match URL
Registry-name: STRING ?
Registry-type: STRING ?
Registry-version: STRING ?       # MUST NOT be present
Registry-epoch: UINT ?           # If present it MUST match current value & URL
Registry-self: STRING ?          # If present it MUST be ignored?
Registry-RESOURCEURI: URI ?      # If present body MUST be empty (singular)

{ ...Resource entity... } ?      # If empty then content is erased
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING
Registry-RESOURCEURI: URI ?       # singular
Content-Location: URL            # Same as self
Location: .../GROUPs/ID/RESOURCEs/ID   # or self?

{ ...Resource entity... } ?
```

**Example:**

Request:

``` meta
TODO
```

Response:

``` meta
TODO
```

##### Retrieving a version of a Resource

This will retrieve a particular version of a Resource.

The request MUST be of the form:

``` meta
GET /GROUPs/ID/RESOURCEs/ID/versions/VERSION
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK  or 307 Temporary Redirect    # 307 if RESOURCEURI is present
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING            # URL to the specific version
Registry-RESOURCEURI: URI ?      # If present body MUST be empty (singular)
Content-Location: URL            # Same as Registry-self value
Location: URL                    # If 307. Same a Registry-RESOURCEURI

{ ...Resource entity... } ?
```

**Example:**

Request:

``` meta
TODO
```

##### Retrieving a version of a Resource's metadata

This will retrieve the metadata for a particular version of a Resource.

The request MUST be of the form:

``` meta
GET /GROUPs/ID/RESOURCEs/ID/versions/ID?meta
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "epoch": UINT,
  "self": "URL",
  "RESOURCEUri": "URI" ?          # singular
}
```

**Example:**

Request:

``` meta
TODO
```

##### Updating a version of a Resource

This will update a particular version of a Resource. Missing Registry HTTP
headers MUST NOT be interpreted as deleting the attribute. However, a Registry
HTTP headers with an empty string for its value MUST be interpreted as a
request to delete the attribute.

The request MUST be of the form:

``` meta
PUT /GROUPs/ID/RESOURCEs/ID/versions/VERSION[?epoch=EPOCH]
Registry-id: STRING ?            # If present it MUST match URL
Registry-name: STRING ?
Registry-type: STRING ?
Registry-version: STRING ?       # If present it MUST match current value & URL
Registry-epoch: UINT ?           # If present it MUST match current value & URL
Registry-self: STRING ?          # If present it MUST be ignored?
Registry-RESOURCEURI: URI ?      # If present body MUST be empty (singular)

{ ...Resource entity... } ?      # If empty then content is erased
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT             # MUST be incremented
Registry-self: STRING
Registry-RESOURCEURI: URI ?      # singular
Content-Location: URL

{ ...Resource entity... } ?
```

Note: if some of the Registry attributes are shared with the Resource itself
then those values MUST appear in both the Registry HTTP headers as well as in
the Resource itself when retrieving the Resource. However, in this "update"
case, if the attribute only appears in the HTTP body and the corresponding
Registry HTTP header is missing then the Registry attribute MUST be updated to
match the Resource's attribute. If both are present on the request and do not
have the same value then an error MUST be generated.

**Example:**

Request:

``` meta
TODO
```

##### Updating a version of a Resource's metadata

This will update the metadata of a particular version of a Resource without
creating a new version.

The request MUST be of the form:

``` meta
PUT /GROUPs/ID/RESOURCEs/ID/versions/ID?meta[&epoch=EPOCH]

{
  "id": "STRING",
  "name": "STRING",
  "epoch": UINT, ?             # If present it MUST match current value & URL
  "self": "URL", ?             # If present it MUST be ignored
  "RESOURCEUri": "URI" ?       # singular
}
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "epoch": UINT,               # MUST be incremented
  "self": "URL",
  "RESOURCEUri": "URI" ?       # singular
}
```

**Example:**

Request:

``` meta
TODO
```

Response:

``` meta
TODO
```

##### Deleting versions of a Resource

To delete a single version of a Resource the following API can be used.

The request MUST be of the form:

``` meta
DELETE /GROUPs/ID/RESOURCEs/ID/versions/VERSION[?epoch=EPOCH]
```

If `epoch` is present then it MUST match the current value.

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING
Registry-RESOURCEURI: URI ?        # singular
Content-Location: URL              # Does this make sense if it's been deleted?

{ ...Resource entity... } ?
```

**Example:**

Request:

``` meta
TODO
```

Response:

``` meta
TODO
```

To delete multiple versions of a Resource the following API can be used.

The request MUST be of the form:

``` meta
DELETE /GROUPs/ID/RESOURCEs/ID/versions

[
  {
    "id": "STRING",
    "epoch": UINT ?     # If present it MUST match current value
  } *
]
```

A successful response MUST be of the form:

``` meta
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ "ID": { ... } * } ?   # RECOMMENDED
```

If any of the individual deletes fails then the entire request MUST fail
and none of the Resources are deleted.

If the latest version is deleted then the remaining version with the largest
`versionId` value MUST become the latest.

An attempt to delete all versions MUST generate an error.

A `DELETE /GROUPs/ID/RESOURCEs/ID/versions` without a body MUST delete all
versions (except the latest) of the Resource.

## CloudEvents Registry

The CloudEvents Registry is a universal catalog and discovery metadata format
as well as a metadata service API for messaging and eventing schemas,
metaschemas, and messaging and eventing endpoints.

The CloudEvents registry model contains three separate registries that can be
implemented separately or in combination.

- The [Schema Registry](#schema-registry) section describes the metadata
  description of payload schemas for events and messages. The schema registry is
  universally applicable to any scenario where collaborating parties share
  structured data that is defined by formal schemas. For instance, when storing
  Protobuf encoded structured data in a cloud file store, you might place a
  schema registry in file form in the parent directory, which formally organizes
  and documents all versions of all Protobuf schemas that are used in the
  directory.
- The [Message Definitions Registry](#message-definitions-registry) section
  describes the metadata description of events and messages. The payload schemas
  for events and messages can be embedded in the definition, reference an
  external schema document, or can be referenced into the schema registry. The
  message definitions registry is universally applicable to any asynchronous
  messaging and eventing scenario. You might define a group of definitions that
  describe precisely which messages, with which metadata, are permitted to flow
  into a channel and can thus be expected by consumers of that channel and then
  associate that definition group with a topic or queue in your eventing or
  messaging infrastructure. That association might be a metadata attribute on
  the topic or queue in the messaging infrastructure that embeds the metadata or
  points to it.
- The [Endpoint Registry](#endpoint-registry) section defines the metadata
  description of network endpoints that accept or emit events and messages. The
  endpoint registry is a formal description of associations of message
  definitions and network endpoints, which can be used to discover endpoints
  that consume or emit particular messages or events via a central registry. The
  message definitions can be embedded into the endpoint metadata or as
  a reference into the message definitions registry.

The metadata model is structured such that network endpoint information and
message metadata and payload schemas can be described compactly in a single
metadata object (and therefore as a single document) in the simplest case or can
be spread out and managed across separate registry products in a sophisticated
large-enterprise scenario.

The following is an exemplary, compact definition of an MQTT 5.0 consumer
endpoint with a single, embedded message definition using an embedded Protobuf 3
schema for its payload.

``` JSON
{
  "$schema": "https://cloudevents.io/schemas/registry",
  "specversion": "0.5-wip",
  "id": "urn:uuid:3978344f-8596-4c3a-a978-8fc9a6a469f7",
  "endpoints":
  {
    "com.example.telemetry": {
      "id": "com.example.telemetry",
      "usage": "consumer",
      "config": {
        "protocol": "MQTT/5.0",
        "strict": false,
        "endpoints": [
            "mqtt://mqtt.example.com:1883"
        ],
        "options": {
            "topic": "{deviceid}/telemetry"
        }
      },
      "format": "CloudEvents/1.0",
      "definitions": {
        "com.example.telemetry": {
          "id": "com.example.telemetry",
          "description": "device telemetry event",
          "format": "CloudEvents/1.0",
          "metadata": {
            "attributes": {
              "id": {
                "type": "string",
                "required": true
              },
              "type": {
                "type": "string",
                "value": "com.example.telemetry",
                "required": true
              },
              "time": {
                "type": "datetime",
                "required": true
              },
              "source": {
                "type": "uritemplate",
                "value": "{deploymentid}/{deviceid}",
                "required": true
              }
            }
          },
          "schemaformat": "Protobuf/3.0",
          "schema": "syntax = \"proto3\"; message Metrics { float metric = 1; } }"
        }
      }
    }
  }
}
```

The same metadata can be expressed by spreading the metadata across the message
definition and schema registries, which makes the definitions reusable for other
scenarios:

``` JSON
{
  "$schema": "https://cloudevents.io/schemas/registry",
  "specversion": "0.4-wip",
  "id": "urn:uuid:3978344f-8596-4c3a-a978-8fc9a6a469f7",

  "endpointsCount": 1,
  "endpoints":
  {
    "com.example.telemetry": {
      "id": "com.example.telemetry",
      "usage": "consumer",
      "config": {
        "protocol": "MQTT/5.0",
        "strict": false,
        "endpoints": [
          "mqtt://mqtt.example.com:1883"
        ],
        "options": {
          "topic": "{deviceid}/telemetry"
        }
      },
      "format": "CloudEvents/1.0",
      "definitionGroups": [
        "#/definitionGroups/com.example.telemetryEvents"
      ]
    }
  },

  "definitionGroupsCount": 1,
  "definitionGroups": {
    "com.example.telemetryEvents": {
      "id": "com.example.telemetryEvents",

      "definitionsCount": 1,
      "definitions": {
        "com.example.telemetry": {
          "id": "com.example.telemetry",
          "description": "device telemetry event",
          "format": "CloudEvents/1.0",
          "metadata": {
            "attributes": {
              "id": {
                "type": "string",
                "required": true
              },
              "type": {
                "type": "string",
                "value": "com.example.telemetry",
                "required": true
              },
              "time": {
                "type": "datetime",
                "required": true
              },
              "source": {
                "type": "uritemplate",
                "value": "{deploymentid}/{deviceid}",
                "required": true
              }
            }
          },
          "schemaformat": "Protobuf/3.0",
          "schemaurl": "#/schemaGroups/com.example.telemetry/schema/com.example.telemetrydata/versions/1.0"
        }
      }
    }
  },

  "schemaGroupsCount": 1,
  "schemaGroups": {
    "com.example.telemetry": {
      "id": "com.example.telemetry",

      "schemasCount": 1,
      "schemas": {
        "com.example.telemetrydata": {
          "id": "com.example.telemetrydata",
          "description": "device telemetry event data",
          "format": "Protobuf/3.0",

          "versionsCount": 1,
          "versions": {
            "1.0": {
              "id": "1.0",
              "schema": "syntax = \"proto3\"; message Metrics { float metric = 1; }"
            }
          }
        }
      }
    }
  }
}
```

If we assume the message definitions and schemas to reside at an API endpoint,
an endpoint definition might just reference the associated message definition
group with a deep link to the respective object in the service:

``` JSONC
{
  "$schema": "https://cloudevents.io/schemas/registry",
  "specversion": "0.4-wip",
  "id": "urn:uuid:3978344f-8596-4c3a-a978-8fc9a6a469f7",

  "endpointsCount": 1,
  "endpoints":
  {
    "com.example.telemetry": {
      "id": "com.example.telemetry",
      "usage": "consumer",
      "config": {
        // ... details ...
      },
      "format": "CloudEvents/1.0",
      "definitionGroups": [
          "https://site.example.com/registry/definitiongroups/com.example.telemetryEvents"
      ]
    }
  }
}
```

If the message definitions and schemas are stored in a file-based registry,
including files shared via public version control repositories, the reference
link will first reference the file and then the object within the file, using
[JSON Pointer][JSON Pointer] syntax:

``` JSONC
{
  "$schema": "https://cloudevents.io/schemas/registry",
  "specversion": "0.4-wip",
  "id": "urn:uuid:3978344f-8596-4c3a-a978-8fc9a6a469f7",

  "endpointsCount": 1,
  "endpoints":
  {
    "com.example.telemetry": {
      "id": "com.example.telemetry",
      "usage": "consumer",
      "config": {
        // ... details ......
      },
      "format": "CloudEvents/1.0",
      "definitionGroups": [
        "https://rawdata.repos.example.com/myorg/myproject/main/example.telemetryEvents.cereg#/definitionGroups/com.example.telemetryEvents"
      ]
    }
  }
}
```

All other references to other objects in the registry can be expressed in the
same way.

While the CloudEvents Registry is primarily motivated by enabling development of
CloudEvents-based event flows, the registry is not limited to CloudEvents. It
can be used to describe any asynchronous messaging or eventing endpoint and its
messages, including endpoints that do not use CloudEvents at all. The [Message
Formats](#message-formats) section therefore not only describes the attribute
meta-schema for CloudEvents, but also meta-schemas for the native message
envelopes of MQTT, AMQP, and other messaging protocols.

The registry is designed to be extensible to support any structured data
encoding and related schemas for message or event payloads. The [Schema
Formats](#schema-formats) section describes the meta-schema for JSON Schema, XML
Schema, Apache Avro schema, and Protobuf schema.

### File format

A CloudEvents Registry can be implemented using the Registry API or with plain
text files.

When using the file-based model, files with the extension `.cereg` use JSON
encoding. Files with the extension `.cereg.yaml` or `.cereg.yml` use YAML
encoding. The formal JSON schema for the file format is defined in the
[CloudEvents Registry Document Schema](#cloudevents-registry-document-schema),
which implements the Registry format and the CloudEvents Registry format.

The media-type for the file format is `application/cloudevents-registry+json`
for the JSON encoding and `application/cloudevents-registry+yaml` for the YAML
encoding.

The JSON schema identifier is `https://cloudevents.io/schemas/registry` and the
`specversion` property indicates the version of this specification that the
elements of the file conform to.

A CloudEvents Registry file MUST contain a single JSON object or YAML document.
The object declares the roots of the three sub-registries, which are either
embedded or referenced. Any of the three sub-registries MAY be omitted.

``` meta
{
   "$schema": "https://cloudevents.io/schemas/registry",
   "specversion": "0.4-wip",

   "endpointsUrl": "URL",
   "endpointsCount": INT,
   "endpoints": { ... },

   "definitionGroupsUrl": "URL",
   "definitionGroupsCount": INT,
   "definitionGroups": { ... },

   "schemaGroupsUrl": "URL",
   "schemaGroupsCount": INT,
   "schemaGroups": { ... }
}
```

While the file structure leads with endpoints followed by definition groups and
then schema groups by convention, the order of the sub-registries is not
significant.

### Schema Registry

The schema registry is a metadata store for organizing data schemas of any kind.

The Registry API extension model of the Schema Registry is:

``` JSON
{
  "groups": [
    {
      "singular": "schemaGroup",
      "plural": "schemaGroups",
      "schema": "TBD",
      "resources": [
        {
          "singular": "schema",
          "plural": "schemas",
          "versions": 0
        }
      ]
    }
  ]
}
```

#### Group: schemaGroups

The group (GROUP) name for the Schema Registry is `schemaGroups`. The group does
not have any specific extension attributes.

A schema group is a collection of schemas that are related to each other in some
application-defined way. A schema group does not impose any restrictions on the
contained schemas, meaning that a schema group can contain schemas of different
formats. Every schema MUST reside inside a schema group.

Example:

``` meta
{
  "schemaGroupsUrl": "http://example.com/schemagroups",
  "schemaGroupsCount": 1,
  "schemaGroups": {
    "com.example.schemas": {
      "id": "com.example.schemas",
      "schemasUrl": "https://example.com/schemagroups/com.example.schemas/schemas",
      "schemasCount": 5,
      "schemas": {
        ...
      }
    }
  }
}
```

#### Resource: schemas

The resources (RESOURCE) collection inside of schema groups is named `schemas`.
The type of the resource is `schema`. Any single `schema` is a container for
one or more `versions`, which hold the concrete schema documents or schema
document references.

Any new schema version that is added to a schema definition MUST be backwards
compatible with all previous versions of the schema, meaning that a consumer
using the new schema MUST be able to understand data encoded using a prior
version of the schema. If a new version introduces a breaking change, it MUST be
registered as a new schema with a new name.

When you retrieve a schema without qualifying the version, you will get the
latest version of the schema, see [retrieving a
resource](#retrieving-a-resource). The latest version is the lexically greatest
version number, whereby all version ids MUST be left-padded with spaces to the
same length before being compared.

The following extension is defined for the `schema` object in addition to the
basic [attributes](#attributes-and-extensions):

##### `format` (Schema format)

- Type: String
- Description: Identifies the schema format. In absence of formal media-type
  definitions for several important schema formats, we define a convention here
  to reference schema formats by name and version as `{NAME}/{VERSION}`. This
  specification defines a set of common [schema format names](#schema-formats)
  that MUST be used for the given formats, but applications MAY define
  extensions for other formats on their own.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST follow the naming convention `{NAME}/{VERSION}`, whereby `{NAME}` is
    the name of the schema format and `{VERSION}` is the version of the schema
    format in the format defined by the schema format itself.
- Examples:
  - `JsonSchema/draft-07`
  - `Protobuf/3`
  - `XSD/1.1`
  - `Avro/1.9`

#### Resource Version: schemaversion

The `VERSION` object of the `schema` resource is of type `schemaversion`. The
[`format`](#format-schema-format) extension attribute of `schema` MAY be
repeated in `schemaversion` for clarity, but MUST be identical.
`schemaversion` has the following extension attributes.

##### `schema`

- Type: String | Object
- Description: Embedded schema string or object. The format and encoding of the
  schema is defined by the `format` attribute.
- Constraints:
  - Mutually exclusive with `schemaurl`. One of the two MUST be present.

##### `schemaurl`

- Type: URI
- Description: Reference to a schema document external to the registry.
- Constraints:
  - Mutually exclusive with `schemaurl`. One of the two MUST be present.
  - Cross-references to a schema document within the same registry MUST NOT be
    used.

The following example shows three embedded `Protobuf/3` schema versions for a
schema named `com.example.telemetrydata`:

``` JSON
{
  "schemaGroupsUrl": "...",
  "schemaGroupsCount": 1,
  "schemaGroups": {
    "com.example.telemetry": {
      "id": "com.example.telemetry",

      "schemasUrl": "...",
      "schemasCount": 1,
      "schemas": {
        "com.example.telemetrydata": {
          "id": "com.example.telemetrydata",
          "description": "device telemetry event data",
          "format": "Protobuf/3",

          "versionsUrl": "...",
          "versionsCount": 3,
          "versions": {
            "1.0": {
              "id": "1.0",
              "schema": "syntax = \"proto3\"; message Metrics { float metric = 1; } }"
            },
            "2.0": {
              "id": "2.0",
              "schema": "syntax = \"proto3\"; message Metrics { float metric = 1; string unit = 2; } }"
            },
            "3.0": {
              "id": "3.0",
              "schema": "syntax = \"proto3\"; message Metrics { float metric = 1; string unit = 2; string description = 3; } }"
            }
          }
        }
      }
    }
  }
}
```

#### Schema Formats

This section defines a set of common schema formats that MUST be used for the
given formats, but applications MAY define extensions for other formats on their
own.

##### JSON Schema

The [`format`](#format-schema-format) identifier for JSON Schema is
`JsonSchema`.

When the `format` attribute is set to `JsonSchema`, the `schema` attribute of
the `schemaversion` is a JSON object representing a JSON Schema document
conformant with the declared version.

A URI-reference, like [`schemaurl`](#schemaurl-message-schema-url) that points
to a JSON Schema document MAY use a JSON pointer expression to deep link into
the schema document to reference a particular type definition. Otherwise the
top-level object definition of the schema is used.

The version of the JSON Schema format is the version of the JSON
Schema specification that is used to define the schema. The version of the JSON
Schema specification is defined in the `$schema` attribute of the schema
document.

The identifiers for the following JSON Schema versions

- Draft 07: `http://json-schema.org/draft-07/schema`
- Draft 2019-09: `https://json-schema.org/draft/2019-09/schema`
- Draft 2020-12: `https://json-schema.org/draft/2020-12/schema`

are defined as follows:

- `JsonSchema/draft-07`
- `JsonSchema/draft/2019-09`
- `JsonSchema/draft/2020-12`

which follows the exact convention as defined for JSON schema and expecting an
eventually released version 1.0 of the JSON Schema specification using a plain
version number.

##### XML Schema

The [`format`](#format-schema-format) identifier for XML Schema is `XSD`. The
version of the XML Schema format is the version of the W3C XML Schema
specification that is used to define the schema.

When the `format` attribute is set to `XSD`, the `schema` attribute of
`schemaversion` is a string containing an XML Schema document conformant with
the declared version.

A URI-reference, like [`schemaurl`](#schemaurl-message-schema-url) that points
to a XSD Schema document MAY use an XPath expression to deep link into the
schema document to reference a particular type definition. Otherwise the root
element definition of the schema is used.

The identifiers for the following XML Schema versions

- 1.0: `https://www.w3.org/TR/xmlschema-1/`
- 1.1: `https://www.w3.org/TR/xmlschema11-1/`

are defined as follows:

- `XSD/1.0`
- `XSD/1.1`

##### Apache Avro Schema

The [`format`](#format-schema-format) identifier for Apache Avro Schema is
`Avro`. The version of the Apache Avro Schema format is the version of the
Apache Avro Schema release that is used to define the schema.

When the `format` attribute is set to `Avro`, the `schema` attribute of the
`schemaversion` is a JSON object representing an Avro schema document conformant
with the declared version.

Examples:

- `Avro/1.8.2` is the identifier for the Apache Avro release 1.8.2.
- `Avro/1.11.0` is the identifier for the Apache Avro release 1.11.0

A URI-reference, like [`schemaurl`](#schemaurl-message-schema-url) that points
to an Avro Schema document MUST reference an Avro record declaration contained
in the schema document using a URI fragment suffix `[:]{record-name}`. The ':'
character is used as a separator when the URI already contains a fragment.

Examples:

- If the Avro schema document is referenced using the URI
`https://example.com/avro/telemetry.avsc`, the URI fragment `#TelemetryEvent`
references the record declaration of the `TelemetryEvent` record.
- If the Avro schema document is a local schema registry reference like
`#/schemaGroups/com.example.telemetry/schemas/com.example.telemetrydata`, in the
which the reference is already in the form of a URI fragment, the suffix is
appended separated with a colon, for instance
`.../com.example.telemetrydata:TelemetryEvent`.

##### Protobuf Schema

The [`format`](#format-schema-format) identifier for Protobuf Schema is
`Protobuf`. The version of the Protobuf Schema format is the version of the
Protobuf syntax that is used to define the schema.

When the `format` attribute is set to `Protobuf`, the `schema` attribute of the
`schemaversion` is a string containing a Protobuf schema document conformant
with the declared version.

- `Protobuf/3` is the identifier for the Protobuf syntax version 3.
- `Protobuf/2` is the identifier for the Protobuf syntax version 2.

A URI-reference, like [`schemaurl`](#schemaurl-message-schema-url) that points
to an Protobuf Schema document MUST reference an Protobuf `message` declaration
contained in the schema document using a URI fragment suffix
`[:]{message-name}`. The ':' character is used as a separator when the URI
already contains a fragment.

Examples:

- If the Protobuf schema document is referenced using the URI
  `https://example.com/protobuf/telemetry.proto`, the URI fragment
  `#TelemetryEvent` references the message declaration of the `TelemetryEvent`
  message.
- If the Protobuf schema document is a local schema registry reference like
  `#/schemaGroups/com.example.telemetry/schemas/com.example.telemetrydata`, in
  the which the reference is already in the form of a URI fragment, the suffix
  is appended separated with a colon, for instance
  `.../com.example.telemetrydata:TelemetryEvent`.

### Message Definitions Registry

The Message Definitions Registry (or "Message Catalog") is a registry of
metadata definitions for messages and events. The entries in the registry
describe constraints for the metadata of messages and events, for instance the
concrete values and patterns for the `type`, `source`, and `subject` attributes
of a CloudEvent.

All message definitions (events are a from of messages and are therefore always
implied to be included from here on forward) are defined inside definition
groups.

A definition group is a collection of message definitions that are related to
each other in some application-specific way. For instance, a definition group
can be used to group all events raised by a particular application module or by
a particular role of an application protocol exchange pattern.

The Registry API extension model of the Message Definitions Registry is

``` JSON
{
  "groups": [
    {
      "singular": "definitionGroup",
      "plural": "definitionGroups",
      "schema": "TBD",
      "resources": [
        {
          "singular": "definition",
          "plural": "definitions",
          "versions": 1,
        }
      ]
    }
  ]
}
```

#### Message Definition Groups

The Group (GROUP) name is `definitionGroups`. The type of a group is
`definitionGroup`.

The following attributes are defined for the `definitionGroup` object in
addition to the basic [attributes](#attributes-and-extensions):

##### `format` (Message format)

- Type: String
- Description: Identifies the message metadata format. Message metadata formats
  are referenced by name and version as `{NAME}/{VERSION}`. This specification
  defines a set of common [message format names](#message-formats) that MUST be
  used for the given formats, but applications MAY define extensions for other
  formats on their own. All definitions inside a group MUST use this same
  format.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
  - MUST follow the naming convention `{NAME}/{VERSION}`, whereby `{NAME}` is
    the name of the message format and `{VERSION}` is the version of the schema
    format in the format defined by the schema format itself.
- Examples:
  - `CloudEvents/1.0`
  - `MQTT/3.1.1`
  - `AMQP/1.0`
  - `Kafka/0.11`

#### Message Definitions

The resource (RESOURCE) collection name inside `definitionGroup` is
`definitions`. The resource name is `definition`.

Different from schemas, message definitions do not contain a
version history. If the metadata of two messages differs, they are considered
different definitions.

The following extension is defined for the `definition` object in addition to
the basic [attributes](#attributes-and-extensions):

##### `format` (Message format, definition)

Same as the [`format`](#format-message-format) attribute of the
`definitionGroup` object.

Since definitions MAY be cross-referenced ("borrowed") across definition group
boundaries, this attribute is also REQUIRED and MUST be the same as the `format`
attribute of the `definitionGroup` object into which the definition is embedded
or referenced.

Illustrating example:

``` JSONC

"definitionGroupsUrl": "...",
"definitionGroupsCount": 2,
"definitionGroups": {
  "com.example.abc": {
    "id": "com.example.abc",
    "format": "CloudEvents/1.0",

    "definitionsUrl": "...",
    "definitionsCount": 2,
    "definitions": {
      "com.example.abc.event1": {
        "id": "com.example.abc.event1",
        "format": "CloudEvents/1.0",
         // ... details ...
        }
      },
      "com.example.abc.event2": {
        "id": "com.example.abc.event1",
        "format": "CloudEvents/1.0",
        // ... details ...
      }
  },
  "com.example.def": {
    "id": "com.example.def",
    "format": "CloudEvents/1.0",

    "definitionsUrl": "...",
    "definitionsCount": 1,
    "definitions": {
      "com.example.abc.event1": {
        "uri": "#/definitionGroups/com.example.abc/definitions/com.example.abc.event1",
        // ... details ...
      }
    }
  }
}
```

##### `metadata` (Message metadata)

- Type: Object
- Description: Describes the metadata constraints for messages of this type. The
  content of the metadata property is defined by the message format, but all
  formats use a common schema for the constraints defined for their metadata
  headers, properties or attributes.
- Constraints:
  - REQUIRED
- Examples:
  - See [Message Formats](#message-formats)

##### `schemaformat`

- Type: String
- Description: Identifies the schema format applicable to the message payload,
  equivalent to the schema ['format'](#format-schema-format) attribute.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string
  - If present, MUST follow the naming convention `{NAME}/{VERSION}`, whereby
    `{NAME}` is the name of the schema format and `{VERSION}` is the version of
    the schema format in the format defined by the schema format itself.
- Examples:
  - 'JSONSchema/draft-07'
  - 'Avro/1.9.0'
  - 'Protobuf/3'

##### `schema` (Message schema)

- Type: String | Object as defined by the schema format
- Description: Contains the inline schema for the message payload. The schema
  format is identified by the `schemaformat` attribute. Equivalent to the
  schemaversion
  ['schema'](#schema) attribute
- Constraints:
  - OPTIONAL.
  - Mutually exclusive with the `schemaurl` attribute.
  - If present, `schemaformat` MUST be present.
- Examples:
  - See [Schema Formats](#schema-formats)

##### `schemaurl` (Message schema URL)

- Type: URI-reference
- Description: Contains a relative or absolute URI that points to the schema
  object to use for the message payload. The schema format is identified by the
  `schemaformat` attribute. See [Schema Formats](#schema-formats) for details on
  how to reference specific schema objects for the message payload. It is not
  sufficient for the URI-reference to point to a schema document; it MUST
  resolve to a concrete schema object.
- Constraints:
  - OPTIONAL.
  - Mutually exclusive with the `schema` attribute.
  - If present, `schemaformat` MUST be present.

#### Message Formats

This section defines the message formats that are directly supported by this
specification. Message formats lean on a protocol-neutral metadata definition
like CloudEvents or on the message model definition of a specific protocol like
AMQP or MQTT or Kafka. A message format defines constraints for the fixed and
variable headers/properties/attributes of the event format or protocol message
model.

> Message format definitions might be specific to a particular client instance
> and used to configure that client. Therefore, the message format definitions
> allow for specifying very narrow constraints like the exact value of an Apache
> Kafka record `key`.

##### Common properties

The following properties are common to all definitions of message
headers/properties/attributes constraints:

###### `required` (REQUIRED)

- Type: Boolean
- Description: Indicates whether the property is REQUIRED to be present in a
  message of this type.
- Constraints:
  - OPTIONAL. Defaults to `false`.
  - If present, MUST be a boolean value.

###### `description` (Description)

- Type: String
- Description: A human-readable description of the property.
- Constraints:
  - OPTIONAL.
  - If present, MUST be a non-empty string.

###### `value` (Value)

- Type: Any
- Description: The value of the property. With a few exceptions, see below, this
  is the value that MUST be literally present in the message for the message to
  be considered conformant with this metaschema.
- Constraints:
  - OPTIONAL.
  - If present, MUST be a valid value for the property.

If the `type` property has the value `uritemplate`, `value` MAY contain
placeholders. As defined in [RFC6570][RFC6570] (Level 1), the placeholders MUST
be enclosed in curly braces (`{` and `}`) and MUST be a valid `symbol`.
Placeholders that are used multiple times in the same message definition are
assumed to represent identical values.

When validating a message property against this value, the placeholders act as
wildcards. For example, the value `{foo}/bar` would match the value `abc/bar` or
`xyz/bar`.

When creating a message based on a metaschema with such a value, the
placeholders MUST be replaced with valid values. For example, the value
`{foo}/bar` would be replaced with `abc/bar` or `xyz/bar` when creating a
message.

If the `type` property has the value `timestamp` and the `value` property is
set to a value of `01-01-0000T00:00:00Z`, the value MUST be replaced with the
current timestamp when creating a message.

###### `type` (Type)

- Type: String
- Description: The type of the property. This is used to constrain the value of
  the property.
- Constraints:
  - OPTIONAL. Defaults to "string".
  - The valid types are those defined in the [CloudEvents][CloudEvents Types]
    core specification, with some additions:
    - `var`: Any type of value, including `null`.
    - `boolean`: CloudEvents "Boolean" type.
    - `string`: CloudEvents "String" type.
    - `symbol`: A `string` that is restricted to alphanumerical characters and
      underscores.
    - `binary`: CloudEvents "Binary" type.
    - `timestamp`: CloudEvents "Timestamp" type (RFC3339 DateTime)
    - `duration`: RFC3339 Duration
    - `uritemplate`: [RFC6570][RFC6570] Level 1 URI Template
    - `uri`: CloudEvents "URI" type (RFC3986 URI)
    - `urireference`: CloudEvents "URI-reference" type (RFC3986 URI-reference)
    - `number`: IEEE754 Double
    - `integer`: CloudEvents "Integer" type (RFC 7159, Section 6)

###### `specurl` (Specification URL)

- Type: URI-reference
- Description: Contains a relative or absolute URI that points to the
  human-readable specification of the property.
- Constraints:
  - OPTIONAL

###### CloudEvents/1.0

For the "CloudEvents/1.0" format, the [`metadata`](#metadata-message-metadata)
object contains a property `attributes`, which is an object whose properties
correspond to the CloudEvents context attributes.

As with the [CloudEvents specification][CloudEvents], the attributes form a
flat list and extension attributes are allowed. Attribute names are restricted
to lower-case alphanumerical characters without separators.

The base attributes are defined as follows:

| Attribute | Type |
| ---- | ---- |
| `type` | `string` |
| `source` | `uritemplate` |
| `subject` | `string` |
| `id` | `string` |
| `time` | `timestamp` |
| `dataschema` | `uritemplate` |
| `datacontenttype` | `string` |

The following rules apply to the attribute declarations:

- All attribute declarations are OPTIONAL. Requirements for absent
  definitions are implied by the CloudEvents specification.
- The `specversion` attribute is implied by the message format and is NOT
  REQUIRED. If present, it MUST be declared with a `string` type and set to the
  value "1.0".
- The `type`, `id`, and `source` attributes implicitly have the `required` flag
  set to `true` and MUST NOT be declared as `required: false`.
- The `id` attribute's `value` SHOULD NOT be defined.
- The `time` attribute's `value` defaults to `01-01-0000T00:00:00Z` ("current
  time") and SHOULD NOT be declared with a different value.
- The `datacontenttype` attribute's `value` is inferred from the
  [`schemaformat`](#schemaformat) attribute of the message definition if absent.
- The `dataschema` attribute's `value` is inferred from the
  [`schemaurl`](#schemaurl-message-schema-url) attribute or
  [`schema`](#schema-message-schema) attribute of the message definition if
  absent.
- The `type` of the property definition defaults to the CloudEvents type
  definition for the attribute, if any. The `type` of an attribute MAY be
  modified. For instance, the `source` type `urireference` MAY be changed to
  `uritemplate` or the `subject` type `string` MAY be constrained to a
  `urireference` or `integer`. If no CloudEvents type definition exists, the
  type defaults to `string`.

The values of all `string` and `uritemplate`-typed attributes MAY contain
placeholders using the [RFC6570][RFC6570] Level 1 URI Template syntax. When the
same placeholder is used in multiple properties, the value of the placeholder is
assumed to be identical.

The following example declares a CloudEvent with a JSON payload. The attribute
`id` is REQUIRED in the declared event per the CloudEvents specification in
spite of such a declaration being absent here, the `type` of the `type`
attribute is `string` and the attribute is `required` even though the
declarations are absent. The `time` attribute is made `required` contrary to the
CloudEvents base specification. The implied `datacontenttype` is
`application/json` and the implied `dataschema` is
`https://example.com/schemas/com.example.myevent.json`:

``` JSON
{
  "format": "CloudEvents/1.0",
  "metadata": {
    "attributes": {
      "type": {
        "value": "com.example.myevent"
      },
      "source": {
        "value": "https://{tenant}/{module}/myevent",
        "type": "uritemplate"
      },
      "subject": {
        "type": "urireference"
      },
      "time": {
        "required": true
      },
    }
  },
  "schemaformat": "JsonSchema/draft-07",
  "schemaurl": "https://example.com/schemas/com.example.myevent.json",
}
```

For clarity of the definition, you MAY always declare all implied attribute
properties explicitly, but they MUST conform with the rules above.

#### "HTTP/1.1", "HTTP/2", "HTTP/3"

The "HTTP" format is used to define messages that are sent over an HTTP
connection. The format is based on the [HTTP Message Format][HTTP Message
 Format] and is common across all version of HTTP.

The [`metadata`](#metadata-message-metadata) object MAY contain several
properties:

| Property | Type | Description |
| --- | --- | --- |
| `headers` | Array | The HTTP headers. See below. |
| `query` | Map | The HTTP query parameters. |
| `path` | `uritemplate` | The HTTP path. |
| `method` | `string` | The http method |
| `status` | `string` | The http status code |

HTTP allows for multiple headers with the same name. The `headers` property is
therefore an array of objects with `name` and `value` properties. The `name`
property is a string that MUST be a valid HTTP header name.

The `query` property is a map of string keys to string values.

The `path` property is a URI template.

The `method` property is a string that MUST be a valid HTTP method.

The `status` property is a string that MUST be a valid HTTP response
code. The `status` and `method` properties are mutually exclusive and
MUST NOT be present at the same time.

The values of all `string` and `uritemplate`-typed properties and headers and
query elements MAY contain placeholders using the [RFC6570][RFC6570] Level 1 URI
Template syntax. When the same placeholder is used in multiple properties, the
value of the placeholder is assumed to be identical.

The following example defines a message that is sent over HTTP/1.1:

``` JSON
{
  "format": "HTTP/1.1",
  "metadata": {
    "headers": [
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ],
    "query": {
      "foo": "bar"
    },
    "path": "/foo/{bar}",
    "method": "POST"
  },
  "schemaformat": "JsonSchema/draft-07",
  "schemaurl": "https://example.com/schemas/com.example.myevent.json",
}
```

#### "AMQP/1.0"

The "AMQP/1.0" format is used to define messages that are sent over an
[AMQP][AMQP 1.0] connection. The format is based on the default
[AMQP 1.0 Message Format][AMQP 1.0 Message Format].

The [`metadata`](#metadata-message-metadata) object MAY contain several
properties, each of which corresponds to a section of the AMQP 1.0 Message:

| Property | Type | Description |
| ---- | --- | ---- |
| `properties` | Map | The AMQP 1.0 [Message Properties][AMQP 1.0 Message Properties] section. |
| `application-properties` | Map | The AMQP 1.0 [Application Properties][AMQP 1.0 Application Properties] section. |
| `message-annotations` | Map | The AMQP 1.0 [Message Annotations][AMQP 1.0 Message Annotations] section. |
| `delivery-annotations` | Map | The AMQP 1.0 [Delivery Annotations][AMQP 1.0 Delivery Annotations] section. |
| `header` | Map | The AMQP 1.0 [Message Header][AMQP 1.0 Message Header] section. |
| `footer` | Map | The AMQP 1.0 [Message Footer][AMQP 1.0 Message Footer] section. |

As in AMQP, all sections and properties are OPTIONAL.

The values of all `string`, `symbol`, `uri`, and `uritemplate`-typed properties
MAY contain placeholders using the [RFC6570][RFC6570] Level 1 URI Template
syntax. When the same placeholder is used in multiple properties, the value of
the placeholder is assumed to be identical.

Example for an AMQP 1.0 message type that declares a fixed `subject` (analogous
to CloudEvents' `type`), a custom property, and a `content-type` of
`application/json` without declaring a schema reference in the message
definition:

``` JSON
{
  "format": "AMQP/1.0",
  "metadata": {
    "properties": {
      "message-id": {
        "required": true
      },
      "to": {
        "value": "https://{host}/{queue}"
      },
      "subject": {
        "value": "MyMessageType"
        "required": true
      },
      "content-type": {
        "value": "application/json"
      },
      "content-encoding": {
        "value": "utf-8"
      }
    },
    "application-properties": {
      "my-application-property": {
        "value": "my-application-property-value"
      }
    }
  }
}
```

##### `properties` (AMQP 1.0 Message Properties)

The `properties` property is an object that contains the properties of the
AMQP 1.0 [Message Properties][AMQP 1.0 Message Properties] section. The
following properties are defined, with type constraints:

| Property | Type | Description |
| --- | --- | --- |
| `message-id` | `string` | uniquely identifies a message within the message system |
| `user-id` | `binary` | identity of the user responsible for producing the message |
| `to` | `uritemplate` | address of the node to send the message to |
| `subject` | `string` | message subject |
| `reply-to` | `uritemplate` | address of the node to which the receiver of this message ought to send replies |
| `correlation-id` | `string` | client-specific id that can be used to mark or identify messages between clients |
| `content-type` | `symbol` | MIME content type for the message |
| `content-encoding` | `symbol` | MIME content encoding for the message |
| `absolute-expiry-time` | `timestamp` | time when this message is considered expired |
| `group-id` | `string` | group this message belongs to |
| `group-sequence` | `integer` | position of this message within its group |
| `reply-to-group-id` | `uritemplate` | group-id to which the receiver of this message ought to send replies to |

##### `application-properties` (AMQP 1.0 Application Properties)

The `application-properties` property is an object that contains the custom
properties of the AMQP 1.0 [Application Properties][AMQP 1.0 Application
Properties] section.

The names of the properties MUST be of type `symbol` and MUST be unique.
The values of the properties MAY be of any permitted type.

##### `message-annotations` (AMQP 1.0 Message Annotations)

The `message-annotations` property is an object that contains the custom
properties of the AMQP 1.0 [Message Annotations][AMQP 1.0 Message Annotations]
section.

The names of the properties MUST be of type `symbol` and MUST be unique.
The values of the properties MAY be of any permitted type.

##### `delivery-annotations` (AMQP 1.0 Delivery Annotations)

The `delivery-annotations` property is an object that contains the custom
properties of the AMQP 1.0
[Delivery Annotations][AMQP 1.0 Delivery Annotations] section.

The names of the properties MUST be of type `symbol` and MUST be unique.
The values of the properties MAY be of any permitted type.

###### `header` (AMQP 1.0 Message Header)

The `header` property is an object that contains the properties of the
AMQP 1.0 [Message Header][AMQP 1.0 Message Header] section. The
following properties are defined, with type constraints:

| Property | Type | Description |
| --- | --- | --- |
| `durable` | `boolean` | specify durability requirements |
| `priority` | `integer` | relative message priority |
| `ttl` | `integer` | message time-to-live in milliseconds |
| `first-acquirer` | `boolean` | indicates whether the message has not been acquired previously |
| `delivery-count` | `integer` | number of prior unsuccessful delivery attempts |

##### `footer` (AMQP 1.0 Message Footer)

The `footer` property is an object that contains the custom properties of the
AMQP 1.0 [Message Footer][AMQP 1.0 Message Footer] section.

The names of the properties MUST be of type `symbol` and MUST be unique.
The values of the properties MAY be of any permitted type.

#### "MQTT/3.1.1" and "MQTT/5.0"

The "MQTT/3.1.1" and "MQTT/5.0" formats are used to define messages that are
sent over [MQTT 3.1.1][MQTT 3.1.1] or [MQTT 5.0][MQTT 5.0] connections. The
format describes the [MQTT PUBLISH packet][MQTT 5.0] content.

The [`metadata`](#metadata-message-metadata) object contains the elements of the
MQTT PUBLISH packet directly, with the `user-properties` element corresponding
to the application properties collection of other protocols.

The following properties are defined. The MQTT 3.1.1 and MQTT 5.0 columns
indicate whether the property is supported for the respective MQTT version.

| Property | Type | MQTT 3.1.1 | MQTT 5.0 | Description |
| --- | --- | --- | --- | --- |
| `qos` | `integer` | yes | yes | Quality of Service level |
| `retain` | `boolean` | yes | yes | Retain flag |
| `topic-name` | `string` | yes | yes | Topic name |
| `payload-format` | `integer` | no | yes | Payload format indicator |
| `message-expiry-interval` | `integer` | no | yes | Message expiry interval |
| `response-topic` | `uritemplate` | no | yes | Response topic |
| `correlation-data` | `binary` | no | yes | Correlation data |
| `content-type` | `symbol` | no | yes | MIME content type of the payload |
| `user-properties` | Array | no | yes | User properties |

Like HTTP, the MQTT allows for multiple user properties with the same name,
so the `user-properties` property is an array of objects, each of which
contains a single property name and value.

The values of all `string`, `symbol`, and `uritemplate`-typed properties and
user-properties MAY contain placeholders using the [RFC6570][RFC6570] Level 1
URI Template syntax. When the same placeholder is used in multiple properties,
the value of the placeholder is assumed to be identical.

The following example shows a message with the "MQTT/5.0" format, asking for
QoS 1 delivery, with a topic name of "mytopic", and a user property of
"my-application-property" with a value of "my-application-property-value":

``` JSON
{
  "format": "MQTT/5.0",
  "metadata": {
    "qos": {
      "value": 1
    },
    "retain": {
      "value": false
    },
    "topic-name": {
      "value": "mytopic"
    },
    "user-properties": [
      { "my-application-property": {
            "value": "my-application-property-value"
          }
      }
    ]
  }
}
```

#### "Kafka/0.11" format

The "Kafka" format is used to define messages that are sent over [Apache
Kafka][Apache Kafka] connections. The version number reflects the last version
in which the record structure was changed in the Apache Kafka project, not the
current version. If the version number is omitted, the latest version is
assumed.

The [`metadata`](#metadata-message-metadata) object contains the common elements
of the Kafka [producer][Apache Kafka producer] and [consumer][Apache Kafka
consumer] records, with the `headers` element corresponding to the application
properties collection of other protocols.

The following properties are defined:

| Property | Type | Description |
| --- | --- | --- |
| `topic` | `string` | The topic the record will be appended to |
| `partition` | `integer` | The partition to which the record ought be sent |
| `key` | `binary` | The key that will be included in the record |
| `headers` | Map | A map of headers to set on the record |
| `timestamp` | `integer` | The timestamp of the record; if 0 (default), the producer will assign the timestamp |

The values of all `string`, `symbol`, `uritemplate`-typed properties
and headers MAY contain placeholders using the [RFC6570][RFC6570] Level 1 URI
Template syntax. When the same placeholder is used in multiple properties, the
value of the placeholder is assumed to be identical.

Example:

``` JSON
{
  "format": "Kafka/0.11",
  "metadata": {
    "topic": {
      "value": "mytopic"
    },
    "key": {
      "value": "thisdevice"
    }
  }
}

```

### Endpoint Registry

The Endpoint Registry is a registry of metadata definitions for abstract and
concrete network endpoint to which messages can be produced, from which messages
can be consumed, or which makes messages available for subscription and
delivery to a consumer-designated endpoint.

As discussed in [CloudEvents Registry overview](#cloudevents-registry),
endpoints are supersets of
[message definition groups](#message-definition-groups) and MAY contain
inlined definitions. Therefore, the RESORCE level in the meta-model for the
Endpoint Registry are likewise `definitions`:

``` JSON
{
  "groups": [
    {
      "singular": "endpoint",
      "plural": "endpoints",
      "schema": "TBD",
      "resources": [
        {
          "singular": "definition",
          "plural": "definitions",
          "versions": 1,
          "mutable": true
        }
      ]
    }
  ]
}
```

#### Endpoints: endpoints

A Group (GROUP) name is `endpoints`. The type of a group is `endpoint`.

The following attributes are defined for the `endpoint` type:

##### `usage`

- Type: String (Enum: `subscriber`, `consumer`, `producer`)
- Description: The `usage` attribute is a string that indicates the intended
  usage of the endpoint by communicating parties.

  Each of these parties will have a different perspective on an endpoint. For
  instance, a `producer` endpoint is seen as a "target" by the originator of
  messages, and as a "source" by the party that accepts the messages. The
  nomenclature used for the `usage` field is primarily oriented around the
  common scenario of network endpoints being provided by some sort of
  intermediary like a message broker. The term `producer` primarily describes
  the relationship of a client with that intermediary.

  In a direct-delivery scenario where the originator of messages connects
  directly to the target (e.g. a "WebHook" call), the target endpoint implements
  the accepting end of the `producer` relationship.

  Some of these perspectives are mentioned below for illustration, but not
  formally defined or reflected in the metadata model. Perspectives depend on
  the context in which the endpoint metadata is used and this metadata model is
  intentionally leaving perspectives open to users.

  The following values are defined for `usage`

  - `subscriber`: The endpoint offers managing subscriptions for delivery of
    messages to another endpoint, using the [CloudEvents Subscriptions
    API][CloudEvents Subscriptions API].

    Some perspectives that might exist on a subscriber endpoint:
    - Application from which messages originate
    - Application which accepts messages from the delivery agent
    - Application which manages subscriptions for delivery of messages to the
      target application. This might be a message broker subscription manager.

  - `consumer`:  The endpoint offers messages being consumed from it.

    Some perspectives that might exist on a consumer endpoint:
    - Message store or source which makes messages available for consumption;
      this might be a message broker topic or a queue.
    - Proxy or other intermediary which solicits messages from the source and
      forwards them to the target endpoint.
    - Application which consumes messages

  - `producer`: The endpoint offers messages being produces (sent) to it.

    Some perspectives might exist on a producer endpoint:
    - Application from which messages originate
    - Reverse proxy or other intermediary which accepts messages from the
      originator and forwards them to the target endpoint.
    - Application which accepts messages. This might be a message broker topic
      or a queue. This might be an HTTP endpoint that directly accepts and
      handles messages.

  Any endpoint can be seen from different role perspectives:

  There might also be further perspectives such as pipeline stages for
  pre-/post-processing, etc.

- Constraints:
  - REQUIRED.
  - MUST be one of "subscriber", "consumer", or "producer".

#### `origin`

- Type: URI
- Description: A URI reference to the original source of this Endpoint. This
  can be used to locate the true authority owner of the Endpoint in cases of
  distributed Endpoint Registries. If this property is absent its default value
  is the value of the `self` property and in those cases its presence in the
  serialization of the Endpoint is OPTIONAL.
- Constraints:
  - OPTIONAL if this Endpoint Registry is the authority owner
  - REQUIRED if this Endpoint Registry is not the authority owner
  - if present, MUST be a non-empty URI
- Examples:
  - `https://example2.com/myregistry/endpoints/9876`

#### `deprecated`

- Type: Object containing the following properties:
  - effective<br>
    An OPTIONAL property indicating the time when the Endpoint entered, or will
    enter, a deprecated state. The date MAY be in the past or future. If this
    property is not present the Endpoint is already in a deprecated state.
    If present, this MUST be an [RFC3339][rfc3339] timestamp.

  - removal<br>
    An OPTIONAL property indicating the time when the Endpoint MAY be removed.
    The Endpoint MUST NOT be removed before this time. If this property is not
    present then client can not make any assumption as to when the Endpoint
    might be removed. Note: as with most properties, this property is mutable.
    If present, this MUST be an [RFC3339][rfc3339] timestamp and MUST NOT be
    sooner than the `effective` time if present.

  - alternative<br>
    An OPTIONAL property specifying the URL to an alternative Endpoint the
    client can consider as a replacement for this Endpoint. There is no
    guarantee that the referenced Endpoint is an exact replacement, rather the
    client is expected to investigate the Endpoint to determine if it is
    appropriate.

  - docs<br>
    An OPTIONAL property specifying the URL to additional information about
    the deprecation of the Endpoint. This specification does not mandate any
    particular format or information, however some possibilities include:
    reasons for the deprecation or additional information about likely
    alternative Endpoints. The URL MUST support an HTTP GET request.

- Description: This specification makes no statement as to whether any
  existing secondary resources (such as subscriptions) will still be valid and
  usable after the Endpoint is removed. However, it is expected that new
  requests to create a secondary resource will likely be rejected.

  Note that an implementation is not mandated to use this attribute in
  advance of removing an Endpoint, but is it RECOMMENDED that they do so.
- Constraints:
  - OPTIONAL
- Examples:
  - `"deprecated": {}`
  - ```
    "deprecated": {
      "removal": "2030-12-19T00:00:00-00:00",
      "alternative": "https://example.com/endpoints/123"
    }
    ```

#### `channel`

- Type: String
- Description: A string that can be used to correlate Endpoints. Any Endpoints
  within an instance of an Endpoint Registry that share the same non-empty
  `channel` value MUST have some relationship. This specification does not
  define that relationship or the specific values used in this property.
  However, it is expected that the `usage` value in combination with this
  `channel` property will provide some information to help determine the
  relationship.

  For instance, a message broker queue "queue1" might be represented with a
  `producer` endpoint and a `consumer` endpoint, both with the same `channel`
  attribute value of "queue1".

  An event processing pipeline might have a sequence of stages, each with a
  `producer` endpoint and a `consumer` endpoint, all with the same `channel`
  attribute value of "pipeline1", or some further qualification like
  "pipeline1-stage1", etc.

  When this property has no value it MUST either be serialized as an empty
  string or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, MUST be a string
- Examples:
  - `queue1`

##### `definitions` (Endpoint)

Endpoints are supersets of
[message definition groups](#message-definition-groups) and MAY contain
inlined definitions. See [Message Definitions](#message-definitions).

Example:

``` JSON
{
  "protocol": "HTTP/1.1",
  "options": {
    "method": "POST"
    },
  "definitionsUrl": "..."
  "definitionsCount": 1,
  "definitions": {
    "myevent": {
      "format": "CloudEvents/1.0",
      "metadata": {
        "attributes": {
          "type": {
            "value": "myevent"
          }
}}}}}
```

##### `definitionGroups` (Endpoint)

The `definitionGroups` attribute is an array of URI-references to message
definition groups. The `definitionGroups` attribute is used to reference
message definition groups that are not inlined in the endpoint definition.

Example:

``` JSON
{
  "protocol": "HTTP/1.1",
  "options": {
    "method": "POST"
    },
  "definitionGroups": [
    "https://example.com/registry/definitiongroups/mygroup"
  ]
}
```

##### `config`

- Type: Map
- Description: Configuration details of the endpoint. An endpoint
  MAY be defined without detail configuration. In this case, the endpoint is
  considered to be "abstract".
  > Note: Authentication and authorization details are intentionally **not**
  > included in the endpoint metadata. The supported authentication and
  > authorization mechanisms are either part of the protocol, negotiated at
  > runtime (e.g. SASL), made available through the specific endpoint's
  > documentation, or separate metadata specific to security policies.
- Constraints:
  - OPTIONAL

##### `config.protocol`

- Type: String
- Description: The transport or application protocol used by the endpoint. This
  specification defines a set of common protocol names that MUST be used for
  respective protocol endpoints, but implementations MAY define and use
  additional protocol names.

  Predefined protocols are referred to by name and version as
  `{NAME}/{VERSION}`. If the version is not specified, the default version of
  the protocol is assumed. The version number format is determined by the
  protocol specification's usage of versions.

  The predefined protocol names are:
  - "HTTP/1.1", "HTTP/2", "HTTP/3" - Use the *lowest* HTTP version
    that the endpoints supports; that is commonly "HTTP/1.1". The default
    version is "HTTP/1.1" and MAY be shortened to "HTTP".
  - "AMQP/1.0" - Use the [AMQP 1.0][AMQP 1.0] protocol. MAY be shortened to
    "AMQP". AMQP draft versions before 1.0 (e.g. 0.9) are *not* AMQP.
  - "MQTT/3.1.1", "MQTT/5.0" - Use the MQTT [3.1.1][MQTT 3.1.1] or [5.0][MQTT
    5.0] protocol. The shorthand "MQTT" maps to "MQTT/5.0".
  - "NATS/1.0.0" - Use the [NATS][NATS] protocol. MAY be shortened to "NATS",
  - which assumes usage of the latest NATS clients.
  - "KAFKA/3.5" - Use the [Apache Kafka][Apache Kafka] protocol. MAY be
    shortened to "KAFKA", which assumes usage of the latest Apache Kafka
    clients.

  An example for an extension protocol identifier might be "BunnyMQ/0.9.1".

- Constraints:
  - REQUIRED
  - MUST be a non-empty string.

##### `config.endpoints`

- Type: Array of URI
- Description: The network addresses that are for communication with the
  endpoint. The endpoints are ordered by preference, with the first endpoint
  being the preferred endpoint. Some protocol implementations might not support
  multiple endpoints, in which case all but the first endpoint might be ignored.
  Whether the URI just identifies a network host or links directly to a resource
  managed by the network host is protocol specific.
- Constraints:
  - OPTIONAL
  - Each entry MUST be a valid, absolute URI (URL)
- Examples:
  - `["tcp://example.com", "wss://example.com"]`
  - `["https://example.com"]`

##### `config.options`

- Type: Map
- Description: Additional configuration options for the endpoint. The
  configuration options are protocol specific and described in the
  [protocol options](#protocol-options) section below.
- Constraints:
  - OPTIONAL
  - When present, MUST be a map of non-empty strings to non-empty strings.
  - If `config.protocol` is a well-known protocol, the options MUST be
    compliant with the [protocol's options](#protocol-options).

##### `config.strict`

- Type: Boolean
- Description: If `true`, the endpoint metadata represents a public, live
  endpoint that is available for communication and a strict validator MAY test
  the liveness of the endpoint.
- Constraints:
  - OPTIONAL.
  - Default value is `false`.

##### Protocol Options

The following protocol options (`config.options`) are defined for the respective
protocols. All of these are OPTIONAL.

###### HTTP options

The [endpoint URIs](#configendpoints) for "HTTP" endpoints MUST be valid HTTP
URIs using the "http" or "https" scheme.

The following options are defined for HTTP:

- `method`: The HTTP method to use for the endpoint. The default value is
  `POST`. The value MUST be a valid HTTP method name.
- `headers`: An array of HTTP headers to use for the endpoint. HTTP allows for
  duplicate headers. The objects in the array have the following attributes:
  - `name`: The name of the HTTP header. The value MUST be a non-empty string.
  - `value`: The value of the HTTP header. The value MUST be a non-empty string.
- `query`: A map of HTTP query parameters to use for the endpoint. The value
  MUST be a map of non-empty strings to non-empty strings.

The values of all `query` and `headers` MAY contain placeholders using the
[RFC6570][RFC6570] Level 1 URI Template syntax. When the same placeholder is
used in multiple properties, the value of the placeholder is assumed to be
identical.

Example:

```JSON
{
  "protocol": "HTTP/1.1",
  "options": {
    "method": "POST",
    "headers": [
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ],
    "query": {
      "operation": "send"
    }
  }
}
```

##### AMQP options

The [endpoint URIs](#configendpoints) for "AMQP" endpoints MUST be valid AMQP
URIs using the "amqp" or "amqps" scheme. If the path portion of the URI is
present, it MUST be a valid AMQP node name.

The following options are defined for AMQP endpoints.

- `node`: The name of the AMQP node (a queue or topic or some addressable
  entity) to use for the endpoint. If present, the value overrides the path
  portion of the Endpoint URI.
- `durable`: If `true`, the AMQP `durable` flag is set on transfers. The default
  value is `false`. This option only applies to `usage:producer` endpoints.
- `link-properties`: A map of AMQP link properties to use for the endpoint. The
  value MUST be a map of non-empty strings to non-empty strings.
- `connection-properties`: A map of AMQP connection properties to use for the
  endpoint. The value MUST be a map of non-empty strings to non-empty strings.
- `distribution-mode`: Either `move` or `copy`. The default value is `move`. The
  distribution mode is AMQP's way of expressing whether a receiver operates on
  copies of messages (it's a topic subscriber) or whether it moves messages from
  the queue (it's a queue consumer). This option only applies to
  `usage:consumer` endpoints.

The values of all `link-properties` and `connection-properties` MAY contain
placeholders using the [RFC6570][RFC6570] Level 1 URI Template syntax. When the
same placeholder is used in multiple properties, the value of the placeholder is
assumed to be identical.

Example:

```JSON
{
  "usage": "producer",
  "protocol": "AMQP/1.0",
  "options": {
    "node": "myqueue",
    "durable": true,
    "link-properties": {
      "my-link-property": "my-link-property-value"
    },
    "connection-properties": {
      "my-connection-property": "my-connection-property-value"
    },
    "distribution-mode": "move"
  }
}
```

##### MQTT options

The [endpoint URIs](#configendpoints) for "MQTT" endpoints MUST be valid MQTT
URIs using the (informal) "mqtt" or "mqtts" scheme. If the path portion of the
URI is present, it MUST be a valid MQTT topic name. The informal schemes "tcp"
(plain TCP/1883), "ssl" (TLS TCP/8883), and "wss" (Websockets/443) MAY also be
used, but MUST NOT have a path.

The following options are defined for MQTT endpoints.

- `topic`: The MQTT topic to use for the endpoint. If present, the value
  overrides the path portion of the Endpoint URI. The value MAY contain
  placeholders using the [RFC6570][RFC6570] Level 1 URI Template syntax
- `qos`: The MQTT Quality of Service (QoS) level to use for the endpoint. The
  value MUST be an integer between 0 and 2. The default value is 0. The value is
  overidden by the `qos` property of the
  [MQTT message format](#mqtt311-and-mqtt50).
- `retain`: If `true`, the MQTT `retain` flag is set on transfers. The default
  value is `false`. The value is overidden by the `retain` property of the [MQTT
  message format](#mqtt311-and-mqtt50). This option only applies to
  `usage:producer` endpoints.
- `clean-session`: If `true`, the MQTT `clean-session` flag is set on
  connections. The default value is `true`.
- `will-topic`: The MQTT `will-topic` to use for the endpoint. The value MUST be
  a non-empty string. The value MAY contain placeholders using the
  [RFC6570][RFC6570] Level 1 URI Template syntax
- `will-message`: This is URI and/or JSON Pointer that refers to the MQTT
  `will-message` to use for the endpoint. The value MUST be a non-empty string.
  It MUST point to a valid [´definition´](#message-definitions) that MUST either
  use the ["CloudEvents/1.0"](#cloudevents10) or ["MQTT/3.1.1." or
  "MQTT/5.0"](#mqtt311-and-mqtt50) [`format`](#format-message-format).

Example:

```JSON
{
  "usage": "producer",
  "protocol": "MQTT/5.0",
  "options": {
    "topic": "mytopic",
    "qos": 1,
    "retain": false,
    "clean-session": false,
    "will-topic": "mytopic",
    "will-message": "#/definitionGroup/mygroup/definitions/my-will-message"
  }
}
```

##### KAFKA options

The [endpoint URIs](#configendpoints) for "Kafka" endpoints MUST be valid Kafka
bootstrap server addresses. The scheme follows Kafka configuration usage, e.g.
`SSL://{host}:{port}` or `PLAINTEXT://{host}:{port}`.

The following options are defined for Kafka endpoints.

- `topic`: The Kafka topic to use for the endpoint. The value MUST be a
  non-empty string if present. The value MAY contain placeholders using the
  [RFC6570][RFC6570] Level 1 URI Template syntax
- `acks`: The Kafka `acks` setting to use for the endpoint. The value MUST be an
  integer between -1 and 1. The default value is 1. This option only applies to
  `usage:producer` endpoints.
- `key`: The fixed Kafka key to use for this endpoint. The value MUST be a
  non-empty string if present. This option only applies to `usage:producer`
  endpoints. The value MAY contain placeholders using the
  [RFC6570][RFC6570] Level 1 URI Template syntax
- `partition`: The fixed Kafka partition to use for this endpoint. The value
  MUST be an integer if present. This option only applies to `usage:producer`
  endpoints.
- `consumer-group`: The Kafka consumer group to use for this endpoint. The value
  MUST be a non-empty string if present. This option only applies to
  `usage:consumer` endpoints. The value MAY contain placeholders using the
  [RFC6570][RFC6570] Level 1 URI Template syntax

Example:

```JSON
{
  "usage": "producer",
  "protocol": "Kafka/2.0",
  "options": {
    "topic": "mytopic",
    "acks": 1,
    "key": "mykey",
  }
}
```

##### NATS options

The [endpoint URIs](#configendpoints) for "NATS" endpoints MUST be valid NATS
URIs. The scheme MUST be "nats" or "tls" or "ws" and the URI MUST include a port
number, e.g. `nats://{host}:{port}` or `tls://{host}:{port}`.

The following options are defined for NATS endpoints.

- `subject`: The NATS subject to use. The value MAY contain placeholders using
  the [RFC6570][RFC6570] Level 1 URI Template syntax

Example:

```JSON
{
  "usage": "producer",
  "protocol": "NATS/1.0.0",
  "options": {
    "subject": "mysubject"
  }
}
```

## References

### CloudEvents Registry Document Schema

See [CloudEvents Registry Document Schema](./schemas/xregistry_messaging_catalog.json).

[JSON Pointer]: https://www.rfc-editor.org/rfc/rfc6901
[CloudEvents Types]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type-system
[AMQP 1.0]: https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-overview-v1.0-os.html
[AMQP 1.0 Message Format]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#section-message-format
[AMQP 1.0 Message Properties]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-properties
[AMQP 1.0 Application Properties]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-application-properties
[AMQP 1.0 Message Annotations]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-message-annotations
[AMQP 1.0 Delivery Annotations]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-delivery-annotations
[AMQP 1.0 Message Header]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-header
[AMQP 1.0 Message Footer]: http://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-messaging-v1.0-os.html#type-footer
[MQTT 5.0]: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
[MQTT 3.1.1]: https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html
[CloudEvents]: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
[CloudEvents Subscriptions API]: https://github.com/cloudevents/spec/blob/main/subscriptions/spec.md
[NATS]: https://docs.nats.io/reference/reference-protocols/nats-protocol
[Apache Kafka]: https://kafka.apache.org/protocol
[Apache Kafka producer]: https://kafka.apache.org/31/javadoc/org/apache/kafka/clients/producer/ProducerRecord.html
[Apache Kafka consumer]: https://kafka.apache.org/31/javadoc/org/apache/kafka/clients/consumer/ConsumerRecord.html
[HTTP Message Format]: https://www.rfc-editor.org/rfc/rfc9110#section-6
[RFC6570]: https://www.rfc-editor.org/rfc/rfc6570
[rfc3339]: https://tools.ietf.org/html/rfc3339
