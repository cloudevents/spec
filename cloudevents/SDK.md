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
- [Kotlin SDK](https://github.com/cloudevents/sdk-kotlin)
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

1. Compose an Event [[CloudEventBuilder](#cloudeventbuilder)].
1. Encode an Event given a transport and encoding (into a Transport Message if
   appropriate) [[Encode](#encode)].
1. Decode an Event given a transport specific message, request or response (into
   a Transport Message if appropriate) [[Decode](#decode)].

### Data Model

#### CloudEvent

Each SDK will provide a generic CloudEvents class/object/structure that
represents the canonical form of an Event.

#### CloudEventMapping

The CloudEventMapping provides a class/object/structure which is designed to be a
transport agnostic.

The properties are:

- **Body(object):** the cloud event once it has been encoded using the format.
This should map to a body field for the transport.
- **ContentType(string):** a string which describes the format of the body.
The transport protocol defines where this field is transmitted.
- **Metadata(object):** A transport specific representation of properties which
is to be used for the transport.

#### CloudEventAttribute

The properties are:

- **Key(string):** The key/name of the attribute.
- **ValueType(string):** What data type must the value be.
- **Required(boolean):** When validating a cloud event is this attribute required to be present.

### SDK Services

#### CloudEventBuilder

Provide a convenient way to compose a CloudEvent representation of an event.
Implementers will need a way to quickly build up and convert their event data
into the a CloudEvents encoded Event. In practice there tend to be two modes
to event composition,

1. Event Creation

- "I have this data that is not formatted as a CloudEvent and I want it to be."

1. Event Mutation

- "I have a CloudEvents formatted Event and I need it to be a different Event."
- "I have a CloudEvents formatted Event and I need to mutate the Event."

The builder is to enable setting the following in a language idiomatic manner
in addition to the core cloud event properties. This can be achieved via be methods or properties:

- **Extensions([Extension](#extension)[]):** Adds support for additional attributes.

In addition there must be the following methods:

- [Validate](#validate)
- [Build](#build)
- [Mutate](#mutate)

##### Validate

Validation MUST be possible on an individual Event. Validation MUST take into
account the spec version, and all the requirements put in-place by the spec at
each version.

SDKs SHOULD perform validation on context attribute values provided to it by
the SDK user. This will help ensure that only valid CloudEvents are generated.

##### Build

Event build is responsible for generating a [CloudEvent](#cloudevent) using the
properties/attributes set on the builder

The build operation should perform a validation of the event, raising an error if
the validation fails.

**Returns:** [CloudEvent](#cloudevent)

##### Mutate

Event mutation tends to be solved with an accessor pattern, like getters and
setters. But direct key access could be leveraged, or named-key accessor
functions.

The mutate operation should perform a validation of the event, raising an error if
the validation fails.

**Parameters:** adapter([Adapter](#adapter)) & data(object) which corresponds to
what is to be mutated.

**Returns:** [CloudEvent](#cloudevent)

#### CloudEventConverter

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

The converter is to enable setting the following in a language idiomatic manner
which could be methods or properties:

- **Formatters([Formatter](#formatter)):** Sets the possible formatters to be used when
converting a [CloudEvent](#cloudevent) to/from a [CloudEventMapping](#cloudeventmapping) representation.
- **Injectors([Injector](#injector)):** Sets the injectors which should be used to inject
additional attributes into the CloudEvent.
- **Verifiers([Verifier](#verifier)):** Sets the verification which should be done on the
CloudEvent prior to FromCloudEvent or after ToCloudEvent on the formatter.
- **DefaultContentType(string):** What content type should be used for encoding if none is provided
- **Binder([Binder](#binder)):** Sets how metadata is represented within the [CloudEventMapping](#cloudeventmapping).

In addition there must be the following methods:

- [Encode](#encode)
- [Decode](#decode)

##### Encode

The encode operation is responsible for taking a [CloudEvent](#cloudevent),
using the configured formatter to generate a [CloudEventMapping](#cloudeventmapping).

This mapping can then be optionally bound to a transport specific representation which
can then be used to easily send the cloud event via the transport.

**Parameters:** event([CloudEvent](#cloudevent)) & optionally contentType(string)

**Returns:** [CloudEventMapping](#cloudeventmapping)

##### Decode

This performs the inverse of [Encode](#encode) which is to take a [CloudEventMapping](#cloudeventmapping)
constructed using information from a transport and give the developer a
[CloudEvent](#cloudevent) which they can use.

This process involves [Debinding](#debind) the metadata to a generic representation,
and then using the configured formatter to produce a [CloudEvent](#cloudevent).

Note that when decoding an event, the media type's type and subtype MUST be
matched case-insensitively, as specified in
[RFC6838, section 4.2](https://www.rfc-editor.org/info/rfc6838/#section-4.2).

**Parameters:** mapping([CloudEventMapping](#cloudeventmapping))

**Returns:** [CloudEvent](#cloudevent)

### API Definitions

#### Adapter

An adapter is needed when you need to convert an existing events into CloudEvents.
This will typically mean extracting metadata from the event which is to then be used
as CloudEvents attributes.

##### Transform

**Parameters:** event([CloudEvent](#cloudevent)) & data(object) which corresponds to what is to be mutated.

**Returns:** [CloudEvent](#cloudevent)

#### Formatter

Is responsible for the conversion between [CloudEvent](#cloudevent) and
[CloudEventMapping](#cloudeventmapping). This is what makes it possible to simultaneously
support multiple formats ie json & protobuf.

This will influence what attributes remain in the body & which one’s are transported
as metadata.

The formatter is to expose a readonly list of supported content types. 

##### FromCloudEvent

Called as part of the encoding process.

**Parameters:** event([CloudEvent](#cloudevent)) & contentType(string)

**Returns:** [CloudEventMapping](#cloudeventmapping)

##### ToCloudEvent

Called as part of the decoding process

**Parameters:** mapping([CloudEventMapping](#cloudeventmapping))

**Returns:** [CloudEvent](#cloudevent)

#### Binder

Is responsible for ensuring that the [CloudEventMapping](#cloudeventmapping) metadata can be
converted to/from a transport agnostic form.

For instance http would use ie key-value collection for http headers or amqp would use
a metadata object.

#### Bind

Called as part of the encoding process.

**Parameters:** mapping([CloudEventMapping](#cloudeventmapping))

**Returns:** [CloudEventMapping](#cloudeventmapping)

##### De-bind

Called as part of the decoding process.

**Parameters:** mapping([CloudEventMapping](#cloudeventmapping))

**Returns:** [CloudEventMapping](#cloudeventmapping)

#### Extension

Supporting CloudEvents extensions is idiomatic again, but a method that mirrors
the data access seems to work.

The extension is to expose a readonly list of supported attributes
[CloudEventAttribute](#cloudeventattribute).

#### Injector

The injector is responsible for setting additional attribute values if the attribute
is not already present.

An injector will commonly be used alongside [Extensions](#extension).

Injectors must provide the following methods:

- [Inject](#inject)

##### Inject

Called as the first encoding step. 

**Parameters:** event([CloudEvent](#cloudevent))

**Returns:** [CloudEvent](#cloudevent)

#### Verifier

The verifier is responsible for providing additional verification of a cloudeve

A verifier will commonly be used alongside [Extensions](#extension).

Verifiers must provide the following methods:

- [Verify](#verify)

##### Verify

Called as part of the encoding process just prior to the formatting step. 

**Parameters:** [CloudEvent](#cloudevent)

**Returns:** valid(boolean)

### Data

Data access from the event has some considerations, the Event at rest could be
encoded into the `base64` form, as structured data, or as a wire format like
`json`. An SDK MUST provide a method for unpacking the data from these formats
into a native format.

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

| Feature                                                                                                                                       | C#  | Go  | Java | Kotlin | JS  | PHP | PS  | Python | Ruby | Rust |
|:----------------------------------------------------------------------------------------------------------------------------------------------| :-: | :-: | :--: | :--: | :-: | :-: | :-: | :----: | :--: | :--: |
| **[v1.0](https://github.com/cloudevents/spec/tree/v1.0)**                                                                                     |
| [CloudEvents Core](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md)                                                       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:    | :heavy_check_mark:  | :heavy_check_mark:  |
| Event Formats                                                                                                                                 |
| [Avro](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md)                                                    | :heavy_check_mark: |     | :x:  |     | :x: |     |     |        | :x: | :x:  |
| [Avro Compact](https://github.com/cloudevents/spec/blob/main/cloudevents/working-drafts/avro-compact-format.md)                       | :heavy_check_mark: |     | :x:  |     | :x: |     |     |        |     | :x:  |
| [JSON](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md)                                                    | :heavy_check_mark: |     | :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [Protobuf ](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/protobuf-format.md)                                           | :heavy_check_mark: |     | :heavy_check_mark:  | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |
| Bindings / Content Modes                                                                                                                      |
| [AMQP Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/amqp-protocol-binding.md#31-binary-content-mode)           | :heavy_check_mark: |     | :heavy_check_mark:  |     | :x: |     |     |        | :x: | :x:  |
| [AMQP Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/amqp-protocol-binding.md#32-structured-content-mode)   | :heavy_check_mark: |     | :heavy_check_mark:  |     | :x: |     |     |        | :x: | :x:  |
| [HTTP Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md#31-binary-content-mode)           | :heavy_check_mark: |     | :heavy_check_mark:  |     | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [HTTP Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md#32-structured-content-mode)   | :heavy_check_mark: |     | :heavy_check_mark:  |     | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [HTTP Batch](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md#33-batched-content-mode)           | :heavy_check_mark: |     | :x:  |     | :x: |     |     |        | :heavy_check_mark: | :heavy_check_mark:  |
| [Kafka Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md#32-binary-content-mode)         | :heavy_check_mark: |     | :heavy_check_mark:  |     | :heavy_check_mark: |     |     | :heavy_check_mark:    | :x: | :heavy_check_mark:  |
| [Kafka Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md#33-structured-content-mode) | :heavy_check_mark: |     | :heavy_check_mark:  |     | :heavy_check_mark: |     |     | :heavy_check_mark:    | :x: | :heavy_check_mark:  |
| [MQTT v5 Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/mqtt-protocol-binding.md#31-binary-content-mode)        | :x: |     | :x:  |     | :heavy_check_mark: |     |     |        | :x: | :x:  |
| [MQTT Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/mqtt-protocol-binding.md#32-structured-content-mode)   | :heavy_check_mark: |     | :x:  |     | :heavy_check_mark: |     |     |        | :x: | :x:  |
| [NATS Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/nats-protocol-binding.md)                                  | :x: |     | :x:  |     | :x: |     |     |        | :x: | :heavy_check_mark:  |
| [NATS Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/nats-protocol-binding.md)                              | :x: |     | :x:  |     | :x: |     |     |        | :x: | :heavy_check_mark:  |
| [WebSockets Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/websockets-protocol-binding.md)                      | :x: |     | :x:  |     | :heavy_check_mark: |     |     |        | :x: | :x:  |
| [WebSockets Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/websockets-protocol-binding.md)                  | :x: |     | :x:  |     | :heavy_check_mark: |     |     |        | :x: | :x:  |
| Proprietary Bindings                                                                                                                          |
| [RocketMQ](https://github.com/apache/rocketmq-externals/blob/master/rocketmq-cloudevents-binding/rocketmq-transport-binding.md)               | :x: |     | :heavy_check_mark:  |     | :x: |     |     |        | :x: | :x:  |
| [RabbitMQ](https://github.com/knative-extensions/eventing-rabbitmq/blob/main/cloudevents-protocol-spec/spec.md)                               | :x: |     |      |     |     |     |     |        |     |      |
|                                                                                                                                               |
| **[v0.3](https://github.com/cloudevents/spec/tree/v0.3)**                                                                                     |
| [CloudEvents Core](https://github.com/cloudevents/spec/blob/v0.3/spec.md)                                                                     | :x: | :heavy_check_mark: | :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | :heavy_check_mark:    | :heavy_check_mark:  | :heavy_check_mark:  |
| Event Formats                                                                                                                                 |
| [AMQP](https://github.com/cloudevents/spec/blob/v0.3/amqp-format.md)                                                                          | :x: |     | :x:  |     | :x: |     |     |        | :x: | :x:  |
| [JSON](https://github.com/cloudevents/spec/blob/v0.3/json-format.md)                                                                          | :x: |     | :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [Protobuf](https://github.com/cloudevents/spec/blob/v0.3/protobuf-format.md)                                                                  | :x: |     | :heavy_check_mark:  | :heavy_check_mark:  | :x: |     |     |        | :x: | :x:  |
| Bindings / Content Modes                                                                                                                      |
| [AMQP Binary](https://github.com/cloudevents/spec/blob/v0.3/amqp-transport-binding.md#31-binary-content-mode)                                 | :x: |     | :heavy_check_mark:  |     | :x: |     |     |        | :x: | :x:  |
| [AMQP Structured](https://github.com/cloudevents/spec/blob/v0.3/amqp-transport-binding.md#32-structured-content-mode)                         | :x: |     | :heavy_check_mark:  |     | :x: |     |     |        | :x: | :x:  |
| [HTTP Binary](https://github.com/cloudevents/spec/blob/v0.3/http-transport-binding.md)                                                        | :x: |     | :heavy_check_mark:  |     | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [HTTP Structured](https://github.com/cloudevents/spec/blob/v0.3/http-transport-binding.md)                                                    | :x: |     | :heavy_check_mark:  |     | :heavy_check_mark: |     |     | :heavy_check_mark:    | :heavy_check_mark: | :heavy_check_mark:  |
| [HTTP Batch](https://github.com/cloudevents/spec/blob/v0.3/http-transport-binding.md)                                                         | :x: |     | :x:  |     | :x: |     |     |        | :heavy_check_mark: | :heavy_check_mark:  |
| [Kafka Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md#32-binary-content-mode)         | :x: |     | :heavy_check_mark:  |     | :heavy_check_mark: |     |     | :heavy_check_mark:    | :x: | :heavy_check_mark:  |
| [Kafka Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md#33-structured-content-mode) | :x: |     | :heavy_check_mark:  |     | :heavy_check_mark: |     |     | :heavy_check_mark:    | :x: | :heavy_check_mark:  |
| [MQTT v5 Binary](https://github.com/cloudevents/spec/blob/v0.3/mqtt-transport-binding.md)                                                     | :x: |     | :x:  |     | :x: |     |     |        | :x: | :x:  |
| [MQTT Structured](https://github.com/cloudevents/spec/blob/v0.3/mqtt-transport-binding.md)                                                    | :x: |     | :x:  |     | :x: |     |     |        | :x: | :x:  |
| [NATS Binary](https://github.com/cloudevents/spec/blob/v0.3/nats-transport-binding.md)                                                        | :x: |     | :x:  |     | :x: |     |     |        | :x: | :heavy_check_mark:  |
| [NATS Structured](https://github.com/cloudevents/spec/blob/v0.3/nats-transport-binding.md)                                                    | :x: |     | :x:  |     | :x: |     |     |        | :x: | :heavy_check_mark:  |
| [WebSockets Binary](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/websockets-protocol-binding.md)                      | :x: |     | :x:  |     | :heavy_check_mark: |     |     |        | :x: | :x:  |
| [WebSockets Structured](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/websockets-protocol-binding.md)                  | :x: |     | :x:  |     | :heavy_check_mark: |     |     |        | :x: | :x:  |
| Proprietary Bindings                                                                                                                          |
| [RocketMQ](https://github.com/apache/rocketmq-externals/blob/master/rocketmq-cloudevents-binding/rocketmq-transport-binding.md)               | :x: |     | :heavy_check_mark:  |     | :x: |     |     |        | :x: | :x:  |

