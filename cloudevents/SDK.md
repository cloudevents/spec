# CloudEvents SDK Requirements

<!-- no verify-specs -->

The intent of this document to describe a minimum set of requirements for new
Software Development Kits (SDKs) for CloudEvents. These SDKs are designed and
implemented to enhance and speed up CloudEvents integration. As part of
community efforts CloudEvents team committed to support and maintain the
following SDKs:

- [CSharp](https://github.com/cloudevents/sdk-csharp)
- [Go SDK](https://github.com/cloudevents/sdk-go)
- [Java SDK](https://github.com/cloudevents/sdk-java)
- [JavaScript SDK](https://github.com/cloudevents/sdk-javascript)
- [PHP SDK](https://github.com/cloudevents/sdk-php)
- [PowerShell](https://github.com/cloudevents/sdk-powershell)
- [Python SDK](https://github.com/cloudevents/sdk-python)
- [Ruby SDK](https://github.com/cloudevents/sdk-ruby)
- [Rust SDK](https://github.com/cloudevents/sdk-rust)

This is intended to provide guidance and requirements for SDK authors. This
document is intended to be kept up to date with the CloudEvents spec.

## Contribution Acceptance

Being an open source community the CloudEvents team is open for new members as
well open to their contributions. In order to ensure that an SDK is going to be
supported and maintained the CloudEvents community would like to ensure that:

- Each SDK has active points of contact.
- Each SDK supports the latest(N), and N-1, major releases of the
  [CloudEvent spec](spec.md)\*.
- Within the scope of a major release, only support for the latest minor
  version is needed.

Support for release candidates is not required, but strongly encouraged.

\* Note: v1.0 is a special case and it is recommended that as long as v1.0
  is the latest version, SDKs should also support v0.3.

## Technical Requirements

Each SDK MUST meet these requirements:

- Supports CloudEvents at spec milestones and ongoing development version.
  - Encode a canonical Event into a transport specific encoded message.
  - Decode transport specific encoded messages into a Canonical Event.
- Idiomatic usage of the programming language.
  - Using current language version(s).
- Supports HTTP transport renderings in both `structured` and `binary`
  content mode.

### Object Model Structure Guidelines

Each SDK will provide a generic CloudEvents class/object/structure that
represents the canonical form of an Event.

The SDK should enable users to bypass implementing transport specific encoding
and decoding of the CloudEvents `Event` object. The general flow for Objects
should be:

```
Event (-> Message) -> Transport
```

and

```
Transport (-> Message) -> Event
```

An SDK is not required to implement a wrapper around the transport, the focus
should be around allowing programming models to work with the high level `Event`
object, and providing tools to take the `Event` and turn it into something that
can be used with the implementation transport selected.

At a high level, the SDK needs to be able to help with the following tasks:

1. Compose an Event.
1. Encode an Event given a transport and encoding (into a Transport Message if
   appropriate).
1. Decode an Event given a transport specific message, request or response (into
   a Transport Message if appropriate).

#### Compose an Event

Provide a convenient way to compose both a single message and many messages.
Implementers will need a way to quickly build up and convert their event data
into the a CloudEvents encoded Event. In practice there tend to be two aspects
to event composition,

1. Event Creation

- "I have this data that is not formatted as a CloudEvent and I want it to be."

1. Event Mutation

- "I have a CloudEvents formatted Event and I need it to be a different Event."
- "I have a CloudEvents formatted Event and I need to mutate the Event."

Event creation is highly idiomatic to the SDK language.

Event mutation tends to be solved with an accessor pattern, like getters and
setters. But direct key access could be leveraged, or named-key accessor
functions.

In either case, there MUST be a method for validating the resulting Event object
based on the parameters set, most importantly the CloudEvents spec version.

#### Encode/Decode an Event

Each SDK will support encoding and decoding an Event with regards to a transport
and encoding. `Structured` encoding is the easiest to support, as it is just
`json`, but `Binary` is fairly custom for each transport.

#### Data

Data access from the event has some considerations, the Event at rest could be
encoded into the `base64` form, as structured data, or as a wire format like
`json`. An SDK MUST provide a method for unpacking the data from these formats
into a native format.

#### Extensions

Supporting CloudEvents extensions is idiomatic again, but a method that mirrors
the data access seems to work.

#### Validation

Validation MUST be possible on an individual Event. Validation MUST take into
account the spec version, and all the requirements put in-place by the spec at
each version.

## Documentation

Each SDK must provide examples using at least HTTP transport of:

- Composing an Event.
- Encoding and sending a composed Event.
- Receiving and decoding an Event.
