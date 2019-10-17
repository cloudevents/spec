# Partitioning extension

This extension defines an attribute for use by message brokers and their clients
that support partitioning of events, typically for the purpose of scaling.

Often in large scale systems, during times of heavy load, events being received
need to be partitioned into multiple buckets so that each bucket can be
separately processed in order for the system to manage the incoming load. A
partitioning key can be used to determine which bucket each event goes into. The
entity sending the events can ensure that events that need to be placed into the
same bucket are done so by using the same partition key on those events.

## Attributes

### partitionkey

- Type: `String`
- Description: A partition key for the event, typically for the purposes of
  defining a causal relationship/grouping between multiple events. In cases
  where the CloudEvent is delivered to an event consumer via multiple hops,
  it is possible that the value of this attribute might change, or even be
  removed, due to protocol semantics or business processing logic within
  each hop.
- Examples:
  - The ID of the entity that the event is associated with
- Constraints:
  - REQUIRED
  - MUST be a non-empty string
