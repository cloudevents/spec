# CloudEvent Specs for Proprietary Protocols and Encodings

<!-- no verify-specs -->

Disclaimer: CloudEvents does not endorse these protocols or specs, and does not
ensure that they are up to date with the current version of CloudEvents. That is
the responsibility of the respective project maintainers.

- [Apache RocketMQ Transport Binding](https://github.com/apache/rocketmq-externals/blob/master/rocketmq-cloudevents-binding/rocketmq-transport-binding.md)
- [Google Cloud Pub/Sub Protocol Binding](https://github.com/googleapis/google-cloudevents/blob/main/docs/spec/pubsub.md)

**Want to add a binding to a proprietary transport?**

- Create a spec that follows the structure of an existing binding specification (e.g. [http](bindings/http-protocol-binding.md) or [amqp](bindings/amqp-protocol-binding.md)) - this will help SDK development.
  - **NOTES:**
    - The spec must be publicly accessible and managed by the proposing organization.
    - The spec must clearly state the version(s) of CloudEvents supported.
- Open a pull request against this file.
- Respond to any comments on the pull request and potentially join one of the regularly scheduled working group sessions.
