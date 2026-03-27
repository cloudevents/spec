# Custom Event Types

## Introduction

CDEvents brings standardization for events consumed and produced by tools in the software development life-cycle (SDLC).
Some of the tools that are candidate for CDEvents adoption already produce events, in their own specific formats.
Some of these events exist or can be mapped to events available in the CDEvents specification.
Some events might be added to CDEvents, if they're considered for interoperability by the CDEvents community.
Some events however, are very specific to a tool or are not relevant from an interoperability point of view.

Custom event types exist as a mean to make it easier for tools to adopt CDEvents and provide event producers and consumers with a consistent way to produce and consume events aligned to the CDEvents specification.

To ensure interoperability, tools should use events available in the CDEvents specification as much as possible. Missing events can be proposed to the CDEvents community and included in future releases. Custom events are meant for events that are strictly tool specific and thus not good candidates for CDEvents.

Custom events can be used as an interim solution until new events are included in the CDEvents specification. When considering this option, please note that the migration from custom events to CDEvents may be disruptive for both event consumers and producers. Thus it is not recommended to use interim custom events at a large scale.

### Specification

The following features of the specification are related to custom events:

- **The `dev.cdeventsx` event-type namespace**: This namespace is reserved for events that are compliant with the CDEvents specification, whose subject structure and semantics are defined outside of CDEvents.
- **The [`schemaUri`](/spec.md#schemauri) property in the `context`**: events may supply their schema URI via this new `context` property. Events must **always** validate against the CDEvents official schema too.
- **The [`dev.cdeventsx` jsonschema](schema.json)**: any event of type `dev.cdeventsx.*` must respect this schema as well as any additional schema supplied via `schemaUri`
- **The `subject` format for `dev.cdeventsx` events**: subjects must be in the format `<tool-name>-<subject-name>` to avoid event-type conflicts across tools
- **The [registry](registry.md)**: maintainers of the specifications of CDEvents custom events are encouraged to add their specification to the shared [registry](registry.md)

### Versioning

Similar to regular CDEvents, custom CDEvents include two versions:

- The specification version: this indicates the base CDEvents-defined [schema](schema.json) that is adopted by the event.
- The event version: this must follow the [semantic versioning approach of CDEvents][cdevents-versions]. Changes of versions for custom CDEvents are decoupled from CDEvents releases. When a custom CDEvents adopts a new version of the CDEvents spec, the event version must be updated as the change in spec version corresponds to a change in the schema of the event.

### SDKs

When consuming (parsing) an event with `context.schemaUri`, SDKs SHOULD fetch the schema defined in `context.schemaUri` and **additionally** validate the event against that schema, unless security concerns dictate otherwise.

When consuming (parsing) an event with `dev.cdeventsx` type, the SDKs will return a object that is identical in structure for all events, and which include an unparsed blob for the `subject.content` part. SDKs MAY provide a way for users to register a function to be used to parse the `subject.content` of these messages.

When producing events, the SDK MAY provide a way for users to register additional functions to be used to render `dev.cdeventsx` events as `JSON` and `CloudEvents`.

## Transitioning Custom CDEvents to Standard CDEvents

In certain cases, custom events may be implemented as a stopgap solution to allow for faster CDEvents adoption. The custom events may be eventually make its way into the CDEvents specification, with a structure that could be different from the original one defined in the custom events.

This situation is not dissimilar from the process of adopting a new, backwards incompatible version of an existing event. Once the new CDEvent is introduced in the spec, newer versions of the SDKs will be able to produce it and consume it.

### Promoting a Custom CDEvent to Standard CDEvent

To create a new CDEvent, start with the [guide](https://cdevents.dev/docs/primer/#adding-new-event-types) available in the CDEvents primer. Use cases and experiences from using the custom event would be a great addition to the proposal:

- Start proposing the new CDEvent in a GitHub issue. Attach relevant use cases and context from the corresponding custom event. Highlight why the event would be beneficial from interoperability point of view
- (Optional) Join one of the CDEvents working groups to present your proposal. This can also happen asynchronously if the working group schedule is not convenient
- Create a PR that adds the new event. You may search in the recent PR history for other similar PRs to guide you in the process. Promote your PR at the working groups and/or on Slack to obtain feedback. If struggling with the CI jobs, ask on slack for help
- Once the PR is merged, the new event will be available in the spec and in the SDKs with their next release. The release of the SDKs may happen some time after the release of the specification

### Handling Heterogeneous Producers and Consumers

It is safe to assume that several producers and consumers of the event exist. At some point in time only a fraction of producers and consumers will have adopted the new SDK.

Consumers with the latest SDK will be able to parse the old custom event as well as the new CDEvent. This means that there is no pressure for producers to adopt the new version, even after all consumers have been updated.

Consumers with the old SDK however, won't be able to parse the new CDEvents.
This means that producers that adopt the new SDK may have to consider producing both the old and the new events, until all consumers have updated to the latest SDK.
In this case, it is responsibility of the system architect to ensure that old events are only sent to legacy consumers, to avoid the case of consumers receiving duplicate events.

## CDEvents and Links

The CDEvents community is working on the introduction of [links](https://github.com/cdevents/spec/pull/139) to the specification. Links will let CDEvents producer connect one event to others with specific semantics, and will help consumers trace through events to understand complete workflows.

Custom CDEvents can be linked like any other CDEvent, so links may exist between custom CDEvents as well as between a custom CDEvent and a normal CDEvent.
> Note: some custom events may be intended for a limited audience; when linking a standard CDEvent to a custom CDEvent, it should be considered that that consumers of the standard CDEvent may not have access to the linked custom event.

## Example of Custom Event

The following example shows how an existing event can be adapted into a CDEvents custom event.
It's based on an operational event of the [Harbor registry][harbor-docs], which would not be a good fit for CDEvents.

Original Harbor event:

```jsonld=
{
  "specversion": "1.0",
  "id": "81f243ce-699c-44d6-9dbe-b2ee5f10237a",
  "requestid": "4b9dcf9a-db23-460c-9b52-c9d994e362ee",
  "source": "/projects/2/webhook/policies/15",
  "type": "harbor.quota.exceeded",
  "datacontenttype": "application/json",
  "time": "2023-04-03T07:04:44Z",
  "data": {
    "resources": [
      {
        "digest": "sha256:402d21757a03a114d273bbe372fa4b9eca567e8b6c332fa7ebf982b902207242"
      }
    ],
    "repository": {
      "name": "alpine",
      "namespace": "harbor",
      "repo_full_name": "harbor/alpine",
      "repo_type": "private"
    },
    "custom_attributes": {
      "Details": "adding 2.1 MiB of storage resource, which when updated to current usage of 8.3 MiB will exceed the configured upper limit of 10.0 MiB."
    }
  },
  "operator": ""
}
```

Corresponding CDEvent using a `dev.cdeventsx.*` type:

```jsonld=
{
  "context": {
    "specversion": "0.1.0",
    "id": "271069a8-fc18-44f1-b38f-9d70a1695819",
    "source": "/harbor/alpine",
    "type": "dev.cdeventsx.harbor-quota.exceeded.0.1.0",
    "timestamp": "2023-03-20T14:27:05.315384Z",
    "schemaUri": "https://goharbor.io/cdeventsx/schema/harbor-quota/exceeded/0_1_0"
  },
  "subject": {
    "id": "/projects/2/webhook/policies/15",
    "source": "/harbor/alpine",
    "content": {
      "operator": "",
      "resources": [
        {
          "digest": "sha256:402d21757a03a114d273bbe372fa4b9eca567e8b6c332fa7ebf982b902207242"
        }
      ],
      "repository": {
        "name": "alpine",
        "namespace": "harbor",
        "repo_full_name": "harbor/alpine",
        "repo_type": "private"
      },
    }
  },
  "customData": {
    "requestid": "4b9dcf9a-db23-460c-9b52-c9d994e362ee",
    "details": "adding 2.1 MiB of storage resource, which when updated to current usage of 8.3 MiB will exceed the configured upper limit of 10.0 MiB."
  }
}
```

To help with the transition from a custom event to a standard one, the original custom event, or sections of it can be included in the `customData`, as shown in the example above.

[harbor-docs]: https://goharbor.io/docs/2.10.0/working-with-projects/project-configuration/configure-webhooks/
[cdevents-versions]: https://cdevents.dev/docs/primer/#versioning-of-cdevents
