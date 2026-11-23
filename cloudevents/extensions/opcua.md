# OPC UA

This extension lets a Consumer route
[OPC UA](https://reference.opcfoundation.org/Core/Part1/v105/docs/)
[PubSub](https://reference.opcfoundation.org/Core/Part14/v105/docs/)
messages using CloudEvents attributes. A DataSetWriter publishes a
DataSetMessage that carries measurements or an event. In this example,
the CloudEvents `type` identifies a keyframe and `subject` identifies its
writer. The Consumer has the OPC UA metadata for this stream. The HTTP
request uses CloudEvents binary mode:

```http
POST /events HTTP/1.1
Host: consumer.example
Content-Type: application/json
Content-Length: 16
ce-specversion: 1.0
ce-id: pump7-sample-1
ce-source: urn:example:pump7
ce-type: ua-keyframe
ce-subject: pump7-process
ce-time: 2026-10-29T12:00:00Z

{"Pressure":4.5}
```

When Consumers need metadata shared by a stream, the Producer can use
[`describedby`](descriptor.md#describedby) to point to a Descriptor. This
**Processing Descriptor** supplies shared inputs. For example, an inline
`opcuawriter` entry can carry publisher and writer identity:

```json
{
  "entries": {
    "writer": {
      "class": "opcuawriter",
      "opcuapublisherid": "UInt16:12",
      "opcuadatasetwriterid": 17
    }
  }
}
```

Values such as the event ID and time stay with each event. The
[OPC UA Descriptor profile](#opc-ua-descriptor-profile) defines the shared
fields. The [combined WoT mapping](#wot-mapping) covers events that also
use the Web of Things (WoT) profile.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is
used. For example, an attribute marked as "REQUIRED" needs to be included
when the event uses this extension and meets the stated conditions.

## Mapping of REQUIRED Attributes

### id

MUST map to [Network Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.3#Table163)
field `MessageId`.

### source

An OPC UA Producer MAY identify the server using its [Application
Description](https://reference.opcfoundation.org/Core/Part4/v104/docs/7.1) field
`applicationUri` or a customer-configured identifier such as a unified namespace
path. A Producer MAY include the query parameters defined in
[Publisher and Writer Metadata](#publisher-and-writer-metadata), subject to
that section's requirements for the combined WoT mapping.

### type

An OPC UA Producer MAY map `type` to the
[Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `MessageType`. For data and event messages without the WoT profile,
the Producer MUST use that native value as `type` when the DataSetMessage
`MessageType` field is absent from `data`. For a retained header, the
native content mask determines whether it carries that field.

A Producer using the WoT profile MUST instead follow its semantic
event-type rules and the [opcuamessagetype](#opcuamessagetype) requirements
for conveying the native message type. The [WoT mapping section](#wot-mapping)
specifies the combined mapping.

## Mapping of OPTIONAL Attributes

### datacontenttype

MUST be `application/json` for OPC UA PubSub JSON payload and MAY be appended with
`+gzip` when the payload is gzip compressed.

### dataschema

PubSub metadata messages carry type information. For non-OPC UA Consumers
or alternate encodings such as Avro, a schema based on that metadata is
REQUIRED, for example [JSON Schema](https://json-schema.org/specification)
or [Avro Schema](https://avro.apache.org/docs/1.11.1/specification/).
`dataschema` identifies and versions that schema.

A Processing Descriptor MAY supply the schema. The Consumer MUST use
`dataschema` when present. Otherwise, when a Processing Descriptor is
available, select its [schema entry][Schema Descriptor Profile] by the
name in the publication profile. If the profile supplies no name, select
the sole `schema` entry; zero entries means no schema, and multiple entries
are ambiguous. A named entry that is missing or has the wrong class is
invalid. Use the selected schema at its `url` or from its bundled
`document`.

The Consumer MUST report a missing REQUIRED schema. An ambiguous selection,
invalid selector, unavailable schema or unsupported format MUST NOT cause
fallback to another schema. If `dataschema` is present, the Consumer MUST
still validate applicable Descriptor selectors and use `dataschema` as the
sole schema input. Producers and Descriptor
publishers SHOULD supply one schema source or identify the same schema in
both. The Producer SHOULD omit `dataschema` when the Descriptor supplies
the schema. The selected schema MUST describe `data`, including the
NetworkMessage envelope if retained.

### subject

For metadata, data, and event messages, a Producer MAY map `subject` to
`DataSetWriterId` or `DataSetWriterName` from the [Data Set Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164).
A Producer using the WoT profile MUST instead follow its
[rules for `subject`](wot.md#subject).

For a native OPC UA event message (`MessageType` equals `ua-event`), a
Producer using the OPC UA-specific `subject` mapping MUST append "/" and the
[Base Event Type](https://reference.opcfoundation.org/Core/Part5/v104/docs/6.4.2)
field `EventId`.

### time

MUST map to [Data Set Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `Timestamp`.

## Mapping for other extensions

The following well-known extension attributes apply to data and event
messages. Determine the native message type from the retained DataSetMessage
`MessageType` field when present. Otherwise, use `opcuamessagetype` for the
WoT mapping or `type` for the non-WoT mapping, as specified above.

### sequence

Without WoT, `sequence`, if present, MUST map to the native DataSetMessage
[`SequenceNumber`][UA SequenceNumber]. The Publisher increments it per
DataSetWriter.
The Producer MUST scope `source` to the writer's ordering scope and format
`sequence` so lexical comparison preserves event order, for example by
padding the unsigned decimal value to ten digits. The Producer MUST NOT
use the counter if a reset, rollover or shared source prevents that ordering.

For events using WoT, see the [combined mapping](#wot-mapping).

### traceparent

See the [Distributed Tracing extension](./distributed-tracing.md#traceparent).

### tracestate

See the [Distributed Tracing extension](./distributed-tracing.md#tracestate).

### recordedtime

See the [Recorded Time extension](./recordedtime.md#recordedtime).

## Attributes

### opcuametadatamajorversion

- Type: `Integer`
- Description: Links dataset message to the current version of the metadata.
Contains value from `MajorVersion` of [Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `MetaDataVersion`.
- Constraints
  - OPTIONAL, subject to the [schema and metadata-version rules](#metadata-versions)

### opcuametadataminorversion

- Type: `Integer`
- Description: Links dataset message to the current version of the metadata.
Contains value from `MinorVersion` of [Data Set Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `MetaDataVersion`.
- Constraints
  - OPTIONAL, subject to the [schema and metadata-version rules](#metadata-versions)

Both event attributes map unsigned [VersionTime][UA VersionTime] to
CloudEvents `Integer` (`0` to `2147483647`, inclusive). Producers MUST
preserve the value or report an encoding error, without truncation, wrap
or signed reinterpretation. Descriptor metadata and applicable native
payload representations can carry the full native range.

### opcuastatus

- Type: `Integer`
- Description: Defines the overall status of the data set message, maps to
[Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164) field `Status`.
- Constraints
  - OPTIONAL
  - REQUIRED if status is not _Good_ and `data` omits the native `Status` field
  - MAY be omitted if status is _Good_ or `data` retains the native `Status` field

CloudEvents `Integer` is limited to the signed 32-bit range. If the status
to be conveyed in `opcuastatus` cannot be represented, the Producer MUST
report an error rather than omit it, wrap the value, or report it as _Good_.

### opcuamessagetype

- Type: `String`
- Description: Carries the OPC UA PubSub DataSetMessage type when its
  `MessageType` field is absent from `data`.
- Constraints
  - OPTIONAL
  - In combination with the WoT profile, the value is REQUIRED for data and
    event messages when `data` omits the DataSetMessage `MessageType` field,
    including when other DataSetMessage header fields are retained.
  - MUST NOT be present when `data` includes the DataSetMessage `MessageType`.
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

The following names identify the OPC UA Publisher and DataSetWriter
when supplied as `source` query parameters or in an `opcuawriter` entry.
The native envelope carries these values under their OPC UA field names.
The [combined WoT mapping](#wot-mapping) defines when the identities are
REQUIRED; in the OPC UA-only mapping these values are OPTIONAL.

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

If both writer values are supplied, they MUST identify the same DataSetWriter.
A writer name MUST uniquely identify the DataSetWriter within the PublisherId
scope. Consumers MUST compare names exactly, without case folding or Unicode
normalization.

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

Changing `source`, including its query parameters, changes the scope
of [event identity](../spec.md#id) and the [Sequence extension](sequence.md).

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

A Producer MUST supply the REQUIRED CloudEvents attributes and, when the
WoT mapping applies, the per-event `opcuasequence` even with a retained
envelope.
Native message type conveyance follows [type](#type) and
[opcuamessagetype](#opcuamessagetype), according to whether the WoT profile
is used and whether the DataSetMessage `MessageType` field is present.
Read the native message type from the DataSetMessage header when present.
Any duplicated native values MUST agree after applying the specified mappings.
The Consumer MUST report a conflict and MUST NOT interpret a message as
conforming to this extension when they disagree.

## OPC UA Descriptor Profile

This profile defines Descriptor fields for OPC UA Part 14 Publisher,
DataSetWriter, DataSet and ConfigurationVersion metadata. A Processing
Descriptor is OPTIONAL. The native envelope and event can also carry inputs.

### Descriptor entry

A message stream here is a configured flow from one Publisher and
DataSetWriter with a defined payload contract. A broker topic or a
CloudEvents `source` can carry several such streams.

Publishers MUST derive shared values from the native writer and metadata
configuration for the emitted message. For an agreed [Descriptor
binding](descriptor.md#descriptor-profiles), they SHOULD store stream-constant
values in an `opcuawriter` entry. An `opcuawriter` entry carries its values
inline and MUST omit `url`. When the entry supplies shared inputs, the
Descriptor URL MUST identify a fixed version so that replay selects the
same inputs.

A publication profile is the agreed set of rules for interpreting the event.
Use the `opcuawriter` entry named by the publication profile, or the unique
entry of that class if the profile supplies no name. With no name and no
entry, writer metadata is absent from the Descriptor. A Consumer MUST
report a missing or wrong-class named entry or an ambiguous selection and
MUST take Descriptor writer metadata from the selected entry alone.

### Shared Stream Metadata in a Descriptor

Each member in the following table is OPTIONAL in the entry. The binding
determines which values the event needs. Supply these fields inside the
entry. Report invalid metadata for supplied values that violate this
profile, including null values. Interpret the fields as JSON members of
the entry under their declared types.

| Member of an `opcuawriter` entry | JSON representation | Meaning and conditions |
| --- | --- | --- |
| `opcuapublisherid` | String | The stream's typed native PublisherId, under the rules in [Publisher and Writer Metadata](#publisher-and-writer-metadata). |
| `opcuadatasetwriterid` | Integer, `1` to `65535` | The stream's native DataSetWriterId, when used. |
| `opcuadatasetwritername` | Non-empty String | The stream's exact configured DataSetWriterName, when used. |
| `opcuadatasetname` | Non-empty String | The `Name` of the applicable DataSet metadata. |
| `opcuametadatamajorversion` | Integer, `0` to `4294967295` | The native MajorVersion, when no payload schema is selected. |
| `opcuametadataminorversion` | Integer, `0` to `4294967295` | The native MinorVersion, when no payload schema is selected. |

Ranges are inclusive. Publisher and writer fields MUST follow [Publisher
and Writer Metadata](#publisher-and-writer-metadata).

#### Metadata versions

Represent each Descriptor metadata-version field as a JSON integer in the
full `VersionTime` (`UInt32`) range. Consumers MUST compare duplicate
values without narrowing and report out-of-range values as invalid metadata.

Metadata-version values retain their native [ConfigurationVersion][UA
ConfigurationVersion] meaning. Apply Part 14's MajorVersion and
MinorVersion update rules independently of Descriptor versioning.

When `dataschema` or the Descriptor supplies a schema, Producers MUST NOT
include metadata-version values in CloudEvents context attributes or the
`opcuawriter` entry. Native fields retained in `data` are unaffected.

#### DataSet name

`opcuadatasetname` belongs only in Descriptor metadata. It MUST equal
`DataSetMetaDataType.Name` from the applicable
[DataSet metadata][UA DataSet Metadata] or its approved configuration.
It is descriptive and can recur across writers. A Consumer MUST obtain
any REQUIRED native identifier independently. Repeated dataset names MUST
match exactly; a mismatch is a metadata conflict.

### Using shared inputs

For the listed values, an applicable Descriptor satisfies this extension's
presence requirements for the corresponding field, including those of the
combined WoT mapping. A Producer MAY omit the corresponding event attribute
or source query parameter.

Apply the [identity consistency rules](#publisher-and-writer-metadata)
across the query, Descriptor, and native envelope. If an event attribute
and the Descriptor both supply a metadata version, their typed values MUST
agree. On a conflict, the Consumer MUST report a metadata conflict and
treat the event as nonconforming. If a REQUIRED value is absent from all
applicable locations, the Consumer MUST report missing metadata and treat
the event as nonconforming.

A Consumer MUST use the selected Processing Descriptor as the sole
Descriptor source for shared schema and native metadata. If `describedby`
is present but the URL is invalid or the Consumer cannot obtain a valid
Descriptor there, the Consumer MUST report the failure and treat the
Descriptor-based inputs as unavailable.
The Consumer MAY still interpret the native payload if the envelope, source
query, and explicit event attributes supply every native requirement.
That result is independent of WoT correlation.

The Descriptor Publisher MUST NOT change these values in a Descriptor Version
after any Producer is configured with its URL. A change requires a new
Descriptor Version and reconfigured Producers. Consumers MUST NOT retain values
from a previous Descriptor when processing an event that selects another
Descriptor. The OPC UA identifiers determine the writer identity; the
Descriptor version identifies the shared inputs. For a changed WoT payload
contract, apply the [WoT `type` revision rules](wot.md#type).

Values that vary by occurrence remain in each event. In particular,
the Producer MUST supply `opcuamessagetype`, `opcuasequence`, `opcuastatus`,
`id`, and `time` on the event when their respective rules require them.
Consumers MUST obtain these attributes and any tracing, recording time,
and CloudEvents `sequence` values from the event itself. Core attributes
retain their CloudEvents placement and meaning.

An OPC UA-only event can omit `describedby`. In that case the Producer
MUST supply all REQUIRED OPC UA values through the other applicable locations.
Producers SHOULD use Descriptor metadata only when the intended Consumers
support the agreed mapping.

JSON integers in this profile preserve the full native ranges. An alternate
serialization or generated schema MUST preserve those same values, or report
an encoding error. For example, use an Avro type wide enough to preserve
the full UInt32 range.

The [OPC UA entry schema](opcua.schema.json) checks entry shape. Verify
PublisherId encoding, ranges, and the event context under the rules above.

## WoT mapping

When a CloudEvent uses both this extension and the [WoT profile](wot.md),
[`describedby` is REQUIRED](wot.md#description-selection). The same
Descriptor supplies the WoT selection and any Descriptor-based OPC UA
metadata. For data and event messages, the following mappings take
precedence over the corresponding OPC UA-only mappings:

- The Producer MUST use the WoT [`type`](wot.md#type) and
  [`subject`](wot.md#subject) mappings. Keep the native `EventId` in the
  OPC UA event payload.
  Convey the native message type under the
  [`opcuamessagetype`](#opcuamessagetype) rules.
- The native PublisherId and at least one of DataSetWriterId and
  DataSetWriterName are REQUIRED. Supply each value in the envelope, a
  `source` query parameter, or the selected `opcuawriter` entry, under
  [Publisher and Writer Metadata](#publisher-and-writer-metadata).
- Use [`opcuasequence`](#opcuasequence) for the native `SequenceNumber`.
  If the Producer also supplies CloudEvents `sequence`, it MUST satisfy
  the [Sequence extension](sequence.md) independently. The Producer MUST
  obtain that value independently of `opcuasequence`.

All other applicable OPC UA requirements remain in effect.

## Examples

The OPC UA-only examples use writer name `energy-consumption-asset` in
`subject`. Some also supply publisher `UInt16:12` and the writer name in the
`source` query. Those query parameters are OPTIONAL without WoT.

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

This example uses a writer-specific `source` for sequence ordering without
carrying an explicit PublisherId or writer query parameter.

```text
------------------ PUBLISH -------------------

Topic Name: opcua/json/DataSetMessage/publisher-on-ot-edge
Content Type: application/json; charset=utf-8

------------- User Properties ----------------

specversion: 1.0
type: ua-deltaframe
time: 2024-03-28T21:56:42Z
id: 1235-1235-1235
source: https://factory.example.com/aggregationserver/opcua/energy-consumption-asset
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

This binary-mode keyframe uses the WoT event type. Its Descriptor selects
the pump's `processData` property and supplies the payload schema, publisher,
and writer metadata. The native OPC UA message type and sequence remain in
the event. This example uses writer ID `17` within publisher `UInt16:12`.

```text
------------------ PUBLISH -------------------

Topic Name: opcua/json/DataSetMessage/pump
Content Type: application/json

------------- User Properties ----------------

specversion: 1.0
id: ua-message-25460
source: urn:example:actor:telemetry-service
type: com.example.models.tm.pump.properties.processData.v1
subject: pump7
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

The referenced Descriptor version contains these entries:

```json
{
  "entries": {
    "pump7": {
      "class": "thingdescription",
      "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0",
      "affordanceselector": "/properties/processData"
    },
    "payload": {
      "class": "schema",
      "url": "https://schemas.example/pump-process-data/versions/3"
    },
    "writer": {
      "class": "opcuawriter",
      "opcuapublisherid": "UInt16:12",
      "opcuadatasetwriterid": 17,
      "opcuadatasetwritername": "pump7-process",
      "opcuadatasetname": "PumpProcessData"
    }
  }
}
```

The Consumer selects `/properties/processData` from the TD entry and
reads the schema and native identity from the `payload` and `writer`
entries. The event's `subject` is available for filtering.

#### WoT telemetry with a retained NetworkMessage envelope

This event retains the full Part 14 NetworkMessage envelope. Its PublisherId
and DataSetWriterId satisfy the identity requirements, so `source` needs no
publisher or writer query parameters. Part 14 JSON encodes the configured
PublisherId `UInt16:12` as the string `"12"`.

`describedby` selects the [WoT example Descriptor](wot.md#web-of-things)
for the Thing and affordance. `dataschema` takes precedence over that
Descriptor's schema entry and identifies the envelope's schema. The event
type uses revision `v2` because retaining the envelope changes the payload
contract.

```text
------------------ PUBLISH -------------------

Topic Name: opcua/json/DataSetMessage/pump
Content Type: application/json

------------- User Properties ----------------

specversion: 1.0
id: ua-message-25461
source: mqtt://site/line/cell/device/sensor?site=north
type: com.example.models.tm.pump.properties.processData.v2
describedby: https://devices.example/pump7/descriptors/process-data.json
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

The rollover from `4294967295` to `0` is carried in `opcuasequence`. The
retained DataSetMessage header supplies the native `MessageType`.

## Descriptor Retrieval Security

Follow the [Descriptor Reference security and caching rules](descriptor.md#security-considerations).
A Consumer MUST establish trust in the Descriptor before using it as OPC UA
metadata. Publisher authentication and authorization to access the TD or
schema depend on checks independent of the writer metadata.

[UA DataSetWriterName]: https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table185
[UA NetworkMessage]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/7.2.5.3
[UA DataSetWriterId]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/6.2.4.1
[UA PublisherId]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/6.2.7.1
[UA SequenceNumber]: https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.3
[UA DataSet Metadata]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/6.2.3.2.3
[UA VersionTime]: https://reference.opcfoundation.org/specs/OPC-10000-4/v1.05.07/7.43
[UA ConfigurationVersion]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/6.2.3.2.6
[URI]: https://www.rfc-editor.org/rfc/rfc3986
[Schema Descriptor Profile]: descriptor.md#schema
