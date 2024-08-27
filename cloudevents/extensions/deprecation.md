# Deprecation extension

This specification defines attributes that can be included in CloudEvents to
indicate to [consumers](../spec.md#consumer) or
[intermediaries](../spec.md#intermediary) the deprecation of events. These
attributes inform CloudEvents consumers about upcoming changes or removals,
facilitating smoother transitions and proactive adjustments.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is
used. For example, an attribute being marked as "REQUIRED" does not mean it
needs to be in all CloudEvents, rather it needs to be included only when this
extension is being used.

## Attributes

### deprecated

- Type: `Boolean`
- Description: Indicates whether the event type is deprecated.
- Constraints
  - MUST be `true`
  - REQUIRED
- Example: `"deprecated": true`

### deprecationfrom

- Type: `Timestamp`
- Description: Specifies the date and time when the event type was
  officially marked as deprecated.
- Constraints
  - OPTIONAL
  - The `deprecationfrom` timestamp SHOULD remain stable once set and SHOULD
    reflect a point in the past or present. Pre-announcing deprecation by
    setting a future date is not encouraged.
- Example: `"deprecationfrom": "2024-10-11T00:00:00Z"`

### deprecationsunset

- Type: `Timestamp`
- Description: Specifies the future date and time when the event type will
  become unsupported.
- Constraints
  - OPTIONAL
  - The timestamp MUST be later than or the same as the one given in the
    `deprecationfrom` field, if present. It MAY be extended to a later date but
    MUST NOT be shortened once set.
- Example: `"deprecationsunset": "2024-11-12T00:00:00Z"`

### deprecationmigration

- Type: `URI`
- Description: Provides a link to documentation or resources that describe
the migration path from the deprecated event to an alternative. This helps
consumers transition away from the deprecated event.
- Constraints
  - OPTIONAL
  - The URI SHOULD point to a valid and accessible resource that helps
    consumers understand what SHOULD replace the deprecated event.
- Example: `"deprecationmigration": "https://example.com/migrate-to-new-evt"`

## Usage

When this extension is used, producers MUST set the value of the `deprecated`
attribute to `true`. This gives consumers a heads-up that they SHOULD begin
migrating to a new event or version.

Consumers SHOULD make efforts to switch to the suggested replacement before the
specified `deprecationsunset` timestamp. It is advisable to begin transitioning
as soon as the event is marked as deprecated to ensure a smooth migration and
avoid potential disruptions after the sunset date.

If an event is received after the `deprecationsunset` timestamp, consumers
SHOULD choose to stop processing such events, especially if unsupported events
can cause downstream issues.

Producers SHOULD stop emitting deprecated events after the `deprecationsunset`
timestamp. They SHOULD also provide detailed documentation via the
`deprecationmigration` attribute to guide consumers toward the correct replacement
event.
