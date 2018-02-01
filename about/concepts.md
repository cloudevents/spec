
# CloudEvents Concepts

**Event**: data representing an occurrence, a change in state, that something happened (or did not happen).

**Occurrence**: something that happens (or doesn’t happen) and is detected by a software system (“source”).

Events include context and data. Each occurrence is uniquely identified by the data of the event. Events represent facts and therefore do not include a destination, whereas messages convey intent, transporting data from a source to a given destination.

## Eventing

Events are commonly used in server-side code to connect disparate systems where the change of state in one system causes code to execute in another. For example, a source may generate an event when it receives an external signal (e.g. HTTP or RPC) or observes a changing value (e.g. an IoT sensor or period of inactivity).

To illustrate how a system uses CloudEvents, the simplified diagram below shows how an **event** from a **source** triggers an **action**.

![alt text](img/source-event-action.png "A box representing the source with arrow pointing to a box representing the action. The arrow is annotated with 'e' for event and 'protocol'.")

The source generates a message where the event is encapsulated in a protocol.  The event arrives to a destination, triggering an action which is provided with the event data.

**Source**: the software instance that generates the event at runtime.

A **source** is a specific instance of a **source-type** which allows for staging and test instances. Open source software of a specific **source-type** may be deployed by multiple companies or providers.

Events can be delivered through various industry standard protocols (e.g. HTTP, AMQP, MQTT, SMTP), open-source protocols (e.g. Kafka, NATS), or platform/vendor specific protocols (AWS Kinesis, Azure Event Grid).

An **action** processes an **event** defining a behavior or effect which was triggered by a specific **occurrence** from a specific **source**.


