# OPC Unified Architecture CloudEvents Adapter

This document describes how to convert [OPC UA](https://reference.opcfoundation.org/Core/Part1/v105/docs/) [PubSub](https://reference.opcfoundation.org/Core/Part14/v105/docs/) dataset into CloudEvents.

All OPC UA events are converted into CloudEvents using the same pattern as described in the following table:

## Common Mapping

| CloudEvents Attribute | Value | Remark                                            |
| :-------------------- | :----------------------------------------------| :-------------------- |
| `id`                  | `MessageId` mapped from [Network Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.3#Table163) | |
| `source`              | `applicationUri` of the OPC UA server mapped from [Application Description](https://reference.opcfoundation.org/Core/Part4/v104/docs/7.1)  | Alternatively a customer configured identifier like a unified namespace path |
| `type`                | `MessageType` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164).         |
| `datacontenttype`     | `application/json` for OPC UA PubSub JSON payload. | MAY be appended with `+gzip` when the payload is gzip compressed.         |
| `dataschema`          | OPC UA provides type information as part of PubSub metadata messages. | For non OPC UA consumers or when different payload encoding like Avro is used, it is REQUIRED to provide schema information (based on metadata information) in a separate format like [JSON schema](https://json-schema.org/specification) or [Avro schema](https://avro.apache.org/docs/1.11.1/specification/) or others.                                             |
| `time`                | `Timestamp` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)                                | |
| `data`                | content of the OPCUA  event                                        | |
| `opcuametadatamajorversion` |  `MajorVersion` in MetaDataVersion field mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) | |
| `opcuametadataminorversion` | `MinorVersion` in MetaDataVersion field mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) | |
| `opcuastatus` | `Status` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)                                | |

## Message specific Mapping

### Metadata

A metadata message is indicated by setting the type property to  `ua-metadata`

| CloudEvents Attribute | Value | Remark                                            |
| :-------------------- | :----------------------------------------------| :-------------------- |
| `subject`             | `DataSetWriterId` or `DataSetWriterName` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164). | |

### Keyframe

A keyframe message is indicated by setting the type property to  `ua-keyframe`

| CloudEvents Attribute | Value | Remark                                            |
| :-------------------- | :----------------------------------------------| :-------------------- |
| `subject`             | `DataSetWriterId` or `DataSetWriterName` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164).                            | |
| `sequence`            | `SequenceNumber` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) | Attribute as defined by [sequence extensions](./../extensions/sequence.md) |
| `traceparent`            | | Attribute as defined by [distributed-tracing extension](./../extensions/distributed-tracing.md) to allow tracing from event publisher towards consumer. |
| `tracestate`            | | Attribute as defined by [distributed-tracing extension](./../extensions/distributed-tracing.md) MAY be used to allow tracing from event publisher towards consumer. |
| `recordedtime`            | | Attribute as defined by [recordedtime extension](./../extensions/recordedtime.md) to determine the latency between event publisher towards consumer. |

### Deltaframe

A deltaframe message is indicated by setting the type property to  `ua-deltaframe`

| CloudEvents Attribute | Value | Remark                                            |
| :-------------------- | :----------------------------------------------| :-------------------- |
| `subject`             | `DataSetWriterId` or `DataSetWriterName` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164).                            | |
| `sequence`            | `SequenceNumber` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) | Attribute as defined by [sequence extensions](./../extensions/sequence.md) |
| `traceparent`            | | Attribute as defined by [distributed-tracing extension](./../extensions/distributed-tracing.md) to allow tracing from event publisher towards consumer. |
| `tracestate`            | | Attribute as defined by [distributed-tracing extension](./../extensions/distributed-tracing.md) MAY be used to allow tracing from event publisher towards consumer. |
| `recordedtime`            | | Attribute as defined by [recordedtime extension](./../extensions/recordedtime.md) to determine the latency between event publisher towards consumer. |

### Event

An event message is indicated by setting the type property to `ua-event`

| CloudEvents Attribute | Value | Remark                                            |
| :-------------------- | :----------------------------------------------| :-------------------- |
| `subject`             | `DataSetWriterId` or `DataSetWriterName` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164).                            | |
| `sequence`            | `SequenceNumber` mapped from [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) | Attribute as defined by [sequence extensions](./../extensions/sequence.md) |
| `traceparent`            | | Attribute as defined by [distributed-tracing extension](./../extensions/distributed-tracing.md) to allow tracing from event publisher towards consumer. |
| `tracestate`            | | Attribute as defined by [distributed-tracing extension](./../extensions/distributed-tracing.md) MAY be used to allow tracing from event publisher towards consumer. |
| `recordedtime`            | | Attribute as defined by [recordedtime extension](./../extensions/recordedtime.md) to determine the latency between event publisher towards consumer. |

## General Constraints

- OPC UA messages MUST use `binary-mode` of CloudEvents.
- OPC UA PubSub JSON messages MUST be encoded using non-reversible encoding as the decoding information is contained in metadata messages or by schema referenced via `dataschema` attribute.
- Payload of OPC UA PubSub JSON messages MUST NOT contain Network Message Header and Data Set Header as that information is mapped into CloudEvents attributes.
- OPC UA PubSub JSON messages MUST contain exactly one dataset message.

## Examples

### Metadata message

The metadata message helps Cloud applications to understand the semantics and structure of dataset messages.

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

The telemetry or data messages contain values of all OPC UA nodes that had changed in a given period of time (`ua-deltaframe`) or contain values for all OPC UA nodes that were monitored (`ua-keyframe`). The complete list of monitored OPC UA nodes as well as the related type information are defined in the metadata message. The attributes `opcuametadatamajorversion` and `opcuametadataminorversion` are used to reference the correct metadata message. The `ua-deltaframe` messages will be used for hot and/or cold path processing and `ua-keyframe` messages can additional be used to update last-known-value tables.

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
sequence: 7
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

Using CloudEvents and model the OPC UA PubSub header information as CloudEvent attributes enables integration into various system (independent from used protocols) and simplifies the payload structure.

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

The event message will contain a single event and the identifier of this event is added to the `subject` to allow routing it into different systems without parsing the payload. Events are routed for example in systems like Manufacturing Execution Systems (MES), Supervisory Control and Data Acquisition systems (SCADA), Alerting Systems or Operation Technology Operator Terminals (HMI Clients) and also in hot and/or cold path processing. The attributes `opcuametadatamajorversion` and `opcuametadataminorversion` are used to reference the correct metadata message.

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
sequence: 18
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

One major benefit of CloudEvents for OPC UA is that it is possible to support other encoding and external schema, while keeping the same OPC UA information for routing.

The example below uses Avro binary encoded payload, with the corresponding schema referenced by `dataschema`. The `source` will be defined by an customer defined hierarchical path.

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
sequence: 3141
traceparent: 22222f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-00000011
recordedtime: 2024-03-28T23:59:59Z
       .... further attributes ...

------------------ payload -------------------

    ... application data 
        (OPC UA PubSub Single DataSet Message as AVRO binary)...

-----------------------------------------------
```
