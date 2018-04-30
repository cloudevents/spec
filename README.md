# CloudEvents

![CloudEvents logo](https://github.com/cncf/artwork/blob/master/other/cloudevents/horizontal/color/cloudevents-horizontal-color.png)

Events are everywhere.  However, event publishers tend to describe events
differently.

The lack of a common way of describing events means developers must constantly
re-learn how to receive events.  This also limits the potential for libraries,
tooling and infrastructure to aide the delivery of event data across
environments, like SDKs, event routers or tracing systems.  The portability and
productivity we can achieve from event data is hindered overall.

Enter CloudEvents, a specification for describing event data in a common way.
CloudEvents seeks to ease event declaration and delivery across services,
platforms and beyond.

CloudEvents is a new effort and it's still under active development.  However,
its working group has received a surprising amount of industry interest,
ranging from major cloud providers to popular SaaS companies.  Our end goal is
to offer this specification to the
[Cloud Native Computing Foundation](https://www.cncf.io/).

## CloudEvents Documents

The following specifications are available:

| | Latest Release | Working Draft |
| :--- | :---: | :---: |
| **CloudEvents** | [v0.1](https://github.com/cloudevents/spec/blob/v0.1/spec.md) | [master](https://github.com/cloudevents/spec/blob/master/spec.md) |
| **HTTP Transport Binding** | [v0.1](https://github.com/cloudevents/spec/blob/v0.1/http-transport-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/http-transport-binding.md) |
| **JSON Event Format** | [v0.1](https://github.com/cloudevents/spec/blob/v0.1/json-format.md) | [master](https://github.com/cloudevents/spec/blob/master/json-format.md) |

There is also the [CloudEvents Extension Attributes](https://github.com/cloudevents/spec/blob/master/extensions.md)
document.

## Community

Learn more about the people and organizations who are creating a dynamic
cloud native ecosystem by making our systems interopable with CloudEvents.

* [Contributors](community/contributors.md): people and organizations who helped
us get started or are actively working on the CloudEvents specification.
* Coming soon: [demos & open source](community/README.md) -- if you have
something to share about your use of CloudEvents, please submit a PR!


## Working Group process

The CNCF Serverless WG is working to formalize the [specification](spec.md)
based on [design goals](spec.md#design-goals) which focus on interoperability
between systems which generate and respond to events.

In order to achieve these goals, the Serverless WG must describe:
- Common attributes of an *event* that facilitate interoperability
- One or more common architectures that are in active use today or planned to be
built by WG members
- How events are transported from producer to consumer via at least one protocol
- Identify and resolve whatever else is needed for interoperability

## Communications

We have google group for e-mail communications:
 [cncf-wg-serverless](https://groups.google.com/forum/#!forum/cncf-wg-serverless)

And a #cloudevents Slack channel under
[CNCF's Slack workspace](https://slack.cncf.io/).

## Meeting Time

See the [CNCF public events calendar](https://www.cncf.io/community/calendar/).
This specification is being developed by the
[CNCF Serverless Working Group](https://github.com/cncf/wg-serverless).
This working group meets every Thursday at 9AM PT (USA Pacific):

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

## In Person Meetings

None planned at this time.

## Meeting Minutes

The minutes from our calls are available
[here](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#).

Recording from our calls are available
[here](https://www.youtube.com/playlist?list=PLj6h78yzYM2Ph7YoBIgsZNW_RGJvNlFOt).
