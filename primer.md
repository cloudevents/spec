# CloudEvents Primer

## Abstract

This non-normative document provides an overview of the CloudEvents
specification. It is meant to compliment the CloudEvent specification
to provide additional background and insight into the history and
design decisions made during the development of the specification. This
allows the specification itself to focus on the normative technical
details.

## Status of this document

This document is a working draft.

## Table of Contents

- [History](#history)
- [CloudEvents Concepts](#cloudevents-concepts)
- [Design Goals](#design-goals)
- [CloudEvent Attributes Extensions](#cloudevent-attribute-extensions)
- [Qualifying Protocols and Encodings](#qualifying-protocols-and-encodings)
- [Prior Art](#prior-art)
- [Roles](#roles)
- [Value Proposition](#value-proposition)
- [Existing Event Formats](#existing-event-formats)

## History

The [CNCF Serverless Working group](https://github.com/cncf/wg-serverless)
was originally created by the CNCF's
[Technical Oversight Committee](https://github.com/cncf/toc) to investigate
Serverless Technology and to recommend some possible next steps for some
CNCF related activities in this space. One of the recommendations was to
investigate the creation of a common event format to aid in the
portability of functions between Cloud providers and the interoperability of
processing of event streams. As a result, the CloudEvents specification
was created.

While initially the work on CloudEvents was done as part of the Serverless
Working group, once the specification reached its v0.1 milestone, the TOC
approved the CloudEvents work as a new stand-alone CNCF sandbox project.

## CloudEvents Concepts

An [event](spec.md#event) includes context and data about an
[occurrence](spec.md#occurrence). Each *occurrence* is uniquely
identified by the data of the *event*.

*Events* represent facts and therefore do not include a destination, whereas
messages convey intent, transporting data from a source to a given destination.

### Eventing

Events are commonly used in server-side code to connect disparate systems where
the change of state in one system causes code to execute in another. For
example, a source may generate an event when it receives an external signal
(e.g. HTTP or RPC) or observes a changing value (e.g. an IoT sensor or period of
inactivity).

To illustrate how a system uses CloudEvents, the simplified diagram below shows
how an event from a [source](spec.md#source) triggers an action.

![alt text](source-event-action.png "A box representing the source with
arrow pointing to a box representing the action. The arrow is annotated with
'e' for event and 'protocol'.")

The source generates a message where the event is encapsulated in a protocol.
The event arrives to a destination, triggering an action which is provided with
the event data.

A *source* is a specific instance of a source-type which
allows for staging and test instances. Open source software of a specific
*source-type* may be deployed by multiple companies or providers.

Events can be delivered through various industry standard protocols (e.g. HTTP,
AMQP, MQTT, SMTP), open-source protocols (e.g. Kafka, NATS), or platform/vendor
specific protocols (AWS Kinesis, Azure Event Grid).

An action processes an event defining a behavior or effect which was
triggered by a specific *occurrence* from a specific *source*. While outside
of the scope of the specification, the purpose of generating an *event* is
typcially to allow other systems to easily react to changes in a source that
they do not control. The *source* and action are typically built by different
developers. Often the *source* is a managed service and the *action* is custom
code in a serverless Function (such as AWS Lambda or Google Cloud Functions).

## Design Goals

CloudEvents are typically used in a distributed system to allow for services to
be loosely coupled during development, deployed independently, and later
can be connected to create new applications.

The goal of the CloudEvents specification is to define interoperability of event
systems that allow services to produce or consume events, where the producer and
consumer can be developed and deployed independently. A producer can generate
events before a consumer is listening, and a consumer can express an interest in
an event or class of events that is not yet being produced. Note that the
specifications produced by this effort are focused on interoperability of the
event format and how it appears while being sent on various transports,
such as HTTP. The specifications will not focus on the processing model of
either the event producer or event consumer.

CloudEvents, at its core, defines a set of metadata, called attributes, about
the event being transferred between systems, and how those pieces of metadata
should appear in that message. This metadata is meant to be the minimal 
set of information needed to route the request to the proper component that
will process the event. So, while this might mean that some of the application
data of the event itself might be duplicated as part of the CloudEvent's set
of properties, this is to be done solely for the purpose of proper delivery
of the message.  Data that is meant strictly for use by the component
processing the event should be within the event.

Along with the definition of these attributes, there will also be
specifications of how to serialize the event in different formats and
transports (e.g. JSON and HTTP).

### Non-Goals
The following will not be part of the specification:
* Function build and invocation process
* Language-specific runtime APIs
* Selecting a single identity/access control system

## CloudEvent Attribute Extensions

In order to achieve the stated goals, the working group will attempt to
constrain the number of metadata attributes they define in CloudEvents. To
that end, attributes defined by this working group will fall into three
 categories:
- required
- optional
- extensions

As the category names imply, "required" attributes will be the ones that
the working group considers vital to all events in all use cases, while
"optional" ones will be used in a majority of the cases. Both of the attributes
in these cases will be defined within the specfication itself.

When the working group determines that an attribute is not common enough to
fall into those two categories but would still benefit from the level of
interoperability that comes from being well-defined, then they will be placed
into the "extensions" category and put into 
(documented extensions)[documented-extensions.md].
The specification defines how these extension attributes will
appear within a CloudEvent.

In determining which category a proposed attribute belongs, or even if it
will be included at all, the working group uses use-cases and
user-stories to explain the rationale and need for them. This supporting
information will be added to the [Prior Art](#prior-art) section of this
document.

Extension attributes to the CloudEvent specification are meant to
be additional metadata that needs to be included to help ensure proper
routing and processing of the CloudEvent. Additional metadata for other
purposes, that is related to the event itself and not needed in the
transportation of the CloudEvent, should instead be placed within the proper
extensibility points of the event itself.

## Qualifying Protocols and Encodings

The explicit goal of the CloudEvents effort, as expressed in the specification,
is "describing event data in a common way" and "to define interoperability of
event systems that allow services to produce or consume events, where the
producer and consumer can be developed and deployed independently".

The foundation for such interoperability are open data formats and open
protocols, with CloudEvents aiming to provide such an open data format and
projections of its data format onto commonly used protocols and with commonly
used encodings.

While each software or service product and project can obviously make its own 
choices about which form of communication it prefers, its unquestionable that 
a proprietary protocol that is private to such a product or project does not 
further the goal of broad interoperability across producers and consumers of 
events.

Especially in the area of messaging and eventing, the industry has made
significant progress in the last decade in developing a robust and broadly
supported protocol foundation, like HTTP 1.1 and HTTP/2 as well as WebSockets
or events on the web, or MQTT and AMQP for connection-oriented messaging and
telemetry transfers.

Some widely used protocols have become de-facto standards emerging out of strong
ecosystems of top-level multi-company consortia projects, such as Apache Kafka, 
and largely in parallel to the evolution of the aforementioned standards stacks.

The CloudEvents effort shall not become a vehicle to even implicitly endorse 
or promote project- or product-proprietary protocols, because that would be 
counterproductive towards CloudEvents' original goals. 

For a protocol or encoding to qualify for a core CloudEvents event format or 
protocol binding, it must belong to either one of the following categories:

- The protocol has a formal status as a standard with a widely-recognized 
  multi-vendor protocol standardization body (e.g. W3C, IETF, OASIS, ISO)
- The protocol has a "de-facto standard" status for its ecosystem category,
  which means it is used so widely that it is considered a standard for a
  given application. Practically, we would like to see at least one open
  source implementation under the umbrella of a vendor-neutral open-source
  organization (e.g. Apache, Eclipse, CNCF, .NET Foundation) and at least
  a dozen independent vendors using it in their products/services.

Aside from formal status, a key criterion for whether a protocol or encoding
shall qualify for a core CloudEvents event format or transport binding is
whether the working group agrees that the specification will be of sustained
practical benefit for any party that is unrelated to the product or project
from which the protocol or encoding emerged. A base requirement for this is
that the protocol or encoding is defined in a fashion that allows alternate
implementations independent of the product or project's code.

All other protocol and encoding formats for CloudEvents are welcome to be
included in a list pointing to the CloudEvents binding information in the
respective project's own public repository or site.

## Prior Art

This section describes some of the input material used by the working group
during the development of the CloudEvent specification.

### Roles

The list below enumerates the various participants, and scenarios, that might
be involved in the producing, managing or consuming of events.

In these the roles of event producer and event consumer are kept
distinct. A single application context can always take on multiple roles
concurrently, including being both a producer and a consumer of events.

1) Applications produce events for consumption by other parties, for instance
   for providing consumers with insights about end-user activities, state
   changes or environment observations, or for allowing complementing the
   application's capabilities with event-driven extensions.

   Events are typically produced related to a context or a producer-chosen
   classification. For example, a temperature sensor in a room might be
   context-qualified by mount position, room, floor, and building. A sports
   result might be classified by league and team.

   The producer application could run anywhere, such as on a server or a device.

   The produced events might be rendered and emitted directly by the producer
   or by an intermediary; as example for the latter, consider event data
   transmitted by a device over payload-size-constrained networks such as
   LoRaWAN or ModBus, and where events compliant to this
   specification will be rendered by a network gateway on behalf of the
   producer.

   For example, a weather station transmits a 12-byte, proprietary event
   payload indicating weather conditions once every 5 minutes over LoRaWAN. A
   LoRaWAN gateway is then used to publish the event to an Internet destination
   in the CloudEvents format. The LoRaWAN gateway is the event producer,
   publishing on behalf of the weather station, and will set event metadata
   appropriately to reflect the source of the event.

2) Applications consume events for the purposes such as display, archival,
   analytics, workflow processing, monitoring the condition and/or providing
   transparency into the operation of a business solution and its foundational
   building blocks.

   The consumer application could run anywhere, such as on a server or a
   device.

   A consuming application will typically be interested in:
   - distinguishing events such that the exact same event is not
     processed twice.
   - identifying and selecting the origin context or the
     producer-assigned classification.
   - identifying the temporal order of the events relative to the
     originating context and/or relative to a wall-clock.
   - understanding the context-related detail information carried
     in the event.
   - correlating event instances from multiple event producers and send
     them to the same consumer context.

   In some cases, the consuming application might be interested in:
   - obtaining further details about the event's subject from the
     originating context, like obtaining detail information about a
     changed object that requires privileged access authorization.
     For example, a HR solution might only publish very limited
     information in events for privacy reasons, and any event consumer
     needing more data will have to obtain details related to the event
     from the HR system under their own authorization context.
   - interact with the event's subject at the originating context,
     for instance reading a storage blob after having been informed
     that this blob has just been created.

   Consumer interests motivate requirements for which information
   producers ought to include an event.

3) Middleware routes events from producers to consumers, or onwards
   to other middleware. Applications producing events might delegate
   certain tasks arising from their consumers' requirements to
   middleware:

   - Management of many concurrent interested consumers for one of
     multiple classes or originating contexts of events
   - Processing of filter conditions over a class or originating context
     of events on behalf of consumers.
   - Transcoding, like encoding in MsgPack after decoding from JSON
   - Transformation that changes the event's structure, like mapping from
     a proprietary format to CloudEvents, while preserving the
     identity and semantic integrity of the event.
   - Instant "push-style" delivery to interested consumers.
   - Storing events for eventual delivery, either for pick-up initiated
     by the consumer ("pull"), or initiated by the middleware ("push")
     after a delay.
   - Observing event content or event flow for monitoring or
     diagnostics purposes.

   To satisfy these needs, middleware will be interested in:
   - A metadata discriminator usable for classification or
     contextualization of events so that consumers can express interest
     in one or multiple such classes or contexts.
     For instance, a consumer might be interested in all events related
     to a specific directory inside a file storage account.
   - A metadata discriminator that allows distinguishing the subject of
     a particular event of that class or context.
     For instance, a consumer might want to filter out all events related
     to new files ending with ".jpg" (the file name being the "new file"
     event's subject) for the context describing specific directory
     inside a file storage account that it has registered interest on.
   - An indicator for the encoding of the event and its data.
   - An indicator for the structural layout (schema) for the event and
     its data.

   Whether its events are available for consumption via a middleware is
   a delegation choice of the producer.

   In practice, middleware can take on role of a producer when it changes
   the semantic meaning of an event, a consumer when it takes action based
   on an event, or middleware when it routes events without making semantic
   changes.

4) Frameworks and other abstractions make interactions with event platform
   infrastructure simpler, and often provide common API surface areas
   for multiple event platform infrastructures.

   Frameworks are often used for turning events into an object graph,
   and to dispatch the event to some specific handling user-code or
   user-rule that permits the consuming application to react to
   a particular kind of occurrence in the originating context and
   on a particular subject.

   Frameworks are most interested in semantic metadata commonality
   across the platforms they abstract, so that similar activities can
   be handled uniformly.

   For a sports application, a developer using the framework might be
   interested in all events from today's game (subject) of a team in a
   league (topic of interest), but wanting to handle reports
   of "goal" differently than reports of "substitution".
   For this, the framework will need a suitable metadata discriminator
   that frees it from having to understand the event details.

### Value Proposition

This section describes some of the use-cases that explain the value
of CloudEvents.

#### Normalizing Events Across Services & Platforms

Major event publishers (e.g. AWS, Microsoft, Google, etc.) all publish events
in different formats on their respective platforms. There are even a few cases
where services on the same provider publish events in different formats (e.g.
AWS). This forces event consumers to implement custom logic to read or munge
event data across platforms and occasionally across services on a single
platform.

CloudEvents can offer a single experience for authoring consumers that handle
events across all platforms and services.

#### Facilitating Integrations Across Services & Platforms

Event data being transported across environments is increasingly common.
However, without a common way of describing events, delivery of events across
environments is hindered. There is no single way of determining where an event
came from and where it might be going. This prevents tooling to facilitate
successful event delivery and consumers from knowing what to do with event
data.

CloudEvents offers useful metadata which middleware and consumers can rely upon
to facilitate event routing, logging, delivery and receipt.

#### Increasing Portability of Functions-as-a-Service

Functions-as-a-Service (also known as serverless computing) is one of the
fastest growing trends in IT and it is largely event-driven. However, a
primary concern of FaaS is vendor lock-in. This lock-in is partially caused
by differences in function APIs and signatures across providers, but the
lock-in is also caused by differences in the format of event data received
within functions.

CloudEvents' common way of describing event data increases the portability of
Functions-as-a-Service.

#### Improving Development & Testing of Event-Driven/Serverless Architectures

The lack of a common event format complicates development and testing of
event-driven and serverless architectures. There is no easy way to mock events
accurately for development and testing purposes, and help emulate event-driven
workflows in a development environment.

CloudEvents can enable better developer tools for building, testing and
handling the end-to-end lifecycle of event-driven and serverless architectures.

#### Event Data Evolution

Most platforms and services version the data model of their events differently
(if they do this at all). This creates an inconsistent experience for
publishing and consuming the data model of events as those data models evolve.

CloudEvents can offer a common way to version and evolve event data. This will
help event publishers safely version their data models based on best practices,
and this help event consumers safely work with event data as it evolves.

#### Normalizing Webhooks

Webhooks is a style of event publishing which does not use a common format.
Consumers of webhooks don’t have a consistent way to develop, test, identify,
validate, and overall process event data delivered via webhooks.

CloudEvents can offer consistency in webhook publishing and consumption.

#### Policy Enforcement

The transiting of events between systems may need to be filtered, transformed,
or blocked due to security and policy concerns. Examples may be to prevent
ingress or egress of the events such as event data containing sensitive
information or wanting to disallow the information flow between the sender and
receiver.

A common event format would allow easier reasoning about the data being
transited and allow for better introspection of the data.

#### Event Tracing

An event sent from a source may result in a sequence of additional events
sent from various middleware devices such as event brokers and gateways.
CloudEvents includes metadata in events to associate these events as being
part of an event sequence for the purpose of event tracing and
troubleshooting.

An event sent from a source may result in a sequence of additional events
sent from various middleware devices such as event brokers and gateways.
CloudEvents includes metadata in events to associate these events as being
part of an event sequence for the purpose of event tracing and
troubleshooting.

#### Cloudbursting

TBD

#### IoT

IoT devices send and receive events related to their functionality.
For example, a connected thermostat will send telemetry on the current
temperature and could receive events to change temperatures.
These devices typically have a constrained operating environment
(cpu, memory) requiring a well defined event message format.
In a lot of cases these messages are binary encoded instead of textual.
Whether directly from the device or transformed via a gateway, CloudEvents
would allow for a better description of the origin of the message and the
format of the data contained within the message.

#### Event Correlation

A serverless application/workflow could be associated with multiple events from
different event sources/producers. For example, a burglary detection
application/workflow could involve both a motion event and a door/window open
event. A serverless platform could receive many instances of each type of
events, e.g. it could receive motion events and window open events from
different houses.

The serverless platform needs to correlate one type of event instance correctly
with other types of event instances and map a received event instance to the
correct application/workflow instance. CloudEvents will provide a standard way
for any event consumer (eg. the serverless platform) to locate the event
correlation information/token in the event data and map a received event
instance to the correct application/workflow instance.

### Existing Event Formats

As with the previous section, the examination (and understanding) of the
current state of the world was very important to the working group. To that
end, a sampling of existing current event formats that are used in practice
today was gathered.

#### Microsoft - Event Grid
```
{
    "topic":"/subscriptions/{subscription-id}",
    "subject":"/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.EventGrid/eventSubscriptions/LogicAppdd584bdf-8347-49c9-b9a9-d1f980783501",
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

#### Google - Cloud Functions (potential future)
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

#### AWS - SNS
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

#### AWS - Kinesis
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

#### IBM - OpenWhisk - Web Action Event
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

#### OpenStack - Audit Middleware - Event
```
{
  "typeURI": "http://schemas.dmtf.org/cloud/audit/1.0/event",
  "id": "d8304637-3f63-5092-9ab3-18c9781871a2",
  "eventTime": "2018-01-30T10:46:16.740253+00:00",
  "action": "delete",
  "eventType": "activity",
  "outcome": "success",
  "reason": {
    "reasonType": "HTTP",
    "reasonCode": "204"
  },
  "initiator": {
    "typeURI": "service/security/account/user",
    "name": "user1",
    "domain": "domain1",
    "id": "52d28347f0b4cf9cc1717c00adf41c74cc764fe440b47aacb8404670a7cd5d22",
    "host": {
      "address": "127.0.0.1",
      "agent": "python-novaclient"
    },
    "project_id": "ae63ddf2076d4342a56eb049e37a7621"
  },
  "target": {
    "typeURI": "compute/server",
    "id": "b1b475fc-ef0a-4899-87f3-674ac0d56855"
  },
  "observer": {
    "typeURI": "service/compute",
    "name": "nova",
    "id": "1b5dbef1-c2e8-5614-888d-bb56bcf65749"
  },
  "requestPath": "/v2/ae63ddf2076d4342a56eb049e37a7621/servers/b1b475fc-ef0a-4899-87f3-674ac0d56855"
}
```
[Documentation](https://github.com/openstack/pycadf/blob/master/doc/source/event_concept.rst)

#### Adobe - I/O Events
```
{
    "event_id": "639fd17a-d0bb-40ca-83a4-e78612bce5dc",
    "event": {
        "@id": "82235bac-2b81-4e70-90b5-2bd1f04b5c7b",
        "@type": "xdmCreated",
        "xdmEventEnvelope:objectType": "xdmAsset",
        "activitystreams:to": {
            "xdmImsUser:id": "D13A1E7053E46A220A4C86E1@AdobeID",
            "@type": "xdmImsUser"
        },
        "activitystreams:generator": {
            "xdmContentRepository:root": "https://cc-api-storage.adobe.io/",
            "@type": "xdmContentRepository"
        },
        "activitystreams:actor": {
            "xdmImsUser:id": "D13A1E7053E46A220A4C86E1@AdobeID",
            "@type": "xdmImsUser"
        },
        "activitystreams:object": {
            "@type": "xdmAsset",
            "xdmAsset:asset_id": "urn:aaid:sc:us:4123ba4c-93a8-4c5d-b979-ffbbe4318185",
            "xdmAsset:asset_name": "example.jpg",
            "xdmAsset:etag": "6fc55d0389d856ae7deccebba54f110e",
            "xdmAsset:path": "/MyFolder/example.jpg",
            "xdmAsset:format": "image/jpeg"
        },
        "activitystreams:published": "2016-07-16T19:20:30+01:00"
    }
}
```
[Documentation](https://www.adobe.io/apis/cloudplatform/events/documentation.html)
