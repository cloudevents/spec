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
  defined in [section 2.2.2](https://w3c.github.io/trace-context/#field-value)
- Constraints
  - REQUIRED

#### tracestate

- Type: `String`
- Description: a comma-delimited list of key-value pairs, defined by
  [section 2.3.2](https://w3c.github.io/trace-context/#header-value).
- Constraints
  - OPTIONAL

## Encoding

### In-memory formats

The Distributed Tracing extension uses the key `distributedtracing` for
in-memory formats

### HTTP

To integrate with existing tracing libraries, the Distributed Tracing attributes
MUST be encoded over HTTP(S) as headers. E.g.

```bash
CURL -X POST example/webhook.json \
-H 'traceparent:  00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01' \
-H 'tracestate: rojo=00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01,congo=lZWRzIHRoNhcm5hbCBwbGVhc3VyZS4=` \
-H 'content-type: application/cloudevents+json' \
-d '@sample-event.json'
```
