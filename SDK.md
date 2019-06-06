# CloudEvents SDK

The intent of this document to describe bare minimum set of requirements for a
new SDKs.

## Status of this document

Since [CloudEvent spec](spec.md) still considered as a working draft this
document also suppose to be considered as a working draft.

## Contribution acceptance

Being an open source community CloudEvents team is open for a new members as
well open to their contribution. In order to ensure that an SDK is going to be
supported and maintained CloudEvents community would like to ensured that:

- a person (developer, committer) is going to become a maintainer
- a person commits to support ongoing changes to the [CloudEvent spec](spec.md)

## Officially maintained software development kits (SDK)

Software Development Kit (SDK) is a set of helpers designed and implemented to
enhance and speed up a CloudEvents integration. As part of community efforts
CloudEvents team committed to support and maintain the following SDKs:

- [Go SDK](https://github.com/cloudevents/sdk-go)
- [Java SDK](https://github.com/cloudevents/sdk-java)
- [Python SDK](https://github.com/cloudevents/sdk-python)
- [CSharp](https://github.com/cloudevents/sdk-csharp)
- [JavaScript SDK](https://github.com/cloudevents/sdk-javascript)

## SDK contribution

That's said, being an open source community CloudEvents is all about building
open for contribution. In order to keep the development/user experience the same
(as much as possible) CloudEvents team agreed to establish minimum requirements
for a new SDK.

### Technical requirements

Supports CloudEvents spec milestones and ongoing development version.
HTTP transport support (both structured and binary).
Widely used programming language version.

### Object model structure guidelines

The CloudEvents specification set consists of

* the base specification that defines the abstract information model and
  associated rules for a CloudEvent,
* a set of extensions to the base specification that define use-case
  specific attributes and associated rules,
* a set of event format specifications that define how a CloudEvent and  
  its attributes are encoded in a particular wire transfer format, and
* a set of transport bindings that define how a wire-encoded CloudEvent is
  interoperably transported from a publisher or intermediary to a target
  endpoint using a particular application protocol.

The object model of any API projection of CloudEvents MUST reflect the
specification architecture with the following elements:

* A generic CloudEvent class/object/structure that provides access to the
  CloudEvent attributes and enforces data type constraints and all further
  conformance rules defined in the core CloudEvents specification. Instances
  of this class/object/structure MUST always be in a conformant state.
  The generic CloudEvent abstraction SHOULD provide strongly typed access
  to all well-known attributes, and MUST also provide name-indexed access
  to any application-specific extension attributes that the event might carry.
  Name-indexed access MUST include well-known attributes from the core
  specification and from application-activated specification extensions (see
  below). The related rules MUST be enforced when setting the attribute 
  values through the name-indexed access path.
* A generic abstraction for extensions that allows for one or more active
  extensions to be added to the CloudEvent abstraction such that the
  extension-defined attributes are attached to the CloudEvent and
  the conformance of their values can be validated.
  Each SDK MUST implement all extensions defined in the CloudEvents
  repository. "Active" extensions are those that the application explicitly
  selects for use. Any application MAY ignore a particular
  extension and even use well-known extension attribute names for semantically
  different purposes.
* An encoder abstraction and implementation for each event format which turns
  a CloudEvent instance and its active extensions into a conformant
  wire-representation and vice versa. If defined in the event format, the
  encoder MUST be able to render the entire event in a structured transport
  representation, and MUST also be able to render individual attribute values
  for a binary transport representation.
* At least one implementation for each transport binding which integrates with
  the most commonly used transport implementation for the respective language
  and runtime. If there are multiple equally popular platform libraries for
  the same transport, the SDK SHOULD provide implementations for each.
  The transport binding implementation MUST NOT obscure or encapsulate the
  regular interaction with the respective platform API for its core send
  and receive functionality; instead, the SDK SHOULD provide an extension or
  complement to the respective platform API that fits the respective API style
  and allows for mapping a CloudEvent from and to the respective application
  protocol message/event.
  Because selecting and detecting structured or binary transfer modes is a
  transport level choice, the respective mapping function MUST be given a
  reference to the desired event format encoder for mapping to the application
  protocol message/event. This reference MAY also be given through a default
  configuration choice.
  When mapping from the application protocol message/event, the SDK
  SHOULD identify and choose the required event format encoder from the content
  type information of the protocol, if available on the protocol.

### Preferable API signature guidelines

In order to remain developer/user UX the same among existing officially
supported SDKs CloudEvents team asks maintainers to align with the following API
signatures. Please consider the following code as pseudo-code.

#### Event object constructor API

Event build considered to be an event constructor:

```
    v01.Event()
```

#### Event object setters API

This particular code sample represents bare minimum number of setters:

```
    v01.Event().
    SetDataContentType("application/json").
    SetData('{"name":"john"}').
    SetEventID("my-id").
    SetSource("from-galaxy-far-far-away").
    SetEventTime("tomorrow").
    SetEventType("cloudevent.greet.you")
```

Content type setter represents an event MIME content type setter:

```
    SetDataContentType(content_type string)
```

Data setter represents an event data setter:

```
    SetData(event_data serializable)
```

ID setter represents an event ID setter:

```
    SetEventID(id string)
```

Source setter represents an event source setter:

```
    SetSource(source URL)
```

Time setter represents event emit time setter:

```
    SetEventTime(time RFC3339)
```

Type setter represents an event type setter:

```
    SetEventType(type string)
```

Extensions setter represents an event type setter:

```
    SetExtensions(exts map[string]string)
```

Generic setter represents an event attribute setter:

```
    Set(key string, value serializable)
```

#### Event object getters API

Event getters are set of methods designed to retrieve an event attributes.
Here's the list of getters:

```
    EventType() -> string
    Source() -> URL
    EventID() -> string
    EventTime() -> RFC3339
    SchemaURL() -> string
    DataContentType() -> string
    Data() -> serializable
    Extensions() -> map[string]string

    Get(key string) -> serializable

```

All these getters correspond to setters from above.

#### HTTP API

CloudEvents spec defines an HTTP transport, that's said, SDK suppose to support
an HTTP transport routine. As part of an CloudEvent spec, defines two formats:

- [structured](http-transport-binding.md#32-structured-content-mode)
- [binary](http-transport-binding.md#31-binary-content-mode)

#### HTTP API unmarshaller

An HTTP unmarshaller should be capable of detecting a CloudEvent format from an
HTTP request headers and a body. Here's the signature of an unmarshaller:

```
    FromRequest(
        headers HTTP-Headers,
        body Stream,
        data_unmarshaller function(data serializable) -> object
    ) -> CloudEvent:
```

In this signature:

- `headers` could be a `map of string to string` or a
  `map of string to list of strings`, the type of this parameter may vary
- `body` is a stream, since CloudEvent spec does not define exact type of an
  event data, SDK should not be responsible for data coercing
- `data_unmarshaller` is a function that performs data unmarshaller, logic of
  this method may vary depending on the type of an event format
- the return statement is a CloudEvent of the particular spec

#### HTTP API marshaller

An HTTP marshaller is a method that should be capable to convert a CloudEvent
into a combination of an HTTP request headers and a body. Here's the signature
of a marshaller:

```
    ToRequest(
        event CloudEvent,
        converter_type FormatRef,
        data_marshaller function(data serializable) -> object
    ) -> map[string]string, Stream :
```

In this signature:

- `event` is a CloudEvent of the particular spec
- `converter_type` represents a type of an HTTP binding format
  ([binary](http-transport-binding.md#31-binary-content-mode) or
  [structured](http-transport-binding.md#32-structured-content-mode))
- `data_marshaller` is a function that serialized an event data
- the return statement is a set of an HTTP headers and request body

The reason for such signature is that in most of programming languages there are
a lot if different HTTP frameworks and route handling signature may vary, but
HTTP headers and a request body is common (or may be easily converted to the
appropriate type).

#### HTTP Converters API

Each transport binding unmarshaller/marshaller is a set of converters. In terms
of an SDK the converter is a set API methods that are actually converting a
CloudEvent of the particular spec into a transport binding-ready data.

Converter API consists of at least two methods:

```
    Read(...)
    Write(...)
```

Signature of these methods may vary depending on the the type of a transport
binding.

HTTP Converters API is the example of Converters API implementation for the
[HTTP transport binding](http-transport-binding.md). Taking into account that
the CloudEvent spec defines 2 (structured and binary) formats, an SDK suppose to
implement two converters (one per each format):

- `BinaryHTTPCloudEventConverter`
- `StructuredHTTPCloudEventConverter`

HTTP Converters suppose to comply the following signature:

```
    Read(
        event CloudEvent,
        headers headers HTTP-Headers,
        body Stream,
        data_unmarshaller function(data serializable) -> object
    ) -> CloudEvent

    Write(
        event CloudEvent,
        data_marshaller function(data serializable) -> object
    ) -> HTTP-Headers, Stream

```

As you may see, Converter signature follows the signature of
marshaller/unmarshaller. It means that an HTTP marshaller/unmarshaller is a set
of binary and structured converters.

In `Read`:

- `event` - a placeholder (empty event object), see
  [event constructor](#event-object-constructor-api).
- `headers` - an HTTP request headers
- `body` - an HTTP request body
- `data_unmarshaller` - a function that turns an event data into an object of
  the particular type
- returns a valid CloudEvent of the particular spec

In `Write`:

- `event` - a CloudEvent
- `data_marshaller` - a function that marshals an event data
- returns a set of an HTTP headers and a body.

### AMQP API

#### AMQP marshaller/unmarshaller

TBA

#### AMQP Converters API

TBA

### MQTT API

#### MQTT marshaller/unmarshaller

TBA

##### MQTT Converters API

TBA

### NATS API

#### NATS marshaller/unmarshaller

TBA

##### NATS Converters API

TBA
