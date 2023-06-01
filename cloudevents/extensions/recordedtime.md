# Recorded Time Extension

This extension defines an attribute that represents the time when an
[_occurrence_](../spec.md#occurrence)
was recorded in a particular
[_event_](../spec.md#event),
which is the time when the CloudEvent was created by a producer.

This attribute is distinct from the [`time`
attribute](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md#time),
which, according to the CloudEvents specification, SHOULD be the time when the
occurrence happened, if it can be determined.

This attribute makes it possible to represent
[bitemporal](https://en.wikipedia.org/wiki/Bitemporal_modeling) data with
CloudEvents so that, for every event, both of the following times can be known
by consumers:

- _Occurrence time_: timestamp of when the occurrence recorded in the event
  happened, which corresponds to the `time` attribute.
- _Recorded time_: the timestamp of when the occurrence was recorded in a
  specific CloudEvent instance, which is represented by this extension.

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

### recordedtime

- Type: `Timestamp`
- Description: Timestamp of when the occurrence was recorded in this CloudEvent,
  i.e. when the CloudEvent was created by a producer.
- Constraints:
  - REQUIRED
  - If present, MUST adhere to the format specified in
    [RFC 3339](https://tools.ietf.org/html/rfc3339)
  - SHOULD be equal to or later than the _occurrence time_.

## Usage

When this extension is used, producers MUST set the value of the `recordedtime`
attribute to the timestamp of when they create the owning CloudEvent.

If the same occurrence MUST be recorded differently, or the event data or
attributes of a previous record of the occurrence MUST be amended or redacted,
then the new CloudEvent with the necessary changes SHOULD have a different
`recordedtime` attribute value than the previous record of the occurrence.

Intermediaries MUST NOT change the value of the `recordedtime` attribute.

## Use cases

Examples of when an occurrence might need to be recorded differently are:

- When incompatible changes to the event data schema are made, and there are
  systems that can only process the new schema.
- When a previous record contains incorrect information.
- When a previous record contains personal information that can no longer be
  kept because of regulatory or statutory reasons and needs to be redacted.

Having bitemporal data makes it easier to get reproducible datasets for
analytics and data science, as the datasets can be created by placing
constraints on both the `time` and `recordedtime` attributes of events.

Knowing when an occurrence was recorded in a particular event also makes it
possible to determine latency between event producers and consumers. It also
makes it possible to do operations which are sensitive to the time when an event
was recorded, such as capturing events into time-intervalled files.

The recorded time also makes it easier to differentiate different records of the
same occurrence in analytical data stores.
