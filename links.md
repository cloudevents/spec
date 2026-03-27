# Connecting Events - Links Proposal

## Abstract

This proposal will outline how to connect individual CDEvents to one other.
Currently there's no way of associating events without needing to backtrack
across certain subject attributes, e.g.
[id](https://github.com/CDEvents/spec/blob/main/spec.md#id-subject). While
this does give us the ability to construct some graph, we do not know when a
particular chain starts or finishes.

This proposal will outline a new approach that will allow for connecting
CDEvents and give a clear distinction of when an activity chain starts and
finishes.

## CDEvents Architecture

Below is an example diagram for a CDEvent system to help illustrate how users
and systems may utilize CDEvents. In this case, a user is merging a GitHub pull
request and then using some CDEvent front-end to query all links for their
request to get a full view of all that has happened.

```plaintext
+--------------------------------------------------------------------------+          +------------------+
|                                                                          | (links)  |                  |
|                                 Event Bus                                +--------->|                  |
|                                                                          |          |                  |
+----------------------+---------------------------------------------------+          |                  |
       ^               |   ^                               |   ^                      |                  |
       |               |   |                               |   |                      |                  |
       |               |   |                               |   |                      |                  |
       |               v   |                               v   |                      |                  |
+------+------+   +--------+----+   +-------------+   +--------+----+                 |     Links        |
|             |   |             |   |             |<--+             |                 |     Service      |
|    GitHub   |   |   Jenkins   +-->| Artifactory |   |  Spinnaker  |                 |                  |
|             |   |             |   |             +-->|             |                 |                  |
+-------------+   +-------------+   +-------------+   +------+------+                 |                  |
       ^                                                     |                        |                  |
       |                                                     v                        |                  |
       |                                              +-------------+                 |                  |
       |                                              |             |                 |                  |
       |                                              | Kubernetes  |                 |                  |
       |                                              |             |                 |                  |
       | user merges a pull                           +-------------+                 +------------------+
       | request from GitHub                                                                  ^  |
       |                                                                                      |  |
       |                                                                                      |  |
       |                                                                                      |  |
+------+-----+                                                                                |  |
|            |                                                                                |  |
|    User    |  front-end requests all links for a particular request                         |  |
|            +--------------------------------------------------------------------------------+  |
|     o      |                                                                                   |
|    /|\     |<----------------------------------------------------------------------------------+
|    / \     |
+------------+
```

## Semantics

This section will define various terms to ensure there are no assumptions being
made when we talk about linking events

* **CI**        - [Continuous integration](https://bestpractices.cd.foundation/learn/ci/)
* **CD**        - [Continuous delivery](https://bestpractices.cd.foundation/learn/cd/)
* **Chain**     - A chain is an end to end representation of all activities performed
  in the CI/CD life cycle of some entity
* **Link**      - A link is an object which describes how an event is related to another event.

## Goals

The biggest challenge in this whole process is ensuring that connected events
can be retrieved quickly and efficiently, while also providing the necessary
metadata and structure to give a detailed picture of how things occurred.

1) Provide a way of quickly retrieving all related links
2) Keep link data structured small and simple
3) Scalable

## Use Cases

This section will go over a few use cases and explain how this approach can be
used to solve for each particular case.

### 1. Fan Out Fan In

The fan out fan in use case is an example where a system may make parallel
requests (fan out), and merge back to some other or the very same system (fan in)

Let us assume we have 3 system in our CI/CD environment. A continuous
integration environment, which we will call CI system, that runs tests and
builds artifacts, an artifact store that receives artifacts from the CI system,
and lastly the CD system which consume these artifacts shown in the diagram
below.

```plaintext
                    +-------------------+   +-----------------+
                +-->|   Build for Mac   |-->|   Test on Mac   |---+
+-----------+   |   +-------------------+   +-----------------+   |
|  Static   |   |   +-------------------+   +-----------------+   |   +---------------------------+
|  Code     |---+-->|   Build for SLES  |-->|   Test on SLES  |---+-->| Promote & Deliver Release |
|  Analysis |   |   +-------------------+   +-----------------+   |   +---------------------------+
+-----------+   |   +-------------------+   +-----------------+   |
                +-->| Build for Windows |-->| Test on Windows |---+
                    +-------------------+   +-----------------+
```

The diagram above shows the CI event creating 3 separate artifacts that will
make it's way to the artifact store. Some CD system would then consume those
artifact, but would need to group all the artifact when the CI system finishes
its pipeline. This is not meant to be a full diagram of the whole CDEvents
flow, but a simple representation of the artifact(s) life cycle.

### 2. Generic UI

With the goal of interoperability, this allows for compatible standalone
generic UIs for any CI/CD system.

## Connecting Events

An individual event usually has some connection to some trigger. This can be a
new commit added to a pull request, a test suite being called in the CI
process, or publishing a new artifact for some system to consume. While these
events mean something themselves, they do not give the proper context of what
caused what. This section will introduce two new fields, `chainId` and
`links`, within the CDEvents context that will allow for giving some path
between CDEvents.

```json
{
  "context": {
    "specversion": "0.6.0-draft",
    "id": "505b31c2-8bc8-47b3-a1a0-269d7a8530ac",
    "source": "dev/jenkins",
    "type": "dev.cdevents.testsuite.finished.0.1.1",
    "chainId": "00000000-0000-0000-0000-000000000001", # new chain id field
    "timestamp": "2023-03-20T14:27:05.315384Z"
  },
  "subject": {
    "id": "MyTestSuite",
    "source": "/tests/com/org/package",
    "content": {}
  }
}
```

The `chainId` is an ID that will be generated when a new CDEvent chain is
wanted or if no CDEvent chain is present. This ID will follow the
[UUID](https://datatracker.ietf.org/doc/html/rfc4122) format. Chain IDs will
serve as a bucket for all CDEvents with some sort of path to each other.

### Optional Links Field

While links can be sent separately, links can also be embedded in the CDEvent
context as an optional field. Embedded links look similar to separate links
except `START` links are not needed since we can infer when a chain has started
based on the context of the event. This leaves only three types of links that
may be embedded, `PATH`, `RELATION` and `END`. While `END` might be possible to
infer, it may not be as simple especially if there are gaps or islands. Having
an event specifically say it is the `END` of a chain will allow for UIs or
systems to act accordingly based off the ending notation.

```json
{
  "context": {
    "specversion": "0.6.0-draft",
    "id": "271069a8-fc18-44f1-b38f-9d70a1695819",
    "chainId": "7ff3f526-1a0e-4d35-8a4c-7d6295e97359",
    "source": "/event/source/123",
    "type": "dev.cdevents.pipelinerun.queued.0.1.1",
    "timestamp": "2023-03-20T14:27:05.315384Z",
    "links": [
      {
        "linkType": "RELATION",
        "linkKind": "TRIGGER",
        "target": {
          "contextId": "5328c37f-bb7e-4bb7-84ea-9f5f85e4a7ce"  # context id of a change.merged CDEvent
        }
      }
    ]
  },
  "subject": {
    "id": "mySubject123",
    "source": "/event/source/123",
    "content": {
      "pipelineName": "myPipeline",
      "uri": "https://www.example.com/mySubject123"
    }
  }
}
```

Above shows a simple relation link that would allow a trigger relation of a
`changed.merge` and the `pipelinerun.queued` event. To illustrate links
further, we can allow for a path link between `pipelinerun.queued` to the
`pipelinerun.started` event shown below.

```json
{
  "context": {
    "specversion": "0.6.0-draft",
    "id": "271069a8-fc18-44f1-b38f-9d70a1695819",
    "chainId": "7ff3f526-1a0e-4d35-8a4c-7d6295e97359",
    "source": "/event/source/123",
    "type": "dev.cdevents.pipelinerun.started.0.1.1",
    "timestamp": "2023-03-20T14:27:05.315384Z",
    "links": [
      {
        "linkType": "PATH",
        "from": {
          "contextId": "271069a8-fc18-44f1-b38f-9d70a1695819" # context id of the pipelinerun.queued event
        }
      }
    ]
  },
  "subject": {
    "id": "mySubject123",
    "source": "/event/source/123",
    "content": {
      "pipelineName": "myPipeline",
      "uri": "https://www.example.com/mySubject123"
    }
  }
}
```

## Propagation

Chain propagation will be handled differently depending on the protocol that is
used. At a high level, the SDK expects calls to construct the proper paths, but
connecting of events will be handled completely by the SDKs.

There are a couple cases where propagation is difficult, and maybe even
impossible depending on what the receiving services are willing to do. In
events where the SDKs are not used, it is up to these receiving services to
pass the chain IDs. If this is not done, then there will be a break in the
chain, which means that a new chain will be started, or missing links that will
cause these services to not be visible.

## Links Spec

So far we have only talked about what a service may receive when consuming a
CDEvent with links. However, when we store a link, there's a lot more metadata
that can and should be added.

The idea is we would expect users to start links, connect links, and end links
accordingly through APIs we would provide. This is very similar to how tracing
works in that the individual services dictate when a tracing span starts and
finishes.  Granularity in tracing is completely up to the engineer which this
proposal also intends users to do.

This will introduce new APIs to the CDEvents SDKs to handle automatic injection
of links or allow users to provide their own definition of what a CDEvent chain
is.

These links can be, but are not limited to being, sent when a CDEvent has
completed: to some collector, the link service, or the event bus. Further
the link service will allow for tagging of various metadata allowing for users
to specify certain labels when looking at links.

Some users may prefer to not run a separate links service especially if they
know their overall flow may only contain a few links. If that is the case,
simply turning on link payload aggregation, will send all links in the
payload. Mind you, this can make the payload very large, but may be good for
debugging.

The chain ID header will continue to propagate, unless the user explicitly
starts a new CDEvent chain. If there is no chain ID, the client will generate
one and that will be used for the lifetime of the whole events chain.

In the case when an event consumer is also an event producer, such a consumer
will easily be able to construct the link to the consumed event. A producer of events
with start links is often not an event consumer itself. When links are sent stand-alone,
and not embedded within the CDEvents themselves, an event consumer that is not
an event producer could still construct the links if it has the necessary information for
it. An event producer that wants to provide a link to some earlier sent event will need
to look it up in a links service or similar if the producer wants to embed the link into
the produced event itself. For events produced within a service, that service should
be able to construct the links between those events by itself.

```plaintext
+-----+      +-----+      +-----+                                                                +--------------+         +-----------+
| Git |      | CI  |      | CD  |                                                                | Link Service |         | Event Bus |
+--+--+      +--+--+      +--+--+                                                                +-------+------+         +-----+-----+
   |            |            |           #1 (send change merged event)                                   |                        |
   +----------------------------------------------------------------------------------------------------------------------------->|
   |            |            |           #2 (source change link to start chain)                          |                        |
   +----------------------------------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |   #3 (proxy link #1)   |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #4 (receive change merged event)                                |                        |
   |            |<----------------------------------------------------------------------------------------------------------------+
   |            |            |           #5 (send pipeline queued event)                                 |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |           #6 (source change links connecting #1 -> #5)                    |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |   #7 (proxy link #6)   |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #8 (send pipeline started event)                                |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |           #9 (pipeline queued links connecting #5 -> #8)                  |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |  #10 (proxy link #9)   |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #11 (send build queued event)                                   |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |           #12 (pipeline started links connecting #6 -> #9)                |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |  #13 (proxy link #12)  |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #14 (send build started event)                                  |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |           #15 (build queued event links connecting #11 -> #14)             |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |  #17 (proxy link #16)  |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #18 (send build completed event)                                |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |           #19 (build started event links connecting #14 -> #18)           |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |  #20 (proxy link #15)  |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #21 (send pipeline finished event)                              |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |           #22 (build completed event links connecting #18 -> #21)         |                        |
   |            +---------------------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |  #23 (proxy link #22)  |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #24 (receive pipeline finished event)                           |                        |
   |            |            |<---------------------------------------------------------------------------------------------------+
   |            |            |           #25 (send pipeline queued event)                                |                        |
   |            |            +--------------------------------------------------------------------------------------------------->|
   |            |            |           #26 (pipeline finished event links connecting #21 -> #25)       |                        |
   |            |            +--------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |  #27 (proxy link #26)  |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #28 (send pipeline started event)                               |                        |
   |            |            +--------------------------------------------------------------------------------------------------->|
   |            |            |           #29 (pipeline queued links connecting #25 -> #28)               |                        |
   |            |            +--------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |  #30 (proxy link #29)  |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #31 (send environment created event)                            |                        |
   |            |            +--------------------------------------------------------------------------------------------------->|
   |            |            |           #32 (pipeline started links connecting #28 -> #31)              |                        |
   |            |            +--------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |  #33 (proxy link #32)  |
   |            |            |                                                                           |<-----------------------|
   |            |            |           #34 (environment created end link for #31)                      |                        |
   |            |            +--------------------------------------------------------------------------------------------------->|
   |            |            |                                                                           |  #32 (proxy link #31)  |
   |            |            |                                                                           |<-----------------------|
```

This example shows how these different types would be used in a CI/CD setting,
but is not the only architecture.

### Payloads

This section will describe the first few sequences in the sequence diagram to
help explain the overall flow using payloads from CDEvents.

1. This is our very first event to the start of our CI/CD chain. This event
   would have been sent from some source management tool like Github, Gitlabs,
   etc.

```json
{
  "context": {
    "specversion": "0.6.0-draft",
    "chainId": "d0be0005-cca7-4175-8fe3-f64d2f27bc01",
    "id": "38a09112-a1ab-4c26-94c4-edfc234ef631",
    "source": "/event/source/123",
    "type": "dev.cdevents.change.merged.0.1.2",
    "timestamp": "2023-03-20T14:27:05.315384Z"
  },
  "subject": {
    "id": "mySubject123",
    "source": "/event/source/123",
    "type": "change",
    "content": {
      "repository": {
        "id": "cdevents/service",
        "source": "https://github.com/cdevents/service/pull/1234"
      }
    }
  }
}
```

Something to call out here is that the `chainId` may have been `null`, for
whatever reason, prior to this event. This means any parents to this event did
not generate a `chainId`. When an event is sent, it is important that the
sender generates this id.

2. We send the start link to let the links service know that we are creating a
   new chain.

```json
{
  "chainId": "d0be0005-cca7-4175-8fe3-f64d2f27bc01",
  "linkType": "START",
  "timestamp": "2023-03-20T14:27:05.315384Z",
  "start": {
    "contextId": "38a09112-a1ab-4c26-94c4-edfc234ef631" # context.id of #1
  }
}
```

3. Event bus proxies the link payload from `#2` to the links service.

4. Shows some consumer consuming `#1` to do some action.

5. The CI system will queue a pipeline execution, and will generates a
`context.id` to be sent

```json
{
  "context": {
    "specversion": "0.6.0-draft",
    "chainId": "d0be0005-cca7-4175-8fe3-f64d2f27bc01",
    "id": "AA6945F8-B0F1-48DD-B658-25ACF95BD2F5",
    "source": "/event/source/123",
    "type": "dev.cdevents.pipelinerun.queued.0.1.1",
    "timestamp": "2023-03-20T14:27:05.315384Z"
  },
  "subject": {
    "id": "mySubject123",
    "source": "/event/source/123",
    "content": {
      "pipelineName": "myPipeline",
      "uri": "https://www.example.com/mySubject123"
    }
  }
}
```

6. As the send change merge event is sent, the system will follow up with
sending a link associated with the prior event which connects `#1` to `#5`

```json
{
  "chainId": "d0be0005-cca7-4175-8fe3-f64d2f27bc01",
  "linkType": "PATH",
  "timestamp": "2023-03-20T14:27:05.315384Z",
  "from": {
      "contextId": "38a09112-a1ab-4c26-94c4-edfc234ef631" # context.id of #1
  },
  "to": {
      "contextId": "aa6945f8-b0f1-48dd-b658-25acf95bd2f5" # context.id of #5
  },
  "tags": {
    "ci.environment": "prod"
  }
}
```

7. The event bus will then forward link `#6` to the links service

34. Paylods from `8-33` are very similar to all prior payloads shown here, but
    the last sequence is the ending link.

```json
{
  "chainId": "d0be0005-cca7-4175-8fe3-f64d2f27bc01",
  "linkType": "END",
  "timestamp": "2023-03-20T14:27:05.315384Z",
  "end": {
    "contextId": "7d5e011f-5073-44a7-b4f0-86dd7d4c2c7f" # context.id of #31
  }
}
```


### Link Types

This section will describe the four different `linkType`s: `START`, `END`, `PATH`, and
`RELATION`.

First is the common link fields shared between all links

| Name            | Description                                                                                              |
|-----------------|----------------------------------------------------------------------------------------------------------|
| chainId   | This represents the full life cycles of a series of events in CDEvents                                        |
| linkType  | An enum that represents the type of link, e.g. 'START', 'END', 'PATH', 'RELATION'                             |
| timestamp  | The timestamp of when the link was created. This field is omitted when embedding links in the CDEvent context |
| tags       | Custom metadata that an individual link can have. It is important to note values and keys can only be strings |

#### Start Link

Start links are used to indicate that a new chain has been started, and is a
special type of `PATH` link. The reasoning for having a separate link type for
both `START` and `END` is that it allows for clear indication of starting and
stopping a chain. If we relied only on `PATH` link types to indicate either of
these states, then consumers may not be able to distinguish the two different
states.  This makes it very clear and easy for consuming systems.

| Name  | Description                                                                        |
|-------|------------------------------------------------------------------------------------|
| start | An node object that describes the event that is associated with starting the chain |

```json
{
  "chainId": "97ef590e-0285-45ad-98bb-9660ffaa567e",
  "linkType": "START",
  "timestamp": "2023-03-20T14:27:05.315384Z",
  "start": {
    "contextId": "a721d6ba-bbd6-4737-9274-5ddd2526b92f"
  },
  "tags": {
    "ci.environment": "prod"
  }
}
```

#### End Link

End links are used to indicate that a new chain has completed, and are a
special type of `PATH` link.

| Name | Description                                                                        |
|------|------------------------------------------------------------------------------------|
| from | Where the link is coming from. This field is omitted when embedded this link type. |
| end  | An node object that describes the event that is associated with ending the chain   |

```json
{
  "chainId": "97ef590e-0285-45ad-98bb-9660ffaa567e",
  "linkType": "END",
  "timestamp": "2023-03-20T14:27:05.315384Z",
  "from": {
    "contextId": "bf9d3c52-1c12-4029-a8d6-e4aca6c69127"
  },
  "end": {
    "contextId": "bf9d3c52-1c12-4029-a8d6-e4aca6c69127"
  },
  "tags": {
    "ci.environment": "prod"
  }
}
```

#### Path Link

A path link is used to indicate a path that a request has taken, which may be
from system to system or could describe a path within a system like tests.

| Name            | Description              |
|-----------------|--------------------------|
| from       | Where the link is coming from. This field is omitted when embedded this link type. |
| to         | Where the link is going to |

```json
{
  "chainId": "97ef590e-0285-45ad-98bb-9660ffaa567e",
  "linkType": "PATH",
  "timestamp": "2023-03-20T14:27:05.315384Z",
  "from": {
    "contextId": "f27e36a4-5c78-43c0-840a-52524dfeed03"
  },
  "to": {
    "contextId": "f004290e-5e45-45f4-b97a-fa82499f534c"
  },
  "tags": {
    "ci.environment": "prod"
  }
}
```

#### Relation Link

Relation links are used to add some context to certain events

| Name            | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| linkKind  | A stringed value representing any sort of relationship the link has to the event |
| source     | The entity from which the `linkKind` is applied to. This field is omitted when embedding this link type. |
| target     | An event that will be associated with the `source` |

```json
{
  "chainId": "97ef590e-0285-45ad-98bb-9660ffaa567e",
  "linkType": "RELATION",
  "linkKind": "ARTIFACT",
  "timestamp": "2023-03-20T14:27:05.315384Z",
  "source": {
    "contextId": "5668c352-dd9d-4dee-b334-384e4661d21b"
  },
  "target": {
    "contextId": "3579a5aa-ef46-4ee8-95db-0540298835de"
  },
  "tags": {
    "ci.environment": "prod"
  }
}
```
### Scalability

Scalability is one of the bigger goals in this proposal and we wanted to ensure
fast lookups. This section is going to describe how the proposed links format
will be scalable and also provide tactics on how DB read/writes can be done.

The purpose of the chain ID is to ensure very fast lookups no matter the
database. Without a chain ID the database or its client would need to
recursively follow event references, upstream or downstream depending on the
use case. A graph DB would easily provide that, and it is also possible to
implement on top of SQL like DBs and document DBs, but it will never be as fast
as querying for a chain ID.

Instead a link service that processes and stores the links to some DB is much
preferred as it gives companies and developers options to choose from.  When
using an SQL database, the chain ID could be the secondary key to easily
retrieve indexed entities. Links could be easily sorted by timestamps which
should roughly coordinate to their linked neighbors, parent and child.

CDEvents that are to be ingested by some service would also have to worry about
the number of events returned. This problem is mitigated in that only the
immediate parent(s) links are returned, and any higher ancestry are excluded.
If some service needs to get access to a higher (a parent's parent) they would
need to use the links API to retrieve them.
