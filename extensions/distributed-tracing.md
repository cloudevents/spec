# Distributed Tracing extension

This extension embeds context from
[Distributed Tracing](https://w3c.github.io/trace-context/) so that distributed
systems can include traces that span an event-driven system. This is the
foundation of many other systems, such as Open Tracing, on which platforms like
Prometheus are built.

## Attributes

#### traceparent

- Type: `String`
- Description: Contains a version, trace ID, span ID, and trace options as
  defined in [section 3.2](https://w3c.github.io/trace-context/#traceparent-header)
- Constraints
  - REQUIRED

#### tracestate

- Type: `String`
- Description: a comma-delimited list of key-value pairs, defined by
  [section 3.3](https://w3c.github.io/trace-context/#tracestate-header).
- Constraints
  - OPTIONAL

## HTTP encoding

To integrate with existing tracing libraries, the Distributed Tracing attributes
MUST be encoded over HTTP(S) as headers. E.g.

```bash
CURL -X POST example/webhook.json \
-H 'traceparent:  00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01' \
-H 'tracestate: rojo=00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01,congo=lZWRzIHRoNhcm5hbCBwbGVhc3VyZS4` \
-H 'content-type: application/cloudevents+json' \
-d '@sample-event.json'
```

## Conflicts

Since this extension defines secondary, special, serialization that differs
from other CloudEvents attributes, it is possible that the values of these two
could differ by the time the event is received at a destination. In those
cases, the serialization that followed the "general CloudEvents serialization
rules" MUST be used as the CloudEvents attribute. The other, secondary,
mapping MAY be picked-up and offered to the receiving application as
"additional" metadata.
