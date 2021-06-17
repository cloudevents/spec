# Sampled Rate Extension

There are many cases in an Event's life when a system (either the system
creating the event or a system transporting the event) might wish to only emit a
portion of the events that actually happened. In a high throughput system where
creating the event is costly, a system might wish to only create an event for
1/100 of the times that something happened. Additionally, during the
transmission of an event from the source to the eventual recipient, any step
along the way might choose to only pass along a fraction of the events it
receives.

In order for the system receiving the event to understand what is actually
happening in the system that generated the event, information about how many
similar events happened would need to be included in the event itself. This
field provides a place for a system generating an event to indicate that the
emitted event represents a given number of other similar events. It also
provides a place for intermediary transport systems to modify the event when
they impose additional sampling.

## Attributes

### sampledrate

- Type: `Integer`
- Description: The rate at which this event has already been sampled. Represents
  the number of similar events that happened but were not sent plus this event.
  For example, if a system sees 30 occurrences and emits a single event,
  `sampledrate` would be 30 (29 not sent and 1 sent). A value of `1` is the
  equivalent of this extension not being used at all.
- Constraints
  - The rate MUST be greater than zero.
