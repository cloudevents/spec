# Data Distribution Service (DDS) Event Format for CloudEvents - Version 1.0.3-wip

## Abstract

The Data Distribution Service (DDS) Format for CloudEvents defines how event
attributes are expressed using data types defined in the [Object Management
Group (OMG)][omg] [Interface Definition Language (IDL) Specification][idl-spec].

The [OMG DDS Specification][dds-spec] is closely related to the IDL specification as
messages transmitted over the DDS protocol are defined via the IDL type system.
These messages are sent over the wire using the Common Data Representation (CDR)
serialization, as defined in the OMG [Real-Time Publish Subscribe (RTPS)][rtps]
specification.

It is noted here that the DDS Event Format is coupled to the DDS Protocol Binding
for CloudEvents. CloudEvents defined in the DDS Event Format can only be
decoded by a message receiver that is using the DDS protocol.  

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Data](#3-data)
4. [Transport](#4-transport)
5. [Batch Format](#5-batch-format)
6. [Examples](#6-examples)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are represented using a DDS
schema.

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvent attributes for use as DDS message
properties.

The [Data](#3-data) section describes how the event payload is carried.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2 Content-Type

There is no official IANA *media-type* designation for DDS, as such this
specification uses 'application/dds' to identify such content.

### 1.3 DDS Schema  

DDS encoded CloudEvent messages MUST adhere to the format defined in the [DDS Schema][dds-schema].

## 2. Attributes

This section defines how CloudEvents attributes are represented in the [DDS schema][dds-schema].

## 2.1 Type System

The CloudEvents type system is mapped to IDL datatypes as follows :

| CloudEvents   | DDS |
| ------------- | ---------------------------------------------------------------------- |
| Boolean       | [boolean][dds-schema] |
| Integer       | [int32][dds-schema] |
| String        | [string][dds-schema] |
| Binary        | [bytes][dds-schema] |
| URI           | [string][dds-schema] following [RFC 3986 §4.3][rfc3986-section43]|
| URI-reference | [string][dds-schema] following [RFC 3986 §4.1][rfc3986-section41] |
| Timestamp     | [Timestamp][dds-schema]  |

## 2.3 REQUIRED Attributes

REQUIRED attributes are represented explicitly as fields in the [Event type definition][dds-schema].

## 2.4 OPTIONAL Attributes & Extensions

At this time OPTIONAL and extension attributes are not supported in the DDS format.  

There is overlap between the extension attributes and protocol level parameters
that are specified using DDS Quality of Service (QoS) settings. For example, the
Expiry Time extension attribute is very similar to the Lifespan QoS defined in the
[DDS Specification][dds-spec]. There also is some overlap between the Sampling and
Partitioning extension attributes and the DDS Time-Based Filter and Partition QoS.
It is expected that a future revision of this binding will include support for these
attributes once we have resolved any ambiguities.

Similarly, support for OPTIONAL attributes is deferred to a later draft of this binding as
the DDS User Data, Group Data and Topic Data QoS also enable the transmission of
user-defined contextual data. It is expected that a future revision of this binding will
include support for OPTIONAL attributes.

## 3. Data

The specification allows for data payloads of the following types to be explicitly represented:

* binary
* string

```xml

 <enum name="DataKind">
   <enumerator name="BINARY"/>
   <enumerator name="TEXT"/>
 </enum>
	  
 <union name="Data" extensibility="final">
   <discriminator type="nonBasic" nonBasicTypeName="io::cloudevents::DataKind"/>
   <case>
     <caseDiscriminator value="(io::cloudevents::BINARY)"/>
     <member name="binary_data" type="byte" sequenceMaxLength="LENGTH_UNLIMITED"/>
   </case>
   <case>
     <caseDiscriminator value="(io::cloudevents::TEXT)"/>
     <member name="text_data" type="string" stringMaxLength="LENGTH_UNLIMITED"/>
   </case>
 </union>
```

* When the type of the data is binary the DataKind attribute MUST be set to BINARY.
* When the type of the data is generic text the DataKind attribute MUST be set to TEXT.

* It is noted here that when using DDS it is not necessary to specify the dataschema
as the DDS protocol itself transmits the schema during the discovery handshake
between event producers and consumers.

## 4. Transport

Transports that support content identification MUST use the following designation:

```text
   application/cloudevents+dds
```

## 5. Batch Format

The DDS event format does not currently define a batch mode format.

## 6. Examples

The following code-snippet shows how messages in the DDS event format might
be constructed and transmitted assuming the availability of some convenience
methods.

### 6.1 Binary message event data

```javascript

const emit = async () => {
  
  const type = "org.cncf.cloudevents.example";
  const source = "urn:event:from:myapi/resource/123";
  const time = new Date().toISOString();
  
  // cloudevent+dds / binary
  const ce_dds_binary_obj = new CloudEvent({
    specversion: "1.0",
    id: "b46cf653-d48a-4b90-8dfa-355c01061364",
    type,
    source,
    datacontenttype: "application/cloudevent+dds",
    subject: "SQUARE",
    time,
    datakey:"Somekey",
    datacontentencoding: "binary",
    data: Buffer.from("Some text string" as string) // send the binary representation of a string
  })

  try {
    console.log('Event producer listening for consumers...')
    await output.waitForSubscriptions()

    const dds_binary_event_obj = DDS.binary(ce_dds_binary_obj);
    output.instance.setFromJson(dds_binary_event_obj) // Json translation needed for the DDS JS API
    output.write() // emit the message

    sleep.msleep(500)

    // Wait for all subscriptions to receive the data
    await output.wait()
  }
}

```

## References
- [OMG][omg] Object Management Group (OMG)
- [idl-spec] OMG Interface Definition Language (IDL) Specification 
- [DDS][dds-spec] OMG Data Distribution Service (DDS) Specification
- [RTPS][rtps] OMG Real-Time Publish Subscribe Wire Protocol
- [dds-schema] XML representation of DDS event schema
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels
- [CE-Extensions][ce-extensions] CloudEvents Extension Attributes 

[ce]: ../spec.md
[omg]: https://www.omg.org/
[idl-spec]: https://www.omg.org/spec/IDL/4.2/PDF
[dds-spec]: https://www.omg.org/spec/DDS/1.4/PDF
[rtps]: https://www.omg.org/spec/DDSI-RTPS/2.3/PDF
[dds-schema]: ./dds-cloudevent.xml
[ce-types]: ../spec.md#type-system
[ce-extensions]: ..//documented-extensions.md
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986-section41]: https://tools.ietf.org/html/rfc3986#section-4.1
[rfc3986-section43]: https://tools.ietf.org/html/rfc3986#section-4.3
[rfc3339]: https://tools.ietf.org/html/rfc3339

