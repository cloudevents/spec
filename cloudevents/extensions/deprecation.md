# Deprecation and Sunset extension

This specification defines attributes that can be included in CloudEvents to
indicate to [consumers](../spec.md#consumer) or
[intermediaries](../spec.md#intermediary) the deprecation and sunset status of
the event type. These attributes inform consumers of CloudEvents about upcoming
changes or removals, facilitating smoother transitions and proactive
adjustments.

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

### deprecation

- Type: `String`
- Description: Indicates that the event type is deprecated. This can be a
  boolean `true` or a date in [RFC 5322](https://tools.ietf.org/html/rfc5322)
  format indicating when the deprecation was announced.
- Constraints
  - REQUIRED
  - If the value is a date, it MUST be formatted according to RFC 5322.
- Examples:
  - A boolean deprecation: `"deprecation": "true"`
  - A date-based deprecation: `"deprecation": "Sun, 11 Aug 2024 23:59:59 GMT"`

### sunset

- Type: `String`
- Description: Specifies the future date and time when the event type will
  become unsupported, formatted according to
  [RFC 8594](https://tools.ietf.org/html/rfc8594).
- Constraints
  - OPTIONAL
  - The timestamp MUST be later or the same as the one given in the
    `deprecation` field.
- Example: `"sunset": "Wed, 14 Aug 2024 23:59:59 GMT"`

## Usage

When this extension is used, producers MUST set the value of the `deprecation`
attribute to `true` or the `timestamp` of when an event is being phased out but
still supported. This gives consumers a heads-up that they SHOULD begin
migrating to a new event type or version.

The `sunset` attribute SHOULD specify the exact date and time when the event
will no longer be supported. This is the final cutoff date after which the
event will no longer function as expected.
