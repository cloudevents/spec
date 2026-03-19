# App Context

<!-- no-verify-translation -->

This extension gives information about a mobile app that triggered an event.
This is a way to authenticate the app that triggered an event, orthogonally
to a source.

For example, in an end-user accessible backend like a Supabase or Firebae database,
the source of a data change event is the database. But the authentication for that
write might be the user (covered by the [authcontext](./authcontext.md) extension)
and the app that triggered the event (covered by this extension).

Common uses can be to track engagement with a particular app, or to
allow a backend to enforce policies based on the app that triggered
an event. For example, either the user or the app can be used to identify
whether an AI API could have high or low rate limits, expensive or cost effective
models, etc.

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

### appid
- Type: `String`
- Description: A cloud provider opaque string identifying the mapping of a given
  app to a given backend.
- Constraints
  - OPTIONAL

### appdisplayname
- Type: `String`
- Description: How the app appears to users.
- Constraints
  - OPTIONAL

### androidpackagename
- Type: `String`
- Description: The Android package name of the app triggering the event.
  It MUST follow Android package naming conventions: it MUST have at least two segments,
  separated by periods (`.`); each segment MUST start with a letter; and all characters
  MUST be alphanumeric or an underscore (`[a-zA-Z0-9_]`).
- Constraints
  - OPTIONAL
  - MUST be present if the app is an Android app.

### iosbundleid
- Type: `String`
- Description: The Apple bundle identifier of the app triggering the event.
  It MUST follow Apple bundle naming conventions: it MUST contain only alphanumeric
  characters (`A-Z`, `a-z`, `0-9`), hyphens (`-`), and periods (`.`), typically adopting
  a reverse-DNS format.
- Constraints
  - OPTIONAL
  - MUST be present if the app is an iOS app.
