# OPC UA

This extension maps [OPC UA](https://reference.opcfoundation.org/Core/Part1/v105/docs/)
[PubSub](https://reference.opcfoundation.org/Core/Part14/v105/docs/)
DataSetMessages to CloudEvents for routing over supported protocols. It defines
mappings for Core and other extension attributes and specifies OPC UA extension
attributes.

When used with the [Descriptor Reference extension](describedby.md) and the
xRegistry Descriptor model, metadata that stays constant for a message stream is
preferably stored in the selected Descriptor rather than repeated in each event.
The existing OPC UA attributes remain defined and usable. A Producer MUST supply
publisher and writer metadata REQUIRED by this mapping in the `source` query
when neither the full Part 14 NetworkMessage envelope nor the selected
Descriptor supplies it. The [shared metadata
rules](#shared-stream-metadata-in-a-descriptor) describe how a Consumer obtains
these values. A direct WoT TD subject can identify its description without a
Descriptor, but does not supply these native identities.

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

An OPC UA Producer MAY identify the server using its [Application
Description](https://reference.opcfoundation.org/Core/Part4/v104/docs/7.1) field
`applicationUri` or a customer-configured identifier such as a unified namespace
path. For data and event messages, a Producer MUST include each publisher or
writer query parameter REQUIRED by the mapping unless the full OPC UA Part 14
NetworkMessage envelope or the Descriptor supplies its corresponding value.

### type

An OPC UA Producer MAY map `type` to the
[Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `MessageType`. A Producer using the WoT profile MUST follow its semantic
event-type rules. When the `type` identifies a WoT event contract, a Producer
MUST carry the native `MessageType` as `opcuamessagetype` when `data` omits
that field from the DataSetMessage header. When a retained NetworkMessage
envelope includes the field, the Producer MUST NOT repeat it as an event
attribute. The [WoT mapping section](#wot-mapping) specifies the combined
mapping.

### WoT mapping

When a CloudEvent uses both this extension and the
[WoT profile](./wot.md), the following mappings apply to data and event
messages:

- `type` MUST follow the WoT profile's semantic event-type rules instead of
  mapping to the native `MessageType`.
- `subject` MUST follow the WoT profile's Descriptor-relative or direct-TD
  subject rules.
- The native PublisherId and at least one DataSetWriter identifier MUST be
  available from the full Part 14 NetworkMessage envelope, `source`, or the
  selected Descriptor, as defined in [Publisher and Writer
  Metadata](#publisher-and-writer-metadata).
- Nothing MUST be appended to `subject`. For an event message, the `EventId`
  remains in the OPC UA event payload.
- `opcuasequence` MUST carry the native `SequenceNumber`. The CloudEvents
  `sequence` attribute, when present, MUST satisfy the independent ordering
  requirements of the Sequence extension and MUST NOT be inferred from
  `opcuasequence`.

The [publisher and writer metadata rules](#publisher-and-writer-metadata)
define how OPC UA publisher and writer identifiers are supplied. The Core
attribute mappings above remain unchanged.

These conditional mappings replace only the conflicting OPC UA mappings above.
All other requirements in this extension remain applicable. A profile that
uses only part of this extension MUST NOT claim conformance to it unless the
profile satisfies every applicable requirement in this document.

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

When the Descriptor Reference selection rules are used, a Producer MAY select a
Descriptor whose schema Reference or Message definition supplies this schema
instead. The Consumer follows that extension's [schema
precedence](describedby.md#message-and-schema-selection), including its selector
and ambiguity rules. The Producer SHOULD omit `dataschema` when the selected
Descriptor supplies the schema. The selected schema MUST describe the actual
`data`, including the full NetworkMessage envelope when one is retained.

### subject

For metadata, data, and event messages, a Producer MAY map `subject` to
`DataSetWriterId` or `DataSetWriterName` from the [Data Set Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164).
A Producer using the WoT profile MUST instead follow its Descriptor-relative or
direct-TD subject mapping.

For an OPC UA event message (`type` equals `ua-event`), a Producer using the
OPC UA-specific `subject` mapping MUST append "/" and the
[Base Event Type](https://reference.opcfoundation.org/Core/Part5/v104/docs/6.4.2)
field `EventId`.

### time

MUST map to [Data Set Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `Timestamp`.

## Mapping for other extensions

The following well-known extension attributes apply to data and event
messages. When the WoT profile is used, determine the native message type
from `opcuamessagetype` when present or from the retained NetworkMessage's
DataSetMessage header when it contains `MessageType`.

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

### opcuamessagetype

- Type: `String`
- Description: Carries the OPC UA PubSub DataSetMessage type when the
  DataSetMessage header is omitted from `data`.
- Constraints
  - OPTIONAL
  - In combination with the WoT profile, the value is REQUIRED for data and
    event messages when `data` omits the DataSetMessage header.
  - MUST NOT be present when `data` retains a full NetworkMessage envelope
    that includes the DataSetMessage `MessageType`.
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

## Publisher and Writer Metadata

The following values identify the OPC UA Publisher and DataSetWriter. They are
not CloudEvents extension attributes. A Producer MUST supply each REQUIRED value
as a query parameter in `source` or an extension attribute of the applicable
Descriptor Version unless the full Part 14 NetworkMessage envelope supplies it.
The names are the same in the query and Descriptor representations.

| Name | Value |
| --- | --- |
| `opcuapublisherid` | The native PublisherId, represented as a string. |
| `opcuadatasetwriterid` | The native DataSetWriterId, represented as an integer. |
| `opcuadatasetwritername` | The configured DataSetWriterName, represented as a string. |

In a full [Part 14 NetworkMessage][UA NetworkMessage], the Consumer obtains the
PublisherId from the NetworkMessage header and the DataSetWriterId or
DataSetWriterName from its single DataSetMessage header. Those fields retain
their native names and encodings. The following representation rules apply to
their equivalents in `source` and the Descriptor.

`opcuapublisherid` MUST use `<BuiltInType>:<value>`. The type MUST be `Byte`,
`UInt16`, `UInt32`, `UInt64`, or `String`, as defined for the native
[PublisherId][UA PublisherId]. For an unsigned integer type, the value MUST be
the nonzero unsigned decimal representation within that type's range, without
a sign or leading zeros. For `String`, the value MUST be the unpadded base64url
encoding of the non-empty PublisherId's UTF-8 bytes. If the message encoding
does not preserve the PublisherId's type, the Producer obtains it from
configuration. If the type cannot be determined, the Producer MUST report an
error rather than assign one.

`opcuadatasetwriterid` MUST map to the native DataSetWriterId. It MUST be in
the range 1 to 65535, inclusive; [OPC UA reserves zero][UA DataSetWriterId]
as a null value.
`opcuadatasetwritername` MUST be non-empty and match the DataSetWriter's
configured name. For JSON message mapping, this is the
[`DataSetWriterName` field][UA DataSetWriterName] when present in the
DataSetMessage; otherwise the Producer obtains it from configuration.

The native PublisherId and at least one of DataSetWriterId and DataSetWriterName
are REQUIRED for all data and event messages, whether or not the WoT profile is
used. Each value MUST be supplied by the envelope or by the corresponding query
parameter or Descriptor attribute. A full envelope that omits an identifier does
not satisfy that identifier's presence requirement. If both writer values are
supplied, they MUST identify the same DataSetWriter. A writer name MUST uniquely
identify the DataSetWriter within the PublisherId scope. Consumers MUST compare
names exactly, without case folding or Unicode normalization.

When an identity is supplied in more than one place, the representations MUST
identify the same native Publisher or DataSetWriter. To compare a query or
Descriptor value with an envelope field, the Consumer MUST decode that value and
apply the field's native Part 14 encoding. For example, `UInt16:12` is encoded
as `"12"` in a JSON NetworkMessage. The Consumer MUST report a metadata conflict
and MUST NOT interpret the payload as a conforming OPC UA message if the values
disagree.

A Consumer MUST report invalid metadata and MUST NOT interpret the payload as
a conforming OPC UA message if a supplied publisher or writer value violates
these representation or range constraints.

### Source query syntax

When these values are supplied in `source`, the query parameters carry
stream-constant metadata. The Producer SHOULD omit a query parameter when the
full OPC UA Part 14 NetworkMessage envelope or the selected Descriptor supplies
its value. For each REQUIRED publisher or writer value that neither supplies,
the Producer MUST include the corresponding parameter in `source`.

The Producer MUST use `name=value` for each of these parameters, with a
non-empty value. It MUST separate them from each other and from preceding
query content with `;`, and place the query before any URI fragment. The three
names are case-sensitive and MUST appear literally, at most once each. Other
parameters MAY appear in any order; a Consumer MUST NOT reject the source
solely because it contains parameters not defined by this extension.

For these parameter values, the unescaped characters are the [RFC 3986][URI]
`unreserved` characters and `!`, `$`, `'`, `(`, `)`, `*`, `,`, `:`, `@`,
`/`, and `?`. A Producer MUST leave these characters unescaped and
percent-encode the UTF-8 bytes of all other characters using uppercase
hexadecimal digits. In particular, a literal `%`, `;`, `=`, `&`, `+`, or `#`
MUST be encoded. A Producer MUST NOT use form-query encoding or encode a space
as `+`.

A Consumer MUST split the query at `;` before decoding these values. It MUST
reject an empty or duplicate recognized parameter, an invalid percent escape,
invalid UTF-8, or an unescaped character outside the permitted set. It MUST
percent-decode each value exactly once and MUST NOT interpret `+` as a space.
The writer ID uses unsigned decimal notation without a sign or leading zeros in
the query and an integer in the Descriptor; the other two values use strings in
both places.

For example, the following source supplies the PublisherId and writer name when
neither the envelope nor the Descriptor supplies them. The writer name is
`Pump&Process`.

```text
mqtt://site/line/cell/device/sensor?opcuapublisherid=UInt16:12;opcuadatasetwritername=Pump%26Process;site=north
```

Changing `source`, including its query parameters, changes the CloudEvents
event-identity and [Sequence extension](sequence.md) scope. A Producer MUST
NOT reuse event identities or restart a claimed source-wide sequence when it
returns to a previously used `source`.

## General Constraints

- OPC UA messages MUST use `binary-mode` of CloudEvents.
- OPC UA PubSub JSON messages MUST be encoded using non-reversible encoding as
the decoding information is contained in metadata messages or by schema
referenced via `dataschema` attribute or selected through a Descriptor.
- A Producer MAY retain the full Part 14 NetworkMessage envelope in `data`.
  Otherwise, the payload MUST omit the NetworkMessage and DataSetMessage
  headers and supply their applicable information through the mappings in
  this extension.
- OPC UA PubSub JSON messages MUST contain exactly one DataSetMessage,
  including when a full NetworkMessage envelope is retained.

A retained envelope does not replace the REQUIRED CloudEvents attributes or
the per-event `opcuasequence` attribute when the WoT mapping applies.
`opcuamessagetype` is REQUIRED only when `data` omits the DataSetMessage
header; when the envelope includes that field, the attribute MUST be absent.
The NetworkMessage's `ua-data` type is not the DataSetMessage type. Any
duplicated native values MUST agree after applying the specified mappings.
The Consumer MUST report a conflict and MUST NOT interpret a message as
conforming to this extension when they disagree.

## Shared Stream Metadata in a Descriptor

A message stream here is a configured flow from one Publisher and
DataSetWriter with a defined payload contract. It is not necessarily a broker
topic or a CloudEvents `source`; either can carry several streams.

When Producers and Consumers agree to use this extension with the [Descriptor
Reference selection rules](describedby.md#one-selected-processing-description),
the Publisher SHOULD store metadata that is constant for the stream as
Descriptor Version extension attributes. The agreed binding selects the
Descriptor through `describedby` or a profile-defined source or subject mapping.
Storing stream-constant values once avoids repeating them in event attributes or
the `source` query. The Descriptor has no document body: these values are
members of its metadata object, alongside `references`.

The Publisher MAY store the following values in the Descriptor when they remain
constant for every event using that Version. When a Descriptor supplies any of
these values, its selected URL MUST identify a Descriptor Version, whether
selected explicitly or through a profile-defined mapping. A Resource URL can
select a different default Version when a delayed or replayed event is
processed.

| Descriptor attribute | Meaning and conditions |
| --- | --- |
| `opcuapublisherid` | The stream's native PublisherId. |
| `opcuadatasetwriterid` | The stream's native DataSetWriterId, when used. |
| `opcuadatasetwritername` | The stream's configured DataSetWriterName, when used. |
| `opcuadatasetname` | The non-empty `Name` of the applicable DataSet metadata; descriptive, not a writer identifier. |
| `opcuametadatamajorversion` | The MajorVersion of the applicable native metadata, when no payload schema is selected. |
| `opcuametadataminorversion` | The MinorVersion of the applicable native metadata, when no payload schema is selected. |

Publisher, writer and metadata-version members MUST use the constraints and
mappings defined in [Attributes](#attributes) and [Publisher and Writer
Metadata](#publisher-and-writer-metadata). For example, a Descriptor's
`opcuadatasetwriterid` is a JSON integer, not a string. The Descriptor's
selected schema Reference identifies an external payload schema. Native
metadata-version attributes MUST NOT be supplied in the event or Descriptor when
a schema is selected through `dataschema` or the Descriptor.

`opcuadatasetname` is an OPTIONAL Descriptor attribute, not a new CloudEvents
attribute or source query parameter. If supplied, it MUST be a non-empty String
equal to `DataSetMetaDataType.Name` in the applicable [DataSet metadata][UA
DataSet Metadata], obtained from that metadata or its approved configuration. A
Producer MUST NOT infer it from a writer name, topic or TD affordance name. It
need not be unique and MUST NOT substitute for a REQUIRED PublisherId or
DataSetWriter identity. Repeated dataset-name representations, when the profile
supplies them, MUST compare exactly without case folding or Unicode
normalization. A mismatch is a metadata conflict. This attribute does not permit
removal of native fields REQUIRED by the selected encoding.

For the listed values, an applicable Descriptor satisfies this extension's
presence requirements for the corresponding field, including those of the
combined WoT mapping. The dataset name satisfies no publisher or writer identity
requirement. A Producer MAY omit the corresponding event attribute or source
query parameter. Other event attributes, including `opcuamessagetype`, MUST NOT
be replaced by Descriptor members.

If a publisher or writer value appears in both the `source` query and the
Descriptor, the values MUST agree after decoding and type conversion. If an
event attribute and the Descriptor both supply a metadata version, their typed
values MUST agree. The same consistency requirement applies to publisher and
writer identities retained in the envelope. On a conflict, the Consumer MUST
report a metadata conflict and MUST NOT interpret the payload as a conforming
OPC UA message. If a REQUIRED value is absent from all applicable locations, the
Consumer MUST report missing metadata and MUST NOT interpret the payload as a
conforming OPC UA message.

A Consumer MUST use only the Descriptor selected by the agreed binding. If
`describedby` is present, missing values MUST NOT be taken from a source or
subject description. If its Descriptor cannot be retrieved, the Consumer MAY
interpret the native payload using the envelope, source query and explicit event
attributes when they supply every native requirement, but MUST NOT report
successful Descriptor-based interpretation or WoT correlation. The WoT profile's
explicit-link failure rules still apply.

Without `describedby`, the revised WoT profile can select a direct TD subject
without a Descriptor. Native publisher and writer requirements then have to be
satisfied by the retained envelope or the existing source query. A direct TD
MUST NOT be treated as a source of missing OPC UA metadata. Consumers MUST NOT
retrieve a source Descriptor as an implicit supplement.

The Descriptor Publisher MUST NOT change these values in a Descriptor Version
after any Producer is configured with its URL. A change requires a new
Descriptor Version and reconfigured Producers. Consumers MUST NOT retain values
from a previous Descriptor when processing an event that selects another
Descriptor. A changed payload contract also requires a changed WoT `type`
revision when that profile is used; changing only `describedby` is not
sufficient.

Values that vary by occurrence remain in each event. In particular,
`opcuamessagetype`, `opcuasequence`, `opcuastatus` when REQUIRED, `id`, and
`time` MUST NOT be supplied by the Descriptor as replacements for their event
attributes. Tracing, recording times, and a CloudEvents `sequence`, when used,
also remain in the event. A Consumer MUST NOT use Descriptor members with those
names as event values. Core attributes retain their normal placement and meaning
even when their values happen to be constant for a stream.

When the agreed route selects no Descriptor, the Producer MUST supply all
REQUIRED OPC UA values through the other locations defined above. An absent
`describedby` alone does not determine whether a Descriptor was selected.
Producers SHOULD use Descriptor metadata only when the intended Consumers
support the agreed mapping.

When `source` is itself a Descriptor URL, Producers SHOULD supply shared
identity metadata in the selected versioned Descriptor instead of appending
query parameters to that URL. Appending a query changes the event's source
identity and can change the retrieved resource. Consumers MUST NOT strip a query
to make source-based retrieval work.

## Examples

The examples preceding the WoT section use publisher `UInt16:12` and writer name
`energy-consumption-asset`. Their payloads omit the native headers, so their
`source` queries supply both identifiers.

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
source: https://factory.example.com/aggregationserver/opcua?opcuapublisherid=UInt16:12;opcuadatasetwritername=energy-consumption-asset
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
source: https://factory.example.com/aggregationserver/opcua?opcuapublisherid=UInt16:12;opcuadatasetwritername=energy-consumption-asset
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
source: https://factory.example.com/aggregationserver/opcua?opcuapublisherid=UInt16:12;opcuadatasetwritername=energy-consumption-asset
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
source: bottling-company/amsterdam/FillingArea1/FillingLine9/Cell1/Conveyor?opcuapublisherid=UInt16:12;opcuadatasetwritername=energy-consumption-asset
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

This binary-mode keyframe uses the WoT event type and named affordance subject.
Its Descriptor supplies the resolved TD, payload schema, PublisherId,
DataSetWriter identity and dataset name. The native OPC UA message type and
sequence remain in the event because they can vary within this stream. The
example uses writer ID `17` within publisher `UInt16:12`. The CloudEvents
`sequence` attribute is absent because this example does not define a
source-wide ordering across DataSetWriters.

```text
------------------ PUBLISH -------------------

Topic Name: opcua/json/DataSetMessage/pump
Content Type: application/json

------------- User Properties ----------------

specversion: 1.0
id: ua-message-25460
source: https://registry.example/descriptorgroups/devices/descriptors/pump7
type: com.example.models.tm.pump.properties.processData.v1
subject: pump7#/properties/processData
time: 2026-10-29T12:00:00Z
describedby: https://registry.example/descriptorgroups/streams/descriptors/pump7-telemetry/versions/1
opcuamessagetype: ua-keyframe
opcuasequence: 4294967295

------------------ payload -------------------

{
  "Speed": 1500,
  "Pressure": 4.5
}

-----------------------------------------------
```

The referenced Descriptor Version has the following metadata. Other Core
metadata is omitted from this excerpt.

```json
{
  "descriptorid": "pump7-telemetry",
  "versionid": "1",
  "schemaref": "payload",
  "references": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3",
      "planurl": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7-plan/versions/3"
    },
    "gateway1": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/gateway1/versions/1"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/pump-process-data/versions/3"
    },
    "geometry": {
      "class": "usdasset",
      "url": "https://assets.example/usdassetgroups/line1/usdassets/pump7/versions/2"
    }
  },
  "opcuapublisherid": "UInt16:12",
  "opcuadatasetwriterid": 17,
  "opcuadatasetwritername": "pump7-process",
  "opcuadatasetname": "PumpProcessData"
}
```

The Consumer uses the selected Descriptor's PublisherId and writer identity with
the event's `opcuamessagetype` and `opcuasequence`. The subject's `pump7` prefix
selects the TD among two candidates; `schemaref` selects the payload schema. The
dataset name and writer name deliberately differ.

With an agreed source-Descriptor binding, a Producer can instead use the
stream's Descriptor Version URL as `source` and omit `describedby`. This changes
the source identity; it is not an identity-preserving rewrite of already
published events.

#### Direct TD subject with the NetworkMessage envelope

This event retains the full Part 14 NetworkMessage envelope. Its PublisherId
and DataSetWriterId satisfy the identity requirements, so `source` needs no
publisher or writer query parameters. Part 14 JSON encodes the configured
PublisherId `UInt16:12` as the string `"12"`.

The direct subject supplies the TD URL and affordance pointer; `dataschema`
supplies the envelope's schema. No Descriptor is REQUIRED, so `describedby` is
omitted. The event type uses revision `v2` because retaining the envelope
changes the payload contract.

```text
------------------ PUBLISH -------------------

Topic Name: opcua/json/DataSetMessage/pump
Content Type: application/json

------------- User Properties ----------------

specversion: 1.0
id: ua-message-25461
source: mqtt://site/line/cell/device/sensor?site=north
type: com.example.models.tm.pump.properties.processData.v2
subject: https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3#/properties/processData
time: 2026-10-29T12:00:01Z
dataschema: https://schemas.example/pump-process-data-envelope/versions/1
opcuasequence: 0

------------------ payload -------------------

{
  "MessageId": "ua-message-25461",
  "MessageType": "ua-data",
  "PublisherId": "12",
  "Messages": [
    {
      "DataSetWriterId": 17,
      "MessageType": "ua-keyframe",
      "SequenceNumber": 0,
      "Timestamp": "2026-10-29T12:00:01Z",
      "Payload": {
        "Speed": 1500,
        "Pressure": 4.5
      }
    }
  ]
}

-----------------------------------------------
```

The native sequence has rolled over from `4294967295` to `0`; it remains
`opcuasequence`, not a CloudEvents `sequence`. The subject selects its TD
directly without a source lookup. The DataSetMessage's `MessageType` remains in
the retained NetworkMessage envelope instead of being repeated as
`opcuamessagetype`.

## Descriptor Retrieval Security

The Descriptor Reference extension's retrieval, authorization and cache rules
apply to this mapping. Stable writer metadata in a Descriptor does not
authenticate the Publisher or authorize access to the referenced TD or schema. A
Consumer MUST establish trust in the Descriptor before using it as OPC UA
metadata.

[UA DataSetWriterName]: https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table185
[UA NetworkMessage]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/7.2.5.3
[UA DataSetWriterId]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/6.2.4.1
[UA PublisherId]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/6.2.7.1
[UA SequenceNumber]: https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.3
[UA DataSet Metadata]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/6.2.3.2.3
[URI]: https://www.rfc-editor.org/rfc/rfc3986
