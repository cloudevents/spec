# Registry Service - Version 0.3-wip

## Abstract

A Registry Service exposes resources, and their metadata, for the purposes
of enabling discovery of those resources for either end-user consumption or
automation and tooling.

## Table of Contents

- [Overview](#overview)
- [Notations and Terminology](#notations-and-terminology)
  - [Notational Conventions](#notational-conventions)
  - [Terminology](#terminology)
- [Attributes and Extensions](#attributes-and-extensions)
- [Registry APIs](#registry-apis)
  - [Retrieving the Registry Model](#retrieving-the-registry-model)
  - [Retrieving the Registry](#retrieving-the-registry)
  - [Managing Groups](#managing-groups)
  - [Managing Resources](#managing-resources)
  - [Managing versions of a Resource](#managing-versions-of-a-resource)
- [Endpoint Registry](#endpoint-registry)
  - [Endpoints](#endpoints)
  - [DefinitionGroups](#definitiongroups)
  - [Definition](#definitions)
- [Schema Registry](#schema-registry)
  - [SchemaGroups](#schemagroups)
  - [Schemas](#schemas)

## Overview

A Registry Service is one that manages metadata about resources. At its core,
the management of an individual resource is simply a REST-based interface for
creating, modifying and deleting the resource. However, many resource models
share a common pattern of grouping resources by their "type" and can
optionally support versioning of the resources. This specification aims to
provide a common interaction pattern for these types of services with the goal
of providing an interoperable framework that will enable common tooling and
automation to be created.

This specification itself is meant to be a framework from which additional
specifications will be defined that expose model specific resources and
metadata.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

For clarity, when a feature is marked as "OPTIONAL" this means that it is
OPTIONAL for both the sender and receiver of a message message to support that
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

## Attributes and Extensions

The follow attributes are used by one or more entities defined by this
specification. They are defined here once rather than repeating them
throughout the specification.

List of attributes:
- `"id": "STRING"`
- `"name": "STRING"`
- `"description": "STRING"`
- `"tags": { "STRING": "STRING" * }`
- `"version": UINT`
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

### `id`
- Type: String   # SHOULD this be a URI-Reference?
- Description: A unique identifier of the entity.
- Constraints:
  - MUST be a non-empty string
  - MUST be unique within the scope of the Registry for Groups, or the owning
    Group for Resources
	QUESTION: SHOULD Resource IDs be unique across the entire Registry too?
- Examples:
  - A UUID

### `name`
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

### `description`
- Type: String
- Description: A human readable summary of the purpose of the entity.
- Constraints:
  - When this attributes has no value it MUST be serialized by either an empty
    string or by being excluded from the serialization of the owning entity
- Examples:
  - `A queue of the sensor generated messages`

### `tags`
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

### `version`
- Type: Unsigned Integer       # SHOULD this be a String?
- Description: A numeric value representing a specific instance of an entity.
  Note that versions of an entity can be modified without changing the
  `version` value. Often this value, or when a new version is created, is
  controlled by a user of the Registry. Also see `epoch`.
- Constraints:
  - MUST be an unsigned integer equal to or greater than zero
  - older versions of the entity MUST have numerically smaller `version` values
  - MUST be unique across all versions of the entity
- Examples:
  - `1`, `2`, `3`

### `epoch`
- Type: Unisgned Integer
- Description: A numeric value used to determine whether an entity has been
  modified. Each time the associated entity is updated, this value MUST be
  set to a new value that is greater than the current one.
  Note that unlike `version`, this attribute is most often managed by
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

### `self`
- Type: URL
- Description: A unique URL for the entity. The URL MUST be a combination of
  the base URL for the list of resources of this type of entity appended with
  the `id` of the entity.
- Constraints:
  - MUST be a non-empty URL
- Examples:
  - `https://example.com/registry/endpoints/123`

### `createdBy`
- Type: String
- Description: A reference to the user or component that was responsible for
  the creation of this entity. This specification makes no requirement on
  the semantics or syntax of this value.
- Constraints:
  - When this attributes has no value it MUST be serialized by either an empty
    string or by being excluded from the serialization of the owning entity
- Examples:
  - `John Smith`
  - `john.smith@example.com`

### `createdOn`
- Type: Timestamp
- Description: The date/time of when the entity was created.
- Constraints:
  - MUST be a [RFC3339](https://tools.ietf.org/html/rfc3339) timestamp
- Examples:
  - `2030-12-19T06:00:00Z"

### `modifiedBy`
- Type: String
- Description: A reference to the user or component that was responsible for
  the the latest update of this entity. This specification makes no requirement
  on the semantics or syntax of this value.
- Constraints:
  - When this attributes has no value it MUST be serialized by either an empty
    string or by being excluded from the serialization of the owning entity
- Examples:
  - `John Smith`
  - `john.smith@example.com`

### `modifiedOn`
- Type: Timestamp
- Description: The date/time of when the entity was last updated.
- Constraints:
  - MUST be a [RFC3339](https://tools.ietf.org/html/rfc3339) timestamp
- Examples:
  - `2030-12-19T06:00:00Z"

### `docs`
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


## Registry APIs

This specification defines the following API patterns:

```
/?model                             # Manage the registry model
/                                   # Show all Groups
/GROUP                              # Manage a Group Type
/GROUP/gID                          # Manage a Group
/GROUP/gID/RESOURCE                 # Manage a Resource Type
/GROUP/gID/RESOURCE/rID             # Manage the latest Resource version
/GROUP/gID/RESOURCE/rID?meta        # Metadata about the latest Resource version
/GROUP/gID/RESOURCE/rID/versions    # Show version strings for a Resource
/GROUP/gID/RESOURCE/rID/versions/VERSION         # Manage a Resource version
/GROUP/gID/RESOURCE/rID/versions/VERSION?meta    # Metadata about a Resource version
```

Where:
- `GROUP` is a grouping name (plural). E.g. `endpoints`
- `gID` is the unique identifier of a single Group
- `RESOURCE` is the type of resources (plural). E.g. `definitions`
- `rID` is the unique identifier of a single Resource
- `VERSION` is a version string referencing a versioned instead of a resource

While these APIs are shown to be at the root path of a Registry Service,
implementation MAY choose to prefix them as necessary. However, the same
prefix MUST be used consistently for all APIs in the same Registry Service.

The following sections define the APIs in more detail.

### Retrieving the Registry Model

This returns the metadata describing the model of the Registry Service.

The request MUST be of the form:
```
GET /?model
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "groups": [
    { "singular": "STRING",            # eg. "endpoint"
      "plural": "STRING",              # eg. "endpoints"
      "schema": "URI-Reference", ?     # Schema doc for the group

      "resources": [
        { "singluar": "STRING",        # eg. "definition"
          "plural": "STRING",          # eg. "definitions"
          "versions": INT ?            # Num old versions. Def=0, -1=unlimited
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

**Example:**

Request:
```
GET /?model
```
Response:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ TODO }
```


### Retrieving the Registry

This returns the Groups in the Registry along with metadata about the
Registry itself.

The request MUST be of the form:
```
GET /
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "name": "STRING", ?
  "description": "STRING", ?  # Description of Registry
  "specVersion": "STRING",    # Registry spec version
  "tags": { "STRING": "STRING" * }, ?
  "docs": "URL", ?

  # Repeat for each Group
  "GROUPsURL": "URL",         # eg. "endpointsURL" - repeated for each GROUP
  "GROUPsCount": INT          # eg. "endpointsCount"
}
```

**Example:**

Request:
```
GET /
```
Response:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "specVersion": "0.1",

  "endpointsURL": "https://example.com/endpoints",
  "endpointsCount": 42,

  "groupsURL": "https://example.com/groups",
  "groupsCount": 3
}
```

#### Retrieving all Registry Contents

This returns the Groups and all nested data in the Registry along with
metadata about the Registry itself. This is designed for cases where the
entire Registry's contents are to be represented as a single document.

The request MUST be of the form:
```
GET /?inline
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "name": "STRING", ?
  "description": "STRING", ?  # Description of Registry
  "specVersion": "STRING",    # Registry spec version
  "tags": { "STRING": "STRING" * }, ?
  "docs": "URL", ?

  "model": {
    "groups": [
      { "singular": "STRING",            # eg. "endpoint"
        "plural": "STRING",              # eg. "endpoints"
        "schema": "URI-Reference", ?     # Schema doc for the group

        "resources": [
          { "singluar": "STRING",        # eg. "definition"
            "plural": "STRING",          # eg. "definitions"
            "versions": INT ?            # Num old versions. Def=0, -1=unlimited
          } +
        ]
      } +
    ]
  }

  # Repeat for each Group
  "GROUPsURL": "URL",         # eg. "endpointsURL"
  "GROUPsCount": INT,         # eg. "endpointsCount"
  "GROUPs": {                 # eg. "endpoints"
    "ID": {                   # The Group ID
      "id": "STRING",
      "name": "STRING",
      "epoch": UINT,          # What other common fields?
                              # type? createdBy/On? modifiedBy/On? docs? tags?
                              # description? self?

      # Repeat for each RESOURCE in the Group
      "RESOURCEsURL": "URL",  # URL to retrieve all nested Resources
      "RESOURCEsCount": INT   # Total number resources
      "RESOURCEs": {          # eg. "definitions"
        "ID": {
          "id": "STRING",
          ... remaining RESOURCE ?meta and RESOURCE itself ...
        } *
      } ?                     # OPTIONAL if RESOURCEsCount is zero
    } *
  } ?                         # OPTIONAL if GROUPsCount is zero
}
```

Note: If the Registry can not return all expected data in one response then it
MUST generate an error. In those cases, the client will need to query the
individual Groups via the `/GROUPsURL` API so the Registry can leverage
pagination of the response.

TODO: define the error / add filtering / pagination

**Example:**

Request:
```
GET /?inline
```
Response:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ TODO }
```


### Managing Groups

#### Retrieving all Groups

This returns all entities that are in a Group.

The request MUST be of the form:
```
GET /GROUPs[?inline]
```

The OPTIONAL `inline` query parameter indicates the nested Resources are to
be included in the response.

A successful response MUST be of the form:
```
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
    "RESOURCEsURL": "URL",  # URL to retrieve all nested Resources
    "RESOURCEsCount": INT,  # Total number resources
    "RESOURCEs": {          # Only when ?inline is present
      "ID": {
        "id": "STRING",
        ... remaining RESOURCE ?meta and RESOURCE itself ...
      } *
    } ?                     # OPTIONAL if RESOURCEsCount is zero
  } *
}
```

Note: If the `inline` query parameter is present and the presence of the
`RESOURCES` map results in even a single Group being too large to return in
one response then an error MUST be generated. In those cases the client will
need to query the individual Resources via the `RESOURCEsURL` so the Registry
can leverage pagination of the response data.

**Example:**

Request:
```
GET /endpoints
```
Response:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Link: <http://example.com/endpoints&page=2>;rel=next;count=100

{
  "123": {
    "id": "123",
    "name": "A cool endpoint",
    "epoch": 1,

    "definitionsURL": "https://example.com/endpoints/123/definitions",
    "definitionsCount": 5
  },
  "124": {
    "id": "124",
    "name": "Redis Queue",
    "epoch": 3,

    "definitionsURL": "https://example.com/endpoints/124/definitions",
    "definitionsCount": 1
  }
}
```

TODO: add filtering and define error

#### Creating a Group

This will add a new Group to the Registry.

The request MUST be of the form:
```
POST /GROUPs

{
  "id": "STRING", ?       # If absent then it's server defined
  "name": "STRING",
}
```

A successful response MUST be of the form:
```
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Location: URL             # .../GROUPs/ID

{                         # MUST be full representation of new Group
  "id": "STRING",
  "name": "STRING",
  "epoch": UINT,

  # Repeat for each RESOURCE in the Group
  "RESOURCEsURL": "URL",  # URL to retrieve all nested Resources
  "RESOURCEsCount": INT   # Total number resources
}
```

**Example:**

Request:
```
POST /endpoints

{ TODO }
```
Response:
```
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Location: https://example.com/endpoints/ID

{ TODO }
```

#### Retrieving a Group

This will return a single Group.

The request MUST be of the form:
```
GET /GROUPs/ID[?inline]
```

The OPTIONAL `inline` query parameter indicates the nested Resources are to
be included in the response.

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",         # Group attributes
  "name": "STRING",
  "epoch": UINT,           # Server controlled

  # Repeat for each RESOURCE in the Group
  "RESOURCEsURL": "URL",  # URL to retrieve all nested Resources
  "RESOURCEsCount": INT,  # Total number resources
  "RESOURCEs": {          # Only when ?inline is present
    "ID": {
      "id": "STRING",
      ... remaining RESOURCE ?meta and RESOURCE itself ...
    } *
  } ?                     # OPTIONAL if RESOURCEsCount is zero
}
```

**Example:**

Request:
```
GET /endpoints/123
```
Response:
```
HTTP/1.1 ...
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ TODO }
```

#### Updating a Group

This will update the attributes of a Group.

The request MUST be of the form:
```
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
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "epoch": UINT,          # MUST be greater than previous value

  # Repeat for each RESOURCE in the Group
  "RESOURCEsURL": "URL",
  "RESOURCEsCount": INT
}
```

**Example:**

Request:
```
PUT /endpoints/123

{
  "id": "123",
  "name": "A cooler endpoint",
  "epoch": 1
}
```
Response:
```
HTTP/1.1 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "123",
  "name": "A cooler endpoint",
  "epoch": 2,

  "definitionsURL": "https://example.com/endpoints/123/definitions",
  "definitionsCount": 5,
}
```

#### Deleting Groups

To delete a single Group the following API can be used.

The request MUST be of the form:
```
DELETE /GROUPs/ID[?epoch=EPOCH]
```

If `epoch` is present then it MUST match the current value.

A successful response MUST be of the form:
```
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
```
DELETE /GROUPs

[
  {
    "id": "STRING",
    "epoch": UINT ?     # If present it MUST match current value
  } *
]
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ "ID": { ... } * } ?   # RECOMMENDED
```

If any of the individual deletes fails then the entire request MUST fail
and none of the Groups are deleted.

A `DELETE /GROUPs` without a body MUST delete all Groups.


### Managing Resources

#### Retrieving all Resources

This will retrieve the Resources from a Group.

The request MUST be of the form:
```
GET /GROUPs/ID/RESOURCEs[?inline]
```

The OPTIONAL `inline` query parameter indicates the nested Resources are to
be included in the response.

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Link: <URL>;rel=next;count=INT  # If pagination is needed

{
  "ID": {
    "id": "STRING",
    "name": "STRING",
    "type": "STRING", ?
    "version": INT,
    "epoch": UINT,
    "self": "URL",                   # URL to specific version

    "RESOURCEURI": "URI", ?          # If not locally stored
    "RESOURCE": {} ?,                # If ?inline present & JSON
    "RESOURCEBase64": "STRING" ?     # If ?inline present & ~JSON
  } *
}
```

**Example:**

Request:
```
GET /endpoints/123/definitions
```
Response:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Link: <http://example.com/endpoints/123/definitions&page=2>;rel=next;count=100

{
  "456": {
    "id": "456",
    "name": "Blob Created",
    "type": "CloudEvents/1.0",
    "version": 3,
    "epoch": 1,
    "self": "https://example.com/endpoints/123/definitions/456/version/3"
  }
}
```

#### Creating Resources

This will create a new Resources in a particular Group.

The request MUST be of the form:
```
POST /GROUPs/ID/RESOURCEs
Registry-name: STRING ?          # If absent, default to the ID?
Registry-type: STRING ?
Registry-RESOURCEURI: URI ?      # If present body MUST be empty

{ ...Resource entity... } ?
```

A successful response MUST be of the form:
```
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING            # URL to the specific version
Registry-RESOURCEURI: URI ?      # If present body MUST be empty
Location: URL                    # Points to "latest" URL
Content-Location: URL            # Same as Registry-self value

{ ...Resource entity... } ?
```

**Example:**

Request:
```
TODO
```

#### Retrieving a Resource

This will retrieve the latest version of a Resource. This can be considered an
alias for `/GROUPs/ID/RESOURCEID/versions/VERSION` where `VERSION` is the
latest version value.

The request MUST be of the form:
```
GET /GROUPs/ID/RESOURCEs/ID
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK  or 307 Tempary Redirect    # 307 if RESOURCEURI is present
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING            # URL to the specific version
Registry-RESOURCEURI: URI ?      # If present body MUST be empty
Content-Location: URL            # Same as Registry-self value
Location: URL                    # If 307. Same a Registry-RESOURCEURI

{ ...Resource entity... } ?
```

**Example:**

Request:
```
TODO
```

#### Retrieving a Resource's Metadata

This will retrieve the metadata for the latest version of a Resource. This can
 be considered an alias for `/GROUPs/ID/RESOURCEID/versions/VERSION?meta` where
`VERSION` is the latest version value.

The request MUST be of the form:
```
GET /GROUPs/ID/RESOURCEs/ID?meta
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "type": "STRING", ?
  "version": INT,
  "epoch": UINT,
  "self": "URL",
  "RESOURCEURI": "URI" ?
}
```

**Example:**

Request:
```
TODO
```

#### Updating a Resource

This will update the latest version of a Resource. Missing Registry HTTP
headers MUST NOT be interpreted as deleting the attribute. However, a Registry
HTTP headers with an empty string for its value MUST be interpreted as a
request to delete the attribute.

The request MUST be of the form:
```
PUT /GROUPs/ID/RESOURCEs/ID[?epoch=EPOCH]
Registry-id: STRING ?            # If present it MUST match URL
Registry-name: STRING ?
Registry-type: STRING ?
Registry-version: STRING ?       # If present it MUST match current value
Registry-epoch: UINT ?           # If present it MUST match current value & URL
Registry-self: STRING ?          # If present it MUST be ignored?
Registry-RESOURCEURI: URI ?      # If present body MUST be empty

{ ...Resource entity... } ?      # If empty then content is erased
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT             # MUST be incremented
Registry-self: STRING
Registry-RESOURCEURI: URI ?
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
```
TODO
```
Response:
```
TODO
```

TODO: make a note that empty string and attribute missing are the same thing.
Which error is to be returned?

#### Updating a Resource's metadata

This will update the metadata of the latest version of a Resource without
creating a new version.

The request MUST be of the form:
```
PUT /GROUPs/ID/RESOURCEs/ID?meta[&epoch=EPOCH]

{
  "id": "STRING",
  "name": "STRING",
  "type": "STRING", ?
  "version": INT, ?            # If present it MUST match current value
  "epoch": UINT, ?             # If present it MUST match current value & URL
  "self": "URL", ?             # If present it MUST be ignored
  "RESOURCEURI": "URI" ?
}
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "type": "STRING", ?
  "version": INT,
  "epoch": UINT,               # MUST be incremented
  "self": "URL",
  "RESOURCEURI": "URI" ?
}
```

**Example:**

Request:
```
TODO
```
Response:
```
TODO
```

#### Deleting Resources

To delete a single Resource the following API can be used.

The request MUST be of the form:
```
DELETE /GROUPs/ID/RESOURCEs/ID[?epoch=EPOCH]
```

If `epoch` is present then it MUST match the current value.

A successful response MUST be of the form:
```
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING
Registry-RESOURCEURI: URI ?
Content-Location: URL              # Does this make sense if it's been deleted?

{ ...Resource entity... } ?
```

**Example:**

Request:
```
TODO
```

To delete multiple Resources the following API can be used.

The request MUST be of the form:
```
DELETE /GROUPs/ID/RESOURCEs

[
  {
    "id": "STRING",
    "epoch": UINT ?     # If present it MUST match current value
  } *
]
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ "ID": { ... } * } ?   # RECOMMENDED
```

If any of the individual deletes fails then the entire request MUST fail
and none of the Resources are deleted.

A `DELETE /GROUPs/ID/RESOURCEs` without a body MUST delete all Resources in the
Group.


### Managing versions of a Resource

#### Retrieving all versions of a Resource

This will retrieve all versions of a Resource.

The request MUST be of the form:
```
GET /GROUPs/ID/RESOURCEs/ID/versions[?inline]
```

The OPTIONAL `inline` query parameter indicates the nested Resources are to
be included in the response.

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Link: <URL>;rel=next;count=INT  # If pagination is needed

{
  VERSION: {
    "id": "STRING",
    "name": "STRING",
    "type": "STRING", ?
    "version": INT,
    "epoch": UINT,
    "self": "URL",
    "RESOURCEURI": "URI", ?          # If not locally stored
    "RESOURCE": {} ?,                # If ?inline present & JSON
    "RESOURCEBase64": "STRING" ?     # If ?inline present & ~JSON
  } *
}
```

**Example:**

Request:
```
TODO
```

#### Creating a new version of a Resource

This will create a new version of a Resource. Any metadata not present will be
inherited from latest version. To delete any metadata include its HTTP Header
with an empty value.

The request MUST be of the form:
```
POST /GROUPs/ID/RESOURCEs/ID[?epoch=EPOCH]
Registry-id: STRING ?            # If present it MUST match URL
Registry-name: STRING ?
Registry-type: STRING ?
Registry-version: STRING ?       # MUST NOT be present
Registry-epoch: UINT ?           # If present it MUST match current value & URL
Registry-self: STRING ?          # If present it MUST be ignored?
Registry-RESOURCEURI: URI ?      # If present body MUST be empty

{ ...Resource entity... } ?      # If empty then content is erased
```

A successful response MUST be of the form:
```
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING
Registry-RESOURCEURI: URI ?
Content-Location: URL            # Same as self
Location: .../GROUPs/ID/RESOURCEs/ID   # or self?

{ ...Resource entity... } ?
```

**Example:**

Request:
```
TODO
```
Response:
```
TODO
```

#### Retrieving a version of a Resource

This will retrieve a partiuclar version of a Resource.

The request MUST be of the form:
```
GET /GROUPs/ID/RESOURCEs/ID/versions/VERSION
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK  or 307 Tempary Redirect    # 307 if RESOURCEURI is present
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING            # URL to the specific version
Registry-RESOURCEURI: URI ?      # If present body MUST be empty
Content-Location: URL            # Same as Registry-self value
Location: URL                    # If 307. Same a Registry-RESOURCEURI

{ ...Resource entity... } ?
```

**Example:**

Request:
```
TODO
```

#### Retrieving a version of a Resource's metadata

This will retrieve the metadata for a particular version of a Resource.

The request MUST be of the form:
```
GET /GROUPs/ID/RESOURCEs/ID/versions/VERSION?meta
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "type": "STRING", ?
  "version": INT,
  "epoch": UINT,
  "self": "URL",
  "RESOURCEURI": "URI" ?
}
```

**Example:**

Request:
```
TODO
```

#### Updating a version of a Resource

This will update a particular version of a Resource. Missing Registry HTTP
headers MUST NOT be interpreted as deleting the attribute. However, a Registry
HTTP headers with an empty string for its value MUST be interpreted as a
request to delete the attribute.

The request MUST be of the form:
```
PUT /GROUPs/ID/RESOURCEs/ID/versions/VERSION[?epoch=EPOCH]
Registry-id: STRING ?            # If present it MUST match URL
Registry-name: STRING ?
Registry-type: STRING ?
Registry-version: STRING ?       # If present it MUST match current value & URL
Registry-epoch: UINT ?           # If present it MUST match current value & URL
Registry-self: STRING ?          # If present it MUST be ignored?
Registry-RESOURCEURI: URI ?      # If present body MUST be empty

{ ...Resource entity... } ?      # If empty then content is erased
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT             # MUST be incremented
Registry-self: STRING
Registry-RESOURCEURI: URI ?
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
```
TODO
```

#### Updating a version of a Resource's metadata

This will update the metadata of a particular version of a Resource without
creating a new version.

The request MUST be of the form:
```
PUT /GROUPs/ID/RESOURCEs/ID/versions/VERSION?meta[&epoch=EPOCH]

{
  "id": "STRING",
  "name": "STRING",
  "type": "STRING", ?
  "version": INT, ?            # If present it MUST match current value
  "epoch": UINT, ?             # If present it MUST match current value & URL
  "self": "URL", ?             # If present it MUST be ignored
  "RESOURCEURI": "URI" ?
}
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
  "id": "STRING",
  "name": "STRING",
  "type": "STRING", ?
  "version": INT,
  "epoch": UINT,               # MUST be incremented
  "self": "URL",
  "RESOURCEURI": "URI" ?
}
```

**Example:**

Request:
```
TODO
```
Response:
```
TODO
```

#### Deleting versions of a Resource

To delete a single version of a Resource the following API can be used.

The request MUST be of the form:
```
DELETE /GROUPs/ID/RESOURCEs/ID/versions/VERSION[?epoch=EPOCH]
```

If `epoch` is present then it MUST match the current value.

A successful response MUST be of the form:
```
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn
Registry-id: STRING
Registry-name: STRING
Registry-type: STRING ?
Registry-version: STRING
Registry-epoch: UINT
Registry-self: STRING
Registry-RESOURCEURI: URI ?
Content-Location: URL              # Does this make sense if it's been deleted?

{ ...Resource entity... } ?
```

**Example:**

Request:
```
TODO
```
Response:
```
TODO
```

To delete multiple versions of a Resource the following API can be used.

The request MUST be of the form:
```
DELETE /GROUPs/ID/RESOURCEs/ID/versions

[
  {
    "id": "STRING",
    "version": INT,
    "epoch": UINT ?     # If present it MUST match current value
  } *
]
```

A successful response MUST be of the form:
```
HTTP/1.1 200 OK                  # 202 or 204 are ok
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{ "ID": { ... } * } ?   # RECOMMENDED
```

If any of the individual deletes fails then the entire request MUST fail
and none of the Resources are deleted.

If the latest version is deleted then the remaining version with the largest
`version` value MUST become the latest.

An attempt to delete all versions MUST generate an error.

A `DELETE /GROUPs/ID/RESOURCEs/ID/versions` without a body MUST delete all
versions (except the latest) of the Resource.


## Endpoint Registry

This section defines the custom attributes that an Endpoint Registry supports.

The Registry model defined by an Endpoint Registry is:
```
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
          "versions": 0,
          "mutable": true
        }
      ]
    },
    {
      "singular": "definitiongroup",
      "plural": "definitiongroups",
      "schema": "TBD",
      "resources": [
        {
          "singular": "definition",
          "plural": "definitions",
          "versions": 0,
          "mutable": true
        }
      ]
    }
  ]
}
```


### Endpoints

A Group (GROUP) name of `endpoints` is defined with the following
extension attributes:

```
"self": "URI",
"origin": "URI", ?
"deprecated": { ... }, ?
"channel", "STRING", ?
"authscope": "URI", ?

"usage": "subscriber|consumer|producer",
"config": {
  "protocol": "STRING",
  "endpoints": "URL" | [ "URL", ... ],
  "options": { ... }, ?
  "strict": true|false ?
}, ?

"definitionGroups": [ GROUP-URI-Reference, ... ], ?
```


### DefinitionGroups

A Group (GROUP) name of `definitiongroups` is defined with the following
extension attributes:

```
  "self": "URI",
  "origin": "URI", ?
  "definitionGroups": [ GROUP-URI-Reference, ... ], ?
}
```


### Definitions

A Resource (RESOURCE) name of `definitions` and a Resource Entity are
defined.

The Resource entity is defined as:

```
{
  "id": "STRING",                        # URI-Reference?
  "name": "STRING",
  "description": "STRING", ?
  "tags": { "STRING": "STRING" * }, ?
  "version": "STRING", ?

  "createdBy": "STRING", ?
  "createdOn": "TIME", ?
  "modifiedBy": "STRING", ?
  "modifiedOn": "TIME", ?
  "docs": "URL", ?                           # end of common attributes

  "self": "URI",
  "origin": "URI", ?
  "ownergroup": "GROUP-URI-Reference",
  "format": "STRING", ?                      # type ?
  "metadata": {
    "attributes": {
      "ATTRIBUTE_NAME": {
        "required": true|false,
        "description": "STRING", ?
        "value": JSON_OBJECT,
        "type": "string|object|...", ?
        "specurl": "URL" ?
      }
    } *
  }, ?
  "schema": { ... }, ?
  "schemaurl": "URL" ?
}
```

## Schema Registry

This section defines the custom attributes that a Schema Registry supports.

The Registry model defined by a Schema Registry is:
```
{
  "groups": [
    {
      "singular": "schemagroup",
      "plural": "schemagroups",
      "schema": "TBD",
      "resources": [
        {
          "singular": "schema",
          "plural": "schemas",
          "versions": -1,
        }
      ]
    }
  ]
}
```


### SchemaGroups

A Group (GROUP) name of `schemagroups` is defined with the following extension
attributes:

```
None
```


### Schemas

A Resource (RESOURCE) name of `schemas` is defined with the following `meta`
extension attributes:

```
"authority": "URI" ?
```
