# CloudEvents Extension Attributes

The [CloudEvents specification](../spec.md) defines a set of metadata
attributes that can be used when transforming a generic event into a
CloudEvent. The list of attributes specified in that document represent the
minimal set that the specification authors deemed most likely to be used in a
majority of situations.

This document defines some addition attributes that, while not as commonly used
as the ones specified in the [CloudEvents specification](../spec.md), could
still benefit from being formally specified in the hopes of providing some
degree of interoperability. This also allows for attributes to be defined in an
experimental manner and tested prior to being considered for inclusion in the
[CloudEvents specification](../spec.md).

Implementations of the [CloudEvents specification](../spec.md) are not
mandated to limit their use of extension attributes to just the ones specified
in this document. The attributes defined in this document have no official
standing and might be changed, or removed, at any time. As such, inclusion of
an attribute in this document does not need to meet the same level of maturity,
or popularity, as attributes defined in the
[CloudEvents specification](../spec.md). To be
included in this document, aside from the normal PR review process, the
attribute needs to have at least two
[Voting](../../docs/GOVERNANCE.md#membership) member organizations stating
their support for its inclusion as comments in the PR. If the author of the PR
is also a Voting member, then they are allowed to be one of two.

## Usage

Support for any extension is OPTIONAL. When an extension definition uses
[RFC 2199](https://www.ietf.org/rfc/rfc2119.txt) keywords (e.g. MUST, SHOULD,
MAY), this usage only applies to events that use the extension.

Extensions attributes, while not defined by the core CloudEvents specifications,
MUST follow the same serialization rules as defined by the format and protocol
binding specifications. See
[Extension Context Attributes](../spec.md#extension-context-attributes)
for more information.

## Known Extensions

- [Auth Context](authcontext.md)
- [Dataref (Claim Check Pattern)](dataref.md)
- [Distributed Tracing](distributed-tracing.md)
- [Expiry Time](expirytime.md)
- [Partitioning](partitioning.md)
- [Recorded Time](recordedtime.md)
- [Sampling](sampledrate.md)
- [Sequence](sequence.md)
- [Severity](severity.md)
