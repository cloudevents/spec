# Discovery and Subscription Primer - WIP

<!-- no verify-specs -->

## Abstract

This non-normative document provides an overview of the Discovery and
Subscription API specifications. It is meant to complement those specifications
to provide additional background and insight into the history and design
decisions made during their development. This allows the specification itself
to focus on the normative technical details.

## Table of Contents

- History
- Design Goals
- Architecture
- Design Considerations
- Examples

## History

The CNCF working group created the CloudEvents specification to help with the
delivery of events from event producers to event consumers. The specification
defines some common eventing metadata (that were already part of most events
being generated), and where that data should appear based on how the event
is serialized and over which transport protocol it is being sent.

By doing this, readers of those messages, whether they be the final recipient
of the event or an intermediary, can find and use this metadata without the
need to understand the business logic of the event itself. Often, this
is needed to help properly route the message to the next hop in the event's
journey to its final recipient.

With that specification reaching version 1.0 status, the project members then
considered what additional pain-points might need to be addressed in this
space. And, it seemed only natural that once there was some standardization
around the format of the events, that the group's attention should be to help
with consumers finding the event producers of interest, and programmatically
subscribing to receive events from those producers.

Within that scope, two obvious items popped up:

1 - Discovery:
    This includes things such as: how does an event consumer know which events
    a producer will generated? Which transport, and encoding, mechanisms do
    they support? How should a consumer subscribe for events?
    
2 - Subscriptions: 
    Once the consumer determines if a particular producer will generate events
    that are of interest to them, how can they subscribe? Ideally, in an
    interoperable way so as to not need to have custom logic for each producer.

And with that, the 'Discovery' and 'Subscription API' specifications were born.

## Design Goals

- Re-use existing specifications and technology as much as possible
- Focus on the bare minimum, but have well defined extensibility points

...

## Use Cases

The following list of use cases were driving considerations during the
development of these specifications. These are not meant to imply that other
use cases are not supported, rather they are enumerated here to help provide
insight into the team's focus during the development cycle.

### Consumers

- Consumer wants to programmatically determine the list of events (event types)
  that a producer will generate so they can properly specify the list of events
  they are interested in as part of the subscribe() operation.
  
- Consumer wants to know which producers support certain event types so as to
  allow for the consumer to subscribe only to those producers since those are
  the only events that the consumer is interested in, or can support.

- Consumer wants to know which event delivery mechanisms a producer can support.
  This will allow them to pick a transport that best suits their needs. For
  example, a push vs pull delivery model.

- Consumer wants to know if a producer can support filtering of events, and
  which mechanisms, the producer supports. This can help consumers determine
  which producer might be the best choice to reduce the amount of messages
  sent, and whether filtering can be done by the producer or whether the
  consumer will need to to it themselves.

### Intermediaries

- In order to route subscriptions to producers and to provide a combined
  discovery endpoint to consumers, an intermediary aggregates the producers'
  event catalogs.

### Producers

- Producer wants to register with an intermediary. As the intermediary also
  provides a discovery endpoint, the producer transfers a catalog describing the
  events it produces to the intermediary.

## Architecture

- picts
- flows

...

## Design Considerations

- The Data Model
- Relationship to CE - CE required? ...
- REST vs ...
- REST Queries vs GraphQL
...

### The `id` attribute

Per the Discovery API specification, the Service's `id` is a globally
unique identifier for the Service. By ensuring that this value is immutable,
clients will be able to know when a Service is returned from the
Discovery Endpoints whether it is the same underlying Service as was returned
in a previous query despite any changes to its metadata - even if all of the
metadata has changed (except, of course, for the `id`). This includes the
cases where the same Service is returned from multiple Discovery Endpoints.

Additionally, Discovery Endpoints may have multiple "views" over the set
of Services that they expose. Meaning, the same list of Services might
produce a different set of metadata based on these "views". In these cases,
the `id` attribute would be the same across those views if the Discovery
Endpoints wish for the underlying Service to be considered to be the same
Service.

However, it is expected that given the same set of inputs (e.g. Discovery
Endpoint URL, user credentials, etc.), that the same `id` would be returned
each time for the same Service.

## Examples
...

### Simple Discovery and Subscribe

```
$ curl http://github.com/services
```

Response:
```
- services:
  - service: Github
    subscriptionuri: https://api.github.com/subscribe
    protocols:
    - protocol: HTTP
    types:
    - type: com.github.pull_request.opened
      datacontenttype: application/json
      sourcetemplate: https://api.github.com/repos/{org}/{repo}/pulls/{id}
    - type: com.github.pull_request.edited
      datacontenttype: application/json
      sourcetemplate: https://api.github.com/repos/{org}/{repo}/pulls/{id}
    - type: com.github.pull_request.closed
      datacontenttype: application/json
      sourcetemplate: https://api.github.com/repos/{org}/{repo}/pulls/{id}
    - type: com.github.issue.opened
      datacontenttype: application/json
      sourcetemplate: https://api.github.com/repos/{org}/{repo}/issues/{id}
    - type: com.github.issue.edited
      datacontenttype: application/json
      sourcetemplate: https://api.github.com/repos/{org}/{repo}/issues/{id}
    - type: com.github.issue.closed
      datacontenttype: application/json
      sourcetemplate: https://api.github.com/repos/{org}/{repo}/issues/{id}
```

Now subscribe:

```
$ curl https://api.github.com/subscribe/create -d @- <<
{
"id": "mysub1",
"protocol": "http",
"sink": "https://myfunc.example.com/processor"
}
```

Response:
```
{
"id": "mysub1",
"protocol": "http",
"sink": "https://myfunc.example.com/processor"
}
```

### Filtering

### Pull

### Using 'sourcetemplate' for routing
