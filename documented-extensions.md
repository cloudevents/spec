# CloudEvents Extension Attributes

The [CloudEvents specification](spec.md) defines a set of metadata attributes
than can be used when transforming a generic event into a CloudEvent. The list
of attributes specified in that document represent the minimal set that the
specification authors deemed most likely to be used in a majority of situations.

This document defines some addition attributes that, while not as commonly used
as the ones specified in the [CloudEvents specification](spec.md), could still
benefit from being formally specified in the hopes of providing some degree of
interoperability. This also allows for attributes to be defined in an
experimental manner and tested prior to being considered for inclusion in the
[CloudEvents specification](spec.md).

Implementations of the [CloudEvents specification](spec.md) are not mandated to
limit their use of extension attributes to just the ones specified in this
document. The attributes defined in this document have no official standing and
might be changed, or removed, at any time. As such, inclusion of an attribute in
this document does not need to meet the same level of maturity, or popularity,
as attributes defined in the [CloudEvents specification](spec.md). To be
included in this document, aside from the normal PR review process, the
attribute needs to have at least two [Voting](GOVERNANCE.md#membership) member
organizations stating their support for its inclusion as comments in the PR. If
the author of the PR is also a Voting member, then they are allowed to be one of
two.

## Usage

Support for any extension is OPTIONAL. When an extension definition uses
[RFC 2199](https://www.ietf.org/rfc/rfc2119.txt) keywords (e.g. MUST, SHOULD,
MAY), this usage only applies to events that use the extension.

Extensions always follow a common placement strategy for in-memory formats (e.g.
[JSON](json-format.md), XML, Protobuffer) that are decided by those
representations. Transport bindings (e.g. [HTTP](http-transport-binding.md),
[MQTT](mqtt-transport-binding.md), [AMPQ](amqp-transport-binding.md),
[NATS](nats-transport-binding.md)) provide default placement for extensions, but
an extension MAY require special representation when transported (e.g. tracing
standards that require specific headers). Extension authors SHOULD only require
special representation in transport bindings where extensions integrate with
pre-existing specs; extensions with custom transport bindings are much more
likely to be dropped by middleware that does not understand the extension.

As a convention, extensions of scalar types (e.g. `String`, `Binary`,
`URI-reference`, `Number`) document their `Value` and structured types document
their `Attributes`.

## Known Extensions

- [Dataref (Claim Check Pattern)](extensions/dataref.md)
- [Distributed Tracing](extensions/distributed-tracing.md)
- [Partitioning](extensions/partitioning.md)
- [Sampling](extensions/sampled-rate.md)
- [Sequence](extensions/sequence.md)
- [Tenant Identifier](extensions/tenant.md)