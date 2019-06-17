# Test cases for CloudEvents encoding

These cases provide a set of "difficult" or edge-case encodings of valid CloudEvents, for use in testing various CloudEvents implementations. The cases cover transformation between a [canonical JSON object](../json-format.md) and a transport-specific output. Test cases are organized by common prefix with the following suffixes denoting different transports:

Suffix | Encoding
--- | ---
`json` | [JSON event](../json-format.md)
`http` | [HTTP binary request](../http-transport-binding.md)
`http-json` | [HTTP structured request](../http-transport-binding.md)
`mqtt` | [MQTT binary publish](../mqtt-transport-binding.md)
`mqtt-json` | [MQTT structured publish](../mqtt-transport-binding.md)
`amqp` | [AMQP message](../amqp-transport-binding.md)

If multiple files exist with the same input prefix, they all represent the same CloudEvent rendered across the different transports. For example, given the files:

- `unicode-input.json`
- `unicode-input.http`
- `unicode-input.mqtt`
- `binary-date.json`
- `binary-date.amqp`

These form two sets of tests: the `unicode-input` case is defined for JSON, HTTP, and MQTT, and the `binary-date` case is defined for QSON and AMQP.

Test cases which describe particularly unexpected formats should include comments in the JSON document using Javascript comment format (`//` or `/* .. */`).

<!-- TODO: translation from batch to multiple individual requests.

What are the semantics if a single message in a JSON batch is incorrect?
 - Missing required fields in one array element?
 - Incorrect field types / values in another element?
-->