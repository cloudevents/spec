# Registry Service - Version 0.3-wip

## Registry Service

This specification defines the following APIs:

```
/?model                             # Registry model
/                                   # Shows all groups & resources (can filter)
/GROUP                              # Manage a Group Type
/GROUP/gID                          # Manage a Group
/GROUP/gID/RESOURCE                 # Manage a Resource Type
/GROUP/gID/RESOURCE/rID             # Manage a Resource (latest version)
/GROUP/gID/RESOURCE/rID?meta        # Metadata about latest Resource version
/GROUP/gID/RESOURCE/rID/versions    # Show version strings for a resource
/GROUP/gID/RESOURCE/rID/versions/VERSION         # A certain version
/GROUP/gID/RESOURCE/rID/versions/VERSION?meta    # Metadata about a certain version
```

Where:
- `GROUP` is a grouping name (plural). E.g. `endpoints`
- `gID` is the unique identifier of a single Group
- `RESOURCE` is the type of resources (plural). E.g. `definitions`
- `rID` is the unique identifier of a single Resource
- `VERSION` is a version string

The follow sections define the model and APIs of a Registry service.


### Common Properties

The following properties are defined for Groups and Resource metadata:

```
"id": "STRING",                        # URI-Reference?
"name": "STRING",
"description": "STRING", ?
"tags": { "STRING": "STRING" * }, ?
"version": INT, ?
"epoch": INT,
"self": "URL",

"createdBy": "STRING", ?
"createdOn": "DATETIME", ?
"modifiedBy": "STRING", ?
"modifiedOn": "DATETIME", ?
"docs": "URL", ?
```

TODO talk about extensions

Note: Implementations MAY choose to mandate that `id` and `name` be the same
value.


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
      ]
    } +
  ]
}
```

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
      "epoch": INT,           # What other common fields?
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
    "id": "STRING",         # Group properties
    "name": "STRING",
    "epoch": INT,           # Server controlled

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
  "epoch": INT,

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
  "id": "STRING",         # Group properties
  "name": "STRING",
  "epoch": INT,           # Server controlled

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

This will update the properties of a Group.

The request MUST be of the form:
```
PUT /GROUPs/ID[?epoch=EPOCH]

{
  # Missing properties are deleted from Group
  "id": "STRING",            # MUST match URL if present
  "name": "STRING",
  "epoch": INT ?             # OPTIONAL - MUST be current value if present

  # Presence of the RESOURCEs properties are OPTIONAL and MUST be ignored
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
  "epoch": INT,           # MUST be greater than previous value

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
  "epoch": INT,
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
    "epoch": INT ?      # If present it MUST match current value
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
    "epoch": INT,
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
Registry-epoch: STRING
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
Registry-epoch: STRING
Registry-self: STRING            # URL to the specific version
Registry-RESOURCEURI: URI ?      # If present body MUST be empty
Content-Location: URL            # Same as Registry-self value
Location: URL                    # If 307. Same a Regsitry-RESOURCEURI

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
  "epoch": INT,
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
headers MUST NOT be interpretted as deleting the property. However, a Regsitry
HTTP headers with an empty string for its value MUST be interpretted as a
request to delete the property.

The request MUST be of the form:
```
PUT /GROUPs/ID/RESOURCEs/ID[?epoch=EPOCH]
Registry-id: STRING ?            # If present it MUST match URL
Registry-name: STRING ?
Registry-type: STRING ?
Registry-version: STRING ?       # If present it MUST match current value
Registry-epoch: STRING ?         # If present it MUST match current value & URL
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
Registry-epoch: STRING           # MUST be incremented
Registry-self: STRING
Registry-RESOURCEURI: URI ?
Content-Location: URL

{ ...Resource entity... } ?
```

Note: if some of the Registry properties are shared with the Resource itself
then those values MUST appear in both the Registry HTTP headers as well as in
the Resource itself when retrieving the Resource. However, in this "update"
case, if the property only appears in the HTTP body and the corresponding
Registry HTTP header is missing then the Registry property MUST be updated to
match the Resource's property. If both are present on the request and do not
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

TODO: make a note that empty string and property missing are the same thing.
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
  "epoch": INT, ?              # If present it MUST match current value & URL
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
  "epoch": INT,                # MUST be incremented
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
Registry-epoch: STRING
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
    "epoch": INT ?      # If present it MUST match current value
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
    "epoch": INT,
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
Registry-epoch: STRING ?         # If present it MUST match current value & URL
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
Registry-epoch: STRING
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
Registry-epoch: STRING
Registry-self: STRING            # URL to the specific version
Registry-RESOURCEURI: URI ?      # If present body MUST be empty
Content-Location: URL            # Same as Registry-self value
Location: URL                    # If 307. Same a Regsitry-RESOURCEURI

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
  "epoch": INT,
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
headers MUST NOT be interpretted as deleting the property. However, a Regsitry
HTTP headers with an empty string for its value MUST be interpretted as a
request to delete the property.

The request MUST be of the form:
```
PUT /GROUPs/ID/RESOURCEs/ID/versions/VERSION[?epoch=EPOCH]
Registry-id: STRING ?            # If present it MUST match URL
Registry-name: STRING ?
Registry-type: STRING ?
Registry-version: STRING ?       # If present it MUST match current value & URL
Registry-epoch: STRING ?         # If present it MUST match current value & URL
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
Registry-epoch: STRING           # MUST be incremented
Registry-self: STRING
Registry-RESOURCEURI: URI ?
Content-Location: URL

{ ...Resource entity... } ?
```

Note: if some of the Registry properties are shared with the Resource itself
then those values MUST appear in both the Registry HTTP headers as well as in
the Resource itself when retrieving the Resource. However, in this "update"
case, if the property only appears in the HTTP body and the corresponding
Registry HTTP header is missing then the Registry property MUST be updated to
match the Resource's property. If both are present on the request and do not
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
  "epoch": INT, ?              # If present it MUST match current value & URL
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
  "epoch": INT,                # MUST be incremented
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
Registry-epoch: STRING
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
    "epoch": INT ?      # If present it MUST match current value
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

This section defines the custom properties that an Endpoint Registry supports.

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
      "singular": "group",
      "plural": "groups",
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


### Group: endpoints

A Group (GROUP) name of `endpoints` is defined with the following
extension properties:

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

"groups": [ GROUP-URI-Reference, ... ], ?
```


### Group: groups

A Group (GROUP) name of `groups` is defined with the following
extension properties:

```
  "self": "URI",
  "origin": "URI", ?
  "groups": [ GROUP-URI-Reference, ... ], ?
}
```


### Resource: definition

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
  "createdOn": "DATETIME", ?
  "modifiedBy": "STRING", ?
  "modifiedOn": "DATETIME", ?
  "docs": "URL", ?                           # end of common properties

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

This section defines the custom properties that a Schema Registry supports.

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


### Group: schemagroup

A Group (GROUP) name of `schemagroups` is defined with the following extension
properties:

```
None
```


### Resource: schemas

A Resource (RESOURCE) name of `schemas` is defined with the following `meta`
extension properties:

```
"authority": "URI" ?
```
