# CloudEvents Extension Attributes

The [CloudEvents specification](spec.md) defines a set of metadata attributes
than can be used when transforming a generic event into a CloudEvent.
The list of attributes specified in that document represent the minimal set
that the specification authors deemed most likely to be used in a majority of
situations.

This document defines some addition attributes that, while not as commonly
used as the ones specified in the [CloudEvents specification](spec.md),
could still benefit from being formally specified in the hopes of providing
some degree of interoperability. This also allows for attributes to be
defined in an experimental manner and tested prior to being considered for
inclusion in the [CloudEvents specification](spec.md).

Implementations of the [CloudEvents specification](spec.md) are not mandated
to limit their use of extension attributes to just the ones specified in
this document. The attributes defined in this document have no official
standing and might be changed, or removed, at any time.

## Extension Attributes

### distributedTracing

This extension embeds context from 
[Distributed Tracing](https://w3c.github.io/distributed-tracing/report-trace-context.html)
so that distributed systems can include traces that span an event-driven system.
This is the foundation of many other systems, such as Open Tracing, on which
platforms like Prometheus are built.
 
#### traceparent
* Type: `String`
* Description: Contains a trace ID, span ID, and trace options as defined in
  [section 2.2.2](https://w3c.github.io/distributed-tracing/report-trace-context.html#field-value)
* Constraints
  * REQUIRED
  * To integrate with Distributed Tracing, this field MUST NOT use the normal
    [extension encoding over HTTP(S)](http-transport-binding.md).
    `distributedTracing.traceparent` MUST instead be marshaled as 
    the `traceparent` HTTP header.

#### tracestate
* Type: `String`
* Description: a comma-delimited list of key-value pairs, defined by
  [section 2.3.2](https://w3c.github.io/distributed-tracing/report-trace-context.html#header-value).
* Constraints
  * OPTIONAL
  * To integrate with Distributed Tracing, this field MUST NOT use the normal
    [extension encoding over HTTP(S)](http-transport-binding.md).
    `distributedTracing.tracestate` MUST instead be marshaled as the
    `tracestate` HTTP header.