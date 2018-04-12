# HTTP 1.1 Web Hooks for Event Delivery

## Abstract

"Web hooks" are a popular pattern to deliver notifications between applications
and via HTTP endpoints. In spite of pattern usage being widespread, there is no
formal definition for Web Hooks. This specification aims to provide such a
definition for use with [CNCF Cloud Events][CE], but is considered generally
usable beyond the scope of Cloud Events.

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to HTTP](#12-relation-to-http)
- 1.3. [Security](#15-security)
2. [Delivering notifications](#2-delivering-notifications)
3. [Authorization](#3-authorization)
4. [Abuse Protection](#4-abuse-protection)
5. [References](#4-references)

## 1. Introduction

"Web hooks" are a popular pattern to deliver notifications between applications
and via HTTP endpoints. Applications that make notifications available, allow
for other applications to register an HTTP endpoint to which notifications are
delivered once available.

This specification defines a HTTP method by how notifications are delivered by
the sender, an authorization model for event delivery to protect the receiver,
and a registration handshake that protects the sender from being abused for
flooding arbitrary HTTP sites with requests.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][RFC2119].

### 1.2. Relation to HTTP

This specification prescribes rules constraining the use and handling of
specific [HTTP methods][RFC7231-Section-4] and headers.

This specification also applies equivalently to HTTP/2 ([RFC7540][RFC7540]),
which is compatible with HTTP 1.1 semantics.

## 2. Delivering notifications

### 2.1. Delivery request

Notifications are delivered using a HTTP request. The response indicates the
resulting status of the delivery.

HTTP-over-TLS (HTTPS) [RFC2818][RFC2818] MUST be used for the connection.

The HTTP method for the delivery request MUST be [POST][POST].

The [`Content-Type`][Content-Type] header MUST be carried and the request MUST
carry a notification payload of the given content type. Requests without
payloads, e.g. where the notification is entirely expressed in HTTP headers,
are not permitted by this specification.

This specification does not further constrain the content of the notification,
and it also does not prescribe the [HTTP target resource][RFC7230-Section-5-1]
that is used for delivery.

If the delivery target supports and requires [Abuse Protection][#4-abuse-protection],
the delivery request MUST include the `Origin` header. The `Origin` header value
is a DNS name expression that identifies the sending system.

### 2.2. Delivery response

The delivery response MAY contain a payload providing detail status
information in the case of handling errors. This specification does not attempt
to define such a payload.

The response MUST NOT use any of the [3xx HTTP Redirect status codes][3xx] and
the client MUST NOT follow any such redirection.

If a delivery target has been retired, but the HTTP site still exists, the
site SHOULD return a [410 "Gone"][410] status code and the sender SHOULD refrain
from sending any further notifications.

If the delivery target is unable to process the request due to exceeding a
request rate limit, it SHOULD return a [429 Too Many Requests][429] status code
and MUST include the [`Retry-After`][Retry-After] header. The sender MUST
observe the value of the Retry-After header and refrain from sending further
requests until the indicated time.

If the delivery has been accepted and processed, and if the response carries a
payload with processing details, the response MUST have the [200 OK][200]
status code. In this case, the response MUST carry a
[`Content-Type`][Content-Type] header.

If the delivery has been accepted and processed, but carries no payload, the
response MUST have the [204 No Content][204] status code.

If the delivery has been accepted, but has not yet been processed or if the
processing status is unknown, the response MUST have the [202 Accepted][202]
status code.

## 3. Authorization

The delivery request MUST use one of the following two methods, both of which
lean on the OAuth 2.0 Bearer Token [RFC6750][RFC6750] model.

The delivery target MUST support both methods.

The client MAY use any token-based authorization scheme. Challenge-based
schemes MUST NOT be used.

### 3.1.  Authorization Request Header Field

The access token is sent in the [`Authorization`][Authorization] request
header field defined by HTTP/1.1.

For [OAuth 2.0 Bearer][Bearer] tokens, the "Bearer" scheme MUST be used.

Example:

``` text
GET /resource HTTP/1.1
Host: server.example.com
Authorization: Bearer mF_9.B5f-4.1JqM
```

### 3.2 URI Query Parameter

When sending the access token in the HTTP request URI, the client adds the
access token to the request URI query component as defined by "Uniform Resource
Identifier (URI): Generic Syntax" [RFC3986][RFC3986], using the "access_token"
parameter.

For example, the client makes the following HTTP request:

``` text
POST /resource?access_token=mF_9.B5f-4.1JqM HTTP/1.1
Host: server.example.com
```

The HTTP request URI query can include other request-specific parameters, in
which case the "access_token" parameter MUST be properly separated from the
request-specific parameters using "&" character(s) (ASCII code 38).

For example:

    https://server.example.com/resource?access_token=mF_9.B5f-4.1JqM&p=q

Clients using the URI Query Parameter method SHOULD also send a
Cache-Control header containing the "no-store" option.  Server
success (2XX status) responses to these requests SHOULD contain a
Cache-Control header with the "private" option.

Because of the security weaknesses associated with the URI method (see
[RFC6750, Section 5][RFC6750]), including the high likelihood that the URL
containing the access token will be logged, it SHOULD NOT be used unless it is
impossible to transport the access token in the "Authorization" request header
field or the HTTP request entity-body. All further caveats cited in
[RFC6750][RFC6750] apply equivalently.

## 4. Abuse Protection

Any system that allows registration of and delivery of notifications to
arbitary HTTP endpoints can potentially be abused such that someone maliciously
or inadvertently registers the address of a system that does not expect such
requests and for which the registering party is not authorized to perform such
a registration. In extreme cases, a notification infrastructure could be abused
to launch denial-of-service attacks against an arbitrary web-site.

To protect the sender from being abused in such a way, a legitimate delivery
target needs to indicate that it agrees with notifications being delivered to it.

Reaching the delivery agreement is realized using the following validation
handshake. The handshake can either be executed immediately at registration
time or as a "pre-flight" request immediately preceding a delivery. If the
handshake outcome is that the delivery is denied, the sender MUST NOT deliver
events to the target.

It is important to understand is that the handshake does not aim to establish
an authentication or authorization context. It only serves to protect the
sender from being told to a push to a destination that is not expecting the
traffic. While this specification mandates use of an authorization model, this
mandate is not sufficient to protect any arbitrary website from unwanted
traffic if that website doesn't implement access control and therefore ignores
the `Authorization` header.

Delivery targets SHOULD support the abuse protection feature. If a target does
not support the feature, the sender MAY choose not to send to the target, at
all, or send only at a very low request rate.

### 4.1.1. Validation request

The validation request uses the HTTP [OPTIONS][OPTIONS] method. The request
is directed to the exact resource target URI that is being registered.

With the validation request, the sender asks the target for permission to
send notifications, and it can declare a desired request rate (requests per
minute).

The delivery target will respond with a permission statement and the permitted
request rate.

The following header fields MUST be included in the validation request:

#### 4.1.1.2. WebHook-Request-Origin

The `WebHook-Request-Origin` header requests permission to send notifications
from this sender, and contains a DNS expression that identifies the sending
system, for example "eventemitter.example.com". The value is meant to summarily
identify all sender instances that act on the behalf of a certain system, and
not an individual host.

After the handshake and when permission is granted, the sender MUST use the
`Origin` request header for each delivery request, with the value matching that
of this header.

For example:

``` text
WebHook-Request-Origin: eventemitter.example.com
```

#### 4.1.1.2. WebHook-Request-Rate

The `WebHook-Request-Rate` header MAY be included in the request and asks for
permission to send notifications from this sender at the specified rate. The
value is the string representation of a positive integer number greater than
zero and expresses the request rate in "requests per minute".

For example, the following header asks for permission to send 120 requests per
minute:

``` text
WebHook-Request-Rate: 120
```

### 4.1.2 Validation response

If and only if the delivery target does allow delivery of the events, it MUST
reply to the request by including the `WebHook-Allowed-Origin` and
`WebHook-Allowed-Rate` headers.

If it does not allow delivery of the events or does not expect delivery of
events and nevertheless handles the HTTP OPTIONS method, the existing response
ought not to be interpreted as consent, and therefore the handshake cannot
rely on status codes.

The response SHOULD include the [Allow][Allow] header indicating the [POST][POST]
method being permitted. Other methods MAY be permitted on the resource, but
their function is outside the scope of this specification.

#### 4.1.1.2. WebHook-Allowed-Origin

The `WebHook-Allowed-Origin` header MUST be returned when the delivery target
agrees to notification delivery by the origin service. Its value MUST either be
the origin name supplied in the `WebHook-Request-Origin` header, or a singular
asterisk character ('*'), indicating that the delivery target supports
notifications from all origins.

``` text
WebHook-Allowed-Origin: eventemitter.example.com
```

or

``` text
WebHook-Request-Origin: *
```

#### 4.1.1.2. WebHook-Allowed-Rate

The `WebHook-Allowed-Rate` header MUST be returned if the request contained
teh `WebHook-Request-Rate`, otherwise it SHOULD be returned.

The header grants permission to send notifications at the specified rate. The
value is either an asterisk character or the string representation of a
positive integer number greater than zero. The asterisk indicates that there is
no rate limitation. An integer number expresses the permitted request rate in
"requests per minute". For request rates exceeding the granted notification
rate, the sender ought to expect request throttling. Throttling is indicated
by requests being rejected using HTTP status code [429][429].

For example, the following header permits to send 100 requests per
minute:

``` text
WebHook-Allowed-Rate: 100
```

## 5. References

- [RFC2046][RFC2046] Multipurpose Internet Mail Extensions (MIME) Part Two: 
  Media Types
- [RFC2119][RFC2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC2818][RFC2818] HTTP over TLS
- [RFC3629][RFC3629] UTF-8, a transformation format of ISO 10646
- [RFC3986][RFC3986] Uniform Resource Identifier (URI): Generic Syntax 
- [RFC4627][RFC4627] The application/json Media Type for JavaScript Object
  Notation (JSON)
- [RFC4648][RFC4648] The Base16, Base32, and Base64 Data Encodings
- [RFC6750][RFC6750] The OAuth 2.0 Authorization Framework: Bearer Token Usage
- [RFC6585][RFC6585] Additional HTTP Status Codes
- [RFC6839][RFC6839] Additional Media Type Structured Syntax Suffixes
- [RFC7159][RFC7159] The JavaScript Object Notation (JSON) Data Interchange Format
- [RFC7230][RFC7230] Hypertext Transfer Protocol (HTTP/1.1): Message Syntax
  and Routing
- [RFC7231][RFC7231] Hypertext Transfer Protocol (HTTP/1.1): Semantics and
  Content
- [RFC7235][RFC7235] Hypertext Transfer Protocol (HTTP/1.1): Authentication
- [RFC7540][RFC7540] Hypertext Transfer Protocol Version 2 (HTTP/2)

[CE]: ./spec.md
[JSON-format]: ./json-format.md
[Content-Type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[Retry-After]: https://tools.ietf.org/html/rfc7231#section-7.1.3
[Authorization]: https://tools.ietf.org/html/rfc7235#section-4.2
[Allow]: https://tools.ietf.org/html/rfc7231#section-7.4.1
[POST]: https://tools.ietf.org/html/rfc7231#section-4.3.3
[OPTIONS]: https://tools.ietf.org/html/rfc7231#section-4.3.7
[3xx]: https://tools.ietf.org/html/rfc7231#section-6.4
[429]: https://tools.ietf.org/html/rfc6585#section-4
[Bearer]:https://tools.ietf.org/html/rfc6750#section-2.1
[RFC2046]: https://tools.ietf.org/html/rfc2046
[RFC2119]: https://tools.ietf.org/html/rfc2119
[RFC2818]: https://tools.ietf.org/html/rfc2818
[RFC3629]: https://tools.ietf.org/html/rfc3629
[RFC3986]: https://tools.ietf.org/html/rfc3986
[RFC4627]: https://tools.ietf.org/html/rfc4627
[RFC4648]: https://tools.ietf.org/html/rfc4648
[RFC6585]: https://tools.ietf.org/html/rfc6585
[RFC6839]: https://tools.ietf.org/html/rfc6839#section-3.1
[RFC7159]: https://tools.ietf.org/html/rfc7159
[RFC7230]: https://tools.ietf.org/html/rfc7230
[RFC7231]: https://tools.ietf.org/html/rfc7231
[RFC7235]: https://tools.ietf.org/html/rfc7235
[RFC7230-Section-3]: https://tools.ietf.org/html/rfc7230#section-3
[RFC7231-Section-4]: https://tools.ietf.org/html/rfc7231#section-4
[RFC7230-Section-5-1]: https://tools.ietf.org/html/rfc7230#section-5.1
[RFC7540]: https://tools.ietf.org/html/rfc7540