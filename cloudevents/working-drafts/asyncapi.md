# AsyncAPI With CloudEvents

This document describes how CloudEvents can be defined in [AsyncAPI v3](https://www.asyncapi.com/docs/reference/specification/v3.0.0).
It was created as a follow-up after discussion [cloudevents/spec#1276](https://github.com/cloudevents/spec/issues/1276).

## Purpose

Asynchronous APIs, e.g., events, can be specified in AsyncAPI, similar to how RESTful APIs can be specified in [OpenAPI](https://swagger.io/specification/).
When defining new events in an API-first approach it can be hard to add CloudEvents headers or fields according to spec.
This makes following the standard harder.
This document should clarify how CloudEvents headers can be specified in AsyncAPI.

## Usage

Depending on the protocol and the mode (binary/structured), the inclusion of the CloudEvents fields varies.

## Structured Mode

In structured mode, the entire event, attributes, and data are encoded in the message body.
When using structured mode, the usage only varies depending on the serialization format:

| Format | Example                                                                 | Include                                  |
| ------ | ----------------------------------------------------------------------- | ---------------------------------------- |
| JSON   | [Example](./asyncapi-examples/light-switch-events-structured-json.yaml) | [Reference](../formats/cloudevents.json) |

## Binary Mode

In binary mode, protocol-specific bindings are mapping fields to protocol content-type metadata property or headers; therefore, the AsyncAPI format needs to depend on the protocol:

| Protocol Binding                               | Example                                                              | Trait                                                            |
| ---------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [Kafka](../bindings/kafka-protocol-binding.md) | [Example](./asyncapi-examples/light-switch-events-binary-kafka.yaml) | [Trait](./asyncapi-traits/cloudevents-headers-kafka-binary.yaml) |
