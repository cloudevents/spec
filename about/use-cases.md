# CloudEvents - Use Cases

[WIP] Use-case examples to help end users understand the value of CloudEvents.

### Normalizing Events Across Services & Platforms

Major event publishers (e.g. AWS, Microsoft, Google, etc.) all publish events
in different formats on their respective platforms.  There are even a few cases
where services on the same provider publish events in different formats (e.g.
AWS).  This forces event consumers to implement custom logic to read or munge
event data across platforms and occasionally across services on a single
platform.

CloudEvents can offer a single experience for authoring consumers that handle
events across all platforms and services.

### Facilitating Integrations Across Services & Platforms

Event data being transported across environments is increasingly common.
However, without a common way of describing events, delivery of events across
environments is hindered.  There is no single way of determining where an event
came from and where it might be going.  This prevents tooling to facilitate
successful event delivery and consumers from knowing what to do with event
data.

CloudEvents offers useful metadata which middleware and consumers can rely upon
to facilitate event routing, logging, delivery and receipt.

### Increasing Portability of Functions-as-a-Service

Functions-as-a-Service (also known as serverless computing) is one of the
fastest growing trends in IT and it is largely event-driven.  However, a
primary concern of FaaS is vendor lock-in.  This lock-in is partially caused
by differences in function APIs and signatures across providers, but the
lock-in is also caused by differences in the format of event data received
within functions.

CloudEvents' common way of describing event data increases the portability of
Functions-as-a-Service.

### Improving Development & Testing of Event-Driven/Serverless Architectures

The lack of a common event format complicates development and testing of
event-driven and serverless architectures.  There is no easy way to mock events
accurately for development and testing purposes, and help emulate event-driven
workflows in a development environment.

CloudEvents can enable better developer tools for building, testing and
handling the end-to-end lifecycle of event-driven and serverless architectures.

### Event Data Evolution

Most platforms and services version the data model of their events differently
(if they do this at all).  This creates an inconsistent experience for
publishing and consuming the data model of events as those data models evolve.

CloudEvents can offer a common way to version and evolve event data.  This will
help event publishers safely version their data models based on best practices,
and this help event consumers safely work with event data as it evolves.

### Normalizing Webhooks

Webhooks is a style of event publishing which does not use a common format.
Consumers of webhooks don’t have a consistent way to develop, test, identify,
validate, and overall process event data delivered via webhooks.

CloudEvents can offer consistency in webhook publishing and consumption.

### Policy Enforcement

The transiting of events between systems may need to be filtered, transformed,
or blocked due to security and policy concerns. Examples may be to prevent
ingress or egress of the events such as event data containing sensitive
information or wanting to disallow the information flow between the sender and
receiver.

A common event format would allow easier reasoning about the data being
transited and allow for better introspection of the data.

### Event Tracing

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

### Cloudbursting

### IoT

IoT devices send and receive events related to their functionality.
For example, a connected thermostat will send telemetry on the current
temperature and could receive events to change temperatures.
These devices typically have a constrained operating environment
(cpu, memory) requiring a well defined event message format.
In a lot of cases these messages are binary encoded instead of textual.
Whether directly from the device or transformed via a gateway, CloudEvents
would allow for a better description of the origin of the message and the
format of the data contained within the message.

### Event Correlation
A serverless application/workflow could be associated with multiple events from 
different event sources/producers. For example, a burglary detection 
application/workflow could involve both a motion event and a door/window open event. 
A serverless platform could receive many instances of each type of events, 
e.g. it could receive motion events and window open events from different houses. 
The serverless platform needs to correlate one type of event instance correctly 
with other types of event instances and map a received event instance to the 
correct application/workflow instance. CloudEvents will provide a standard way 
for any event consumer (eg. the serverless platform) to locate the event 
correlation information/token in the event data and map a received event instance 
to the correct application/workflow instance. 
