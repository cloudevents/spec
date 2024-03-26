# OPC UA

This extension defines the mapping of OPC UA dataset to cloud events to allow seamless routing of OPC UA dataset messages via different protocols, it therefor provides an recommendation to map known mandatory and optional attributes using other extensions as well as defines own extended attributes.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is
used. For example, an attribute being marked as "REQUIRED" does not mean
it needs to be in all CloudEvents, rather it needs to be included only when 
this extension is being used.

## Mapping of REQUIRED Attributes

### id

MUST map to [Network Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.3#Table163) field `MessageId`.

### source

MUST either map to [Application Description](https://reference.opcfoundation.org/Core/Part4/v104/docs/7.1) field `applicationUri` of the OPC UA server or to an customer configured identifier like an unified namespace path.

### type

MUST map to [Network Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.3#Table163) field `MessageType`.

## Mapping of OPTIONAL Attributes

### datacontenttype

SHALL be `application/opcua+json` for OPC UA PubSub JSON payload and MAY be extended by `+gzip` when payload is gzip compressed.

### dataschema

OPC UA provides type information as part of PubSub metadata messages, for non OPC UA consumers or when different payload encoding like Avro is used, it is required to provide schema information (based on metadata information) in a separate format like [JSON schema](https://json-schema.org/specification) or [Avro schema](https://avro.apache.org/docs/1.11.1/specification/) or others. For those cases the Attribute references the schema and is used for versioning.

### subject

For metadata and data messages (type one of `ua-metadata`, `ua-keyframe`, `ua-deltaframe`) MUST map to either [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `DataSetWriterId` or `DataSetWriterName`.

For event messages (type equals to `ua-event`) SHALL map to [Base Event Type](https://reference.opcfoundation.org/Core/Part5/v104/docs/6.4.2) field `EventId`. 

### time

MUST map to [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `Timestamp`.

## Mapping for other extensions

The following well-known extensions attributes are used for data messages and event messages (type one of `ua-keyframe`, `ua-deltaframe`, `ua-event`).

### sequence

Attribute as defined by [sequence extensions](./sequence.md) MUST map to [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `SequenceNumber`.

### traceparent

Attribute as defined by [distributed-tracing extension](./distributed-tracing.md) SHALL be used to allow tracing from event publisher towards consumer.

### tracestate

Attribute as defined by [distributed-tracing extension](./distributed-tracing.md) might OPTIONAL be used to allow tracing from event publisher towards consumer.

### recordedtime

Attribute as defined by [recordedtime extension](./recordedtime.md) SHALL be used to determine the latency between event publisher towards consumer. 

## Attributes

### opcuametadatamajorversion

- Type: `Integer`
- Description: Links dataset message to the current version of the metadata. Contains value from `MajorVersion` of [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `MetaDataVersion`. 
- Constraints
  - OPTIONAL
  - Can be omitted if `dataschema` is used

### opcuametadataminorversion

- Type: `Integer`
- Description: Links dataset message to the current version of the metadata. Contains value from `MiniorVersion` of [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `MetaDataVersion`.
- Constraints
  - OPTIONAL
  - Can be omitted if `dataschema` is used

### opcuastatus

- Type: `Integer`
- Description: Defines the overall status of the data set message, maps to [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `Status`.
- Constraints
  - OPTIONAL
  - Can be omitted if status is _Good_

## General Constraints

- OPC UA messages MUST use `binary-mode` of Cloud Events.
- OPC UA PubSub JSON messages MUST be encoded using non-reversible encoding as the decoding information are contained in metadata messages or by schema referenced via `dataschema` attribute.
- Payload of OPC UA PubSub JSON messages MUST NOT contain Network Message Header and Data Set Header as those information are mapped into Cloud Events attributes.
