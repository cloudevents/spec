# WebSockets Protocol Binding for CloudEvents - Version 1.0.3-wip

## Abstract

The WebSockets Protocol Binding for CloudEvents defines how to establish and use
full-duplex CloudEvents streams using [WebSockets][rfc6455].

## Table of Contents

1. [Introduction](#1-introduction)

- 1.1. [Conformance](#11-conformance)
- 1.2. [Relation to WebSockets](#12-relation-to-websockets)
- 1.3. [Content Modes](#13-content-modes)
- 1.4. [Handshake](#14-handshake)
- 1.5. [CloudEvents Subprotocols](#15-cloudevents-subprotocols)
- 1.6. [Security](#16-security)

2. [Use of CloudEvents Attributes](#2-use-of-cloudevents-attributes)

3. [WebSocket Message Mapping](#3-websocket-message-mapping)

- 3.1. [Event Data Encoding](#31-event-data-encoding)

4. [References](#4-references)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be used in
[WebSockets][rfc6455], in order to establish and use a full-duplex CloudEvents
stream.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2. Relation to WebSockets

This specification does not prescribe rules constraining the use or handling of
specific [HTTP target resource][rfc7230-section-5-1] to establish the WebSocket
upgrade.

This specification prescribes rules constraining the [WebSockets
Subprotocols][rfc6455-section-5-1] in order to reach agreement on the event
format to use when sending and receiving serialized CloudEvents.

Events are sent as WebSocket messages, serialized using an [event
format][ce-event-format].

### 1.3. Content Modes

The [CloudEvents specification][ce-message] defines three content modes for
transferring events: _structured_, _binary_ and _batch_.

Because of the nature of WebSockets messages, this specification supports only
_structured_ data mode, hence event metadata attributes and event data are
sent in WebSocket messages using an [event format][ce-event-format].

The [event format][ce-event-format] to be used in a full-duplex WebSocket stream
is agreed during the [handshake](#14-handshake) and cannot change during the
same stream.

### 1.4. Handshake

The [opening handshake][rfc6455-section-1-3] MUST follow the set of rules
specified in the [RFC6455][rfc6455-section-4].

In addition, the client MUST include, in the opening handshake, the
[`Sec-WebSocket-Protocol` header][rfc6455-section-1-9]. The client MUST include
in this header one or more
[CloudEvents subprotocols](#15-cloudevents-subprotocols), depending on the
subprotocols the client supports.

The server MUST reply with the chosen CloudEvents subprotocol using the
`Sec-WebSocket-Protocol` header. If the server doesn't support any of the
subprotocols included in the opening handshake, the server response SHOULD NOT
contain any `Sec-WebSocket-Protocol` header.

#### 1.4.1 Example

Example client request to begin the opening handshake:

```text
GET /events HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==
Sec-WebSocket-Protocol: cloudevents.json, cloudevents.avro
Sec-WebSocket-Version: 13
Origin: http://example.com
```

Example server response:

```text
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=
Sec-WebSocket-Protocol: cloudevents.json
```

### 1.5. CloudEvents Subprotocols

This specification maps a WebSocket subprotocol to each defined event format in
the CloudEvents specification, following the guidelines discussed in the
[RFC6455][rfc6455-section-1-9]. For each subprotocol, senders MUST use the
specified WebSocket frame type:

| Subprotocol        | Event format                     | Frame Type |
| ------------------ | -------------------------------- | ---------- |
| `cloudevents.json` | [JSON event format][json-format] | Text       |
| `cloudevents.avro` | [AVRO event format][avro-format] | Binary     |
| `cloudevents.proto` | [Protobuf event format][proto-format] | Binary |

All implementations of this specification MUST support the [JSON event
format][json-format]. This specification does not support the [JSON batch
format][json-batch-format].

### 1.6. Security

This specification does not introduce any new security features for WebSockets,
or mandate specific existing features to be used.

## 2. Use of CloudEvents Attributes

This specification does not further define any of the [CloudEvents][ce] event
attributes.

## 3. WebSocket Message Mapping

Because the content mode is always _structured_, a WebSocket message just
contains a CloudEvent serialized using the agreed event format.

### 3.1 Event Data Encoding

The chosen [event format][ce-event-format] defines how all attributes, including
the payload, are represented.

The event metadata and data MUST be rendered in accordance with the event
format specification and the resulting data becomes the payload.

## 4. References

- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [RFC6455][rfc6455] The WebSocket Protocol

[ce]: ../spec.md
[ce-message]: ../spec.md#message
[ce-event-format]: ../spec.md#event-format
[json-format]: ../formats/json-format.md
[json-batch-format]: ../formats/json-format.md#4-json-batch-format
[avro-format]: ../formats/avro-format.md
[proto-format]: ../formats/protobuf-format.md
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc6455]: https://tools.ietf.org/html/rfc6455
[rfc6455-section-1-3]: https://tools.ietf.org/html/rfc6455#section-1.3
[rfc6455-section-4]: https://tools.ietf.org/html/rfc6455#section-4
[rfc6455-section-1-9]: https://tools.ietf.org/html/rfc6455#section-1.9
[rfc7230-section-5-1]: https://datatracker.ietf.org/doc/html/rfc7230#section-5.1
[rfc6455-section-5-1]: https://datatracker.ietf.org/doc/html/rfc6455#section-5.1
