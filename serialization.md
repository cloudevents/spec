# CloudEvents Serialization Profile - Version 0.1

This document specifies how a CloudEvent is to be serialized into certain
encoding formats. Compliant CloudEvents implementations that support these
formats MUST adhere to these rules for these formats.

## Table of Contents
- [Notational Conventions](#notational-conventions)
- [JSON](#json)

## Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to
be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

## JSON

When serialized in [JSON](https://tools.ietf.org/html/rfc7159) a CloudEvent
MUST adhere to the following format:

```
{
  "cloud-events-version": "cloud-events-version value",
  "event-id": "event-id value",
  "namespace": "namespace value",
  "source": {
    "type": "source-id value",
    "id": "source-id value"
  },
  "event-type": "event-type value",
  "event-type-version": "event-type value",
  "schema-url": "schema-url value",
  "extensions": {
    ... extensions values ...
  },
  "data": ... data value ...
}
```

Notes:
- The use of whitespace is not significant.
- The order of the properties, at any level, is not significant.
- CloudEvent producers MAY include additional properties in the JSON
  but receivers MAY choose to ignore them. However, it is RECOMMENDED that
  they be placed as children of the `extensions` property. Receivers
  MUST NOT treat unkonwn additional properties as an error and MUST NOT stop
  processing of the event as a result of their presence.
