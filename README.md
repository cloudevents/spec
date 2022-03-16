# CloudEvents

<!-- no verify-specs -->

![CloudEvents logo](https://github.com/cncf/artwork/blob/master/projects/cloudevents/horizontal/color/cloudevents-horizontal-color.png)

Events are everywhere. However, event producers tend to describe events
differently.

The lack of a common way of describing events means developers must constantly
re-learn how to consume events. This also limits the potential for libraries,
tooling and infrastructure to aide the delivery of event data across
environments, like SDKs, event routers or tracing systems. The portability and
productivity we can achieve from event data is hindered overall.

CloudEvents is a specification for describing event data in common formats to
provide interoperability across services, platforms and systems.

CloudEvents has received a large amount of industry interest, ranging from major
cloud providers to popular SaaS companies. CloudEvents is hosted by the
[Cloud Native Computing Foundation](https://cncf.io) (CNCF) and was approved as
a Cloud Native sandbox level project on
[May 15, 2018](https://docs.google.com/presentation/d/1KNSv70fyTfSqUerCnccV7eEC_ynhLsm9A_kjnlmU_t0/edit#slide=id.g37acf52904_1_41).

## CloudEvents Documents

The following documents are available
([Release Notes/Changelog](docs/RELEASE_NOTES.md)):

|                               |                                 Latest Release                                  |                                      Working Draft                                       |
| :---------------------------- | :-----------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------: |
| **Core Specification:**       |
| CloudEvents                   |          [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md)          |            [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md)             |
|                               |
| **Optional Specifications:**  |
| AMQP Protocol Binding         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/amqp-protocol-binding.md)  |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/amqp-protocol-binding.md)    |
| AVRO Event Format             |      [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md)       |         [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/avro-format.md)         |
| HTTP Protocol Binding         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md)  |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md)    |
| JSON Event Format             |      [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md)       |         [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/json-format.md)         |
| Kafka Protocol Binding        | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md) |   [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/kafka-protocol-binding.md)    |
| MQTT Protocol Binding         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/mqtt-protocol-binding.md)  |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/mqtt-protocol-binding.md)    |
| NATS Protocol Binding         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/nats-protocol-binding.md)  |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/nats-protocol-binding.md)    |
| WebSockets Protocol Binding   |                                        -                                        | [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/websockets-protocol-binding.md) |
| Protobuf Event Format         |                                                                                 | [v1.0-rc1](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/protobuf-format.md)                                  |
| XML Event Format              | - | [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/working-drafts/xml-format.md) |
| Web hook                      |      [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/http-webhook.md)      |        [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/http-webhook.md)         |
|                               |
| **Additional Documentation:** |
| CloudEvents Adapters          |                                        -                                        |          [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/adapters.md)           |
| CloudEvents SDK Requirements  |                                        -                                        |             [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/SDK.md)             |
| Documented Extensions         |                                        -                                        |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/documented-extensions.md)    |
| Primer                        |         [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/primer.md)         |           [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/primer.md)            |
| Proprietary Specifications    |                                        -                                        |      [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/proprietary-specs.md)      |

There might be additional work-in-progress specifications being developed
in the [`main`](https://github.com/cloudevents/spec/tree/main) branch.

If you are new to CloudEvents, it is recommended that you start by reading the
[Primer](cloudevents/primer.md) for an overview of the specification's goals
and design decisions, and then move on to the
[core specification](cloudevents/spec.md).

Since not all event producers generate CloudEvents by default, there is
documentation describing the recommended process for adapting some popular
events into CloudEvents, see
[CloudEvents Adapters](https://github.com/cloudevents/spec/blob/main/cloudevents/adapters.md).

## SDKs

In addition to the documentation mentioned above, there is also an
[SDK proposal](cloudevents/SDK.md). A set of SDKs is also being developed:

- [CSharp](https://github.com/cloudevents/sdk-csharp)
- [Go](https://github.com/cloudevents/sdk-go)
- [Java](https://github.com/cloudevents/sdk-java)
- [Javascript](https://github.com/cloudevents/sdk-javascript)
- [PHP](https://github.com/cloudevents/sdk-php)
- [PowerShell](https://github.com/cloudevents/sdk-powershell)
- [Python](https://github.com/cloudevents/sdk-python)
- [Ruby](https://github.com/cloudevents/sdk-ruby)
- [Rust](https://github.com/cloudevents/sdk-rust)

## Community and Docs

Learn more about the people and organizations who are creating a dynamic cloud
native ecosystem by making our systems interoperable with CloudEvents.

- Our [Governance](docs/GOVERNANCE.md) documentation.
- [Contributing](docs/CONTRIBUTING.md) guidance.
- [Roadmap](docs/ROADMAP.md)
- [Adopters](https://cloudevents.io/) - See "Integrations".
- [Contributors](docs/contributors.md): people and organizations who helped
  us get started or are actively working on the CloudEvents specification.
- [Demos & open source](docs/README.md) -- if you have something to share
  about your use of CloudEvents, please submit a PR!
- [Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md)

### Security Concerns

If there is a security concern with one of the specifications in this
repository please [open an issue](https://github.com/cloudevents/spec/issues).

### Communications

The main mailing list for e-mail communications:

- Send emails to: [cncf-cloudevents](mailto:cncf-cloudevents@lists.cncf.io)
- To subscribe see: https://lists.cncf.io/g/cncf-cloudevents
- Archives are at: https://lists.cncf.io/g/cncf-cloudevents/topics

And a #cloudevents Slack channel under
[CNCF's Slack workspace](http://slack.cncf.io/).

For SDK related comments and questions:

- Email to: [cncf-cloudevents-sdk](mailto:cncf-cloudevents-sdk@lists.cncf.io)
- To subscribe see: https://lists.cncf.io/g/cncf-cloudevents-sdk
- Archives are at: https://lists.cncf.io/g/cncf-cloudevents-sdk/topics
- Slack: #cloudeventssdk on [CNCF's Slack workspace](http://slack.cncf.io/)

### Meeting Time

See the [CNCF public events calendar](https://www.cncf.io/community/calendar/).
This specification is being developed by the
[CNCF Serverless Working Group](https://github.com/cncf/wg-serverless). This
working group meets every Thursday at 9AM PT (USA Pacific)
([World Time Zone Converter](http://www.thetimezoneconverter.com/?t=9:00%20am&tz=San%20Francisco&)):

Please see the
[meeting minutes doc](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
for the latest information on how to join the calls.

Recording from our calls are available
[here](https://www.youtube.com/channel/UC70hQml92GsoNgnB-CKNEXg/videos), and
older ones are
[here](https://www.youtube.com/playlist?list=PLj6h78yzYM2Ph7YoBIgsZNW_RGJvNlFOt).

Periodically, the group may have in-person meetings that coincide with a major
conference. Please see the
[meeting minutes doc](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
for any future plans.
