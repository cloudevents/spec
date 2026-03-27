# ![CDEvents](cdevents_horizontal-color.png)

CDEvents is a common specification for Continuous Delivery events, enabling
interoperability in the complete software production ecosystem.

It's an incubated project at the
[Continuous Delivery Foundation](https://cd.foundation) (CDF).

## Background
<!--
Resources used for the background text
https://cd.foundation/blog/2021/03/16/cd-foundation-announces-industry-initiative-to-standardize-events-from-ci-cd-systems/
https://github.com/cdfoundation/toc/blob/master/sigs/sig-events.md
https://github.com/cdfoundation/sig-events
https://github.com/cdfoundation/toc/blob/master/proposals/cdevents/cdevents.md
-->
In a complex and fast moving CI/CD world with a lot of different tools and
platforms that need to communicate with each other interoperability stands as a
crucial thing. The maintainer of a CI/CD system needs to swap out tools in short
time with little to no stops.

The larger and more complex a CI/CD system becomes, challenges increase in
knowing how the tools communicate and what they do.

### What we provide

The CDEvents protocol defines a vocabulary of events enabling tools to
communicate in an interoperable way.

We extend other efforts such as CloudEvents by introducing purpose and semantics
to the event.

![stack](./images/stack.png)

By providing an interoperable way of tools to communicate we also provide means
to give an overview picture increasing observability, but also to give measuring
points for metrics.

## CDEvents Specification

The latest release of the specification on is
[v0.5.0](https://github.com/cdevents/spec/blob/v0.5.0/spec.md), and you can
continuously follow the latest updates of the specification on [the `main`
branch](./spec.md).

To understand more about the concepts and ideas that have formed the current published
specification, visit the [CDEvents Documentation](https://cdevents.dev/docs/) site.

The reference specification is maintained in this repository.

Key assets are as follows:

### [White Paper](./CDEvents_Whitepaper.pdf)

The Continuous Delivery Foundation White Paper on CDEvents

### [Primer](https://cdevents.dev/docs/primer/)

An introduction to CDEvents and associated concepts

### [Common Metadata](./spec.md)

An overview of Metadata common across the CDEvents Specification

### [Core Events](./core.md)

Definition of specific events that are fundamental to pipeline execution and orchestration

### [Source Code Control Events](./source-code-version-control.md)

Handling Events relating to changes in version management of Source Code and related assets

### [Continuous Integration Events](./continuous-integration.md)

Handling Events associated with Continuous Integration activities, typically involving build and test

### [Continuous Deployment Events](./continuous-deployment.md)

Handling Events associated with Continuous Deployment activities

### [Continuous Operations Events](./continuous-operations.md)

Handling Events associated with the health of the services deployed and running in a specific environment

### [Testing Events](./testing-events.md)

Handling Events associated with Test execution performed independently or as part of CI/CD pipelines.

### [CloudEvents Binding and Transport](./cloudevents-binding.md)

Defining how CDEvents are mapped to CloudEvents for transportation and delivery

### [Schemas](./schemas/) and [Conformance](./conformance/)

The [schemas](./schemas/) folder contains `jsonschemas` for all events in the spec. The [conformance](./conformance/) folder contains simple `JSON` examples for all events. The content of the conformance folder is used for testing purposes: the structure of the files in there is sound, the values have correct types but are not particularly meaningful.

## CDEvents SDKs

CDEvents includes SDKs for several languages:

* [Go](https://github.com/cdevents/sdk-go)
* [Java](https://github.com/cdevents/sdk-java)
* [Python](https://github.com/cdevents/sdk-python)
* [Rust](https://github.com/cdevents/sdk-rust)

## Community

### How to get involved

[Reach out](https://github.com/cdevents/community/blob/main/governance.md#project-communication-channels) to see what we're up
via:

* [slack](https://cdeliveryfdn.slack.com/archives/C030SKZ0F4K)
* [our mailing list](https://groups.google.com/g/cdevents-dev)
* [working group meetings (Europe/Asia)](https://calendar.google.com/calendar/u/0/event?eid=YjI4aDcybzA5bTlkdW9hOTBlMmFtcWE4ZDdfMjAyNTA5MDlUMTQwMDAwWiBsaW51eGZvdW5kYXRpb24ub3JnX21oZjBrbWdlZG42N2lobmk4cjEyOWF2cDI0QGc)
* [working group meetings (Americas)](https://calendar.google.com/calendar/u/0/event?eid=MWsxaG9vdGtxcWxuYjJvdHIyN3A0Y3R1ZXFfMjAyNTA5MjNUMTcwMDAwWiBsaW51eGZvdW5kYXRpb24ub3JnX21oZjBrbWdlZG42N2lobmk4cjEyOWF2cDI0QGc)

### Contributing

If you would like to contribute, see our [contributing](https://cdevents.dev/community/contribution-guidelines/)
guidelines.

### Governance

The project has been started by the CDF [SIG Events](https://github.com/cdfoundation/sig-events).
Its governance is [documented in the community repository](https://github.com/cdevents/community/blob/main/governance.md).
