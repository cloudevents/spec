# Sequence

This extension defines two attributes that can be included within a CloudEvent
to describe the position of the event relative to the other events from the
same event source.

The `sequence` attribute represents the value of this event's
order in the stream of events.  The exact value and meaning of this
attribute is defined by the `sequenceType` attribute. 
If the `sequenceType` is missing, or not defined in this specification,
event consumers will need to have some out-of-band communication with the
event producer to understand how to interpret the value of the attribute.

## Attributes

### sequence
* Type: `String`
* Description: Value expressing the relative order of the event. This enables
  interpretation of data supercedence.
* Constraints
  * REQUIRED
  * MUST be a non-empty lexicographically-orderable string
  * RECOMMENDED as contiguous

### sequenceType
* Type: `String`
* Description: Defines the semantics of the sequence attribute.
  See the [SequenceType Values](#sequencetype-values) section for more
  information.
* Constraints:
  * OPTIONAL
  * If present, MUST be a non-empty string

## SequenceType Values

This specification defines the following values for `sequenceType`.
Additional values MAY be defined by other specifications.

### Integer
If the `sequenceType` is set to `Integer`, the `sequence` attribute has
the following semantics:
* The values of `sequence` are string-encoded signed 32-bit Integers
* The first CloudEvent in an `Integer` sequence MUST have the value
  `1`, the second `2`, etc.
* The sequence MUST be contiguous. In other words, if the event consumer
  receives two CloudEvents with `sequence` values of `1` and `3`, another
  CloudEvent with a `sequence` value of `2` exists, but has not been received
  yet.
* The sequence wraps around from 2,147,483,647 (2^31 -1) to
  -2,147,483,648 (-2^31).

