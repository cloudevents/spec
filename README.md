# CloudEvents

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

The following documents are available:

|                               |                                 Latest Release                                 |                                    Working Draft                                    |
| :---------------------------- | :----------------------------------------------------------------------------: | :---------------------------------------------------------------------------------: |
| **Core Specification:**       |
| CloudEvents                   |         [v1.0](https://github.com/cloudevents/spec/blob/v1.0/spec.md)          |          [master](https://github.com/cloudevents/spec/blob/master/spec.md)          |
|                               |
| **Optional Specifications:**  |
| AMQP Protocol Binding         | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/amqp-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/amqp-protocol-binding.md)  |
| AVRO Event Format             | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/avro-format.md)           | [master](https://github.com/cloudevents/spec/blob/master/avro-format.md)            |
| HTTP Protocol Binding         | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/http-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/http-protocol-binding.md)  |
| JSON Event Format             |      [v1.0](https://github.com/cloudevents/spec/blob/v1.0/json-format.md)      |      [master](https://github.com/cloudevents/spec/blob/master/json-format.md)       |
| Kafka Protocol Binding        | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/kafka-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/kafka-protocol-binding.md) |
| MQTT Protocol Binding         | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/mqtt-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/mqtt-protocol-binding.md)  |
| NATS Protocol Binding         | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/nats-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/nats-protocol-binding.md)  |
| Web hook                      |     [v1.0](https://github.com/cloudevents/spec/blob/v1.0/http-webhook.md)      |      [master](https://github.com/cloudevents/spec/blob/master/http-webhook.md)      |
|                               |
| **Additional Documentation:** |
| CloudEvents Adapters          |                                       -                                        |        [master](https://github.com/cloudevents/spec/blob/master/adapters.md)        |
| CloudEvents SDK Requirements  |                                       -                                        |          [master](https://github.com/cloudevents/spec/blob/master/SDK.md)           |
| Documented Extensions         |                                       -                                        | [master](https://github.com/cloudevents/spec/blob/master/documented-extensions.md)  |
| Primer                        |        [v1.0](https://github.com/cloudevents/spec/blob/v1.0/primer.md)         |         [master](https://github.com/cloudevents/spec/blob/master/primer.md)         |
| Proprietary Specifications    |                                       -                                        |   [master](https://github.com/cloudevents/spec/blob/master/proprietary-specs.md)    |

If you are new to CloudEvents, it is recommended that you start by reading the
[Primer](primer.md) for an overview of the specification's goals and design
decisions, and then move on to the [core specification](spec.md).

Since not all event producers generate CloudEvents by default, there is
documentation describing the recommended process for adapting some popular
events into CloudEvents, see
[CloudEvents Adapters](https://github.com/cloudevents/spec/blob/master/adapters.md).

## SDKs

In addition to the documentation mentioned above, there are also an
[SDK proposal](SDK.md) and a set of SDKs being developed:

- [CSharp](https://github.com/cloudevents/sdk-csharp)
- [Go](https://github.com/cloudevents/sdk-go)
- [Java](https://github.com/cloudevents/sdk-java)
- [Javascript](https://github.com/cloudevents/sdk-javascript)
- [Python](https://github.com/cloudevents/sdk-python)
- [Ruby](https://github.com/cloudevents/sdk-ruby)

## Community

Learn more about the people and organizations who are creating a dynamic cloud
native ecosystem by making our systems interoperable with CloudEvents.

- [Contributors](community/contributors.md): people and organizations who helped
  us get started or are actively working on the CloudEvents specification.
- Coming soon: [demos & open source](community/README.md) -- if you have
  something to share about your use of CloudEvents, please submit a PR!

## Process

The CloudEvents project is working to formalize the [specification](spec.md)
based on [design goals](primer.md#design-goals) which focus on interoperability
between systems which generate and respond to events.

In order to achieve these goals, the project must describe:

- Common attributes of an _event_ that facilitate interoperability
- One or more common architectures that are in active use today or planned to be
  built by its members
- How events are transported from producer to consumer via at least one protocol
- Identify and resolve whatever else is needed for interoperability

## Communications

The main mailing list for e-mail communications:

- Send emails to: [cncf-cloudevents](mailto:cncf-cloudevents@lists.cncf.io)
- To subscribe see: https://lists.cncf.io/g/cncf-cloudevents
- Archives are at: https://lists.cncf.io/g/cncf-cloudevents/topics

And a #cloudevents Slack channel under
[CNCF's Slack workspace](https://slack.cncf.io/).

For SDK related comments and questions:

- Email to: [cncf-cloudevents-sdk](mailto:cncf-cloudevents-sdk@lists.cncf.io)
- To subscribe see: https://lists.cncf.io/g/cncf-cloudevents-sdk
- Archives are at: https://lists.cncf.io/g/cncf-cloudevents-sdk/topics
- Slack: #cloudeventssdk on [CNCF's Slack workspace](https://slack.cncf.io/)


## Meeting Time

See the [CNCF public events calendar](https://www.cncf.io/community/calendar/).
This specification is being developed by the
[CNCF Serverless Working Group](https://github.com/cncf/wg-serverless). This
working group meets every Thursday at 9AM PT (USA Pacific):

Join from PC, Mac, Linux, iOS or Android: https://zoom.us/my/cncfserverlesswg

Or iPhone one-tap :

    US: +16465588656,,3361029682#  or +16699006833,,3361029682#

Or Telephone:

    Dial:
        US: +1 646 558 8656 (US Toll) or +1 669 900 6833 (US Toll)
        or +1 855 880 1246 (Toll Free) or +1 877 369 0926 (Toll Free)

Meeting ID: 336 102 9682

International numbers available:
https://zoom.us/zoomconference?m=QpOqQYfTzY_Gbj9_8jPtsplp1pnVUKDr

NOTE: Please use \*6 to mute/un-mute your phone during the call.

World Time Zone Converter:
http://www.thetimezoneconverter.com/?t=9:00%20am&tz=San%20Francisco&

## Meeting Minutes

The minutes from our calls are available
[here](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#).

Recording from our calls are available
[here](https://www.youtube.com/playlist?list=PLj6h78yzYM2Ph7YoBIgsZNW_RGJvNlFOt).

Periodically, the group may have in-person meetings that coincide with a major
conference. Please see the
[meeting minutes](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
for any future plans.
