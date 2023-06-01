# Sequence

This extension defines an attribute that can be included within a CloudEvent
to describe the position of an event in the ordered sequence of events produced
by a unique event source.

The `sequence` attribute represents the value of this event's order in the
stream of events. This specification does not define the meaning or set of
valid value of this attribute, rather it only mandates that the value be
a string that can be lexicographically compared to other `sequence` values
to determine which one comes first. The `sequence` with a lower lexicographical
value comes first.

Produces and consumers are free to define an out-of-band agreement on the
semantic meaning, or valid values, for the attribute.

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

### sequence

- Type: `String`
- Description: Value expressing the relative order of the event. This enables
  interpretation of data supercedence.
- Constraints
  - REQUIRED
  - MUST be a non-empty lexicographically-orderable string
  - RECOMMENDED as monotonically increasing and contiguous

The entity creating the CloudEvent MUST ensure that the `sequence` values
used are formatted such that across the entire set of values used a receiver
can determine the order of the events via a simple string-compare type of
operation. This means that it might be necessary for the value to include
some kind of padding (e.g. leading zeros in the case of the value being the
string representation of an integer).
