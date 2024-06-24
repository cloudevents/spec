# CloudEvents Zero Trust (Pre-proposal)

## Abstract

The ultimate aim is to add zero trust capabilities to cloudevents. To achieve this, we will create two proposals. The first proposal, which we will call the pre-proposal, will explore the different protocols to understand their limitations and how we can implement zero trust. The second proposal will design the implementation of how we can achieve zero trust in cloudevents..

It is important to note that cloudevents’ protocols operate at the application level, encompassing both encodings and wire protocols. This analysis will separate encodings from wire protocols, as encoding refers to the format in which data is sent and does not restrict the security libraries or tools we can use, unlike wire protocols.

The primary focus will be on where metadata can be stored, such as headers in the HTTP protocol, in each protocol, rather than an in-depth examination of each protocol. Having a place to store metadata per request will allow us to configure and send any necessary security-related information, facilitating the implementation of zero trust. This proposal will not delve into various security algorithms or tools to be described in the metadata.

## Wire Protocols

### AMQP

AMQP supports metadata similar to how HTTP handles this. For AMQP, headers live within the message itself. These headers live within the AMQP message meaning that the headers are sent along with the payload, while HTTP sends headers prior to the payload being sent.

Message properties may look something like this and is part of the content header frame where a frame is how AMQP partitions a request over the wire:

```
{
  "content_type": "application/json",
  "delivery_mode": 2,
  "headers": {
    "region": "US-East",
    "order_type": "new"
  }
}
```

The content data is in the content body frame:

```
{
  "order_id": "789",
  "product": "widget",
  "quantity": 10
}
```

All frame are sent together in AMQP, while headers are sent separately from the payload in HTTP.

### HTTP

HTTP supports a metadata format known as [headers](https://datatracker.ietf.org/doc/html/rfc2616#section-4.2). The HTTP RFC does not specify a limit for header sizes, but it is important to call out that implementing web servers may have some limits set, at least as some default. For example, Apache HTTP server defaults to a max header size of 8KB.

```
> GET /data HTTP/1.1
> Host: api.example.com
> Authorization: Bearer your-token-here
> Accept: application/json
>
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 79
<
{
  "status": "success",
  "data": [
    {"id": 1, "name": "Item 1", "value": "A"},
    {"id": 2, "name": "Item 2", "value": "B"}
  ]
}
```

Here we see an example request and response of some curl command, I want to highlight two areas: the headers and the response’s payload.

If we take a look at the headers section we actually see both the request and response headers from the curl command.

The request headers and various other important request information:

```
> GET /data HTTP/1.1
> Host: api.example.com
> Authorization: Bearer your-token-here
> Accept: application/json
```

Then we have the response headers:

```
< HTTP/1.1 200 OK
< Content-Type: application/json
< Content-Length: 79
```

I want to highlight the headers as a separate item from the response’s payload, because headers are sent independently of the payload. When sending an HTTP request or response, we first send the HTTP headers, and then the payloads.

Regardless of how the headers are sent, it is important that custom metadata can be added as headers. This allows us to populate them with the necessary information to verify requests and its senders.

### Kafka

Headers are a concept within Kafka since v0.11.0, and I’d argue a little more powerful than HTTP headers. The biggest benefit is that headers in Kafka are actually byte arrays. Meaning header values allow for more complex encodings, unlike HTTP where header values are generally textual.

However, because of the need to encode these headers a certain way, the producer and consumer must agree on some encoding for them to understand the contents of the headers.

It is important to note that since Kafka is architected as a producer and consumer messaging service, any consumer ingesting message will see the contents of the headers. I do not think this affects zero trust, but it is something to think about when we write the technical specification for zero trust.

```
[Record]
Length:          64                      (0x40)
Attributes:      0                       (0x00)
Timestamp Delta: 0                       (0x00 00)
Offset Delta:    0                       (0x00 00)
Key Length:      3                       (0x00 00 00 03)
Key:             key                     (0x6B 65 79)
Value Length:    42                      (0x00 00 00 2A)
Value:           {"name": "example item", "value": "example value"}
                                        (0x7B 22 6E 61 6D 65 22 3A 20 22 65 78 61 6D 70 6C 65 20 69 74 65 6D 22 2C 20 22 76 61 6C 75 65 22 3A 20 22 65 78 61 6D 70 6C 65 20 76 61 6C 75 65 22 7D)
Header Count:    2                       (0x02)

Header 1:
Key Length:      10                      (0x00 00 00 0A)
Key:             headerKey1              (0x68 65 61 64 65 72 4B 65 79 31)
Value Length:    11                      (0x00 00 00 0B)
Value:           headerValue1            (0x68 65 61 64 65 72 56 61 6C 75 65 31)

Header 2:
Key Length:      10                      (0x00 00 00 0A)
Key:             headerKey2              (0x68 65 61 64 65 72 4B 65 79 32)
Value Length:    11                      (0x00 00 00 0B)
Value:           headerValue2            (0x68 65 61 64 65 72 56 61 6C 75 65 32)
```

### MQTT

With the release of v5 of MQTT, MQTT has added support for variable headers.

See [MQTT spec](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901025) under section 2.2 Variable Header

It is important to note that the format of variable headers is dependent on the MQTT packet type, and that variable headers are only available in a subset of the MQTT control packets.

* PUBLISH (only when [QoS](https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels/) > 0)
* PUBACK
* PUBREC
* PUBREL
* PUBCOMP
* SUBSCRIBE
* SUBACK
* UNSUBSCRIBE
* UNSUBACK


Note that the `PUBLISH` packet type may include a variable header ***only if*** the quality of service (QoS) is greater than zero. QoS is the level of guarantee that a message has been sent and received with QoS of zero makes no guarantees on whether the receiver has received the message.
PUBLISH

### NATS

Out of all protocols, NATS limits its header encoding to ASCII text, which should not be an issue for zero trust, but wanted to call it out. Another key concept in NATS is that messages are asynchronous.

```
Subject: user.login
Headers:
  Content-Type: application/json
  trace-id: 123456
Payload:
{
  "username": "john.doe",
  "action": "login"
}
```

### WebSockets

WebSockets are a high-level abstraction of the TCP protocol. They utilize HTTP to first provide the handshake and then upgrade to a full-duplex TCP connection. This means that metadata is primarily restricted to what can be sent during the initial handshake. Consequently, WebSockets are more restrictive in terms of metadata transmission compared to other protocols.

This may mean we have to handle web sockets slightly differently with whatever zero trust approach we take.

## Other

cloudevents lists a few other “protocols” which some are encodings and others are abstractions on top of other protocols. Luckily these other types do not hinder any implementation of zero trust and instead rely on the transport protocol the data is being sent. However, this section will go over how these higher level protocols will work with the metadata concepts in the prior protocols.

### AVRO | JSON | Protobuf | XML

These are the encodings that cloudevents supports: AVRO, JSON, protobuf, and XML. Encodings do not affect whether we can rely on metadata, and will have no hindrance on the implementation of zero trust.

### Webhook

Webhooks are a high-level abstraction built on top of the HTTP protocol. They allow clients to send arbitrary HTTP requests to a specified endpoint in response to events. This flexibility means that webhooks do not limit the underlying wire protocol used for transmission. Consequently, webhooks enable the use of the protocol’s metadata format and other mechanisms to ensure the trustworthiness of requests.

## Summary

We have explored each wire protocol, and while some have more limitations than
others, cloudevents should be able to support some form of zero trust. The
biggest limitation is MQTT due to only supporting header-like concepts in later
versions. All other limitations are manageable, like NATS' and HTTP's ASCII
only support.
