# Sequence

This extension defines an attribute that can be included within a CloudEvent
to represent the position of the event relative to the other events
from the same event source. The exact value and meaning of this attribute
is not defined by this specification. Event consumers will need to
have some out-of-band communication with the event producer to understand
how to interpret its value.

## Attributes
### sequence
* Type: `String`
* Description: Value expressing the relative order of the event. This enables
  interpretation of data supercedence.
* Constraints
  * REQUIRED
  * MUST be a non-empty lexicographically-orderable string
  * RECOMMENDED as contiguous

