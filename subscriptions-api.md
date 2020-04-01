# CNCF CloudEvents – Subscriptions API - Version 0.1-rc01s

## Abstract

This specification defines mechanisms, including an API definition, for CNCF
CloudEvents event consumers to subscribe to events originating from event
producers on behalf of event sources. The software entity handling these
subscriptions and responsible for distributing events is abstractly referred to
as a "subscription manager".

## Status of this document

This document is a working draft.

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
subscription offers are published in a CloudEvents Discovery service.

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
  channel (like an AMQP link or a MQTT connection) initiated by the consumer
  and connecting to the subscription manager. These kinds of subscriptions are
  typically offered by messaging or eventing middleware and their lifetime
  might be bounded by the lifetime of the communication channel.

- Subscriptions with subscription-manager-initiated delivery ("push"-style) are
  configured on the subscription manager for delivering events through a
  communication channel that the subscription manager initiates when events
  are available for delivery on the subscription. The configuration of such a
  subscription MUST contain all information required for the subscription
  manager to select a transport protocol, establish the desired communication
  channel, and deliver the event(s).

An end-to-end solution using CloudEvents might use only one of these styles or a
combination of those.

For instance, the solution might use an MQTT broker to handle delivery of
events into connected devices that connect into the broker and subscribe on a
particular MQTT topic, which acts as the subscription manager in the sense of
this specification ("pull"-style). The events that ought to be shared with the
connected devices might however originate elsewhere in the overall solution,
and some event router middleware's subscription manager might therefore be
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

The operations are normatively defined in the [MQTT
3.1.1](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html) and [MQTT
5.0](http://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html) specifications.

#### 3.1.2. AMQP 1.0

The AMQP 1.0 protocol has a built-in subscription mechanism.

When an AMQP container establishes a receive-role link to another container, it
can specify a "distribution-mode" on the link source in the other container. If
the distribution mode is "copy", each such established link receives a copy of
the message stream available at the distribution node. If the distribution mode
is "move", messages are exclusively owned by the link and are removed from the
source when the transfer is settled successfully.

Supporting the "copy" mode, is optional for the underlying implementation of the
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

The subscription object describes the consumer's interest in events and 
defines the delivery method. The protocol allows to configure subscriptions
on the subscription manager. Especially in case of subscription manager 
initiated ("push"-style) delivery, the protocol is required to express the 
consumer's interest to the subscription manager before the subscription 
manager can initiate delivery.

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

Each subscription is represented by an object that has the following properties:

- **id** (string) – REQUIRED. The unique identifier of the subscription in the
  scope of the subscription manager.
- **protocol** (string) - REQUIRED. Identifier of a delivery protocol. Because of
  WebSocket tunneling options for AMQP, MQTT and other protocols, the URI
  scheme is not sufficient to identify the protocol. The protocols with
  existing CloudEvents bindings are identified as "AMQP", "MQTT3", "MQTT5",
  "HTTP", "KAFKA", and "NATS". An implementation MAY add support for further
  protocols.
- **protocolsettings** (map) - OPTIONAL. A set of settings specific to the
  selected delivery protocol provider. Options for those settings are listed
  in the following subsection. An implementation MAY offer more options.
  Examples for such settings are credentials, which generally vary by
  transport, rate limits and retry policies, or the QoS mode for MQTT.
  See the [Protocol Settings](#322-protocol-settings) section for further details.
- **sink** (URI) - REQUIRED. The address to which events SHALL be delivered using
  the selected protocol. The format of the address MUST be valid for the
  selected protocol or one of the protocol's own transport bindings (e.g. AMQP
  over WebSockets).
- **filter** - OPTIONAL. A filter is an expression of a particular filter
  dialect that evaluates to true or false and that determines whether an
  instance of a CloudEvent will be delivered to the subscription's sink. If a
  filter expression evaluates to false, the event MUST NOT be sent to the sink.
  If the expression evaluates to true, the event MUST be attempted to be
  delivered. Support for particular filter dialects might vary across different
  subscription managers. If a filter dialect is specified in a subscription that
  is unsupported by the subscription manager, creation or updates of the
  subscription MUST be rejected with an error. See the [Filter
  Dialects](#323-filter-dialects) section for further details.

#### 3.2.2 Protocol Settings

This section enumerates protocol-specific delivery options for the
protocol-settings map, including default values where necessary.

##### 3.2.2.1. HTTP

For HTTP, the following settings properties SHOULD be supported by all
implementations.

- **headers** (map) – OPTIONAL. A set of key/value pairs that is copied into the
  HTTP request as custom headers.
- **method** (string) – OPTIONAL. The HTTP method to use for sending the message.
  This defaults to POST if not set.

##### 3.2.2.2. MQTT

All implementations that support MQTT MUST support the _topicname_ settings. All
other settings SHOULD be supported.

- **topicname** (string) – REQUIRED. The name of the MQTT topic to publish to.
- **qos** (integer) – OPTIONAL. MQTT quality of service (QoS) level: 0 (at most
  once), 1 (at least once), or 2 (exactly once). This defaults to 1 if not
  set.
- **retain** (boolean) – OPTIONAL. MQTT retain flag: true/false. This defaults to
  false if not set.
- **expiry** (integer) – OPTIONAL. MQTT expiry interval, in seconds. This value
  has no default value and the message will not expire if the setting is
  absent. This setting only applies to MQTT 5.0.
- **userproperties** (map) – OPTIONAL. A set of key/value pairs that are copied into
  the MQTT PUBLISH packet's user property section. This setting only applies
  to MQTT 5.0.

##### 3.2.2.3. AMQP

For AMQP, the address property MUST be supported by all implementations and
other settings properties SHOULD be supported by all implementations.

- **address** (string) – OPTIONAL. The link target node in the
  AMQP container identified by the sink URI, if not expressed in the sink URI's
  path portion.
- **linkname** (string) – OPTIONAL. Name to use for the AMQP link. If not set,
  a random link name is used.
- **sendersettlementmode** (string) – OPTIONAL. Allows to control the sender's
  settlement mode, which determines whether transfers are performed "settled"
  (without acknowledgement) or "unsettled" (with acknowledgement). Default
  value is unsettled.
- **linkproperties** (map) – OPTIONAL. A set of key/value pairs that are
  copied into link properties for the send link.

##### 3.2.2.4. Apache Kafka

All implementations that support Apache Kafka MUST support the _topicname_
settings. All other settings SHOULD be supported.

- **topicname** (string) - REQUIRED. The name of the Kafka topic to publish to.
- **partitionkeyextractor** (string) - OPTIONAL. A partition key extractor
  expression per the CloudEvents Kafka transport binding specification.
- **clientid** (string)
- **acks** (string)

##### 3.2.2.5. NATS

- **subject** (string) - REQUIRED. The name of the NATS subject to publish to.

#### 3.2.3 Filter Dialects

The filter expression language supported by an event producer is indicated by
its dialect. This is intended to allow for flexibility, extensibility and to
allow for a variety of filter dialects without enumerating them all in this
specification or predicting what filtering needs every system will have in the
future. This specification will specify a single "basic" dialect, which all
implementations MUST support.

The dialect for a particular filter is indicated by specifying the "dialect"
property at the root of the JSON object. The value of this is a string encoded
unique identifier for the filter dialect. Subscriptions specifying the "filter"
property MUST specify a dialect. All other properties are dependent on the
dialect being used.

##### 3.2.3.1. "basic" filter dialect

The "basic" filter dialect is intended to support the most common filtering use
cases:

- "Exact" match where the filter condition and an attribute value match exactly.
- "Prefix" match where the filter condition is a prefix of the attribute value.
- "Suffix" match where the filter condition is a suffix of the attribute value.

This filter dialect is intentionally constrained to these filter types, since
filtering has a potentially significant impact on the baseline performance of
all implementations. In cases where more filter types or different expression
languages are desired, further dialects can be introduced as extensions.

Extension dialects will have varying support across event producers. It is up to
the subscriber and producer to negotiate which filter dialects can be used
within a given subscription.

The filter conditions specified in the basic dialect will be defined by
specifying a "conditions" property holding an array of filter conditions,
which are logically combined with an implicit "AND" operator. This means the
filter criteria MUST evaluate to true for every filter in the array in order for
a CloudEvent instance to be delivered to the target sink.

Each basic filter is defined with the following properties:

- type (string) - REQUIRED. Value MUST be one of the following: prefix, suffix,
  exact.
- property (string) - REQUIRED. The CloudEvents attribute (including extensions)
  to match the value indicated by the "value" property against.
- value (string) - REQUIRED, The value to match the CloudEvents attribute
  against. This expression is a string and matches are executed against the
  string representation of the attribute value.

###### 3.2.3.1.1. Example: Prefix match

This filter will select events only with the event type having the prefix of
"com.example".

```JSON
{
    "dialect": "basic",
    "filters": [{
        "type": "prefix",
        "property": "type",
        "value": "com.example"
    }]
}
```

###### 3.2.3.1.2. Example: Suffix match

This filter will select events only with the event subject having the suffix of
".jpg".

```JSON
{
    "dialect": "basic",
    "filters": [
        {
            "type": "suffix",
            "property": "subject",
            "value": ".jpg"
        }
    ]
}
```

###### 3.2.3.1.3. Example: Exact match

This filter will select events only with the event type equal to
"com.example.my_event".

```JSON
{
    "dialect": "basic",
    "filters": [
        {
            "type": "exact",
            "property": "type",
            "value": "com.example.my_event"
        }
   ]
}
```

###### 3.2.3.1.4. Example: Exact match and suffix match

This filter will select events only with the event type equal to
"com.example.my_event" AND the event subject having the suffix of ".jpg".

```JSON
{
    "dialect": "basic",
    "filters": [
        {
            "type": "exact",
            "property": "type",
            "value": "com.example.my_event"
        },
        {
            "type": "suffix",
            "property": "subject",
            "value": ".jpg"
        },
    ]
}
```

#### 3.2.4. API Operations

This section enumerates the abstract operations that are defined for
subscription managers. The following sections define bindings of these abstract
operations to concrete protocols.

The operations are `Create`, `Retrieve`, `Query`, `Update`, and `Delete`. Of
those, only the `Retrieve` operation is REQUIRED for conformance. The `Create`
and `Delete` operations SHOULD be implemented. `Query` and `Update` are
OPTIONAL.

Protocol bindings SHOULD provide a discovery mechanism for which operations are
supported.

#### 3.2.4.1. Creating a subscription

The **Create** operation SHOULD be supported by compliant Event Producers. It
creates a new Subscription. The client proposes a subscription object which MUST
contain all REQUIRED properties. The subscription manager then realizes the
subscription and returns a subscription object that also contains all OPTIONAL
properties for which default values have been applied.

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

#### 3.2.4.2. Retrieving a Subscription

The **Retrieve** operation MUST be supported by compliant Event Producers. It
returns the specification of the identified subscription.

Parameters:

- id (string) - REQUIRED. Identifier of the subscription.

Result:

- subscription (subscription) - REQUIRED. Subscription object.

Errors:

- **ok** - the operation succeeded
- **notfound** - a subscription with the given _id_ already exists

#### 3.2.4.3. Querying for a list of Subscriptions

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

#### 3.2.4.4. Updating a Subscription

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

#### 3.2.8. Deleting a Subscription

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

### 3.4. AMQP Binding for the Subscription API

(TBD) This will be a set of bi-directional exchanges for the
respective operations.

## 4. Conformance

(TBD) Conformance clauses.
