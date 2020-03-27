# CloudEvent Specs for Proprietary Protocols and Encodings

Disclaimer: CloudEvents does not endorse these protocols or specs, and does not
ensure that they are up to date with the current version of CloudEvents. That is
the responsibility of the respective project maintainers.

- [Apache RocketMQ Transport Binding](https://github.com/apache/rocketmq-externals/blob/master/rocketmq-cloudevents-binding/rocketmq-transport-binding.md)
- [Google Cloud Pub/Sub Protocol Binding](https://github.com/google/knative-gcp/blob/master/docs/spec/pubsub-protocol-binding.md)

**Want to add a binding to a proprietary transport?**

- Create a spec that follows the structure of an existing binding specification (e.g. [http](http-protocol-binding.md) or [amqp](amqp-protocol-binding.md)) - this will help SDK development.
  - **NOTES:**
    - The spec needs to be publically accessible and managed by the proposing organization.
    - The spec should clearly state the version(s) of CloudEvents supported.
- Open a pull request against this file.
- Respond to any comments on the pull request and potentially join one of the regularly scheduled working group sessions.
