# CloudEvents SDK Requirements - Version 1.0-rc1

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

Supports CloudEvents spec milestones and ongoing development version. HTTP
transport support (both structured and binary). Widely used programming language
version.

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
    DataSchema() -> URL
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
