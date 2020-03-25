# CloudEvent Specs for Proprietary Protocols and Encodings

Disclaimer: CloudEvents does not endorse these protocols or specs, and does not
ensure that they are up to date with the current version of CloudEvents. That is
the responsibility of the respective project maintainers.

- [Apache RocketMQ Transport Binding](https://github.com/apache/rocketmq-externals/blob/master/rocketmq-cloudevents-binding/rocketmq-transport-binding.md)
- [Google Cloud Pub/Sub Protocol Binding](https://github.com/google/knative-gcp/blob/master/docs/spec/pubsub-protocol-binding.md)

Want to add a binding to a proprietary transport?

- Create a specification that follows the structure of the existing binding specifications (e.g. [http binding](http-protocol-binding.md)) - this will help SDK development.
  - `NOTE :` The specification needs to be publically accessible and manged by the proposing organization.
- Open a pull request against this file.
- Respond to any comments on the pull request and potentially join one of the regularly scheduled working group sessions.
