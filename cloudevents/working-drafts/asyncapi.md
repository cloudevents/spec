# AsyncAPI With CloudEvents - Version 1.0.3-wip

## Purpose

Asynchronous APIs, e.g., events, can be specified in AsyncAPI, similar to how
RESTful APIs can be specified in [OpenAPI](https://swagger.io/specification/).
When defining new events in an API-first approach it can be hard to add
CloudEvents headers or fields according to spec. This makes following the
standard harder. This document will clarify how CloudEvents headers can be
specified in AsyncAPI.

## Usage

Depending on the protocol and the mode (binary/structured), the inclusion of the
CloudEvents fields varies.

## Structured Mode

In structured mode, the entire event, attributes, and data are encoded in the
message body. When using structured mode, the usage only varies depending on the
serialization format:

| Format | Example                                                                 | Include                                  |
| ------ | ----------------------------------------------------------------------- | ---------------------------------------- |
| JSON   | [Short Example](#json-example) [Full Example](./asyncapi-examples/light-switch-events-structured-json.yaml) | [Reference](../formats/cloudevents.json) |

### JSON Example

To add CloudEvents in structured mode, the following `allOf` reference needs to
be added:

```yaml
components:
  messages:
    messageKey:
      payload:
        type: object
        allOf:
        - $ref: 'https://raw.githubusercontent.com/cloudevents/spec/v1.0.2/cloudevents/formats/cloudevents.json'
```

See also: [Full Example](./asyncapi-examples/light-switch-events-structured-json.yaml)

## Binary Mode

In binary mode, protocol-specific bindings are mapping fields to protocol
content-type metadata property or headers; therefore, the AsyncAPI format needs
to depend on the protocol:

| Protocol Binding                               | Example                                                              | Trait                                                            |
| ---------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- |
| [Kafka](../bindings/kafka-protocol-binding.md) | [Short Example](#avro-example) [Full Example](./asyncapi-examples/light-switch-events-binary-kafka.yaml) | [Trait](./asyncapi-traits/cloudevents-headers-kafka-binary.yaml) |

### Avro Example

To add CloudEvents in binary mode, the following `traits` reference needs to
be added:

```yaml
components:
  messages:
    messageKey:
      traits:
      - $ref: 'https://raw.githubusercontent.com/cloudevents/spec/main/cloudevents/working-drafts/asyncapi-traits/cloudevents-headers-kafka-binary.yaml'
```

See also: [Full Example](./asyncapi-examples/light-switch-events-binary-kafka.yaml)
