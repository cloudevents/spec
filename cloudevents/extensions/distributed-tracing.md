# Distributed Tracing extension

This extension embeds context from
[W3C TraceContext](https://www.w3.org/TR/trace-context/) into a CloudEvent.
The goal of this extension is to offer means to carry context when instrumenting
CloudEvents based systems with OpenTelemetry.

The [OpenTelemetry](https://opentelemetry.io/) project is a collection
of tools, APIs and SDKs that can be used to instrument, generate, collect,
and export telemetry data (metrics, logs, and traces) to help you
analyze your software’s performance and behavior.

The OpenTelemetry specification defines both
[Context](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.8.0/specification/context/context.md#overview)
and
[Distributed Tracing](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.8.0/specification/overview.md#tracing-signal)
as:

> A `Context` is a propagation mechanism which carries execution-scoped values across
 API boundaries and between logically associated execution units. Cross-cutting
 concerns access their data in-process using the same shared `Context` object.
>
> A `Distributed Trace` is a set of events, triggered as a result of a single
 logical operation, consolidated across various components of an application.
 A distributed trace contains events that cross process, network and security boundaries.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is
used. For example, an attribute being marked as "REQUIRED" does not mean
it needs to be in all CloudEvents, rather it needs to be included only when
this extension is being used.

## Attributes

### traceparent

- Type: `String`
- Description: Contains a version, trace ID, span ID, and trace options as
  defined in [section 3.2](https://w3c.github.io/trace-context/#traceparent-header)
- Constraints
  - REQUIRED

### tracestate

- Type: `String`
- Description: a comma-delimited list of key-value pairs, defined by
  [section 3.3](https://w3c.github.io/trace-context/#tracestate-header).
- Constraints
  - OPTIONAL

## Using the Distributed Tracing Extension

The Distributed Tracing Extension is not intended to replace the protocol specific headers for tracing,
like the ones described in [W3C Trace Context](https://w3c.github.io/trace-context/) for HTTP.

Given a single hop event transmission (from source to sink directly), the Distributed Tracing Extension,
if used, MUST carry the same trace information contained in protocol specific tracing headers.

Given a multi hop event transmission, the Distributed Tracing Extension, if used, MUST
carry the trace information of the starting trace of the transmission.
In other words, it MUST NOT carry trace information of each individual hop, since this information is usually
carried using protocol specific headers, understood by tools like [OpenTelemetry](https://opentelemetry.io/).

The
[OpenTelemetry Semantic Conventions for CloudEvents](https://opentelemetry.io/docs/specs/semconv/cloudevents/cloudevents-spans/)
define the trace structure to follow when instrumenting CloudEvent systems and
in which scenarios this extension can be used and how to use it to achieve said structure.

Middleware between the source and the sink of the event could eventually add a Distributed Tracing Extension
if the source didn't include any, in order to provide to the sink the starting trace of the transmission.

An example with HTTP:

```bash
CURL -X POST example/webhook.json \
-H 'ce-id: 1' \
-H 'ce-specversion: 1.0' \
-H 'ce-type: example' \
-H 'ce-source: http://localhost' \
-H 'ce-traceparent:  00-0af7651916cd43dd8448eb211c80319c-b9c7c989f97918e1-01' \
-H 'traceparent:  00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01' \
-H 'tracestate: rojo=00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01,congo=lZWRzIHRoNhcm5hbCBwbGVhc3VyZS4`
```
