# Ordinal

This extension defines an attribute that can be included within a CloudEvent
to represent the ordinal position of the event relative to the other events
from the same event source.

## Attributes
### ordinal
* Type: `String`
* Description: Value expressing the relative order of the event. This enables
  interpretation of data supercedence.
* Constraints
  * REQUIRED
  * MUST be a non-empty lexicographically-orderable string

