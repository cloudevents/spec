# Partitioning extension

This extension defines an attribute for use by message brokers and their clients
that support partitioning of events, typically for the purpose of scaling.

Often in large scale systems, during times of heavy load, events being received
need to be partitioned into multiple buckets so that each bucket can be
separately processed in order for the system to manage the incoming load. A
partitioning key can be used to determine which bucket each event goes into. The
entity sending the events can ensure that events that need to be placed into the
same bucket are done so by using the same partition key on those events.

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
