# Discovery Service - Version 0.2-wip

## Abstract

The Discovery Service specification allows for the discovery of messaging
Endpoints and their related metadata such as Message Definitions and the
mechanisms by which interactions with those Endpoints can be established.

## Table of Contents

- [Overview](#overview)
- [Notations and Terminology](#notations-and-terminology)
- [Resource Model](#resource-model)
  - [Endpoint](#endpoint)
  - [Definition](#definition)
  - [Group](#group)
- [Serializations](#serializations)
- [Usage Values](#usage-values)
- [Message Formats](#message-formats)
- [API Specification](#api-specification)
- [Privacy & Security](#privacy-and-security)

## Overview

Message Endpoints provide a location from which Message producers and consumers
can share Messages. Endpoints could act as either consumers or producers
of Messages, and the mechanisms by which those Messages are transferred
might vary.

This specification defines a set of APIs, and related documents, that allow
for the discovery of these Endpoints and their related metadata. This
information can then be used to perform actions such as:
- Subscribing for Messages
- Pushing or Pulling of Messages with the Endpoint
- Generating of Message validation code based on the schema associated with
  a Message Definition

While the specification is written in term of "messaging", it applies equally
to "eventing" since it can be considered as subset of messaging.

** we need more verbage here **

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

In the pseudo JSON format snippets `?` means the preceding property is
OPTIONAL, `*` means the preceding property MAY appear zero or more times, and
`+` means the preceding property MUST appear at least once.

### Terminology

This specification defines the following terms:

#### Discovery Service

A compliant implementation of this specification that advertises the set of
Endpoints, Groups, Definitions and other metadata to aid in the programmic
interactions with the Endpoints.

### Conventions

#### References

Discuss uri vs self properties....


## Resource Model

This section defines the resource model of a Discovery Service.

### Endpoint

An Endpoint is ...

The following pseudo JSON shows the basic defintion of an Endpoint:
```
{
    "id": "URI-reference",
    "name": "STRING",
    "self": "URI",
    "epoch": UINT,
    "description": "STRING", ?
    "tags": { "STRING": "STRING", ... } ?
    "docs": "URL", ?
    "deprecated": { ... }, ?
    "channel", "STRING", ?
    "authscope": "URI", ?

    "usage": "subscriber|consumer|producer",
    "config": {
        "protocol": "STRING",
        "endpoints": "URL" | [ "URL", ... ],
        "options": { ... }, ?
        "strict": true|false, ?
    }, ?

    "groups": [ GROUP, ... ], ?
    "definitions": [ DEFINITION, ... ] ?
}

```

The following Endpoint properties are defined:

#### id

- Type: String
- Description: A unique identifier for this Endpoint.
- Constraints:
  - REQUIRED
  - MUST be a non-empty String
  - MUST conform with
    [RFC3986/3.3](https://datatracker.ietf.org/doc/html/rfc3986#section-3.3)
    `segment-nz-nc` syntax
  - MUST be unique across all Endpoints within the authorization scope
    defined by the `authscope` property. If `authscope` has no value then
    the `id` MUST be unique within the current Discovery Service.
- Examples:
  - A UUID
  - `1234`

#### name

- Type: String
- Description: The name of the Endpoint.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
- Examples:
  - My Queue

#### self

- Type: URI
- Description: A unique URI for this Endpoint.  The URI MUST be a combination
  of the base URI of the list of Endpoints for the current Discovery Service
  concatenated with the `id` of this Endpoint.
- Constraints:
  - REQUIRED
  - MUST be a non-empty URI

- Examples:
  - `https://example.com/discovery/endpoints/1234`

#### epoch

- Type: Unsigned Integer
- Description: A number representing the version number of this Endpoint. Each
  time this Endpoint is modified this property MUST be updated with a new value
  that is greater than the current one.
- Constraints:
  - REQUIRED
  - MUST be an unsigned integer
- Examples:
  - `0`
  - `1001`

#### description

- Type: String
- Description: A summary of the purpose of the Endpoint.
- Constraints:
  - OPTIONAL
  - if present, MUST be a non-empty string
- Examples:
  - "A queue of the sensor generated messages"

#### tags

- Type: Map of name/value string pairs
- Description: A mechanism in which additional metadata about the Endpoint can
  be stored.

  When this property has no value it MUST either be serialized as an empty
  map or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, MUST be a map of name/value string pairs
  - Each name MUST be a non-empty, unique within the scope of this map, string.
    Values MAY be empty strings
- Examples:
  - `{ "owner": "John", "verified": "" }`

#### docs

- Type: URI-reference
- Description: A URI-reference to additional documentation about this Endpoint.
  This specification does not define any constraints on the data returned from
  this URI-reference.
- Constraints:
  - OPTIONAL
  - if present, MUST be a non-empty URI-reference
  - if present with a schema, it MUST use either `http` or `https`
- Examples:
  - `https://example.com/docs/myQueue`

#### deprecated

- Type: Object container the following properties:
  - effective<br>
    An OPTIONAL property indicating the time when the Endpoint entered, or will
    enter, a deprecated state. The date MAY be in the past or future.
    If present, this MUST be an [RFC3339][rfc3339] timestamp.

  - removal<br>
    An OPTIONAL property indicating the time when the Endpoint MAY be removed.
    The Endpoint MUST NOT be deleted before this time. If this property is not
    present then client can not make any assumption as to when the Endpoint
    might be removed. Note: as with most Endpoint properties, this property
    is mutable. If present, this MUST be an [RFC3339][rfc3339] timestamp.

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
    alternative Endpoints.

- Description: Presence of this property (even without any nested properties)
  indicates that the Endpoint is, or will be, deprecated and will be removed at
  some point in the future.

  This specification makes no statement as to whether any existing subscription
  will still be valid and usable after this date. However, it is expected that
  new subscription requests after the Endpoint is deleted will likely be
  rejected.

  Note that an implementation is not mandated to use this attribute in
  advance of removing an Endpoint, but is it RECOMMENDED that they do so.
- Constraints:
  - OPTIONAL
- Examples:
  - `"deprecated": {}`
  - ```
    "deprecated": {
      "removaltime": "2030-12-19T00:00:00-00:00",
      "alternative": "https://discovery.example.com/services/123"
    }
    ````

#### channel

- Type: String
- Description: A string that can be used to correlate Endpoints. Any Endpoints
  within an instance of a Discovery Service that share the same `channel` value
  MUST have some relationship. This specification does not define that
  relationship or the specific values used in this property. 

  When this property has no value it MUST either be serialized as an empty
  string or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, MUST be a string
- Examples:
  - `queue1`

#### authscope

- Type: TBD
- Description: TBD
- Constraints:
  - OPTIONAL
- Examples:
  - TBD

#### usage

- Type: String
- Description: The interaction model supported by this Endpoint. This
  specification defines a set of possible values (see the
  [Usage Values](#usage-values) section for more information, however,
  implementations MAY define new values as extensions. It is RECOMMENDED
  that extension values be defined with some organizational unique string
  to reduce the chances of collisions with possible future spec-defined values.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
- Examples:
  - `consumer`

#### config

- Type: Object
- Description: Metadata the provides additional information concerning the
  interactions with this Endpoint. Each `usage` value MUST define the set of
  `config` properties that are valid.

  When this property has no value it MUST either be serialized as an empty
  object or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
- Examples:
  - `{ "protocol": "kafka" , "endpoint": "https://example.com/queue/1234" }`

#### groups

- Type: Array
- Description: A set of Definition Groups supported by this Endpoint. Each
  Group MAY be a full representation of the Group or MAY be a
  [reference](#references) to a Group defined elsewhere. If it is a reference
  then it MAY be to a Group defined outside of the current Discovery Service
  instance.

  When this property has no value it MUST either be serialized as an empty
  array or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, the same Group, as identified by its `id` or `uri`, MUST NOT
    appear more than once within this property.
- Examples:
  - `[ { ...group properties... }, { "uri": "https://example.com/discovery/group/987", "name", "John's blob store messages" } ]`

#### definitions

- Type: Array
- Description: A set of Message Definitions supported by this Endpoint. Each
  Definition MAY be a full representation of the Definition or MAY be a
  [reference](#references) to a Definition defined elsewhere. If it is a
  reference then it MAY be to a Definition defined outside of the current
  Discovery Service instance.

  When this property has no value it MUST either be serialized as an empty
  array or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, the same Definition, as identified by its `id` or `uri`,
    MUST NOT appear more than once within this property.
- Examples:
  - `[ { ...definition properties... }, { "uri", "https://example.com/discovery/defs/8765", "name": "Blob created" } ]`


### Definition

A Definition is ...

Talk about how each has metadata and data

```
{
    "id", "URI-reference",
    "name": "STRING",
    "self": "URI",
    "epoch": "STRING",
    "description": "STRING", ?
    "tags": { "STRING": "STRING", ... } ?
    "docs": "URL", ?

    "format": "STRING",
    "metadata": {
        "attributes": {
            "attributeName": {
                "required": true|false,
                "description": "STRING", ?
                "value": JSON_OBJECT,
                "type": "string|object|...", ?
                "specurl": "URL" ?
            }
        } *
    }, ?
    "schema": { ... }, ?
    "schemaurl": "URL", ?

    "groups": [
        {
            "uri": "URI", ?
            ... Group properties ... ?
        }
    ],

    "endpoints": [ 
        {
            "uri": "URI", ?
            ... Endpoint properties ... ?
        }
    ]
}

```

The following Definition properties are defined:

#### id

- Type: String
- Description: A unique identifier for this Definition.
- Constraints:
  - REQUIRED
  - MUST be a non-empty String
  - MUST conform with
    [RFC3986/3.3](https://datatracker.ietf.org/doc/html/rfc3986#section-3.3)
    `segment-nz-nc` syntax
  - MUST be unique across all Definitions within the current Discovery Service
- Examples:
  - A UUID
  - `2345`

#### name

- Type: String
- Description: The name of the Definition.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
- Examples:
  - Blob created message

#### self

- Type: URI
- Description: A unique URI for this Definition. If the URI is a URL then an
  HTTP GET to this URL MUST return the metadata for this Defintion. The URI
  MUST be a combination of the base URI of the list of Definitions for the
  current Discovery Service concatenated with the `id` of this Definition.
- Constraints:
  - REQUIRED
  - MUST be a non-empty URI

- Examples:
  - `https://example.com/discovery/definitions/2345`

#### epoch

- Type: Unsigned Integer
- Description: A number representing the version number of this Definition. Each
  time this Definition is modified this property MUST be updated with a new
  value that is greater than the current one.
- Constraints:
  - REQUIRED
  - MUST be an unsigned integer
- Examples:
  - `0`
  - `1001`

#### description

- Type: String
- Description: A summary of the purpose of the Definition.
- Constraints:
  - OPTIONAL
  - if present, MUST be a non-empty string
- Examples:
  - "A queue of the sensor generated messages"

#### tags

- Type: Map of name/value string pairs
- Description: A mechanism in which additional metadata about the Definition can
  be stored.

  When this property has no value it MUST either be serialized as an empty
  map or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, MUST be a map of name/value string pairs
  - Each name MUST be a non-empty, unique within the scope of this map, string.
    Values MAY be empty strings
- Examples:
  - `{ "owner": "John", "verified": "" }`

#### format

- Type: String
- Description: Specifies the type of message associated with this Definition.
  This value can be used to definitively identify the type of message without
  checking the individual attributes listed under the `metadata` property.
  See the [Message Formats](#message-formats) section for more information.

  When this property has no value it MUST either be serialized as an empty
  string or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
- Examples:
  - `CloudEvents/1.0`
  - `AMQP/1.0`

#### metadata

- Type: Object
- Description: Specifies the message attributes for the Definition that will
  appear as metadata in the resulting serialized message. Note that this will
  define the metadata of the message, not the data portion of the message.

  When this property has no value it MUST either be serialized as an empty
  object or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
- Examples:
  - TBD

#### schema

- Type: Object
- Description: An in-line definition of the schema of the message's data.

  When this property has no value it MUST either be serialized as an empty
  object or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - MUST NOT be present if `schemaurl` is present
- Examples:
  - TBD

#### schemaurl

- Type: URL
- Description: A URL to the schema of the message's data.
- Constraints:
  - OPTIONAL
  - if present, MUST be a non-empty URL
  - MUST NOT be present if `schema` is present
- Examples:
  - `https://example.com/schema/...`

#### groups

- Type: Array
- Description: A set of Definition Groups that this Definition is part of.
  Each Group MAY be a full representation of the Group or MAY be a
  [reference](#references) to a Group defined elsewhere. If it is a reference
  then it MAY be to a Group defined outside of the current Discovery Service
  instance.

  NOTE: do we need to place any restrictions on this list to avoid recursion?

  NOTE: it really feels like this SHOULD either be removed or just a ref

  When this property has no value it MUST either be serialized as an empty
  array or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, the same Group, as identified by its `id` or `uri`,
    MUST NOT appear more than once within this property.
- Examples:
  - `[ { ...definition properties... }, { "uri", "https://example.com/discovery/defs/8765", "name": "Blob created" } ]`

#### endpoints

- Type: Array
- Description: A set of Endpoints that this Definition is supported by.
  Each Endpoint MAY be a full representation of the Endpoint or MAY be a
  [reference](#references) to a Endpoint defined elsewhere. If it is a reference
  then it MAY be to a Endpoint defined outside of the current Discovery Service
  instance.

  NOTE: do we need to place any restrictions on this list to avoid recursion?

  NOTE: it really feels like this SHOULD either be removed or just a ref

  When this property has no value it MUST either be serialized as an empty
  array or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, the same Endpoint, as identified by its `id` or `uri`,
    MUST NOT appear more than once within this property.
- Examples:
  - TBD


### Group

A Group is ...

```
{
    "id": "URI-reference",
    "name": "STRING",
    "self": "URI",
    "format": "STRING",

    "definitions": [
        {
            "uri": "URI", ?
            ... Definition properties ... ?
        } *
    ],

    "groups": [
        {
            "uri": "URI", ?
            ... Group properties ... ?
        } *
    ]
}
```

The following Definition properties are defined:

#### id

- Type: String
- Description: A unique identifier for this Group.
- Constraints:
  - REQUIRED
  - MUST be a non-empty String
  - MUST conform with
    [RFC3986/3.3](https://datatracker.ietf.org/doc/html/rfc3986#section-3.3)
    `segment-nz-nc` syntax
  - MUST be unique across all Groups within the current Discovery Service
- Examples:
  - A UUID
  - `2345`

#### name

- Type: String
- Description: The name of the Group.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
- Examples:
  - TBD

#### self

- Type: URI
- Description: A unique URI for this Group. If the URI is a URL then an
  HTTP GET to this URL MUST return the metadata for this Group. The URI
  MUST be a combination of the base URI of the list of Group for the
  current Discovery Service concatenated with the `id` of this Group.
- Constraints:
  - REQUIRED
  - MUST be a non-empty URI

- Examples:
  - TBD

#### epoch

- Type: Unsigned Integer
- Description: A number representing the version number of this Group. Each
  time this Group is modified this property MUST be updated with a new
  value that is greater than the current one.
- Constraints:
  - REQUIRED
  - MUST be an unsigned integer
- Examples:
  - `0`
  - `1001`

#### description

- Type: String
- Description: A summary of the purpose of the Group.
- Constraints:
  - OPTIONAL
  - if present, MUST be a non-empty string
- Examples:
  - TBD

#### tags

- Type: Map of name/value string pairs
- Description: A mechanism in which additional metadata about the Group can
  be stored.

  When this property has no value it MUST either be serialized as an empty
  map or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, MUST be a map of name/value string pairs
  - Each name MUST be a non-empty, unique within the scope of this map, string.
    Values MAY be empty strings
- Examples:
  - `{ "owner": "John", "verified": "" }`

#### format

- Type: String
- Description: Specifies the `format` value of the Definitions associated with
  this Group. All Definitions associated with this Group MUST have a `format`
  value that matches this property's value.

  When this property has no value it MUST either be serialized as an empty
  string or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
- Examples:
  - `CloudEvents/1.0`
  - `AMQP/1.0`

#### definitions

- Type: Array
- Description: A set of Message Definitions supported by this Group. Each
  Definition MAY be a full representation of the Definition or MAY be a
  [reference](#references) to a Definition defined elsewhere. If it is a
  reference then it MAY be to a Definition defined outside of the current
  Discovery Service instance.

  When this property has no value it MUST either be serialized as an empty
  array or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, the same Definition, as identified by its `id` or `uri`,
    MUST NOT appear more than once within this property.
- Examples:
  - `[ { ...definition properties... }, { "uri", "https://example.com/discovery/defs/8765", "name": "Blob created" } ]`

#### groups

- Type: Array
- Description: A set of neted Definition Groups supported by this Group. Each
  Group MAY be a full representation of the Group or MAY be a
  [reference](#references) to a Group defined elsewhere. If it is a reference
  then it MAY be to a Group defined outside of the current Discovery Service
  instance.

  When this property has no value it MUST either be serialized as an empty
  array or excluded from the serialization entirely.
- Constraints:
  - OPTIONAL
  - if present, the same Group, as identified by its `id` or `uri`, MUST NOT
    appear more than once within this property.
- Examples:
  - `[ { ...group properties... }, { "uri": "https://example.com/discovery/group/987", "name", "John's blob store messages" } ]`


## Serializations

Serializations are REQUIRED to talk about whether empty properties MAY
appear in the serialization or whether they MUST be excluded entirely.

...

## Usage Values

subscriber | consumer | producer
...

## Message Formats

CloudEvents/1.0
...


## API Specification

The relative paths specified below are NOT REQUIRED to be at the root of
the `fpath` (per RFC1738). However, they are REQUIRED to match the end of it.
For example, the following are valid URLs/paths:

```
https://example.com/
https://example.com/endpoints
https://example.com/myAggregator/endpoints
```

If a Discovery Service can perform authorization checks to determine
which client can see which resource, and the requesting client is not allowed
access to a particular resource, then the Discovery Service MUST respond
as if that resource does not exist. For example, it would be excluded from
any array of Endpoints returned and it would result in a `404 Not Found`
error for a request to that Endpoints directly.

All APIs MUST support JSON encoding, which means that HTTP requests
including an HTTP `Content-Type` Header of `application/json` and body in that
format MUST be supported. Likewise requests with `Accept` header of
`application/json` MUST be supported.

Unknown query parameters on the APIs MUST be ignored.

Any resource previously returned to a client that does not appear in a
subsequent query can be assumed to be no longer available in the scope of the
query specified. In the unfiltered query case this means the resource has been
deleted. In the filtered case it is not possible to know if the resource has
been deleted or if the filters no longer apply to that resource, and therefore
it can not be assumed to be deleted.

### Filtering

In the APIs where an array of resources are returned filtering MAY be used
to reduce the result set. To specify a filter, the `filter` query parameter
MUST be used. The format for the `filter` query parameter MUST be:

```
?filter=ATTRIBUTE[=VALUE]
```

Nested attribute names MUST be specified by using a dot (`.`) as the nesting
operator. For example: `config.protocol` references the `protocol` attribute
under the top-level `config` attribute.

The following rules constrain the filter processing:
- The `=VALUE` portion is OPTIONAL and if not present then the implied
  meaning is that the filter MUST only match resources that contain the
  specified attribute with a non-empty value. This means a non-zero length
  strings or non-zero valued numerics.
- a `VALUE` of "" (empty string) is valid and a filter expression of
  `?filter=ATTRIBUTE=` MUST only match resources that contain the specified
  attribute with an empty string value. Note that an attribute with no
  value (or `null` depending on the data store used) MUST be treated the
  same as an attribute with an empty string (`""`) for the purpose of this
  filter feature.
- when `VALUE` is a non-empty string, then the filter expression MUST only
  match resources that contain the specified attribute with `VALUE` in any
  part of its value.
- Matching of attribute names MUST be case sensitive.
- Matching of attribute values MUST be case insensitive.
- If there are mulitple filter expressions, they MUST be specified as separate
  `filter` query parameters. When there are multiple filters, the resulting
  set of resources MUST only include ones that match all of the filters
  specified. When multiple nested attribute names are used, each nested
  attribute MUST be treated independently and the nested attributes do not
  need to be present in the same nested scope. See the sample filters below.
- Requests with unsupported filter attributes, MUST be rejected with a
  `400 Bad Request` response. Implementations SHOULD return an error message
  that indicates which filter attributes were not supported.

Discovery Services MUST support filtering by the following attributes:

- `name`
- `id`

Other attribute MAY be supported.

Note: an empty result set is not an error and a `200 OK` with a zero sized
array MUST be returned in those cases.

Some sample filter expressions:
| Expression | Results |
| :--- | :--- |
| ?filter=description | All resources that have a non-empty string value for `description` |
| ?filter=description= | All resources that have no value for `description`. Note: either `null` or `""` is a match |
| ?filter=description=test&filter=name=mine | All resources that have a `description` containing the string `test` (in any case), and a `name` containing the string `mine` (in any case) |
| ?filter=description=test,name=mine | All resources that have a `description` with the string `test,name=mine` (in any case) as part of its value |
| ?filter=events.type=abc&filter=events.description=mine | All resources that have an `events.type` containing the string `abc` (in any case) and an `events.description` containing `mine` (in any case) but these two attribute do not need to be part of the same `event` definition |


### Pagination

...

### Discovery APIs

All of the following APIs specified below MUST be supported by compliant
Discovery Service implementations.

#### `GET /`

This MUST return an object that matches the following format:
```
{
    "specversion": "STRING",
    "endpoints": [ ENDPOINT, ... ] ?
    "groups": [ GROUP, ... ] ?
    "definitions": [ DEFINITION, ... ] ?
}
```

Where:
- `specversion` is the version of the Discovery Service specification that
  is supported.
- `endpoints` is an array of zero or more Endpoint resources
- `groups` is an array of zero or more Group resources
- `definitions` is an array of zero or more Defintion resources

If any of the above arrays are empty then that property MAY be omitted from
the output.

Each nested resource (e.g. Endpoints, Groups or Definitions) MAY be in-lined
or MAY be a full representation of the resource.

Without any filtering specified, this MUST return all of the nested resources
available from the Discovery Service. Any resource that appears under another
resource MUST also be included as a stand-alone resource in its respective
array. For example, a Definition that appears within a Group will also appear
in the `definitions` array.

When filtering is specified then only the resources related to the requested
resources MUST be returned. For example, a filter that results in just one
Endpoint being returned would only include Groups and Definitions that are
related to that Endpoint.

#### `GET /endpoints`
#### `GET /definitions`
#### `GET /groups`

This MUST return an array of zero or more instances of the requested resource

In the case of `200 OK`, the response format MUST be a JSON array of resources
that adheres to the following:

```
200 OK
Content-Type: application/json

[
  {
    "id": "URI-reference",
    "name": "STRING", 
    "self": "URI",
    "epoch": UINT,
    ... remainder of resource's attributes ...
  } *
]
```

#### `GET /endpoints/{id}`
#### `GET /definitions/{id}`
#### `GET /groups/{id}`

This MUST return the latest version of the resource with the given `{id}` if
it exists.

The following responses are defined by this specification:
- `200 OK` and the resource representation in the HTTP response body.
- `404 Not Found` if the resource does not exist.

Other responses are allowed, but not defined by this specification.

In the case of `200 OK`, the response format MUST adhere to the following:

```
200 OK
Content-Type: application/json

{
    "id": "URI-reference",
    "name": "STRING", 
    "self": "URI",
    "epoch": UINT,
    ... remainder of resource's attributes ...
  }
```


### OpenAPI

See [Discovery Endpoint OpenAPI Specification](../discovery/discovery.yaml).

## Privacy and Security

This specification does not place restrictions on implementation's choice of
an authentication and authorization mechanism. While the list of entities
returned from each query MAY differ, the format of the output MUST adhere to
this specification.

Additionally, implementations MAY choose different authentication schemes for
each of the APIs defined in this specifications. For example, a valid choice
might be to allow the "features" APIs to not mandate any authentication at all,
while the "discovery" APIs might be restricted to authorized users.

[rfc3339]: https://tools.ietf.org/html/rfc3339
