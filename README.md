# CloudEvents

<!-- no verify-specs -->

![CloudEvents logo](https://github.com/cncf/artwork/blob/main/projects/cloudevents/horizontal/color/cloudevents-horizontal-color.png?raw=true)

[![CLOMonitor](https://img.shields.io/endpoint?url=https://clomonitor.io/api/projects/cncf/cloudevents/badge)](https://clomonitor.io/projects/cncf/cloudevents)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/6770/badge)](https://bestpractices.coreinfrastructure.org/projects/6770)

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
[May 15, 2018](https://docs.google.com/presentation/d/1KNSv70fyTfSqUerCnccV7eEC_ynhLsm9A_kjnlmU_t0/edit#slide=id.g37acf52904_1_41), an
incubator project on [Oct 24, 2019](https://github.com/cncf/toc/pull/297)
and a graduated project on [Jan 25, 2024](https://github.com/cncf/toc/pull/996)
([announcement](https://www.cncf.io/announcements/2024/01/25/cloud-native-computing-foundation-announces-the-graduation-of-cloudevents/)).

## CloudEvents Documents

|                               |                                 Latest Release                                  |                                      Working Draft                                       |
| :---------------------------- | :-----------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------: |
| **Core Specification:**       |
| CloudEvents                   | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md)   | [WIP](cloudevents/spec.md) |
|                               |
| **Optional Specifications:**  |
| AMQP Protocol Binding         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/amqp-protocol-binding.md)  | [WIP](cloudevents/bindings/amqp-protocol-binding.md)       |
| AVRO Event Format             | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md)             | [WIP](cloudevents/formats/avro-format.md)                  |
| AVRO Compact Event Format       | | [WIP](cloudevents/working-drafts/avro-compact-format.md)             |
| HTTP Protocol Binding         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md)  | [WIP](cloudevents/bindings/http-protocol-binding.md)       |
| JSON Event Format             | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md)             | [WIP](cloudevents/formats/json-format.md)                  |
| Kafka Protocol Binding        | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md) | [WIP](cloudevents/bindings/kafka-protocol-binding.md)      |
| MQTT Protocol Binding         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/mqtt-protocol-binding.md)  | [WIP](cloudevents/bindings/mqtt-protocol-binding.md)       |
| NATS Protocol Binding         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/nats-protocol-binding.md)  | [WIP](cloudevents/bindings/nats-protocol-binding.md)       |
| WebSockets Protocol Binding   | -                                                                                                        | [WIP](cloudevents/bindings/websockets-protocol-binding.md) |
| Protobuf Event Format         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/protobuf-format.md)         | [WIP](cloudevents/formats/protobuf-format.md)              |
| XML Event Format              | -                                                                                                        | [WIP](cloudevents/working-drafts/xml-format.md)            |
| Web hook                      | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/http-webhook.md)                    | [WIP](cloudevents/http-webhook.md)                         |
|                               |
| **Additional Documentation:** |
| CloudEvents Primer                                             | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/primer.md) | [WIP](cloudevents/primer.md)                          |
| [CloudEvents Adapters](cloudevents/adapters.md)                | -                                                                               | [Not versioned](cloudevents/adapters.md)              |
| [CloudEvents SDK Requirements](cloudevents/SDK.md)             | -                                                                               | [Not versioned](cloudevents/SDK.md)                   |
| [Documented Extensions](cloudevents/extensions/README.md)  | -                                                                               | [Not versioned](cloudevents/extensions/README.md) |
| [Proprietary Specifications](cloudevents/proprietary-specs.md) | -                                                                               | [Not versioned](cloudevents/proprietary-specs.md)     |

## Other Specifications
|                 | Latest Release | Working Draft                 |
| :-------------- | :------------: | :---------------------------: |
| CE SQL          |       -        | [WIP](cesql/spec.md)          |
| Subscriptions   |       -        | [WIP](subscriptions/spec.md)  |

The Registry and Pagination specifications can now be found in the
[xRegistry/spec](https://github.com/xregistry/spec) repo.

Additional release related information:
  [Historical releases and changelogs](docs/RELEASES.md)

If you are new to CloudEvents, it is recommended that you start by reading the
[Primer](cloudevents/primer.md) for an overview of the specification's goals
and design decisions, and then move on to the
[core specification](cloudevents/spec.md).

Since not all event producers generate CloudEvents by default, there is
documentation describing the recommended process for adapting some popular
events into CloudEvents, see
[CloudEvents Adapters](cloudevents/adapters.md).

## SDKs

In addition to the documentation mentioned above, there are also a set of
language specific SDKs being developed:

- [C#/.NET](https://github.com/cloudevents/sdk-csharp)
- [Go](https://github.com/cloudevents/sdk-go)
- [Java](https://github.com/cloudevents/sdk-java)
- [Javascript](https://github.com/cloudevents/sdk-javascript)
- [PHP](https://github.com/cloudevents/sdk-php)
- [PowerShell](https://github.com/cloudevents/sdk-powershell)
- [Python](https://github.com/cloudevents/sdk-python)
- [Ruby](https://github.com/cloudevents/sdk-ruby)
- [Rust](https://github.com/cloudevents/sdk-rust)

The [SDK requirements](cloudevents/SDK.md) document provides information
on how the SDKs are managed and what is expected of each one.
The SDK [feature support table](cloudevents/SDK.md#feature-support) is a
good resource to see which features, event formats and bindings are supported
by each SDK.

For more information about how the SDKs operate, please see the following
documents:
- [SDK Governance](docs/SDK-GOVERNANCE.md)
- [SDK Maintainer Guidlines](docs/SDK-maintainer-guidelines.md)
- [SDK PR Guidlines](docs/SDK-PR-guidelines.md)

## Community and Docs

Learn more about the people and organizations who are creating a dynamic cloud
native ecosystem by making our systems interoperable with CloudEvents.

- Our [Governance](docs/GOVERNANCE.md) documentation.
- [Contributing](docs/CONTRIBUTING.md) guidance.
- [Roadmap](docs/ROADMAP.md)
- [Adopters](https://cloudevents.io/) - See "Integrations".
- [Contributors](docs/contributors.md): people and organizations who helped
  us get started or are actively working on the CloudEvents specification.
- [Presentations, notes and other misc shared
  docs](https://drive.google.com/drive/folders/1eKH-tVNV25jwkuBEoi3ESqvVjNRlJqYX?usp=sharing)
- [Demos & open source](docs/README.md) -- if you have something to share
  about your use of CloudEvents, please submit a PR!
- [Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md)

### Security Concerns

If there is a security concern with one of the CloudEvents specifications, or
with one of the project's SDKs, please send an email to
[cncf-cloudevents-security@lists.cncf.io](mailto:cncf-cloudevents-security@lists.cncf.io).

A security assessment was performed by
[Trail of Bits](https://www.trailofbits.com/) in October 2022. The report
can be found [here](docs/CE-SecurityAudit-2022-10.pdf) or on the Trail of Bits
[website](https://github.com/trailofbits/publications/blob/master/reviews/CloudEvents.pdf).

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

For SDK specific communications, please see the main README in each
SDK's github repo - see the [list of SDKs](#sdks).

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
[here](https://www.youtube.com/playlist?list=PLO-qzjSpLN1BEyKjOVX_nMg7ziHXUYwec), and
older ones are
[here](https://www.youtube.com/playlist?list=PLj6h78yzYM2Ph7YoBIgsZNW_RGJvNlFOt).

Periodically, the group may have in-person meetings that coincide with a major
conference. Please see the
[meeting minutes doc](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
for any future plans.
