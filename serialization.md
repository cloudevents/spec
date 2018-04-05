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
  "cloudEventsVersion": "cloudEventsVersion value",
  "eventID": "eventID value",
  "source": "source value",
  "eventType": "eventType value",
  "eventTypeVersion": "eventTypeVersion value",
  "eventTime": "eventTime value",
  "schemaURL": "schemaURL value",
  "contentType": "contentType",
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
- Non-mandatory properties are NOT REQUIRED to be included in the JSON, but
  if they are present then they MUST adhere to the format described.

Example:
```
{
  "cloudEventsVersion": "0.1",
  "eventID": "6480da1a-5028-4301-acc3-fbae628207b3",
  "source": "http://example.com/repomanager",
  "eventType": "created",
  "eventTypeVersion": "v1.5",
  "eventTime": "2018-04-01T23:12:34Z",
  "schemaURL": "https://product.example.com/schema/repo-create",
  "contentType": "application/json",
  "data": {
    "path": "/JaneDoe/repos/mycode"
  }
}
```
