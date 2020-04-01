# Sequence

This extension defines two attributes that can be included within a CloudEvent
to describe the position of an event in the ordered sequence of events produced
by a unique event source.

The `sequence` attribute represents the value of this event's order in the
stream of events. The exact value and meaning of this attribute is defined by
the `sequencetype` attribute. If the `sequencetype` is missing, or not defined
in this specification, event consumers will need to have some out-of-band
communication with the event producer to understand how to interpret the value
of the attribute.

## Attributes

### sequence

- Type: `String`
- Description: Value expressing the relative order of the event. This enables
  interpretation of data supercedence.
- Constraints
  - REQUIRED
  - MUST be a non-empty lexicographically-orderable string
  - RECOMMENDED as monotonically increasing and contiguous

### sequencetype

- Type: `String`
- Description: Specifies the semantics of the sequence attribute. See the
  [SequenceType Values](#sequencetype-values) section for more information.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string

## SequenceType Values

This specification defines the following values for `sequencetype`. Additional
values MAY be defined by other specifications.

### Integer

If the `sequencetype` is set to `Integer`, the `sequence` attribute has the
following semantics:

- The values of `sequence` are string-encoded signed 32-bit Integers.
- The sequence MUST start with a value of `1` and increase by `1` for each
  subsequent value (i.e. be contiguous and monotonically increasing).
- The sequence wraps around from 2,147,483,647 (2^31 -1) to -2,147,483,648
  (-2^31).
