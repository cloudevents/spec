# CloudEvents Subscriptions API - Version 0.1-wip

## Abstract

This specification defines mechanisms, including an API definition, for CNCF
CloudEvents event consumers to subscribe to events originating from event
producers on behalf of event sources. The software entity handling these
subscriptions and responsible for distributing events is abstractly referred to
as a "subscription manager".

## 1. Introduction

A subscription manager responsible for a specific set of events can reside
immediately at or near the event producer or it can reside in some middleware
infrastructure. This document does not formalize the relationship between the
original event producer and the subscription manager, and how the subscription
manager obtains the events it distributes to subscribers.

This document also does not formalize the relationship between a specific set of
events and the subscription manager. An event producer that produces multiple
different types of events can offer one subscription manager for all events or a
subscription manager for each type of event, or any other combination. An event
producer can also offer up the same set of events for subscription at multiple
concurrent subscription managers. Regardless of relationship between the event
producer(s) and the subscription manager(s), the advertisement of the
subscription offers are published in a CloudEvents Registry service.

As with the core CloudEvents specification, the goal of this specification is to
reuse mechanisms based on existing standards and conventions where such exist
and only introduce new mechanisms where needed.

Therefore, this specification not only defines a new subscription management API
for certain use-cases, but also refers to existing mechanisms available in the
specifications of transport protocols for which CloudEvents bindings exist.

For instance, introducing and mandating a CloudEvents-specific subscription
mechanism for MQTT would only complicate implementations while not providing any
obvious advantage. Using any of the referred native subscription mechanisms of
the respective transport protocols is therefore within the scope and in
compliance with this specification.

## 2. Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

### Terminology

This specification uses the following terms:

#### Source

An event source is a logical entity in a system on behalf of which events are
produced based on occurrences.

#### Producer

The entity producing the event. The event might reflect an occurrence on a
source elsewhere in the system. The producer is the concrete entity that creates
and sends the event related to an occurrence.

#### Intermediary

An "intermediary" (also referred to as middleware) receives an event for the
purpose of forwarding it to the next receiver, which might be another
intermediary or a consumer. A typical task for an intermediary is to route the
event to receivers based on the information in the event context.

#### Consumer

An entity receiving and processing events. Consumers might receive events from
producers directly or via intermediaries. A consumer might listen and wait for
events to be delivered to it or it might actively solicit them from the producer
or intermediary.

#### Subscription

A relationship established between a consumer and a producer or an intermediary.
The subscription reflects the consumer's interest in receiving events and
describes the method for how to deliver those events.

#### Subscription Manager

An entity, defined in this specification, that manages the lifecycle of a
subscription on behalf of an event consumer and that distributes events to
registered consumers.

## 3. Event Subscriptions

This specification defines mechanisms for CNCF CloudEvents event consumers to
subscribe to events originating from producers on behalf of event sources. The
software entity handling these subscriptions and responsible for distributing
events is abstractly referred to as a "subscription manager".

A compliant CloudEvents subscription manager MUST support at least one of the
transport protocols referenced in this specification and it MUST implement the
subscription mechanism referred to or defined in this specification.

In some cases, the event producer MAY delegate the role of the subscription
manager to some intermediary, in which case produced events are made available
to the intermediary, and the intermediary's subscription manager determines who
receives copies of the published events. In other cases, the event producer MAY
take on the subscription manager role by itself.

In this specification, we distinguish two styles of relationships between an
event consumer and a subscription manager, whereby the key differentiator is how
the event delivery channel to the consumer is initiated:

- Subscriptions with consumer-solicited delivery ("pull"-style) are configured
  on the subscription manager for delivering events through a communication
  channel (like an AMQP link or a MQTT connection) initiated by the consumer and
  connecting to the subscription manager. These kinds of subscriptions are
  typically offered by messaging or eventing middleware and their lifetime might
  be bounded by the lifetime of the communication channel.

- Subscriptions with subscription-manager-initiated delivery ("push"-style) are
  configured on the subscription manager for delivering events through a
  communication channel that the subscription manager initiates when events are
  available for delivery on the subscription. The configuration of such a
  subscription MUST contain all information needed for the subscription manager
  to select a transport protocol, establish the desired communication channel,
  and deliver the event(s).

An end-to-end solution using CloudEvents might use only one of these styles or a
combination of those.

For instance, the solution might use an MQTT broker to handle delivery of events
into connected devices that connect into the broker and subscribe on a
particular MQTT topic, which acts as the subscription manager in the sense of
this specification ("pull"-style). The events that ought to be shared with the
connected devices might however originate elsewhere in the overall solution, and
some event router middleware's subscription manager might therefore be
configured to initiate delivery of events ("push"-style) into the given MQTT
broker topic whenever such events are available.

### 3.1 Native Subscription Management Mechanisms

MQTT, AMQP, NATS, and Apache Kafka are protocols with a formal CloudEvents
binding that have native mechanisms filling the role of a subscription manager.

Using any of these subscription management mechanisms ought to allow an
application to claim conformance with this specification. More specifically, an
application that uses an MQTT or AMQP message broker as its middleware component
ought be able to use the native capabilities of those protocols to subscribe to
CloudEvents event streams without requiring CloudEvents Subscription
API-specific mechanisms or extensions. The conformance section in this document
formally enumerates the requirements.

_The descriptions of the protocol subscription mechanisms in this section are
non-normative. Please refer to the protocol specifications or documentation for
normative definitions._

#### 3.1.1. MQTT 3.x/5.x

The MQTT 3.x/5.x protocol has a native "SUBSCRIBE" (and matching "UNSUBSCRIBE")
operation, which allows a consumer to solicit messages matching a pattern
against the MQTT broker's topic path hierarchy.

Once an MQTT consumer has issued one or multiple SUBSCRIBE requests, matching
events for any of the MQTT session's active subscription are delivered by the
broker to the consumer without requiring further interactions. Depending on the
quality-of-service (QoS) level of the subscription, individual deliveries might
have to be acknowledged by the consumer.

The lifetime of a subscription is bounded by lifetime of the MQTT session.

Events are published using the "PUBLISH" operation on a path into the topic
hierarchy, and all current subscriptions whose topic filters match the path
receive a message.

The operations are normatively defined in the
[MQTT 3.1.1](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html) and
[MQTT 5.0](http://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
specifications.

#### 3.1.2. AMQP 1.0

The AMQP 1.0 protocol has a built-in subscription mechanism.

When an AMQP container establishes a receive-role link to another container, it
can specify a "distribution-mode" on the link source in the other container. If
the distribution mode is "copy", each such established link receives a copy of
the message stream available at the distribution node. If the distribution mode
is "move", messages are exclusively owned by the link and are removed from the
source when the transfer is settled successfully.

Supporting the "copy" mode, is OPTIONAL for the underlying implementation of the
broker

The link source can also be configured with filters. The AMQP core specification
does not define concrete filter types, but the AMQP Filter Expressions 1.0
extension specification and the Apache Qpid project's filter definitions do.

#### 3.1.3. NATS

The NATS protocol has a native subscribe operation "SUB" (and matching "UNSUB"),
which allows a client to solicit a stream of messages that match a given subject
or a wildcard.

Events are published using the "PUB" operation with a subject name that is then
matched against the existing subscriptions.

#### 3.1.4. Apache Kafka

Apache Kafka allows consumers to fetch events stored in topic partitions once or
multiple times.

While Apache Kafka does not have a server-side subscribe operation and also does
not provide filtering capabilities, it allows the fetching client to fully
control from which offset in the partition's log store events are being read
from. This allows multiple parties to retrieve the same set of events from the
stream.

The management of the subscription and selecting which events are being fetched
and dispatched into the application lies completely with the consumer in the
Apache Kafka case.

#### 3.1.5. HTTP

HTTP does not have a built-in subscription mechanism that allows for
establishing a flow of events similar to the aforementioned protocols. HTTP
allows for modeling pull-style retrieval of events from a store and, with HTTP/2
"server push", even for continuous delivery an event stream triggered by a
initial request, but for event delivery scenarios, these techniques are
applications of HTTP rather than inherent features of HTTP per-se.

### 3.2. Subscription Manager API

The subscription manager API defines a subscription object and a protocol for
creating, updating and deleting subscriptions on a subscription manager.

The subscription object describes the consumer's interest in events and defines
the delivery method. The protocol allows to configure subscriptions on the
subscription manager. Especially in case of subscription manager initiated
("push"-style) delivery, the protocol is used to express the consumer's interest
to the subscription manager before the subscription manager can initiate
delivery.

The protocol used to configure the subscription manager is decoupled from the
delivery protocol, meaning that an application can configure a push delivery
into an AMQP destination using an API call initiated over HTTP.

A subscription manager that natively exists in a middleware implementation might
also have a separate CloudEvents subscription manager API endpoint
implementation. If such a separate API endpoint exists and creating
subscriptions is not feasible on such a separate API endpoint, the respective
operation might not be available. For instance, creating an MQTT subscription is
not feasible from outside an MQTT connection, but an existing subscription might
be enumerable through a subscription collection and deleting the subscription
from the collection might terminate it.

#### 3.2.1. Subscription Object

A subscription manager manages a collection of subscriptions. The upper limit on
how many subscriptions are supported is implementation specific.

To help explain the subscription resource, the following non-normative pseudo
json shows its basic structure:

(`*` means zero or more, `+` means one or more, `?` means OPTIONAL)

Subscription:

```
{
  "id": "[a subscription manager scoped unique string]",
  "source": "[...]", ?
  "types": "[ "[ce-type values]" + ]", ?
  "config": { ?
    "[key]": [subscription manager specific value], *
  },

  "filters": [ ?
    { "[dialect name]": [dialect specific object] } +
  ],

  "sink": "[URI to where events are delivered]",
  "protocol": "[delivery protocol]",
  "protocolsettings": { ?
    "[key]": "[type]", *
  }
}
```

Each subscription is represented by an object that has the following properties:

##### id

- Type: `String`
- Description: The unique identifier of the subscription in the scope of the
  subscription manager. This value MUST be unique within the scope of the
  subscription manager and MUST be immutable.

- Constraints:
  - REQUIRED when retrieving the object
  - if present on the input to a subscribe operation then it MUST be ignored
- Examples:
  - `f1d15fd0-6893-11eb-9439-0242ac130002`
  - `bigco-subscription-1234`

##### source

- Type: `URI-reference` - a CloudEvents `source` value
- Description: Indicates the source to which the subscription is related.
  When present on a subscribe request, all events generated due to this
  subscription MUST have a CloudEvents `source` property that matches this
  value. If this property is not present on a subscribe request then there
  are no constraints placed on the CloudEvents `source` property for the
  events generated.

  TODO: add something to discovery to indicate if manager supports this

- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI
- Examples:
  - `/sensors/tn-1234567/alerts`

##### types

- Type: `Array of Strings` - array of CloudEvents `type` values
- Description: Indicates which types of events the subscriber is interested
  in receiving. When present on a subscribe request, all events generated
  due to this subscription MUST have a CloudEvents `type` property that
  matches one of these values.

- Constraints:
  - OPTIONAL
  - If present, any value present MUST a non-empty string
- Examples:
  - `com.github.pull_request.opened`
  - `com.example.object.deleted`

##### config

- Type: `Map` of subscription manager defined types
- Description: A set of key/value pairs that modify the configuration of
  of the subscription related to the event generation process. While this
  specification places no constraints on the data type of the map values.
  When there is a Registry Endpoint Service definition defined for the
  subscription manager, then the `key` MUST be one of the `subscriptionconfig`
  keys specified in the Registry Endpoint Service definition. The `value`
  MUST conform to the data type specified by the value in the
  `subscriptionconfig` entry for the `key`

- Constraints:
  - OPTIONAL
  - If present, any "key" used in the map MUST be a non-empty string
- Examples:
  - `{ "interval": 5 }`

##### filters

- Type: `Array of Objects`
- Description: An array of filter expressions that evaluates to true or false.
  If any filter expression in the array evaluates to false, the event
  MUST NOT be sent to the sink. If all the filter expressions in the array evaluates to true, the event
  MUST be attempted to be delivered. Absence of a filter or empty array implies a value
  of true.

  Each filter dialect MUST have a name that is unique within the scope of the
  subscription manager. Each dialect will define the semantics and syntax of
  the filter expression language. See the [Filters](#324-filters) section for
  more information.

  If a subscription manager does not support filters, or the filter dialect
  specified in a subscription request, then it MUST generate an error and
  reject the subscription create or update request.

- Constraints:
  - OPTIONAL for both subscription managers and subscribers to support
- Examples:
  - [ {"prefix": { "type": "com.github.issue" } } ]

##### sink

- Type: `URI`
- Description: The address to which events MUST be sent. The format of the
  address MUST be valid for the protocol specified in the `protocol`
  property, or one of the protocol's own transport bindings (e.g. AMQP over
  WebSockets).

- Constraints:
  - REQUIRED
- Examples:
  - `https://example.com/event-processor`

##### sinkCredential

- Type: Map of attributes
- Description: A set of settings carrying credential information that
  is enabling the entity delivering events to the subscription target to
  be authorized for delivery at the `sink` endpoint. The well-known
  attribute values are defined in [section 3.2.3](#323-sink-credentials).

  Implementations SHOULD NOT include secrets contained in this map when
  the subscription object is enumerated or retrieved. Secrets SHOULD be
  write-only. Tokens, passphrases, and passwords are such secrets and
  account identifiers might be considered secrets as well.

- Constraints:
  - OPTIONAL

##### protocol

- Type: `String`
- Description: Identifier of a delivery protocol. Because of WebSocket
  tunneling options for AMQP, MQTT and other protocols, the URI scheme is not
  sufficient to identify the protocol. The protocols with existing CloudEvents
  bindings are identified as `AMQP`, `MQTT3`, `MQTT5`, `HTTP`, `KAFKA`, and
  `NATS`. An implementation MAY add support for further protocols.

- Constraints:
  - REQUIRED
  - Value comparisons MUST be case sensitive.
- Examples:
  - `HTTP`

##### protocolsettings

- Type: Map of protocol specific attributes
- Description: A set of settings specific to the selected delivery protocol
  provider. Options for these settings are listed in the following subsection.
  An subscription manager MAY offer more options. See the [Protocol
  Settings](#322-protocol-settings) section for future details.

- Constraints:
  - OPTIONAL
- Examples:
  - Credentials
  - Retry policies
  - QoS modes

In general the intent of this specification is to consider the processing of
events to have 3 conceptual phases:

- event generation. This phase creates the events and is typically controlled
  by the `config`, `source` and `types` properties. This might include settings
  that influence how often events are generated, or the scope of the event
  sources being monitored.
- event filtering. This phase, as the name implies, will "filter" the stream
  of events generated from the previous phase. The **filters** property will be
  used to specify how this filtering will be done. Whether this is done
  separately from the event generation phase, or as part of it, is an
  implementation choice. It is also possible for Subscription Managers to
  control this aspect of the event stream via the **config** property if they
  so choose.
- event transmission. This phase controls how the events are sent to the sink.
  Typically, by this step in the processing the set of events to be sent are
  already known and the only variable is the exact mechanism that will be used
  to send them. The **protocol** and **protocolsettings** properties will
  control this phase.

Additionally, it might be possible for one Subscription property to have
influence over multiple phases of the event processing. Regardless of which
aspect of the Subscription is controlled by which of the above
phases/properties, the Service description specified by the Registry
specification SHOULD contain enough information for a consumer to know which
properties to use when creating a Subscription to get the desired results.

Below is an example JSON serialization of a subscription resource:

```JSON
{
  "id": "sub-193-18365",

  "config": {
    "data": "hello",
    "interval": 5
  },

  "filters": [
    { "prefix": { "type": "com.example." } }
  ],

  "protocol": "HTTP",
  "protocolsettings": {
    "method": "POST"
  },
  "sink": "http://example.com/event-processor"
}
```

#### 3.2.2 Protocol Settings

This section enumerates protocol-specific delivery options for the
protocol-settings map, including default values where necessary.

##### 3.2.2.1. HTTP

For HTTP, the following settings properties SHOULD be supported by all
implementations.

###### headers

- Type: `Map`
- Description: A set of key/value pairs that is copied into the HTTP request
  as custom headers.
- Constraints:
  - OPTIONAL

###### method

- Type: `String`
- Description: The HTTP method to use for sending the message. This defaults
  to POST if not set.
- Constraints:
  - OPTIONAL

##### 3.2.2.2. MQTT

All implementations that support MQTT MUST support the _topicname_ settings.
All other settings SHOULD be supported.

- **topicname** (string) – REQUIRED. The name of the MQTT topic to publish to.

###### topicname

- Type: `String`
- Description: The name of the MQTT topic to publish to.
- Constraints:
  - REQUIRED

###### qos

- Type: `Integer`
- Description: MQTT quality of service (QoS) level: 0 (at most once), 1 (at
  least once), or 2 (exactly once). This defaults to 1 if not set.
- Constraints:
  - OPTIONAL

###### retain

- Type: `Boolean`
- Description: MQTT retain flag: true/false. This defaults to false if not set.
- Constraints:
  - OPTIONAL

###### expiry

- Type: `Integer`
- Description: MQTT expiry interval, in seconds. This value has no default
  value and the message will not expire if the setting is absent. This
  setting only applies to MQTT 5.0.
- Constraints:
  - OPTIONAL

###### userproperties

- Type: `Map`
- Description: A set of key/value pairs that are copied into the MQTT PUBLISH
  packet's user property section. This setting only applies to MQTT 5.0.
- Constraints:
  - OPTIONAL

##### 3.2.2.3. AMQP

For AMQP, the address property MUST be supported by all implementations and
other settings properties SHOULD be supported by all implementations.

###### address

- Type: `String`
- Description: The link target node in the AMQP container identified by the
  sink URI, if not expressed in the sink URI's path portion.
- Constraints:
  - OPTIONAL

###### linkname

- Type: `String`
- Description: Name to use for the AMQP link. If not set, a random link name
  is used.
- Constraints:
  - OPTIONAL

###### sendersettlementmode

- Type: `String`
- Description: Allows to control the sender's settlement mode, which
  determines whether transfers are performed "settled" (without
  acknowledgement) or "unsettled" (with acknowledgement). Default value is
  unsettled.
- Constraints:
  - OPTIONAL

###### linkproperties

- Type: `Map`
- Description: A set of key/value pairs that are copied into link properties
  for the send link.
- Constraints:
  - OPTIONAL

##### 3.2.2.4. Apache Kafka

All implementations that support Apache Kafka MUST support the _topicname_
settings. All other settings SHOULD be supported.

###### topicname

- Type: `String`
- Description: The name of the Kafka topic to publish to.
- Constraints:
  - OPTIONAL

###### partitionkeyextractor

- Type: `String`
- Description: A partition key extractor expression per the CloudEvents Kafka
  transport binding specification.
- Constraints:
  - OPTIONAL

###### clientid

- Type: `String`
- Description:
- Constraints:
  - OPTIONAL

###### acks

- Type: `String`
- Description:
- Constraints:
  - OPTIONAL

##### 3.2.2.5. NATS

###### subject

- Type: `String`
- Description: The name of the NATS subject to publish to.
- Constraints:
  - REQUIRED

#### 3.2.3 Sink Credentials

A sink credential provides authentication or authorization information necessary
to enable delivery of events to a target.

##### credentialType

- Type: `String`
- Description: Identifier of a credential type. The predefined types are "PLAIN",
  "ACCESSTOKEN", and "REFRESHTOKEN", with attributes enumerated below providing
  credential information. Applications MAY implement further credential types.

- Constraints:
  - REQUIRED
- Examples:
  - `PLAIN`

##### identifier

- Type: String
- Description: The identifier of a plain credential might be an account or
  username.

- Constraints:
  - REQUIRED for credentialType="PLAIN"

##### secret

- Type: String
- Description: The secret of a plain credential might be a password or
  passphrase or key.

- Constraints:
  - REQUIRED for credentialType="PLAIN"
  - SHOULD NOT be returned during enumeration or retrieval

##### accessToken

- Type: String
- Description: An access token is a previously acquired token granting access to
  the target resource.

- Constraints:
  - REQUIRED for credentialType="ACCESSTOKEN" and credentialType="REFRESHTOKEN"
  - SHOULD NOT be returned during enumeration or retrieval

##### accessTokenExpiresUtc

- Type: Timestamp
- Description: An absolute UTC instant at which the token SHALL be considered
  expired.

- Constraints:
  - REQUIRED for credentialType="ACCESSTOKEN" and credentialType="REFRESHTOKEN"

##### accessTokenType

- Type: String
- Description: Type of the access token (See [OAuth 2.0](https://tools.ietf.org/html/rfc6749#section-7.1)).

- Constraints:
  - REQUIRED for credentialType="ACCESSTOKEN" and credentialType="REFRESHTOKEN"

##### refreshToken

- Type: String
- Description: A refresh token credential used to acquire access tokens.

- Constraints:
  - REQUIRED for credentialType="REFRESHTOKEN"

##### refreshTokenEndpoint

- Type: String
- Description: A URL at which the refresh token can be traded for an access
  token.

  Not that in some setups, accessing the refresh token endpoint uses an extra
  security layer, whereby the requestor passing the refresh token to the
  endpoint MUST be authorized. The credentials for this authorization
  relationship, which exists between the delivery service managed by the
  subscription API and the refresh endpoint, are out of scope for this
  specification. The sinkCredentials represent the authorization relationship
  between the subscriber and the delivery target it points the subscription to.

#### 3.2.4 Filters

Filters allow for subscriptions to specify that only a subset of events are to
be delivered to the sink based on a set of criteria. The `filters` property in
a subscription is a set of filter expressions, where each expression evaluates
to either true or false for each event generated.

If any of the filter expressions in the set evaluate to false, the event MUST
NOT be sent to the sink. If all the filter expressions in the set evaluate to
true, the event MUST be attempted to be delivered.

Each filter expression includes the specification of a `dialect` that
defines the type of filter and the set of additional properties that are
allowed within the filter expression. If a filter dialect is specified in a
subscription that is unsupported by the subscription manager, creation or
update of the subscription MUST be rejected with an error.

##### 3.2.4.1 Filter Dialects

The filter expression language supported by an event producer is indicated by
its dialect. This is intended to allow for flexibility, extensibility and to
allow for a variety of filter dialects without enumerating them all in this
specification or predicting what filtering needs every system will have in the
future.

Filter dialects are identified by a unique `URI-Reference`.

When encoded in JSON, a filter is encoded as follows:

```
{ "dialect URI-Reference" : { <dialect-specific-properties> } }
```

###### 3.2.4.1.1 REQUIRED Filter Dialects

This specification defines the following 6 filter dialects that MUST be 
supported by every implementation:

**`exact`**

The keys are the names of the CloudEvents attributes to be matched,
and their values are the String values to use in the comparison.
To evaluate to true the values of the matching CloudEvents attributes MUST
all exactly match with the associated value String specified (case sensitive).

The attribute name and value specified in the filter expression MUST NOT be
empty strings.

For example:

```json
{ "exact": { "type": "com.github.push", "subject": "https://github.com/cloudevents/spec" } }
```

**`prefix`**

The keys are the names of the CloudEvents attributes to be matched,
and their values are the String values to use in the comparison.
To evaluate to true the values of the matching CloudEvents attributes MUST
all start with the associated value String specified (case sensitive).

The attribute name and value specified in the filter expression MUST NOT be
empty strings.

For example:

```json
{ "prefix": { "type": "com.github.", "subject": "https://github.com/cloudevents" } }
```

**`suffix`**

The keys are the names of the CloudEvents attributes to be matched,
and their values are the String values to use in the comparison.
To evaluate to true the values of the matching CloudEvents attributes MUST
all end with the associated value String specified (case sensitive).

The attribute name and value specified in the filter expression MUST NOT be
empty strings.

For example:

```json
{ "suffix": { "type": ".created", "subject": "/cloudevents/spec" } }
```

**`all`**

Use of this MUST include a nested array of filter expressions, where all
nested filter expressions MUST evaluate to true in order for the `all`
filter expression to be true.

Note: there MUST be at least one filter expression in the array.

For example:

```json
{
  "all": [
    { "exact": { "type": "com.github.push" } },
    { "exact": { "subject": "https://github.com/cloudevents/spec" } }
  ]
}
```

**`any`**

Use of this MUST include one nested array of filter expressions, where at 
least one nested filter expressions MUST evaluate to true in order for the `any`
filter expression to be true.

Note: there MUST be at least one filter expression in the array.

For example:

```json
{
  "any": [
    { "exact": { "type": "com.github.push" } },
    { "exact": { "subject": "https://github.com/cloudevents/spec" } }
  ]
}
```

**`not`**

Use of this MUST include one nested filter expression, where the result of 
this
filter expression is the inverse of the result of the nested expression.
In other words, if the nested expression evaluated to true, then the `not`
filter expression's result is false.

For example:

```json
{
  "not": { "exact": { "type": "com.github.push" } }
}
```

###### 3.2.4.1.2 OPTIONAL Filter Dialects

The support of the following dialects are OPTIONAL for implementations of
this specification: 

**`sql`**

Use of this MUST have a string value, representing a [CloudEvents SQL 
Expression](../cesql/spec.md).
The filter result MUST be true if the result value of the expression
equals to the `TRUE` boolean value, otherwise MUST be false if an
error occurred while evaluating the expression or if the result value
is equal to the `FALSE` boolean value, or if the result value is not a boolean.

Implementations SHOULD reject subscriptions with invalid CloudEvents SQL 
expressions.

For example:

```json
{ "sql": "source LIKE '%cloudevents%'" }
```

#### 3.2.5. API Operations

This section enumerates the abstract operations that are defined for
subscription managers. The following sections define bindings of these abstract
operations to concrete protocols.

The operations are `Create`, `Retrieve`, `Query`, `Update`, and `Delete`. Of
those, only the `Retrieve` operation is REQUIRED for conformance. The `Create`
and `Delete` operations SHOULD be implemented. `Query` and `Update` are
OPTIONAL.

Protocol bindings SHOULD provide a discovery mechanism for which operations are
supported.

#### 3.2.5.1. Creating a subscription

The **Create** operation SHOULD be supported by compliant Event Producers. It
creates a new Subscription. The client proposes a subscription object which MUST
contain all REQUIRED properties with the exception of the `ID` property, which
will be defined by the subscription manager. The subscription manager then
realizes the subscription and returns a subscription object that also contains
all OPTIONAL properties for which default values have been applied.

Parameters:

- subscription (subscription) - REQUIRED. Proposed subscription object.

Result:

- subscription (subscription) - REQUIRED. Realized subscription object.

Errors:

- **ok** - the operation succeeded
- **conflict** - a subscription with the given _id_ already exists
- **invalid** - the proposed subscription object contains invalid information

Protocol bindings MAY map the Create operation such that the proposed _id_ is
ignored and the subscription manager assigns one instead.

#### 3.2.5.2. Retrieving a Subscription

The **Retrieve** operation MUST be supported by compliant Event Producers. It
returns the specification of the identified subscription.

Parameters:

- id (string) - REQUIRED. Identifier of the subscription.

Result:

- subscription (subscription) - REQUIRED. Subscription object.

Errors:

- **ok** - the operation succeeded
- **notfound** - a subscription with the given _id_ already exists

#### 3.2.5.3. Querying for a list of Subscriptions

The **Query** operation SHOULD be supported by compliant Event Producers. It
allows to query the list of subscriptions on the subscription manager associated
with or otherwise visible to the party making the request. If supported, it MUST
be supported at the same endpoint as the **Create** subscription operation.

Parameters:

- none

Result:

- subscription (list of subscription) - REQUIRED. List of subscription objects

Errors:

- **ok** - the operation succeeded and returned results
- **nocontent** - the operation succeeded and returned no results

Protocol bindings and implementations of such bindings MAY add custom filter
constraints and pagination arguments as parameters. A request without filtering
constraints SHOULD return all available subscriptions associated with or
otherwise visible to the party making the request.

#### 3.2.5.4. Updating a Subscription

The Update operation MAY be supported by compliant Event Producers. To request
the update of a Subscription, the client submits a proposed subscription object
whose _id_ MUST match an existing subscription. All other properties MAY differ
from the original subscription. The subscription manager then updates the
subscription and returns a subscription object that also contains all OPTIONAL
properties for which default values have been applied.

Parameters:

- subscription (subscription) - REQUIRED. Proposed subscription object.

Result:

- subscription (subscription) - REQUIRED. Realized subscription object.

Protocol bindings MAY map the Update and the Create operation into a composite
"upsert" operation that creates a new subscription if one with the given _id_
does not exist. In this case, the operation is \*_Create_ and follows that
operation's rules.

#### 3.2.5.5. Deleting a Subscription

The **Delete** operation SHOULD be supported by compliant Event Producers. It
returns the specification of the identified subscription.

Parameters:

- id (string) - REQUIRED. Identifier of the subscription.

Result:

- subscription (subscription) - REQUIRED. Subscription object.

Errors:

- **ok** - the operation succeeded
- **notfound** - a subscription with the given _id_ already exists

### 3.3. HTTP Binding for the Subscription API

(TBD) This will be a straightforward mapping of the described API to a basic
HTTP CRUD API using PUT, POST, GET, DELETE, and OPTIONS.

Placeholders:

```
Create:
POST /subscriptions
Content-Type: application/json

{
  "config": { ... }
  "filter": { ... },
  "protocol": "...",
  "protocolsettings": { ... },
  "sink": "..."
}

Note: no ID in the request

Retrieve:
GET /subscriptions/{id}

Delete:
DELETE /subscriptions/{id}

Update:
PUT /subscriptions/{id}
Content-Type: application/json

{
  "id": "...",
  "config": { ... }
  "filter": { ... },
  "protocol": "...",
  "protocolsettings": { ... },
  "sink": "..."
}

```

### 3.4. AMQP Binding for the Subscription API

(TBD) This will be a set of bi-directional exchanges for the respective
operations.

## 4. Conformance

(TBD) Conformance clauses.
