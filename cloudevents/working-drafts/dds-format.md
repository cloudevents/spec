# Data Distribution Service (DDS) Event Format for CloudEvents - Version 1.0.0-wip

## Abstract

The Data Distribution Service (DDS) Format for CloudEvents defines how event attributes are
expressed using the data types defined in the [Object Management Group (OMG)][omg]
[Interface Definition Language (IDL) Specification][idl-spec].

The [OMG DDS Specification][dds-spec] is closely related to the IDL specification as
messages transmitted over the DDS protocol are defined via the IDL type system.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Data](#3-data)
4. [Examples](#4-examples)

## 1. Introduction

[CloudEvents][ce] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how the
elements defined in the CloudEvents specification are to be represented in IDL
primitive types.

The [Attributes](#2-attributes) section describes the naming conventions and
data type mappings for CloudEvents attributes for use as DDS message
properties.

This specification does not define an envelope format.

The DDS event format does not currently define a batch mode format.

An eXtensible Markup Language (XML) reprsentation of the [DDS Event Format][dds-event-format]
is provided in conjunction with this document.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

## 2. Attributes

This section defines how CloudEvents attributes are mapped to the IDL
type-system used by DDS. This specification explicitly maps each attribute.

### 2.1 Type System Mapping

The CloudEvents type system MUST be mapped to DDS types as follows.

| CloudEvents   | DDS                                                                   |
| ------------- | ---------------------------------------------------------------------- |
| Boolean       | Boolean                                             |
| Integer       | Int32                                                 |
| String        | String (255)                                              |
| Binary        | Bytes (100)                                               |
| URI           | String (255) following [RFC 3986 §4.3][rfc3986-section43] |
| URI-reference | String (255) following [RFC 3986 §4.1][rfc3986-section41] |
| Timestamp     | seconds: Int64 nanoseconds: UInt32     |

Extension specifications MAY define secondary mapping rules for the values of
attributes they define, but MUST also include the previously defined primary
mapping.

### 2.2 OPTIONAL Attributes

The CloudEvents spec defines OPTIONAL attributes. The set of possible Attribute Types and Values
for OPTIONAL attributes are defined in the [DDS Event Format][dds-event-format] as follows:

```xml
<enum name="AttributeType">
   <enumerator name="BOOL"/>
   <enumerator name="INT32"/>
   <enumerator name="STRING"/>
   <enumerator name="BYTES"/>
   <enumerator name="URI"/>
   <enumerator name="URI_REF"/>
   <enumerator name="TIMESTAMP"/>
</enum>
	  
<union name="AttributeValue" extensibility="final">
   <discriminator type="nonBasic" nonBasicTypeName="io::cloudevents::AttributeType"/>
   <case>
      <caseDiscriminator value="(io::cloudevents::BOOL)"/>
      <member name="ce_boolean" type="boolean"/>
   </case>
   <case>
      <caseDiscriminator value="(io::cloudevents::INT32)"/>
      <member name="ce_integer" type="int32"/>
   </case>
   <case>
      <caseDiscriminator value="(io::cloudevents::STRING)"/>
      <member name="ce_string" type="string" stringMaxLength="255"/>
   </case>
   <case>
      <caseDiscriminator value="(io::cloudevents::BYTES)"/>
      <member name="ce_bytes" type="byte" sequenceMaxLength="100"/>
   </case>
   <case>
      <caseDiscriminator value="(io::cloudevents::URI)"/>
      <member name="ce_uri" type="nonBasic" nonBasicTypeName="io::cloudevents::URI"/>
   </case>
   <case>
      <caseDiscriminator value="(io::cloudevents::URI_REF)"/>
      <member name="ce_uri_reference" type="nonBasic" nonBasicTypeName="io::cloudevents::URI_Ref"/>
   </case>
   <case>
      <caseDiscriminator value="(io::cloudevents::TIMESTAMP)"/>
      <member name="ce_timestamp" type="nonBasic" nonBasicTypeName="io::cloudevents::Timestamp"/>
   </case>
</union>

```

Based on the above, the type definition for OPTIONAL Attributes is as follows:

```xml

<struct name="DDS-CE-Attribute">
    <member name="key" type="string" stringMaxLength="255"/>
    <member name="value" type="nonBasic" nonBasicTypeName="io::cloudevents::AttributeValue"/>
</struct>

<typedef name="DDS-CE-Attributes" type="nonBasic" nonBasicTypeName="io::cloudevents::DDS-CE-Attribute" sequenceMaxLength="100"/>

```

### 2.3 Definition

The [DDS Event Format][dds-event-format] is defined in the io::cloudevents DDS module and is dependent on the following base types:

```xml
 <struct name="Headers" extensibility="mutable">
   <member name="content-type" type="string" stringMaxLength="255" optional="true"/>
 </struct>
	  
 <typedef name="ce_boolean" type="boolean"/>
 <typedef name="ce_int32" type="int32"/>
 <typedef name="ce_string" type="string" stringMaxLength="255"/>
 <typedef name="ce_bytes" type="byte"/>
 <typedef name="ce_uri" type="string" stringMaxLength="255"/>
 <typedef name="ce_uri_reference" type="string" stringMaxLength="255"/>

 <struct name="ce_timestamp" extensibility="final">
   <member name="sec" type="int64"/>
   <member name="nanosec" type="uint32"/>
 </struct>
```

Since the DDS Event Format currently supports only three types of data payloads, these are defined within the io::cloudevents DDS module by the folowing enumeration and union:

```xml
 <enum name="DataKind">
   <enumerator name="BINARY"/>
   <enumerator name="TEXT"/>
   <enumerator name="JSON"/>
 </enum>
	  
 <union name="Data" extensibility="final">
   <discriminator type="nonBasic" nonBasicTypeName="io::cloudevents::DataKind"/>
   <case>
      <caseDiscriminator value="(io::cloudevents::BINARY)"/>
       <member name="binary_data" type="byte" sequenceMaxLength="100"/>
    </case>
    <case>
      <caseDiscriminator value="(io::cloudevents::JSON)"/>
       <member name="json_dds_data" type="string" stringMaxLength="255"/>
    </case>
    <case>
      <caseDiscriminator value="(io::cloudevents::TEXT)"/>
      <member name="text_data" type="string" stringMaxLength="255"/>
    </case>
 </union>
```

Finally, the complete [DDS Event Format][dds-event-format] structure is:

```xml

<struct name="Event" extensibility="mutable">
   <member name="headers" type="nonBasic" nonBasicTypeName="io::cloudevents::Headers"/>
   <member name="id" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_string"/>
   <member name="source" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_uri_reference"/>
   <member name="specversion" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_string"/>
   <member name="type" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_string"/>
   <member name="datacontenttype" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_string" optional="true"/>
   <member name="datacontentencoding" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_string" optional="true"/>
   <member name="dataschema" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_uri" optional="true"/>
   <member name="subject" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_string" optional="true"/>
   <member name="time" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_timestamp" optional="true"/>	    
   <member name="extension" type="nonBasic" nonBasicTypeName="io::cloudevents::Attributes" optional="true"/>
   <member name="datakey" type="nonBasic" nonBasicTypeName="io::cloudevents::ce_string" key="true"/>
   <member name="body" type="nonBasic" nonBasicTypeName="io::cloudevents::Data" optional="true"/>
</struct>
```

## 3 Data

Before encoding, the DDS serializer MUST first determine the runtime data type
of the content. This can be determined by examining by consulting the `datacontenttype`
and `datacontentencoding` attributes.

If the implementation determines that the type of the data is binary, the value
MUST be stored in the `body` field using the `bytes` type.

For other types, the implementation MUST translate the data value into a text or JSON
representation using the union type described for the message body.

## 4 Examples

The following table shows exemplary mappings:

| CloudEvents | Type   | Exemplary DDS Value                           |
| ----------- | ------ | ---------------------------------------------- |
| type        | string | `"org.cncf.cloudevents.example"`                      |
| specversion | string | `"1.0"`                                        |
| source      | string | `"urn:event:from:myapi/resource/123"`                                 |
| id          | string | `"b46cf653-d48a-4b90-8dfa-355c01061361"`                       |
| time        | string | `"sec: 1694707005, nanosec: 996000000"`                       |
| dataschema  | string | `"http://cloudevents.io/schema.json'"`    |
| contenttype | string | `"cloudevent/json"`                           |
| data        | string  | `"{"color":"red","x":120,"y":42,"shapesize":20}"`                    |
| contenttype | string | `"application/cloudevent+dds"`                           |
| data        | bytes  | `"data_base64":"anVzdCBub3JtYWwgdGV4dA=="`                      |

## References
- [OMG][omg] Object Management Group (OMG)
- [idl-spec] OMG Interface Definition Language (IDL) Specification 
- [DDS][dds-spec] OMG Data Distribution Service (DDS) Specification
- [dds-event-format] XML representation of DDS event format
- [RFC2119][rfc2119] Key words for use in RFCs to Indicate Requirement Levels


[ce]: ../spec.md
[omg]: https://www.omg.org/
[idl-spec]: https://www.omg.org/spec/IDL/4.2/PDF
[dds-spec]: https://www.omg.org/spec/DDS/1.4/PDF
[dds-event-format]: ./dds-format.xml
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3986-section41]: https://tools.ietf.org/html/rfc3986#section-4.1
[rfc3986-section43]: https://tools.ietf.org/html/rfc3986#section-4.3
[rfc3339]: https://tools.ietf.org/html/rfc3339
