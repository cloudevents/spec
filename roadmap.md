## Roadmap

The CloudEvents Roadmap.

_Note: The ordered lists for each milestone provide a way to reference each
item; they don't imply an order for implementation._

_Setup_ - Completed - 2018/02/26

1. Establish governance, contributing guidelines and initial stakeholders.
1. Define design goals for CloudEvents V.1.
1. Describe the scope of the specification.
1. Draft educational materials that provide context for reading the spec.

_0.1_ - Completed - 2018/04/20

1. Draft specification that project members agree _could_ provide
   interoperability.
1. Include an initial set of use-cases for CloudEvents.
1. Define a type system for CloudEvents values.
1. Document at least 3 sample events that conform to the specification.
1. Github repo is organized to be approachable to a engineers who might want to
   implement the spec.
1. Finalize logo.
1. Create and deploy a website that features a simple overview, email list and
   directs visitors to Github.
1. Store all website assets in the CloudEvents repository, under the governance
   of the project.
1. Have at least 2 implementations of the specification that can demonstrate
   interoperability.
1. Include a specification for mapping the CloudEvents specification to
   [HTTP](http-transport-binding.md).
1. Include a specification for mapping the CloudEvents specification to
   [JSON](json-format.md).
1. Changes to the spec to facilitate adoption.
1. Publicize at conferences
   ([CloudNativeCon Europe](https://events.linuxfoundation.org/events/kubecon-cloudnativecon-north-america-2018/)).
1. Interoperability demo.
   1. At least one open source implementation of sending and receiving events,
      see
      [community open source](https://github.com/cloudevents/spec/blob/master/community/open-source.md).
   1. Events are sent by code written by Developer1 and received by code written
      by Developer2, where Developer1 has no knowledge of Developer2.

_0.2_ - Completed - 2018/12/06

1. Incorporate learnings and feedback from interop demo to support wider
   adoption.
1. Draft documentation, developer and/or user guide.
1. Resolve all known large design issues (excluding security issues)
1. Resolve all known "proposed required attributes" issues
1. Interoperability demo 2
   1. Details to be determined
   1. Showcase demo at conferences - perhaps KubeCon NA 2018
1. Define the set of protocol and serialization mappings we're going to produce
   for 0.4 milestone

_0.3_

1. Resolve all known "proposed optional attributes" issues
1. Resolve all known "security related" issues
1. Review spec for practical-use issues:
   1. Consider context size limits
   1. Consider restricting character sets of `String` properties or key names
   1. Consider defining uniqueness constraints of event `id`
   1. Consider which fields will be immutable (prevents annotation or redaction)
   1. Consider validating transport bindings with load tests

_0.4_

1. Complete the proposed set of protocol and serialization mappings
1. Resolve "Process" related issues

_0.5_

1. Resolve outstanding clarifications and non-semantic issues
1. Define and prioritize libraries and supporting tools that will accelerate
   adoption of CloudEvents
