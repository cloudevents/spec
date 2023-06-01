# Expiry Time Extension

This extension provides a mechanism to hint to [consumers](../spec.md#consumer)
or [intermediaries](../spec.md#intermediary) a timestamp after which an
[event](../spec.md#event) can be ignored.

In distributed systems with message delivery guarantees, events might be delivered
to a consumer some significant amount of time after an event has been sent.
In this situation, it might be desirable to ignore events that
are no longer relevant. The [`time` attribute](../spec.md#time) could be used
to handle this on the consumer side but can be tricky if the logic varies
depending on the event type or producer.

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

### expirytime

- Type: `Timestamp`
- Description: Timestamp indicating an event is no longer useful after the
  indicated time.
- Constraints:
  - REQUIRED
  - SHOULD be equal to or later than the `time` attribute, if present

## Usage

When this extension is used, producers MUST set the value of the `expirytime`
attribute.

Intermediaries and consumers MAY ignore and discard an event that has an
`expirytime` at or before the current timestamp at the time of any checks.
Any system that directly or indirectly interacts with a consumer SHOULD NOT
make any assumptions on whether a consumer will
keep or discard an event based on this extension alone. The reasoning for this
is that time-keeping can be inaccurate between any two given systems.

Intermediaries MAY modify the `expirytime` attribute, however, they MUST NOT
remove it.

## Potential Scenarios

### Web dashboard for sensors

A series of sensors produce CloudEvents at regular intervals that vary per
sensor. Each sensor can pick an `expirytime` that suits its configured sample
rate. In the event that an intermediary delays delivery of events to a
consumer, older events can be skipped to avoid excessive processing or UI
updates upon resuming delivery.

### Jobs triggered by Continuous Integration

A Continuous Integration (CI) system uses CloudEvents to delegate a job to a
runner machine. The job has a set deadline and needs to complete before that time
has elapsed to be considered successful. The CI system can set the
`expirytime` to match the deadline. The job runner would ignore/reject the job
if the `expirytime` has elapsed since the CI might have likely already determined
the job state.
