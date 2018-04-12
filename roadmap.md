## Roadmap

The CloudEvents Roadmap.

_Note: The ordered lists for each milestone provide a way to reference each item; they don't imply an order for implementation._

*Setup*

1. Establish governance, contributing guidelines and initial stakeholders.
1. Define design goals for CloudEvents V.1.
1. Describe the scope of the specification.
1. Draft educational materials that provide context for reading the spec.

*0.1*

* Draft specification that WG members agree *could* provide interoperability.
* Include an initial set of use-cases for CloudEvents.
* Include a specification for mapping the CloudEvents specification to HTTP.
* Include a specification for mapping the CloudEvents specification to JSON.
* Define a type system for CloudEvents values.
* Document at least 3 sample events that conform to the specification.
* Github repo is organized to be approachable to a engineers who might want to
implement the spec.
* Finalize logo.
* Create and deploy a website that features a simple overview, email list and directs visitors to Github.
* Store all website assets in the CloudEvents repository, under the governance
of the working group.

*0.2*

1. Have at least 2 implementations of the specification that can demonstrate interoperability.
1. Changes to the spec to facilitate adoption.
1. HTTP protocol specification.
1. Draft documentation and developer guide.
1. Publicize at conferences ([CloudNativeCon Europe](https://events.linuxfoundation.org/events/kubecon-cloudnativecon-north-america-2018/)).

*0.3*

1. Interoperability demo.
    1. At least one open source implementation of sending and receiving events.
    1. Events are sent by code written by Developer1 and recieved by code written by Developer2, where Developer1 has no knowledge of Developer2.
    1. Draft trigger specification (e.g. how events + actions are associated).
1. Draft documentation and user guides.

*0.4*

1. Incorporate learnings and feedback from interop demo to support wider adoption.
1. Collaborate on libraries and supporting tools to use CloudEvents and
integrate it with the ecosystem.
