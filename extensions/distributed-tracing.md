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

## Using the Distributed Tracing Extension

The
[OpenTelemetry Semantic Conventions for CloudEvents](https://github.com/open-telemetry/opentelemetry-specification/blob/v1.9.0/specification/trace/semantic_conventions/cloudevents.md)
define in which scenarios this extension should be used and how to use it.

## Attributes

### traceparent

- Type: `String`
- Description: Contains a version, trace ID, span ID, and trace options as
  defined in [section 3.2](https://www.w3.org/TR/trace-context/#traceparent-header)
- Constraints
  - REQUIRED

### tracestate

- Type: `String`
- Description: a comma-delimited list of key-value pairs, defined by
  [section 3.3](https://www.w3.org/TR/trace-context/#tracestate-header).
- Constraints
  - OPTIONAL
