# CloudEvents SDK Requirements

<!-- no verify-specs -->

The intent of this document to describe a minimum set of requirements for new
Software Development Kits (SDKs) for CloudEvents. These SDKs are designed and
implemented to enhance and speed up CloudEvents integration. As part of
community efforts CloudEvents team committed to support and maintain the
following SDKs:

- [C#/.NET SDK](https://github.com/cloudevents/sdk-csharp)
- [Go SDK](https://github.com/cloudevents/sdk-go)
- [Java SDK](https://github.com/cloudevents/sdk-java)
- [JavaScript SDK](https://github.com/cloudevents/sdk-javascript)
- [PHP SDK](https://github.com/cloudevents/sdk-php)
- [PowerShell SDK](https://github.com/cloudevents/sdk-powershell)
- [Python SDK](https://github.com/cloudevents/sdk-python)
- [Ruby SDK](https://github.com/cloudevents/sdk-ruby)
- [Rust SDK](https://github.com/cloudevents/sdk-rust)

This is intended to provide guidance and requirements for SDK authors. This
document is intended to be kept up to date with the CloudEvents spec.

The SDKs are community driven activities and are (somewhat) distinct from the
CloudEvents specification itself. In other words, while ideally the SDKs are
expected to keep up with changes to the specification, it is not a hard
requirement that they do so. It will be continguent on the specific SDK's
maintainers to find the time.

## Contribution Acceptance

Being an open source community the CloudEvents team is open for new members as
well open to their contributions. In order to ensure that an SDK is going to be
supported and maintained the CloudEvents community would like to ensure that:

- Each SDK has active points of contact.
- Each SDK supports the latest(N), and N-1, major releases of the
  [CloudEvent spec](spec.md)\*.
- Within the scope of a major release, only support for the latest minor
  version is needed.

Support for release candidates is not required, but strongly encouraged.

\* Note: v1.0 is a special case and it is recommended that as long as v1.0
  is the latest version, SDKs should also support v0.3.

## Technical Requirements

Each SDK MUST meet these requirements:

- Supports CloudEvents at spec milestones and ongoing development version.
  - Encode a canonical Event into a transport specific encoded message.
  - Decode transport specific encoded messages into a Canonical Event.
- Idiomatic usage of the programming language.
  - Using current language version(s).
- Supports HTTP transport renderings in both `structured` and `binary`
  content mode.

### Object Model Structure Guidelines

Each SDK will provide a generic CloudEvents class/object/structure that
represents the canonical form of an Event.

The SDK should enable users to bypass implementing transport specific encoding
and decoding of the CloudEvents `Event` object. The general flow for Objects
should be:

```
Event (-> Message) -> Transport
```

and

```
Transport (-> Message) -> Event
```

An SDK is not required to implement a wrapper around the transport, the focus
should be around allowing programming models to work with the high level `Event`
object, and providing tools to take the `Event` and turn it into something that
can be used with the implementation transport selected.

At a high level, the SDK needs to be able to help with the following tasks:

1. Compose an Event.
1. Encode an Event given a transport and encoding (into a Transport Message if
   appropriate).
1. Decode an Event given a transport specific message, request or response (into
   a Transport Message if appropriate).

#### Compose an Event

Provide a convenient way to compose both a single message and many messages.
Implementers will need a way to quickly build up and convert their event data
into the a CloudEvents encoded Event. In practice there tend to be two aspects
to event composition,

1. Event Creation

- "I have this data that is not formatted as a CloudEvent and I want it to be."

1. Event Mutation

- "I have a CloudEvents formatted Event and I need it to be a different Event."
- "I have a CloudEvents formatted Event and I need to mutate the Event."

Event creation is highly idiomatic to the SDK language.

Event mutation tends to be solved with an accessor pattern, like getters and
setters. But direct key access could be leveraged, or named-key accessor
functions.

In either case, there MUST be a method for validating the resulting Event object
based on the parameters set, most importantly the CloudEvents spec version.

#### Encode/Decode an Event

Each SDK MUST support encoding and decoding an Event with regards to a transport
and encoding:

- Each SDK MUST support structured-mode messages for each transport that it
  supports.
- Each SDK SHOULD support binary-mode messages for each transport that it
  supports.
- Each SDK SHOULD support batch-mode messages for each transport that it
  supports (where the event format and transport combination supports batch mode).
- Each SDK SHOULD indicate which modes it supports for each supported event
  format, both in the [table below](#feature-support) and in any SDK-specific
  documentation provided.

Note that when decoding an event, media types MUST be matched
case-insensitively, as specified in [RFC 2045]
(https://tools.ietf.org/html/rfc2045).

#### Data

Data access from the event has some considerations, the Event at rest could be
encoded into the `base64` form, as structured data, or as a wire format like
`json`. An SDK MUST provide a method for unpacking the data from these formats
into a native format.

#### Extensions

Supporting CloudEvents extensions is idiomatic again, but a method that mirrors
the data access seems to work.

#### Validation

Validation MUST be possible on an individual Event. Validation MUST take into
account the spec version, and all the requirements put in-place by the spec at
each version.

SDKs SHOULD perform validation on context attribute values provided to it by
the SDK user. This will help ensure that only valid CloudEvents are generated.

## Documentation

Each SDK must provide examples using at least HTTP transport of:

- Composing an Event.
- Encoding and sending a composed Event.
- Receiving and decoding an Event.

## Feature Support

Each SDK must update the following "support table" periodically to ensure
they accurately the status of each SDK's support for the stated features.

<!--
Do these commands in vi with the cursor after these comments.

Easiest to edit table by first doing this:
:g/^|/s/ :heavy_check_mark: / :y: /g
and making the window wide enough that lines don't wrap. Then it should look nice.

Undo it when done:
:g/^|/s/ :y: / :heavy_check_mark: /g
-->

| Feature                                                                                                                                       | C#  | Go  | Java | JS  | PHP | PS  | Python | Ruby | Rust |
|:----------------------------------------------------------------------------------------------------------------------------------------------| :-: | :-: | :--: | :-: | :-: | :-: | :----: | :--: | :--: |
| **[v1.0](https://github.com/cloudevents/spec/tree/v1.0)**                                                                                     |
| [CloudEvents Core](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md)                                                       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:    | :heavy_check_mark:  | :heavy_check_mark:  |
| Event Formats                                                                                                                                 |
| [Avro](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md)                                                    | :heavy_check_mark: |     | :x:  | :x: |     |     |        | :x: | :x:  |
| [Avro Compact](https://github.com/cloudevents/spec/blob/main/cloudevents/working-drafts/avro-compact-format.md)                       | :heavy_check_mark: |     | :x:  | :x: |     |     |        |     | :x:  |
| [JSON](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md)                                                    | :heavy_check_mark: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [Protobuf ](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/protobuf-format.md)                                           | :heavy_check_mark: |     | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |
| Bindings / Content Modes                                                                                                                      |
| [AMQP Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/amqp-protocol-binding.md#31-binary-content-mode)           | :heavy_check_mark: |     | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |
| [AMQP Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/amqp-protocol-binding.md#32-structured-content-mode)   | :heavy_check_mark: |     | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |
| [HTTP Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md#31-binary-content-mode)           | :heavy_check_mark: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [HTTP Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md#32-structured-content-mode)   | :heavy_check_mark: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [HTTP Batch](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md#33-batched-content-mode)           | :heavy_check_mark: |     | :x:  | :x: |     |     |        | :heavy_check_mark: | :heavy_check_mark:  |
| [Kafka Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md#32-binary-content-mode)         | :heavy_check_mark: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :x: | :heavy_check_mark:  |
| [Kafka Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md#33-structured-content-mode) | :heavy_check_mark: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :x: | :heavy_check_mark:  |
| [MQTT v5 Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/mqtt-protocol-binding.md#31-binary-content-mode)        | :x: |     | :x:  | :heavy_check_mark: |     |     |        | :x: | :x:  |
| [MQTT Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/mqtt-protocol-binding.md#32-structured-content-mode)   | :heavy_check_mark: |     | :x:  | :heavy_check_mark: |     |     |        | :x: | :x:  |
| [NATS Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/nats-protocol-binding.md)                                  | :x: |     | :x:  | :x: |     |     |        | :x: | :heavy_check_mark:  |
| [NATS Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/nats-protocol-binding.md)                              | :x: |     | :x:  | :x: |     |     |        | :x: | :heavy_check_mark:  |
| [WebSockets Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/websockets-protocol-binding.md)                      | :x: |     | :x:  | :heavy_check_mark: |     |     |        | :x: | :x:  |
| [WebSockets Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/websockets-protocol-binding.md)                  | :x: |     | :x:  | :heavy_check_mark: |     |     |        | :x: | :x:  |
| Proprietary Bindings                                                                                                                          |
| [RocketMQ](https://github.com/apache/rocketmq-externals/blob/master/rocketmq-cloudevents-binding/rocketmq-transport-binding.md)               | :x: |     | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |
|                                                                                                                                               |
| **[v0.3](https://github.com/cloudevents/spec/tree/v0.3)**                                                                                     |
| [CloudEvents Core](https://github.com/cloudevents/spec/blob/v0.3/spec.md)                                                                     | :x: | :heavy_check_mark: | :heavy_check_mark:  | :heavy_check_mark: | :x: | :x: | :heavy_check_mark:    | :heavy_check_mark:  | :heavy_check_mark:  |
| Event Formats                                                                                                                                 |
| [AMQP](https://github.com/cloudevents/spec/blob/v0.3/amqp-format.md)                                                                          | :x: |     | :x:  | :x: |     |     |        | :x: | :x:  |
| [JSON](https://github.com/cloudevents/spec/blob/v0.3/json-format.md)                                                                          | :x: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [Protobuf](https://github.com/cloudevents/spec/blob/v0.3/protobuf-format.md)                                                                  | :x: |     | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |
| Bindings / Content Modes                                                                                                                      |
| [AMQP Binary](https://github.com/cloudevents/spec/blob/v0.3/amqp-transport-binding.md#31-binary-content-mode)                                 | :x: |     | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |
| [AMQP Structured](https://github.com/cloudevents/spec/blob/v0.3/amqp-transport-binding.md#32-structured-content-mode)                         | :x: |     | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |
| [HTTP Binary](https://github.com/cloudevents/spec/blob/v0.3/http-transport-binding.md)                                                        | :x: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [HTTP Structured](https://github.com/cloudevents/spec/blob/v0.3/http-transport-binding.md)                                                    | :x: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [HTTP Batch](https://github.com/cloudevents/spec/blob/v0.3/http-transport-binding.md)                                                         | :x: |     | :x:  | :x: |     |     |        | :heavy_check_mark: | :heavy_check_mark:  |
| [Kafka Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md#32-binary-content-mode)         | :x: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :x: | :heavy_check_mark:  |
| [Kafka Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md#33-structured-content-mode) | :x: |     | :heavy_check_mark:  | :heavy_check_mark: |     |     | :heavy_check_mark:    | :x: | :heavy_check_mark:  |
| [MQTT v5 Binary](https://github.com/cloudevents/spec/blob/v0.3/mqtt-transport-binding.md)                                                     | :x: |     | :x:  | :x: |     |     |        | :x: | :x:  |
| [MQTT Structured](https://github.com/cloudevents/spec/blob/v0.3/mqtt-transport-binding.md)                                                    | :x: |     | :x:  | :x: |     |     |        | :x: | :x:  |
| [NATS Binary](https://github.com/cloudevents/spec/blob/v0.3/nats-transport-binding.md)                                                        | :x: |     | :x:  | :x: |     |     |        | :x: | :heavy_check_mark:  |
| [NATS Structured](https://github.com/cloudevents/spec/blob/v0.3/nats-transport-binding.md)                                                    | :x: |     | :x:  | :x: |     |     |        | :x: | :heavy_check_mark:  |
| [WebSockets Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/websockets-protocol-binding.md)                      | :x: |     | :x:  | :heavy_check_mark: |     |     |        | :x: | :x:  |
| [WebSockets Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/websockets-protocol-binding.md)                  | :x: |     | :x:  | :heavy_check_mark: |     |     |        | :x: | :x:  |
| Proprietary Bindings                                                                                                                          |
| [RocketMQ](https://github.com/apache/rocketmq-externals/blob/master/rocketmq-cloudevents-binding/rocketmq-transport-binding.md)               | :x: |     | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |

