# CloudEvents Adapters

Not all event producers will produce CloudEvents natively. As a result,
some "adapter" might be needed to convert these events into CloudEvents.
This will typically mean extracting metadata from the events to be used as
CloudEvents attributes. In order to promote interoperability across multiple
implementations of these adpaters, the following documents show the proposed
algorithms that should be used:

* [AWS SNS](adapters/aws-sns.md)
* [Github](adapters/github.md)
* [Gitlab](adapters/gitlab.md)
