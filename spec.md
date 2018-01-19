# CloudEvents - Verson 0.1

CloudEvents is a vendor-neutral specification for event data.

## Table of Contents
- [Overview](#overview)
- [Status](#status)
- [Notations and Terminology](#notations-and-terminology)
- [Context Attributes](#context-attributes)
- [Context Attributes Backlog](#context-attributes-backlog)
- [Use Cases](#use-cases)
- [Additional Topics & Questions](#additional-topics--questions)
- [Reference](#reference)

## Overview
Events are everywhere.  However, event publishers tend to describe events
differently.

The lack of a common way of describing events means developers must constantly
re-learn how to receive events.  This also limits the potential for libraries,
tooling and infrastructure to aide the delivery of event data across
environments, like SDKs, event routers or tracing systems.  The portability
and productivity we can achieve from event data is hindered overall.

Enter CloudEvents, a specification for describing event data in a common way.
CloudEvents seeks to ease event declaration and delivery across services,
platforms and beyond.

CloudEvents is a new effort and it's still under active development.  However,
its working group has received a surprising amount of industry interest,
ranging from major cloud providers to popular SaaS companies.  Our end goal is
to offer this specification to the Cloud Native Computing Foundation.

## Status
A coalition of industry stakeholders have expressed interest in collaborating
on this specification (though this does not constitute an endorsement on their
behalf) and have begun iterating on early drafts.

Version 0.4 of CloudEvents represents the end result of a working session
between engineers at Amazon, Google, and Microsoft.  Many items are left to be
discussed, but this specification does represent the beginning of a level of
consensus between these major industry stakeholders, which is exciting.  Now,
we are opening up this specification for public feedback and conducting all
working sessions through the Serverless Working Group within the CNCF.
Overall, in this early stage, almost all stakeholders have requested the
initial scope of the specification be kept small to ease adoption and
implementation.  At this time we are focused on the following scope:

* Agree upon a set of event metadata attributes (“context”) that:
  * Offer a basic description of the event and the data it carries.
  * Are currently implemented and semantically similar across multiple
    platforms.
  * Can be delivered separately from the event data in the transport headers
    (e.g. HTTP, AMQP, Kafka) or together with the data in a serialized fashion
    (e.g. JSON, protobuf, Avro).
  * Include a description of the transport/protocol and encoding, with an
    initial focus on HTTP.
  * Can be extended to support experimental or uncommon features, while being
    clearly indicated as an extension (e.g. extensions use a common prefix).
  * Allow for evolution of both the payload and CloudEvents definition (e.g.
    versioning).
  * Can be embedded at different stages along the route of the event by
    middleware (e.g. a router may add transport or auth information).
* Establish a backlog of prospective event metadata attributes (“context”)
  for potential inclusion in the future.
* Include use-case examples to help users understand the value of CloudEvents,
  with an initial focus on HTTP and Functions-as-a-Service/Serverless computing.
* Determine process and overall governance of the specification.
* Discuss additional architecture components that complement this specification.

Have questions or want to contribute? Please join the Serverless Working
Group within the CNCF.

## Notations and Terminology

### Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to
be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

### Terminology

This specification defines the following terms:

#### Occurrence
When something happens (or doesn’t happen) and is detected by a software
system.  This is most typically when that system receives an external signal
(e.g HTTP or RPC), though could also be through observing a changing value
 (e.g. an IoT sensor or period of inactivity).

#### Event
Data representing an occurrence, a change in state, that something happened
(or did not happen), usually used for notification.  Events include context
and data.  Each occurrence may be uniquely identified with data in the event.
Events should be considered as facts that have no given destination, whereas
messages contain intent and tend to transport data from a source to a given
destination.

#### Context
A set of consistent metadata attributes included with the event about the
occurrence that tools and developers can rely upon to better handle the event.
These attributes describe the event and the structure of its data, include
information about the originating system, and more.

#### Data
Domain-specific information about the occurrence (i.e. the payload).  This may
include minimal information about the occurrence, details about the data that
was changed, or more.

#### Protocol
Events can be delivered through various industry standard protocol (e.g. HTTP,
AMQP, MQTT, SMTP), open-source protocols (e.g. Kafka, NATS), or
platform/vendor specific protocols (AWS Kinesis, Azure Event Grid).

## Context Attributes
Every event in the CloudEvents specification includes context which is a set
of consistent metadata attributes tools and developers can rely upon to
understand how to handle the event and its data.

Context is designed such that it can be delivered separately from the event data 
(e.g. in protocol headers or protocol specific attributes).  This allows the context
to be inspected at the destination without having to deserialize the event data.  
The context MAY also need to be serialized with the event data for some use cases
(e.g. a JSON implementation might use one JSON object that contains both context 
and data).


### namespace
* Type: String
* Description: Identifier that uniquely identifies the organization publishing
  the event.
* Examples:
  * kafka.apache.org
  * com.microsoft.azure

### event-type
* Type: String
* Description: Type of the event.  Producers can specify the format of this,
  depending on their service.  This enables the interpretation of data, and
  can be used for routing, policy and more.
* Examples:
  * customer.created
* Constraints:
  * Required
* Notes:
  * It is up for discussion whether namespace could be included as a prefix in
    event-type.
  * It is up for discussion whether the event-type should also include a
    version.  It’s currently included in a separate attribute titled
    event-type-version.
  * It is up for discussion whether this specification should enforce a type
    format.

### event-type-version
* Type: String
* Description: The version of the event-type.  This enables the interpretation
  of data by eventual consumers, requires the consumer to be knowledgeable about
  the producer.
* Notes:
  * It is up for discussion whether this is applicable to the whole event or
    to the data payload alone.  Currently, event-type-version covers the data,
    while open-events-version covers the context.

### open-events-version
* Type: String
* Description: The version of the CloudEvents specification which the event
  uses.  This enables the interpretation of the context.

### resource
* Type: Object
* Description: This describes the software instance that emits the event at
  runtime (i.e. the producer).  It contains sub-properties (listed below)


### resource-type
* Type: String
* Description: Type of the event source. Providers define list of event sources.
* Constraints:
  * Required
* Examples:
  * s3

### resource-id
* Type: String
* Description: ID of the event source.
* Constraints:
  * Required
*Examples:
  *my.s3.bucket

### event-id
* Type: String
* Description: ID of the event.  Can be specified by the producer.  The
  semantics of this string are explicitly undefined to ease the implementation
  of producers.  Enables deduplication.
* Examples:
  * A database commit ID
* Constraints:
  * Required
  * Unique per producer

### event-time
* Type: RFC 3339, timezone Z
* Description: Timestamp of when the event happened.

### schema-url
* Type: String
* Description: A link to the schema which can be optionally specified by the
  producer.
* Notes:
  * It is up for discussion whether this is applicable to the whole event or
    to the data alone.

### extensions
* Type: Map <String, Object>
* Description: This is for additional metadata and this does not have a
  required structure.  This enables a place for custom fields a producer or
  middleware may want to include and provides a place to test metadata before
  adding them to the CloudEvents specification.  TBD - Determine a shorter
  prefix for this (e.g. OpenAPI uses “x-”)
* Examples:
  * authorization data
  * content type

### data
* Type: Arbitrary payload
* Description: The event payload.  The payload depends on the event-type,
  schema-url and event-type-version.
* Notes:
  * TBD where the producer specifies format/encoding of the data elsewhere in
    this schema.

## Context Attributes Backlog

### path
* Type: String
* Description: The destination endpoint address (e.g. URL) or target topic

### content-type
* Type: String
* Description:  The data encoding scheme (e.g. application/json).  The data
  content type.
* Constraints:
  * Required if the event contains a body.

### correlation-id
* Type: String
* Description: Correlation ID of event that triggered this event to be
  created (if any). If not triggered in response to an event, a unique ID.
  Can be specified by the producer if event not produced in response to an
  event. Enables traceability through systems.
* Examples:
  * Event A generated with unique correlation-id. Event handler receives event
    and generates a new event in response, Event B. Event B copies the
    correlation-id of Event A so that the chain of events can be properly
    correlated.
* Constraints:
  * Optional

### causation-id
* Type: String
* Description: event-id of event that triggered this event to be created (if
  any). If not triggered in response to an event, then not present. Enables
  traceability through systems.
* Examples:
  * Event A generated with unique event-id. Event handler receives event and
    generates a new event in response, Event B. Event B copies the event-id of
    Event A into its own causation-id so that the chain of events can be
    properly correlated.
* Constraints:
  * Optional

### method
* Type: String
* Description:  The (http) method used in the call

### log-level
* Type: String
* Description:  The level of logging that the publisher may want to log this
  specific event (e.g. debug)

### receipt-queue
* Type: String
* Description:  An optional return endpoint for completion events

### authentication
* Type:
* Description:

## Use Cases
[WIP]  Use-case examples to help end users understand the value of CloudEvents.

### Inter-Service Communication

### Inter-Platform Communication

### Development & Testing of Event-Driven Architectures

### Event Data Evolution

### Policy Enforcement

### Data Access Control

### Event Delivery Tracing

### Cloudbursting

### IoT

## Additional Topics & Questions

* Context Attribute Names - We decided not to spend too much time on property
  names during our working sessions.  Instead the focus has been on semantics.
  We still need to revise property names.
* Event Consumer API - What does this look like?
* Routing, Batching, Failure Semantics - What do these look like?
* Authentication - Should this be included within the event?
  * Initial authN (e.g. auth at the point of event occurrence)
  * Transport level authN (e.g. auth on the event)
* What is the best way to handle encoding for event payloads?
* How to specify an action that is desired to happen based on an event
  notification (also does this violate our interpretation of events)?
* Micro batch considerations – For various streaming and asynchronous
  implementations the client may push one event at a time, but the function
  may want to process multiple events per invocation and obtain higher
  efficiency. There needs to be a mechanism to trigger a function with an
  array of events.  An example implementation can be to indicate in the event
  type that it's a list type and pass a “records” list object where each
  record holds its own headers, body or attributes.
* Event Routing – Once the event structure, protocol, and API are well defined
  it becomes trivial to route from one type to another, or even route internal
  events to external clouds.  It can be accomplished by simply writing a
  serverless function which listens on the source event, opens a connection to
  the destination protocol and maps every incoming event (received through
  event API) to an event message over the destination protocol.

## Reference

Examples of current event formats that exist today.

### Microsoft - Event Grid
```
{
    "topic":"/subscriptions/{subscription-id}",        "subject":"/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.EventGrid/eventSubscriptions/LogicAppdd584bdf-8347-49c9-b9a9-d1f980783501",
    "eventType":"Microsoft.Resources.ResourceWriteSuccess",
    "eventTime":"2017-08-16T03:54:38.2696833Z",
    "id":"25b3b0d0-d79b-44d5-9963-440d4e6a9bba",
    "data": {
        "authorization":"{azure_resource_manager_authorizations}",
        "claims":"{azure_resource_manager_claims}",
        "correlationId":"54ef1e39-6a82-44b3-abc1-bdeb6ce4d3c6",
        "httpRequest":"",
        "resourceProvider":"Microsoft.EventGrid",
        "resourceUri":"/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.EventGrid/eventSubscriptions/LogicAppdd584bdf-8347-49c9-b9a9-d1f980783501",
        "operationName":"Microsoft.EventGrid/eventSubscriptions/write",
        "status":"Succeeded",
        "subscriptionId":"{subscription-id}",
        "tenantId":"72f988bf-86f1-41af-91ab-2d7cd011db47"
    }
}
```
[Documentation](https://docs.microsoft.com/en-us/azure/event-grid/event-schema)

### Google - Cloud Functions (potential future)
```
{
  "data": {
    "@type": "types.googleapis.com/google.pubsub.v1.PubsubMessage",
    "attributes": {
      "foo": "bar",
     },
     "messageId": "12345",
     "publishTime": "2017-06-05T12:00:00.000Z",
     "data": "somebase64encodedmessage"
  },
  "context": {
    "eventId": "12345",
    "timestamp": "2017-06-05T12:00:00.000Z",
    "eventTypeId": "google.pubsub.topic.publish",
    "resource": {
      "name": "projects/myProject/topics/myTopic",
      "service": "pubsub.googleapis.com"
    }
  }
}
```

### AWS - SNS
```
{
  "Records": [
    {
      "EventVersion": "1.0",
      "EventSubscriptionArn": eventsubscriptionarn,
      "EventSource": "aws:sns",
      "Sns": {
        "SignatureVersion": "1",
        "Timestamp": "1970-01-01T00:00:00.000Z",
        "Signature": "EXAMPLE",
        "SigningCertUrl": "EXAMPLE",
        "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
        "Message": "Hello from SNS!",
        "MessageAttributes": {
          "Test": {
            "Type": "String",
            "Value": "TestString"
          },
          "TestBinary": {
            "Type": "Binary",
            "Value": "TestBinary"
          }
        },
        "Type": "Notification",
        "UnsubscribeUrl": "EXAMPLE",
        "TopicArn": topicarn,
        "Subject": "TestInvoke"
      }
    }
  ]
}
```
[Documentation](http://docs.aws.amazon.com/lambda/latest/dg/eventsources.html)

### AWS - Kinesis
```
{
  "Records": [
    {
      "eventID": "shardId-000000000000:49545115243490985018280067714973144582180062593244200961",
      "eventVersion": "1.0",
      "kinesis": {
        "partitionKey": "partitionKey-3",
        "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4=",
        "kinesisSchemaVersion": "1.0",
        "sequenceNumber": "49545115243490985018280067714973144582180062593244200961"
      },
      "invokeIdentityArn": identityarn,
      "eventName": "aws:kinesis:record",
      "eventSourceARN": eventsourcearn,
      "eventSource": "aws:kinesis",
      "awsRegion": "us-east-1"
    }
  ]
}
```

### IBM - OpenWhisk - Web Action Event
```
{
  "__ow_method": "post",
  "__ow_headers": {
    "accept": "*/*",
    "connection": "close",
    "content-length": "4",
    "content-type": "text/plain",
    "host": "172.17.0.1",
    "user-agent": "curl/7.43.0"
  },
  "__ow_path": "",
  "__ow_body": "Jane"
}
```
