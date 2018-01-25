# CloudEvents - Use Cases

[WIP] Use-case examples to help end users understand the value of OpenEventing.

### Normalizing Events Across Services & Platforms

Major event publishers (e.g. AWS, Microsoft, Google, etc.) all publish events
in different formats on their respective platforms.  There are even a few cases
where services on the same provider publish events in different formats (e.g.
AWS).  This forces event consumers to implement custom logic to read or munge
event data across platforms and occasionally across services on a single
platform.

OpenEvents can offer a single experience for authoring consumers that handle
events across all platforms and services.

### Facilitating Integrations Across Services & Platforms

Event data being transported across environments is increasingly common.  
However, without a common way of describing events, delivery of events across
environments is hindered.  There is no single way of determining where an event
came from and where it might be going.  This prevents tooling to facilitate
successful event delivery and consumers from knowing what to do with event
data.

OpenEvents offers useful metadata which middleware and consumers can rely upon
to facilitate successful event delivery and receipt.

### Increasing Portability of Functions-as-a-Service

Functions-as-a-Service (also known as serverless computing) is one of the
fastest growing trends in IT and it is entirely event-driven.  However, a
primary concern of FaaS is vendor lock-in.  This lock-in is partially caused
by differences in function APIs and signatures across providers, but the
lock-in is also caused by differences in the format of event data received
within functions.

OpenEvents' common way of describing event data increase the portability of
Functions-as-a-Service.

### Improving Development & Testing of Event-Driven/Serverless Architectures

The lack of a common event format complicates development and testing of
event-driven and serverless architectures.  There is no easy way to mock events
accurately for development and testing purposes, and help emulate event-driven
workflows in a development environment.

OpenEvents can enable better developer tools for building and testing
event-driven and serverless architectures.

### Event Data Evolution

Most platforms and services version their event data differently, if at all.
This creates an inconsistent experience for handling event data as it evolves.

OpenEvents can offer a common way to version and evolve event data.

### Normalizing Webhooks

Webhooks is a style of event publishing which does not use a common format.  
Consumers of webhooks don’t have a consistent way to develop, test, identify,
validate, and overall process event data delivered via webhooks.

OpenEvents can offer consistency in webhook publishing and consumption.

### Policy Enforcement

### Event Tracing

### Cloudbursting

### IoT
