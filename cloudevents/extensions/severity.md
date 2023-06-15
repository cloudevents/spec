# Severity Extension

## Abstract
This extension defines attributes that MAY be included within a CloudEvent
to describe the "severity" or "level" of an event in relation to other events.

Often systems produce events in form of logs, and these types of events usually
share a common concept of "log-level". This extension aims to provide a
standard way for describing this property in a language agnostic form.

Sharing a common way to describe severity of events allows for better
monitoring systems, tooling and general log consumption.

This extension is heavily inspired by the
[OpenTelemetry Severity Fields](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#severity-fields)
and is intended to interoperate with them.

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

When both attributes are used, all `severitytext` values which MAY be produced
in a context of a `source` SHOULD be in a
[one-to-one and onto](https://en.wikipedia.org/wiki/Bijection) relationship
with all `severitynumber` values which MAY be produced by the same `source`.


### severitytext

- Type: `String`
- Description: Human readable text representation of the event severity (also
  known as log level name).

  This is the original string representation of the severity as it is known
  at the source. If this field is missing and `severitynumber` is present then
  the [short name](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#displaying-severity)
  that corresponds to the `severitynumber` MAY be used as a substitution.

- Constraints
  - OPTIONAL
  - if present, MUST be a non-empty string
  - SHOULD be uppercase
  - RECOMMENDED values are `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, and
    `FATAL`, but others MAY be used.

### severitynumber

- Type: `Integer`
- Description: Numerical representation of the event severity (also known as
  log level number), normalized to values described in this document.

  Severity of all values MUST be numerically ascending from least-severe
  to most-severe. An event with a lower numerical value (such as a debug event)
  MUST be less severe than an event with a higher numerical value (such as
  an error event).

  See OpenTelemetry for [exact severity number meanings](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#field-severitynumber)

- Constraints
  - REQUIRED
  - if present, MUST NOT be negative


# References
  - [Mapping of SeverityNumber](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#mapping-of-severitynumber)
  - [Reverse Mapping](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#reverse-mapping)
  - [Error Semantics](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#error-semantics)
  - [Displaying Severity](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#displaying-severity)
  - [Comparing Severity](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#comparing-severity)
  - [Mapping of existing log formats to severity levels](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/logs/data-model.md#appendix-a-example-mappings)
