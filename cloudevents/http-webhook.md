# HTTP 1.1 Web Hooks for Event Delivery - Version 1.0.3-wip

## Abstract

"Webhooks" are a popular pattern to deliver notifications between applications
and via HTTP endpoints. In spite of pattern usage being widespread, there is no
formal definition for Web Hooks. This specification aims to provide such a
definition for use with [CNCF CloudEvents][ce], but is considered generally
usable beyond the scope of CloudEvents.

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to HTTP](#12-relation-to-http)

2. [Delivering notifications](#2-delivering-notifications)
3. [Authorization](#3-authorization)
4. [Abuse Protection](#4-abuse-protection)
5. [References](#5-references)

## 1. Introduction

["Webhooks"][webhooks] are a popular pattern to deliver notifications between
applications and via HTTP endpoints. Applications that make notifications
available, allow for other applications to register an HTTP endpoint to which
notifications are delivered.

This specification defines a HTTP method by how notifications are delivered by
the sender, an authorization model for event delivery to protect the delivery
target, and a registration handshake that protects the sender from being abused
for flooding arbitrary HTTP sites with requests.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to HTTP

This specification prescribes rules constraining the use and handling of
specific [HTTP methods][rfc7231-section-4] and headers.

This specification also applies equivalently to HTTP/2 ([RFC7540][rfc7540]),
which is compatible with HTTP 1.1 semantics.

## 2. Delivering notifications

### 2.1. Delivery request

Notifications are delivered using a HTTP request. The response indicates the
resulting status of the delivery.

HTTP-over-TLS (HTTPS) [RFC2818][rfc2818] MUST be used for the connection.

The HTTP method for the delivery request MUST be [POST][post].

The [`Content-Type`][content-type] header MUST be carried and the request MUST
carry a notification payload of the given content type. Requests without
payloads, e.g. where the notification is entirely expressed in HTTP headers, are
not permitted by this specification.

This specification does not further constrain the content of the notification,
and it also does not prescribe the [HTTP target resource][rfc7230-section-5-1]
that is used for delivery.

If the delivery target supports and requires [Abuse
Protection](#4-abuse-protection), the delivery request MUST include the
`WebHook-Request-Origin` header. The `WebHook-Request-Origin` header value is a
DNS name expression that identifies the sending system.

### 2.2. Delivery response

The delivery response MAY contain a payload providing detail status information
in the case of handling errors. This specification does not attempt to define
such a payload.

The response MUST NOT use any of the [3xx HTTP Redirect status codes][3xx] and
the client MUST NOT follow any such redirection.

If the delivery has been accepted and processed, and if the response carries a
payload with processing details, the response MUST have the [200 OK][200] or
[201 Created][201] status code. In this case, the response MUST carry a
[`Content-Type`][content-type] header.

If the delivery has been accepted and processed, but carries no payload, the
response MUST have the [201 Created][201] or [204 No Content][204] status code.

If the delivery has been accepted, but has not yet been processed or if the
processing status is unknown, the response MUST have the [202 Accepted][202]
status code.

If a delivery target has been retired, but the HTTP site still exists, the site
SHOULD return a [410 Gone][410] status code and the sender SHOULD refrain from
sending any further notifications.

If the delivery target is unable to process the request due to exceeding a
request rate limit, it SHOULD return a [429 Too Many Requests][429] status code
and MUST include the [`Retry-After`][retry-after] header. The sender MUST
observe the value of the Retry-After header and refrain from sending further
requests until the indicated time.

If the delivery cannot be accepted because the notification format has not been
understood, the service MUST respond with status code [415 Unsupported Media
Type][415].

All further error status codes apply as specified in [RFC7231][rfc7231].

## 3. Authorization

The delivery request MUST use one of the following two methods, both of which
lean on the OAuth 2.0 Bearer Token [RFC6750][rfc6750] model.

The delivery target MUST support both methods.

The client MAY use any token-based authorization scheme. The token can take any
shape, and can be a standardized token format or a simple key expression.

Challenge-based schemes MUST NOT be used.

### 3.1. Authorization Request Header Field

The access token is sent in the [`Authorization`][authorization] request header
field defined by HTTP/1.1.

For [OAuth 2.0 Bearer][bearer] tokens, the "Bearer" scheme MUST be used.

Example:

```text
POST /resource HTTP/1.1
Host: server.example.com
Authorization: Bearer mF_9.B5f-4.1JqM
```

### 3.2 URI Query Parameter

When sending the access token in the HTTP request URI, the client adds the
access token to the request URI query component as defined by "Uniform Resource
Identifier (URI): Generic Syntax" [RFC3986][rfc3986], using the "access_token"
parameter.

For example, the client makes the following HTTP request:

```text
POST /resource?access_token=mF_9.B5f-4.1JqM HTTP/1.1
Host: server.example.com
```

The HTTP request URI query MAY include other request-specific parameters, in
which case the "access_token" parameter MUST be properly separated from the
request-specific parameters using "&" character(s) (ASCII code 38).

For example:

    https://server.example.com/resource?access_token=mF_9.B5f-4.1JqM&p=q

Clients using the URI Query Parameter method SHOULD also send a Cache-Control
header containing the "no-store" option. Server success (2XX status) responses
to these requests SHOULD contain a Cache-Control header with the "private"
option.

Because of the security weaknesses associated with the URI method (see [RFC6750,
Section 5][rfc6750]), including the high likelihood that the URL containing the
access token will be logged, it SHOULD NOT be used unless it is impossible to
transport the access token in the "Authorization" request header field or the
HTTP request entity-body. All further caveats cited in [RFC6750][rfc6750] apply
equivalently.

## 4. Abuse Protection

Any system that allows registration of and delivery of notifications to
arbitrary HTTP endpoints can potentially be abused such that someone maliciously
or inadvertently registers the address of a system that does not expect such
requests and for which the registering party is not authorized to perform such a
registration. In extreme cases, a notification infrastructure could be abused to
launch denial-of-service attacks against an arbitrary web-site.

To protect the sender from being abused in such a way, a legitimate delivery
target needs to indicate that it agrees with notifications being delivered to
it.

Reaching the delivery agreement is realized using the following validation
handshake. The handshake can either be executed immediately at registration time
or as a "pre-flight" request immediately preceding a delivery.

It is important to understand is that the handshake does not aim to establish an
authentication or authorization context. It only serves to protect the sender
from being told to a push to a destination that is not expecting the traffic.
While this specification mandates use of an authorization model, this mandate is
not sufficient to protect any arbitrary website from unwanted traffic if that
website doesn't implement access control and therefore ignores the
`Authorization` header.

Delivery targets SHOULD support the abuse protection feature. If a target does
not support the feature, the sender MAY choose not to send to the target, at
all, or send only at a very low request rate.

### 4.1. Validation request

The validation request uses the HTTP [OPTIONS][options] method. The request is
directed to the exact resource target URI that is being registered.

With the validation request, the sender asks the target for permission to send
notifications, and it can declare a desired request rate (requests per minute).

The delivery target will respond with a permission statement and the permitted
request rate.

The following header fields are for inclusion in the validation request.

#### 4.1.2. WebHook-Request-Origin

The `WebHook-Request-Origin` header MUST be included in the validation request
and requests permission to send notifications from this sender, and contains a
DNS expression that identifies the sending system, for example
"eventemitter.example.com". The value is meant to summarily identify all sender
instances that act on the behalf of a certain system, and not an individual
host.

After the handshake and if permission has been granted, the sender MUST use the
`WebHook-Request-Origin` request header for each delivery request, with the value matching that
of this header.

Example:

```text
WebHook-Request-Origin: eventemitter.example.com
```

#### 4.1.3. WebHook-Request-Callback

The `WebHook-Request-Callback` header is OPTIONAL and augments the
`WebHook-Request-Origin` header. It allows the delivery target to grant send
permission asynchronously, via a simple HTTPS callback.

If the receiving application does not explicitly support the handshake described
here, an administrator could nevertheless still find the callback URL in the
log, and call it manually and therewith grant access.

The delivery target grants permission by issuing an HTTPS GET or POST request
against the given URL. The HTTP GET request can be performed manually using a
browser client. If the WebHook-Request-Callback header is used, the callback 
target MUST support both methods.

The delivery target MAY include the `WebHook-Allowed-Rate` response in the
callback.

The URL is not formally constrained, but it SHOULD contain an identifier for the
delivery target along with a secret key that makes the URL difficult to guess so
that 3rd parties cannot spoof the delivery target.

For example:

```text
WebHook-Request-Callback: https://example.com/confirm?id=12345&key=...base64...
```

#### 4.1.4. WebHook-Request-Rate

The `WebHook-Request-Rate` header MAY be included in the request and asks for
permission to send notifications from this sender at the specified rate. The
value is the string representation of a positive integer number greater than
zero and expresses the request rate in "requests per minute".

For example, the following header asks for permission to send 120 requests per
minute:

```text
WebHook-Request-Rate: 120
```

### 4.2. Validation response

If and only if the delivery target does allow delivery of the events, it MUST
reply to the request by including the `WebHook-Allowed-Origin` and
`WebHook-Allowed-Rate` headers.

If the delivery target chooses to grant permission by callback, it withholds the
response headers.

If the delivery target does not allow delivery of the events or does not expect
delivery of events and nevertheless handles the HTTP OPTIONS method, the
existing response ought not to be interpreted as consent, and therefore the
handshake cannot rely on status codes. If the delivery target otherwise does not
handle the HTTP OPTIONS method, it SHOULD respond with HTTP status code 405, as
if OPTIONS were not supported.

The OPTIONS response SHOULD include the [Allow][allow] header indicating the
[POST][post] method being permitted. Other methods MAY be permitted on the
resource, but their function is outside the scope of this specification.

#### 4.2.1. WebHook-Allowed-Origin

The `WebHook-Allowed-Origin` header MUST be returned when the delivery target
agrees to notification delivery by the origin service. Its value MUST either be
the origin name supplied in the `WebHook-Request-Origin` header, or a singular
asterisk character ('\*'), indicating that the delivery target supports
notifications from all origins.

```text
WebHook-Allowed-Origin: eventemitter.example.com
```

or

```text
WebHook-Allowed-Origin: *
```

#### 4.2.2. WebHook-Allowed-Rate

The `WebHook-Allowed-Rate` header MUST be returned alongside 
`WebHook-Allowed-Origin`if the request contained the `WebHook-Request-Rate` 
header, otherwise it SHOULD be returned. 

For the callback model, the `WebHook-Allowed-Rate` header SHOULD be included
in the callback request. If the header is not included, for instance when a 
callback is issued through a browser as a GET request, the allowed rate SHOULD
correspond to the requested rate. 

The header grants permission to send notifications at the specified rate. The
value is either an asterisk character or the string representation of a positive
integer number greater than zero. The asterisk indicates that there is no rate
limitation. An integer number expresses the permitted request rate in "requests
per minute". For request rates exceeding the granted notification rate, the
sender ought to expect request throttling. Throttling is indicated by requests
being rejected using HTTP status code [429 Too Many Requests][429].

For example, the following header permits to send 100 requests per minute:

```text
WebHook-Allowed-Rate: 100
```

## 5. References

- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC2818][rfc2818] HTTP over TLS
- [RFC6750][rfc6750] The OAuth 2.0 Authorization Framework: Bearer Token Usage
- [RFC6585][rfc6585] Additional HTTP Status Codes
- [RFC7230][rfc7230] Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and
  Routing
- [RFC7231][rfc7231] Hypertext Transfer Protocol (HTTP/1.1): Semantics and
  Content
- [RFC7235][rfc7235] Hypertext Transfer Protocol (HTTP/1.1): Authentication
- [RFC7540][rfc7540] Hypertext Transfer Protocol Version 2 (HTTP/2)

[ce]: ./spec.md
[webhooks]: https://progrium.github.io/blog/2007/05/03/web-hooks-to-revolutionize-the-web/index.html
[content-type]: https://tools.ietf.org/html/rfc7231#section-3.1.1.5
[retry-after]: https://tools.ietf.org/html/rfc7231#section-7.1.3
[authorization]: https://tools.ietf.org/html/rfc7235#section-4.2
[allow]: https://tools.ietf.org/html/rfc7231#section-7.4.1
[post]: https://tools.ietf.org/html/rfc7231#section-4.3.3
[options]: https://tools.ietf.org/html/rfc7231#section-4.3.7
[3xx]: https://tools.ietf.org/html/rfc7231#section-6.4
[200]: https://tools.ietf.org/html/rfc7231#section-6.3.1
[201]: https://tools.ietf.org/html/rfc7231#section-6.3.2
[202]: https://tools.ietf.org/html/rfc7231#section-6.3.3
[204]: https://tools.ietf.org/html/rfc7231#section-6.3.5
[410]: https://tools.ietf.org/html/rfc7231#section-6.5.9
[415]: https://tools.ietf.org/html/rfc7231#section-6.5.13
[429]: https://tools.ietf.org/html/rfc6585#section-4
[bearer]: https://tools.ietf.org/html/rfc6750#section-2.1
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986]: https://tools.ietf.org/html/rfc3986
[rfc2818]: https://tools.ietf.org/html/rfc2818
[rfc6585]: https://tools.ietf.org/html/rfc6585
[rfc6750]: https://tools.ietf.org/html/rfc6750
[rfc7159]: https://tools.ietf.org/html/rfc7159
[rfc7230]: https://tools.ietf.org/html/rfc7230
[rfc7230-section-3]: https://tools.ietf.org/html/rfc7230#section-3
[rfc7231-section-4]: https://tools.ietf.org/html/rfc7231#section-4
[rfc7230-section-5-1]: https://tools.ietf.org/html/rfc7230#section-5.1
[rfc7231]: https://tools.ietf.org/html/rfc7231
[rfc7235]: https://tools.ietf.org/html/rfc7235
[rfc7540]: https://tools.ietf.org/html/rfc7540
