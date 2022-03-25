# Pagination - Version 0.1-wip

This document describes a mechanism by which a server can return a set of
records to a client in an incremental fashion. Often this will be used when
a client is doing a query for a set of records and the result set is too large
to return in one response.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

## Client Request

When a client sends a request to a server which is meant to result in a
set of records being returned, the client MAY include extra attributes
to control how those records are to be returned if the results can not
fit within one response message.

### Client Attributes

The follow list of attributes MAY be included in a client's request for
a set of records from a server. The client MUST only specify these on
the initial request for set. If the results can not fit within one
message then these attributes MUST NOT be added to subsequent requests
by the client. Note, the server MAY include these attributes within
the URI-reference returned in a response message, but the client MUST NOT
modify those values.

#### limit

- Type: unsigned 64-bit integer
- Description: Indicates the maximum number of records per message
  that the cient is willing to accept. If the server is unable to
  meet this criteria then it MUST generate an error.
  There is no default value for this attribute.
  If this attribute is not specified, then the server MAY choose to send back
  as many, or as little, records per response message.
- Constraints:
  - OPTIONAL
  - MUST be an unsigned 64-bit integer with a value greater than 0
- Examples:
  - `100`

## Server Response

When a server returns a set of records, it MAY include additional attributes
to help the client retrieve the next set of records.

### Server Attributes

The following list of attributes MAY be included in a server's response to
a client's request for a set of records.

Note: in the examples listed below, the use of certain query parameters
in the response messages from the server, such as `offset` and `limit`,
are an implementation detail of the server. How the server encodes the
information it needs to retrieve a certain set of records is not
mandated by this specification.

#### link

- Type: `URI-Reference`
- Description: A URI-Reference to another set of records. The relationship
  of the next set, to the current set, MUST be specified by the `rel`
  attribute. This value is meant to be treated as an opaque value by the
  client. If a client uses this value in a subsequent request then it
  MUST use it as it was provided by the server. Any attempt to modify its
  value, or attributes (such as query parameters), is not defined by this
  specification and the results from the server are undefined.
- Constraints:
  - MUST NOT be present if there are no more records for the `rel` type of
    relationship
  - MUST be present if there are more records for the `rel` type of
    relationship
  - MUST be a URI-Reference as defined in RFC...
- Examples:
  - `http://example.com/people?offset=3&limit=100`
  - `http://example.com/people?id=1234`
  - `http://example.com/people?resultset=7a835`

#### rel

- Type: `String`
- Description: A string representing the relationship between the records
  available via the `link` URI-Reference and the current set of records.
  This attribute adheres to the Relation Type as defined in section 5.3
  of RFC5988.
  This specification uses the following values as defined by section 6.2.2
  in RFC598:
  - `next` - indicates the next set of records in the sequence of records
    being returned
  - `prev` - indicates the previous set of records in the sequence of records
    being returned
  - `first` - indicates the first set of records in the sequence of records
    being returned
  - `last` - indicates the last set of records in the sequence of records
    being returned
  Unless otherwise constrained by a specification leveraging this
  specification, additional values MAY be defined.
- Constraints:
  - REQUIRED if the `link` attribute is present
  - MUST be a string as defined by `relation-types` in RFC5988

#### expires

- Type: `Timestamp`
- Description: Indicates when the set of records referenced by the
  `link` will no longer be available. When not specified, the availability
  of the data is undefined by this specification. However, it is RECOMMENDED
  that this attribute only be excluded when the data being interated over
  is not expected to change very often and therefore the server will
  typically not need to save any state related to this client's requests.
- Constraints:
  - OPTIONAL

## HTTP Binding

THe following describes how the attributes defined above would appear in a
flow of HTTP messages during the retrieval of a set of records.

### Request for a record set

To request a set of records from a server, a client will send an HTTP GET
request to the server. How this URL is determined is out of scope of this
specification.

The client MAY include the `limit` attribute as part of this request. Unless
there is some out-of-bands negotiation to determine a different mechanism,
the server MUST accept the `limit` attribute as a query parameter (named
`limit`, case sensitive) in the URL.

For example:
```
http://example.com/people?limit=100
```

### Response for a record set

Each successful response from the server will adhere to the following:
- MUST respond with an HTTP 200
- MUST include zero or more records
- if the response refers to the start of the set of records, then the `prev`
  Link MUST NOT be included in the response
- if the response does not include the start of the set of records, then the
  `prev` Link MAY be included in the response
- the response MAY include the `first` Link in any response
- if  `limit` attribute was specified as part of the flow, the response MUST
  NOT include more records than what the `limit` attribute has indicated
- if the response refers to the end of the set of records, then the `next`
  Link MUST NOT be included in the response
- if the response does not refer to the end of the set of records, then the
  `next` Link MUST be included in the response
- the response MAY include the `last` Link in any response
- the response MAY include the `expires` attribute in any response as an
  HTTP "Expires" header. If present, it MUST adhere to the format specified in
  [RFC 3339](https://tools.ietf.org/html/rfc7234#section-5.3)

Additionally, Links MUST appear in the HTTP response as HTTP headers using
the format described in RFC5988.

Example 1:
```
Link: <http://example.com?limit=100&offset=3>;rel=next
Link: <http://example.com?limit=100&offset=1>;rel=prev
```

Example 2:
```
Link: <http://example.com?resultset=83d71>;rel=next
Expires: Thu, 01 Dec 2021 16:00:00 GMT
```

Example 3:
```
Link: <http://example.com?id=1001>;rel=next
Link: <http://example.com?id=0>;rel=prev
```

### Iterating over the record set

Once the record set retrieval has started, the client MAY use the Links
returned from the server to iterate through the full set of records.
Typically, the client will use the `next` Link from each response to retrieve
the next set of records until a response is returned without a `next` Link -
indicating that it has reached the end.

However, if other Links are provided by the server, then the client MAY
use those Links instead to follow a different traversal path through the
records.
