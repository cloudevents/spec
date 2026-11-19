# OPC UA

This extension maps [OPC UA](https://reference.opcfoundation.org/Core/Part1/v105/docs/)
[PubSub](https://reference.opcfoundation.org/Core/Part14/v105/docs/)
DataSetMessages to CloudEvents for routing over supported protocols. It maps
Core and existing extension attributes and defines OPC UA attributes.

The [OPC UA Descriptor profile](#opc-ua-descriptor-profile) uses the
[Descriptor Reference extension](descriptors.md) and xRegistry model to
share stream metadata. Native identity comes from the NetworkMessage
envelope, Processing Descriptor or `source` query, not from either WoT
subject route (direct TD or Subject Descriptor).

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

These requirements apply only to events using this extension.

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
NetworkMessage envelope or the Processing Descriptor supplies its corresponding
value.

### type

An OPC UA Producer MAY map `type` to the
[Data Set Message Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164)
field `MessageType`. For data and event messages without the WoT profile,
the Producer MUST use that native value as `type` when the DataSetMessage
`MessageType` field is absent from `data`. A retained header does not
guarantee that field is present: the native content mask controls inclusion.

A Producer using the WoT profile MUST instead follow its semantic
event-type rules and the [opcuamessagetype](#opcuamessagetype) requirements
for conveying the native message type. The [WoT mapping section](#wot-mapping)
specifies the combined mapping.

### WoT mapping

When a CloudEvent uses both this extension and the
[WoT profile](./wot.md), the following mappings apply to data and event
messages:

- The Producer MUST use the WoT [`type`](wot.md#type) and
  [`subject`](wot.md#subject) mappings and convey native `MessageType` under
  [`opcuamessagetype`](#opcuamessagetype).
- The Producer MUST supply the PublisherId and writer identity under the
  [Publisher and Writer Metadata](#publisher-and-writer-metadata) rules.
- Nothing MUST be appended to `subject`. For an event message, the `EventId`
  remains in the OPC UA event payload.
- `opcuasequence` MUST carry the native `SequenceNumber`. The CloudEvents
  `sequence` attribute, when present, MUST satisfy the independent ordering
  requirements of the Sequence extension and MUST NOT be inferred from
  `opcuasequence`.

These mappings override only conflicting rules. A profile MUST meet every
other applicable requirement to conform to this extension.

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
`dataschema` when present; otherwise, use the Processing Descriptor's schema
under the [Schema Descriptor profile][Schema Descriptor Profile].
`data.schema.schemaref` names an entry in `references.schema`. Subject-only
lookup cannot supply a schema.

The Consumer MUST report a missing REQUIRED schema. An ambiguous selection,
invalid selector, unavailable schema or unsupported format MUST NOT cause
fallback to another schema. If `dataschema` is present, the Consumer MUST
still validate applicable Descriptor selectors, without selecting a
Descriptor schema or comparing schema documents. Producers and Descriptor
publishers SHOULD supply one schema source or identify the same schema in
both. The Producer SHOULD omit `dataschema` when the Descriptor supplies
the schema. The selected schema MUST describe `data`, including the
NetworkMessage envelope if retained.

### subject

For metadata, data, and event messages, a Producer MAY map `subject` to
`DataSetWriterId` or `DataSetWriterName` from the [Data Set Message
Header](https://reference.opcfoundation.org/Core/Part14/v105/docs/7.2.5.4#Table164).
A Producer using the WoT profile MUST instead follow its Descriptor-relative,
direct-TD or Subject Descriptor Version mapping.

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
DataSetWriter; it does not order multiple writers sharing a `source`.
The Producer MUST scope `source` to the writer's ordering scope and format
`sequence` so lexical comparison preserves event order, for example by
padding the unsigned decimal value to ten digits. The Producer MUST NOT
use the counter if a reset, rollover or shared source prevents that ordering.

With WoT, the subject identifies a Thing or affordance rather than the
writer. `opcuasequence` carries the native counter. If `sequence` is present,
it MUST satisfy the [Sequence extension](./sequence.md) independently and
MUST NOT be inferred from `opcuasequence`.

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
  - REQUIRED if status is not _Good_
  - MAY be omitted if status is _Good_

CloudEvents `Integer` is limited to the signed 32-bit range. If a native
status value cannot be represented, the Producer MUST report an error rather
than omit the status, wrap the value, or report it as _Good_.

### opcuamessagetype

- Type: `String`
- Description: Carries the OPC UA PubSub DataSetMessage type when its
  `MessageType` field is absent from `data`.
- Constraints
  - OPTIONAL
  - In combination with the WoT profile, the value is REQUIRED for data and
    event messages when `data` omits the DataSetMessage `MessageType` field,
    including when other DataSetMessage header fields are retained.
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
Processing Descriptor Version unless the full Part 14 NetworkMessage envelope
supplies it. The names are the same in the query and Descriptor representations.

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
parameter or Descriptor field. A full envelope that omits an identifier does
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
event-identity and [Sequence extension](sequence.md) scope. When returning to
an earlier `source`, the Producer MUST preserve the uniqueness of `source`
plus `id`. When using the Sequence extension, its `sequence` values MUST
remain ordered relative to earlier events from that same source.

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
Native message type conveyance follows [type](#type) and
[opcuamessagetype](#opcuamessagetype), according to whether the WoT profile
is used and whether the DataSetMessage `MessageType` field is present.
The NetworkMessage's `ua-data` type is not the DataSetMessage type. Any
duplicated native values MUST agree after applying the specified mappings.
The Consumer MUST report a conflict and MUST NOT interpret a message as
conforming to this extension when they disagree.

## OPC UA Descriptor Profile

This profile defines Descriptor fields for OPC UA Part 14 Publisher,
DataSetWriter, DataSet and ConfigurationVersion metadata. A Processing
Descriptor is OPTIONAL: the event and native envelope can supply the
inputs. This OPC UA profile requires a Version URL only when the Processing
Descriptor supplies shared fields.

### Shared Stream Metadata in a Descriptor

A message stream here is a configured flow from one Publisher and
DataSetWriter with a defined payload contract. It is not necessarily a broker
topic or a CloudEvents `source`; either can carry several streams.

Publishers MUST derive shared values from the native writer and metadata
configuration for the emitted message. For an agreed [Descriptor
binding](descriptors.md#descriptor-retrieval), they SHOULD store stream-constant
values in the Descriptor's `data.opcuawriter` object instead of repeating them
in events. Those values MUST stay constant across events using that Version.
When the object supplies such values, the selected URL MUST identify the
Version, not a Resource whose default can change before replay.

With WoT, only Descriptor-relative subjects without `describedby` can select
a Processing Descriptor through `source`. A Subject Descriptor or its
annotations do not establish the writer association.

| Member of `data.opcuawriter` | JSON representation | Meaning and conditions |
| --- | --- | --- |
| `opcuapublisherid` | String | The stream's typed native PublisherId, under the rules in [Publisher and Writer Metadata](#publisher-and-writer-metadata). |
| `opcuadatasetwriterid` | Integer, `1` to `65535` | The stream's native DataSetWriterId, when used. |
| `opcuadatasetwritername` | Non-empty String | The stream's exact configured DataSetWriterName, when used. |
| `opcuadatasetname` | Non-empty String | The `Name` of the applicable DataSet metadata; descriptive, not a writer identifier. |
| `opcuametadatamajorversion` | Integer, `0` to `4294967295` | The native MajorVersion, when no payload schema is selected. |
| `opcuametadataminorversion` | Integer, `0` to `4294967295` | The native MinorVersion, when no payload schema is selected. |

Ranges are inclusive. Publisher and writer fields MUST follow [Publisher
and Writer Metadata](#publisher-and-writer-metadata). The Descriptor's
metadata-version fields MUST preserve the full `VersionTime` (`UInt32`) range,
independent of the CloudEvents `Integer` limit. Consumers MUST compare
duplicate values without narrowing. Out-of-range fields are invalid metadata.

Metadata-version values retain their native [ConfigurationVersion][UA
ConfigurationVersion] meaning. Descriptor versioning does not change when Part
14 requires a MajorVersion or MinorVersion update.

The Descriptor's selected schema Reference identifies an external payload
schema. Native metadata-version values MUST NOT be supplied in the event
or `data.opcuawriter` when a schema is selected through `dataschema` or the
Descriptor.

`opcuadatasetname` is OPTIONAL and valid only in Descriptor metadata.
It MUST equal `DataSetMetaDataType.Name` from the applicable
[DataSet metadata][UA DataSet Metadata] or its approved configuration, not
a name inferred from the writer, topic or TD affordance. It need not be
unique and MUST NOT replace a REQUIRED PublisherId, DataSetWriter identity
or native field. Repeated dataset names MUST match exactly, without case
folding or Unicode normalization; a mismatch is a metadata conflict.

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

A Consumer MUST use only the Processing Descriptor selected by the agreed
binding for shared schema and native metadata inputs. If `describedby` is
present, missing values MUST NOT be taken from a source or subject description.
If the Consumer cannot retrieve that Descriptor, it MAY interpret the native
payload when the envelope, source query and explicit event attributes supply
every native requirement. It MUST NOT report that result as successful WoT
correlation. This is native-only interpretation, not a fallback to another
Descriptor. The [Descriptor Reference failure
rules](descriptors.md#failure-outcomes) still apply.

Without `describedby`, the WoT profile can select a direct TD subject or a
Subject Descriptor Version without selecting a Processing Descriptor. Native
publisher and writer requirements then have to be satisfied by the retained
envelope or the existing source query. A direct TD, Subject Descriptor or its
subject annotations MUST NOT supply missing OPC UA metadata or a payload schema.
Consumers MUST NOT retrieve a source Descriptor as an implicit supplement.

Apply the [WoT correlation rules](wot.md#subject-descriptor-selection) to
match the subject's TD URL to exactly one Processing Descriptor Reference.
If `subject` and `describedby` explicitly select the same URL, only the
separately validated processing role MAY supply native metadata.

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

When the agreed route selects no Processing Descriptor, the Producer MUST supply
all REQUIRED OPC UA values through the other locations defined above. An absent
`describedby` alone does not determine whether a Processing Descriptor was
selected. Producers SHOULD use Descriptor metadata only when the intended
Consumers support the agreed mapping.

When `source` is itself a Descriptor URL, Producers SHOULD supply shared
identity metadata in the selected versioned Descriptor instead of appending
query parameters to that URL. Appending a query changes the event's source
identity and can change the retrieved resource. Consumers MUST NOT strip a query
to make source-based retrieval work.

### xRegistry Model Mapping

The Descriptor Registry's `data` map holds the OPTIONAL `opcuawriter`
object. Each member above is OPTIONAL in the object; the binding determines
which values the event needs. An absent or empty object supplies none. A
top-level Descriptor attribute with the same name as a member does not supply
that value.

The Consumer MUST report invalid metadata if `opcuawriter` is not an object
or if a supplied member violates this profile's type, range or native mapping
constraints. This includes a null object or a null value for a listed member.
Core write/null rules apply to Descriptor updates; CloudEvents event-attribute
null decoding does not apply to a retrieved Descriptor.

JSON integers in this profile preserve the full native ranges. An alternate
serialization or generated schema MUST preserve those same values, or report
that it cannot represent them. In particular, an Avro `int` cannot represent the
upper half of UInt32; an appropriate wider encoding is needed rather than
narrowing or wrapping the value. This profile does not change the generic
xRegistry schema generator.

Descriptor identity, References, schema selection and publication stability
follow the Descriptor Registry. Publishers MUST retain stable referenced
representations, selectors and shared metadata for the intended processing and
replay period. A new Descriptor Version conveys changed inputs; it does not make
the native writer identity equal to a Descriptor identifier.

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
  "references": {
    "thingdescription": {
      "pump7": {
        "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0"
      },
      "gateway1": {
        "url": "https://registry.example/thingdescriptiongroups/factory/thingdescriptions/gateway1/versions/1.0.0"
      }
    },
    "schema": {
      "payload": {
        "url": "https://schemas.example/pump-process-data/versions/3"
      }
    },
    "usdasset": {
      "geometry": {
        "url": "https://assets.example/usdassetgroups/line1/usdassets/pump7/versions/2"
      }
    }
  },
  "data": {
    "schema": { "schemaref": "payload" },
    "opcuawriter": {
      "opcuapublisherid": "UInt16:12",
      "opcuadatasetwriterid": 17,
      "opcuadatasetwritername": "pump7-process",
      "opcuadatasetname": "PumpProcessData"
    }
  }
}
```

The Consumer uses the selected Descriptor's PublisherId and writer identity with
the event's `opcuamessagetype` and `opcuasequence`. The subject's `pump7` prefix
selects one of two TDs; `data.schema.schemaref` selects the payload schema.
The dataset name and writer name differ.

With an agreed source-Descriptor binding, a Producer can instead use the
stream's Descriptor Version URL as `source` and omit `describedby`. This changes
the source identity; it is not an identity-preserving rewrite of already
published events.

#### Subject Descriptor with separate processing metadata

The following binary-mode event uses the [Subject Descriptor
example](wot.md#subject-descriptor-with-separate-processing-inputs) for its
Thing reference and affordance selector. Its `describedby` selects the
complete `pump7-telemetry` Processing Descriptor shown above.

```http
POST /events HTTP/1.1
Host: consumer.example
Content-Type: application/json
ce-specversion: 1.0
ce-id: ua-message-25462
ce-source: urn:example:actor:telemetry-service
ce-type: com.example.models.tm.pump.properties.processData.v1
ce-subject: https://registry.example/descriptorgroups/subjects/descriptors/pump7-process/versions/1
ce-describedby: https://registry.example/descriptorgroups/streams/descriptors/pump7-telemetry/versions/1
ce-opcuamessagetype: ua-keyframe
ce-opcuasequence: 18

{"Speed":1500,"Pressure":4.5}
```

`data.wot.subject` selects one matching TD URL and the `/properties/processData`
affordance. The Processing Descriptor supplies the payload schema, `UInt16:12`
PublisherId and writer identity. Without `describedby` these inputs are missing:
neither the subject nor a source lookup supplies them.

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
subject: https://registry.example/thingdescriptiongroups/factory/thingdescriptions/pump7/versions/3.0.0#/properties/processData
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
[UA VersionTime]: https://reference.opcfoundation.org/specs/OPC-10000-4/v1.05.07/7.43
[UA ConfigurationVersion]: https://reference.opcfoundation.org/specs/OPC-10000-14/v1.05.06/6.2.3.2.6
[URI]: https://www.rfc-editor.org/rfc/rfc3986
[Schema Descriptor Profile]: https://github.com/xregistry/spec/pull/796/files#diff-392fa7cefe828f037942a4b1cc7901449d3578fbb5704d00f851f252e5f2e44a
