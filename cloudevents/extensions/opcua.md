# OPC UA

This extension maps [OPC UA](https://reference.opcfoundation.org/Core/Part1/v105/docs/)
[PubSub](https://reference.opcfoundation.org/Core/Part14/v105/docs/)
DataSetMessages to CloudEvents for routing over supported protocols. It defines
mappings for Core and other extension attributes and specifies OPC UA extension
attributes.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is used.
For example, an attribute being marked as "REQUIRED" does not mean it needs to
be in all CloudEvents, rather it needs to be included only when this extension
is being used.

## Mapping of REQUIRED Attributes

### id

MUST map to [Network Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.3#Table163)
field `MessageId`.

### source

Without the WoT profile, MUST either map to [Application
Description](https://reference.opcfoundation.org/Core/Part4/v104/docs/7.1)
field `applicationUri` of the OPC UA server or to a customer configured
identifier like a unified namespace path.

With the WoT profile, MUST follow its `source` mapping.

### type

Without the WoT profile, MUST map to
[Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `MessageType`. With the WoT profile, MUST follow its semantic event-type
rules.

### WoT mapping

When a CloudEvent uses both this extension and the
[WoT profile](./wot.md), the following mappings apply to data and event
messages:

- `source` MUST follow the WoT profile's Thing identity and version rules.
- `type` MUST follow the WoT profile's semantic event-type rules instead of
  mapping to the native `MessageType`.
- `opcuamessagetype` MUST carry the native `MessageType`.
- `subject` MUST follow the WoT profile's resolved-TD pointer rules.
- `opcuadatasetwriterid` and `opcuadatasetwritername`, when present, MUST
  identify the native DataSetWriter; neither MAY be appended to `subject`.
- For data and event messages, at least one of `opcuadatasetwriterid` and
  `opcuadatasetwritername` MUST be present. If both are present, they MUST
  identify the same DataSetWriter.
- For an event message, the `EventId` remains in the OPC UA event payload and
  MUST NOT be appended to `subject`.
- `opcuapublisherid` MUST identify the native PublisherId.
- `opcuasequence` MUST carry the native `SequenceNumber`. The CloudEvents
  `sequence` attribute, when present, MUST satisfy the independent ordering
  requirements of the Sequence extension and MUST NOT be inferred from
  `opcuasequence`.

These conditional mappings replace only the conflicting OPC UA mappings above.
All other requirements in this extension remain applicable. A profile that
uses only part of this extension MUST NOT claim conformance to it unless the
profile satisfies every applicable requirement in this document. Producers
sharing a WoT `source` MUST assign distinct native `MessageId` values to
distinct events within that source to satisfy Core's `source` and `id`
uniqueness requirement.

## Mapping of OPTIONAL Attributes

### datacontenttype

MUST be `application/json` for OPC UA PubSub JSON payload and MAY be appended with
`+gzip` when the payload is gzip compressed.

### dataschema

OPC UA provides type information as part of PubSub metadata messages, for non
OPC UA consumers or when different payload encoding like Avro is used, it is
REQUIRED to provide schema information (based on metadata information) in a
separate format like [JSON schema](https://json-schema.org/specification) or
[Avro schema](https://avro.apache.org/docs/1.11.1/specification/) or others. For
those cases the attribute references the schema and is used for versioning.

### subject

When the WoT profile is not used, the following OPC UA mappings apply:

For metadata, event and data messages (type one of `ua-metadata`, `ua-keyframe`,
`ua-deltaframe`, `ua-event`), `subject` MUST map to either [Data Set Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `DataSetWriterId` or `DataSetWriterName`.

For event messages (type equals to `ua-event`) `subject` MUST be appended with
"/" and [Base Event Type](https://reference.opcfoundation.org/Core/Part5/v104/docs/6.4.2)
field `EventId`.

### time

MUST map to [Data Set Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `Timestamp`.

## Mapping for other extensions

For data and event messages, the following well-known extension attributes
apply when this extension is used without the WoT profile. When both
extensions are used, determine message type from `opcuamessagetype`.

### sequence

Without the WoT profile, a `sequence` attribute, when present, MUST map to
the native DataSetMessage `SequenceNumber`. The OPC UA Publisher assigns and
increments this counter for messages from a DataSetWriter, as defined in
[OPC UA Part 14, Section 7.2.3][UA SequenceNumber]. This is the existing
OPC UA mapping for the [Sequence extension](./sequence.md), but it does not by
itself establish an ordering across multiple DataSetWriters that share one
CloudEvents `source`. A Publisher using this mapping MUST scope `source` to the
DataSetWriter's ordering scope; otherwise, it MUST NOT present the per-writer
counter as the CloudEvents `sequence`.

The Sequence extension compares String values lexicographically. The Producer
MUST format the mapped counter so that string comparison preserves the event
order; padding the unsigned decimal value to ten digits is one way to do so.
A reset or rollover can reverse that order within the same source scope. The
Producer MUST NOT use the counter for `sequence` when it cannot preserve the
ordering defined by the Sequence extension.

When the WoT profile is also used, `subject` identifies a TD or affordance, not
the DataSetWriter. `opcuasequence` therefore carries the native OPC UA counter;
a CloudEvents `sequence`, if present, MUST satisfy the Sequence extension's
ordering requirements independently and MUST NOT be inferred from
`opcuasequence`.

### traceparent

Attribute as defined by [distributed-tracing extension](./distributed-tracing.md)
to allow tracing from event publisher towards consumer.

### tracestate

Attribute as defined by [distributed-tracing extension](./distributed-tracing.md)
MAY be used to allow tracing from event publisher towards consumer.

### recordedtime

Attribute as defined by [recordedtime extension](./recordedtime.md) to
determine the latency between event publisher towards consumer.

## Attributes

### opcuametadatamajorversion

- Type: `Integer`
- Description: Links dataset message to the current version of the metadata.
Contains value from `MajorVersion` of [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `MetaDataVersion`.
- Constraints
  - OPTIONAL but MUST NOT be present if `dataschema` is used

### opcuametadataminorversion

- Type: `Integer`
- Description: Links dataset message to the current version of the metadata.
Contains value from `MinorVersion` of [Data Set Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `MetaDataVersion`.
- Constraints
  - OPTIONAL but MUST NOT be present if `dataschema` is used

### opcuastatus

- Type: `Integer`
- Description: Defines the overall status of the data set message, maps to
[Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `Status`.
- Constraints
  - OPTIONAL
  - REQUIRED if status is not _Good_
  - MAY be omitted if status is _Good_

CloudEvents `Integer` is limited to the signed 32-bit range. If a native
status value cannot be represented, the Producer MUST report an error rather
than omit the status, wrap the value, or report it as _Good_.

### opcuapublisherid

- Type: `String`
- Description: Identifies the OPC UA PubSub PublisherId.
- Constraints
  - OPTIONAL
  - If present, MUST use `<BuiltInType>:<value>`.
  - For `Byte`, `UInt16`, `UInt32` and `UInt64`, `<value>` MUST be the
    canonical unsigned decimal representation of the PublisherId.
  - For `Guid`, `<value>` MUST be the lowercase canonical UUID representation
    of the PublisherId.
  - For `String`, `<value>` MUST be the unpadded base64url encoding of the
    PublisherId's UTF-8 bytes.
  - In combination with the WoT profile, REQUIRED for data and event
    messages.
  - MUST map to the Network Message Header `PublisherId`.

### opcuadatasetwriterid

- Type: `Integer`
- Description: Identifies the DataSetWriter that produced the DataSetMessage.
- Constraints
  - OPTIONAL
  - If present, MUST be in the range 0 to 65535, inclusive.
  - MUST map to the Data Set Message Header `DataSetWriterId`.

### opcuadatasetwritername

- Type: `String`
- Description: Carries the human-readable name of the DataSetWriter that
  produced the DataSetMessage.
- Constraints
  - OPTIONAL
  - If present, MUST be non-empty.
  - MUST match the DataSetWriter's configured `DataSetWriterName`. For JSON
    message mapping, this is the [`DataSetWriterName` field][UA DataSetWriterName]
    when present in the DataSetMessage; otherwise the publisher obtains it
    from configuration.
  - In combination with the WoT profile, MUST uniquely identify the
    DataSetWriter within the configured `opcuapublisherid` scope.
  - In combination with the WoT profile, names MUST be compared exactly,
    without case folding or Unicode normalization.

### opcuamessagetype

- Type: `String`
- Description: Carries the OPC UA PubSub DataSetMessage type when `type`
  identifies a WoT semantic event type.
- Constraints
  - OPTIONAL
  - In combination with the WoT profile, REQUIRED for data and event
    messages.
  - MUST map to the Data Set Message Header `MessageType`.
  - The value MUST be the native OPC UA message type, such as `ua-keyframe`,
    `ua-deltaframe` or `ua-event`.

### opcuasequence

- Type: `String`
- Description: Carries the native DataSetMessage sequence counter without
  assigning CloudEvents Sequence extension ordering semantics to it.
- Constraints
  - OPTIONAL
  - If present, MUST be a canonical unsigned decimal representation in the
    range `0` to `4294967295`, inclusive, with no leading zero except for `0`.
  - In combination with the WoT profile, REQUIRED for keyframe, deltaframe
    and event messages.
  - MUST map to the Data Set Message Header `SequenceNumber`. The
    [OPC UA JSON mapping][UA DataSetWriterName] defines this field as `UInt32`;
    the String representation retains the full range of that value.
  - MUST NOT be interpreted as a source-wide sequence unless it also
    independently satisfies the Sequence extension's requirements.

## General Constraints

- OPC UA messages MUST use `binary-mode` of CloudEvents.
- OPC UA PubSub JSON messages MUST be encoded using non-reversible encoding as
the decoding information is contained in metadata messages or by schema
referenced via `dataschema` attribute.
- Payload of OPC UA PubSub JSON messages MUST NOT contain Network Message Header
and Data Set Header as that information is mapped into CloudEvents attributes.
- OPC UA PubSub JSON messages MUST contain exactly one dataset message.

## Examples

### Metadata message

The metadata message helps Cloud applications to understand the semantics and
structure of dataset messages.

```text
------------------ PUBLISH -------------------

Topic Name: opcua/json/DataSetMetaData/publisher-on-ot-edge
Content Type: application/json; charset=utf-8

------------- User Properties ----------------

specversion: 1.0
type: ua-metadata
time: 2024-03-28T21:56:24Z
id: 1234-1234-1234
source: urn:factory:aggregationserver:opcua
datacontenttype: application/json; charset=utf-8
subject: energy-consumption-asset
       .... further attributes ...

------------------ payload -------------------

{
    ... application data (OPC UA PubSub metadata) ...
    "ConfigurationVersion": {
      "MajorVersion": 672338910,
      "MinorVersion": 672341762
    }
    ...
}

-----------------------------------------------
```

### Telemetry message

The telemetry or data messages contain values of all OPC UA nodes that had
changed in a given period of time (`ua-deltaframe`) or contain values for all
OPC UA nodes that were monitored (`ua-keyframe`).
The complete list of monitored OPC UA nodes as well as the related type
information are defined in the metadata message. The attributes
`opcuametadatamajorversion` and `opcuametadataminorversion` are used to
reference the correct metadata message. The `ua-deltaframe` messages will be
used for hot and/or cold path processing and `ua-keyframe` messages can
additional be used to update last-known-value tables.


```text
------------------ PUBLISH -------------------

Topic Name: opcua/json/DataSetMessage/publisher-on-ot-edge
Content Type: application/json; charset=utf-8

------------- User Properties ----------------

specversion: 1.0
type: ua-deltaframe
time: 2024-03-28T21:56:42Z
id: 1235-1235-1235
source: urn:factory:aggregationserver:opcua
datacontenttype: application/json; charset=utf-8
subject: energy-consumption-asset
sequence: 0000000007
traceparent: 4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-00000011
recordedtime: 2024-03-28T21:56:43Z
opcuametadatamajorversion: 672338910
opcuametadataminorversion: 672341762
       .... further attributes ...

------------------ payload -------------------

{
    ... application data
        (OPC UA PubSub JSON single dataset Message)...
}

-----------------------------------------------
```

#### OPC UA PubSub JSON single dataset Message

Using CloudEvents and model the OPC UA PubSub header information as CloudEvent
attributes enables integration into various system (independent from used
protocols) and simplifies the payload structure.

```text
{
    "IsRunning": {
        "Value": true,
        "SourceTimestamp": "2024-03-29T07:31:19.555Z"
    },
    "EnergyConsumption": {
        "Value": 31
        "SourceTimestamp": "2024-03-29T07:31:37.546Z",
        "StatusCode": {
            "Code":1073741824,
            "Symbol":"Uncertain"
        }
    },
    "EnergyPeak": {
        "Value": 54
        "SourceTimestamp": "2024-03-29T07:31:06.978Z"
    },
    "EnergyLow": {
        "Value": 22
        "SourceTimestamp": "2024-03-29T07:31:17.582Z"
    }
}

```

### Event message

The event message will contain a single event and the identifier of this event is
added to the `subject` to allow routing it into different systems without parsing
the payload. Events are routed for example in systems like Manufacturing Execution
Systems (MES), Supervisory Control and Data Acquisition systems (SCADA),
Alerting Systems or Operation Technology Operator Terminals (HMI Clients) and
also in hot and/or cold path processing. The attributes
`opcuametadatamajorversion` and `opcuametadataminorversion` are used to
reference the correct metadata message.

```text
------------------ PUBLISH -------------------

Topic Name: opcua/json/DataSetMessage/publisher-on-ot-edge
Content Type: application/json; charset=utf-8

------------- User Properties ----------------

specversion: 1.0
type: ua-event
time: 2024-03-28T21:57:01Z
id: 1236-1237-1238
source: urn:factory:aggregationserver:opcua
datacontenttype: application/json; charset=utf-8
subject: energy-consumption-asset/444321
sequence: 0000000018
traceparent: caffef3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-00000011
recordedtime: 2024-03-28T21:57:01Z
opcuametadatamajorversion: 672338910
opcuametadataminorversion: 672341762
       .... further attributes ...

------------------ payload -------------------

{
    ... application data
        (OPC UA PubSub JSON Single Event Message)...
}

-----------------------------------------------
```

### Telemetry message with different Encoding

One major benefit of CloudEvents for OPC UA is that it is possible to support
other encoding and external schema, while keeping the same OPC UA information for
routing.

The example below uses Avro binary encoded payload, with the corresponding schema
referenced by `dataschema`. The `source` will be defined by an customer defined
hierarchical path.

```text
------------------ PUBLISH -------------------

Topic Name: bottling-company/amsterdam/FillingArea1/FillingLine9/Cell1/Conveyor
Content Type: application/avro

------------- User Properties ----------------

specversion: 1.0
type: ua-keyframe
time: 2024-03-28T23:59:59Z
id: 6235-7235-8235
source: bottling-company/amsterdam/FillingArea1/FillingLine9/Cell1/Conveyor
datacontenttype: application/avro
subject: energy-consumption-asset
dataschema: http://example.com/schemas/energy-consumption-asset/v1.8
sequence: 0000003141
traceparent: 22222f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-00000011
recordedtime: 2024-03-28T23:59:59Z
       .... further attributes ...

------------------ payload -------------------

    ... application data
        (OPC UA PubSub Single DataSet Message as AVRO binary)...

-----------------------------------------------
```

### WoT and OPC UA telemetry message

This binary-mode keyframe uses the WoT event type and affordance subject while
retaining the native OPC UA message type, writer identity, and sequence
number. The DataSetWriter name is used without a numeric writer ID. The
example assumes that `PumpProcessData` uniquely identifies a writer within
publisher `UInt16:12`. The CloudEvents `sequence` attribute is absent because
this example does not define a source-wide ordering across DataSetWriters.

```text
------------------ PUBLISH -------------------

Topic Name: opcua/json/DataSetMessage/pump
Content Type: application/json

------------- User Properties ----------------

specversion: 1.0
id: ua-message-25460
source: https://factory.example.com/line1?wotid=urn:example:pump:7;wotversion=3.0.0;site=north
type: com.example.models.tm.pump.properties.processData.v1
subject: #/properties/processData
time: 2026-10-29T12:00:00Z
dataschema: https://example.com/schemas/pump-process-data/versions/3
opcuapublisherid: UInt16:12
opcuadatasetwritername: PumpProcessData
opcuamessagetype: ua-keyframe
opcuasequence: 4294967295

------------------ payload -------------------

{
  "Speed": 1500,
  "Pressure": 4.5
}

-----------------------------------------------
```

[UA DataSetWriterName]: https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table185
[UA SequenceNumber]: https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.3
