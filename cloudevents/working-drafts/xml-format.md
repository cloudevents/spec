# XML Event Format for CloudEvents - Version 1.0.3-wip

## Abstract

This format specification for CloudEvents defines how events are expressed
in XML documents.

## Status of this document

This document is a working draft.

## Table of Contents

1. [Introduction](#1-introduction)
2. [Attributes](#2-attributes)
3. [Data](#3-data)
4. [Envelope](#4-envelope)
5. [XML Batch Format](#5-xml-batch-format)
6. [Examples](#6-examples)

## 1. Introduction

[CloudEvents][ce-spec] is a standardized and protocol-agnostic definition of the
structure and metadata description of events. This specification defines how
elements defined in the CloudEvents specification are to be represented using
[Extensible Markup Language (XML)][xml-spec] elements.

* The [Attributes](#2-attributes) section describes the representation and
data type mappings for CloudEvents context attributes.

* The [Data](#3-data) section defines the container for the data portion of a
CloudEvent.

* The [Envelope](#4-envelope) section defines an XML element to contain CloudEvent
context attributes and data.

* The [Batch](#5-xml-batch-format) section describes how multiple CloudEvents
can be packaged into a single XML element.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2 Approach

The XML representation used is deliberately verbose in favor of readability
and deterministic processing.

Preservation of type information for CloudEvent attributes is supported allowing
custom extensions to be communicated without type loss.

A schema-less approach has been taken favoring convention over rigid document
structure.

The namespace `http://cloudevents.io/xmlformat/V1` MUST be used.

When namespace prefixes are used a prefix of `ce` is preferred but MUST NOT
be expected from an XML document processing perspective.

Where an event (or batch of events) is represented as a complete XML document,
an XML document preamble SHOULD be included to ensure deterministic processing.

XML comments are permitted anywhere within an XML representation of a
CloudEvent or CloudEvent batch. Comments MUST be ignored during processing, except
for the child element of a `<data>` element containing [XML element data](#33-xml-element-data),
where all nodes MUST be preserved.

CDATA nodes and regular text nodes MUST be treated interchangeably during processing,
except for the child element `<data>` element containing [XML element data](#33-xml-element-data),
where all nodes MUST be preserved.

XML elements in namespaces other than `http://cloudevents.io/xmlformat/V1`, and
XML attributes other than those described in this specification MAY appear within an XML
representation of a CloudEvent or CloudEvent batch. These SHOULD be ignored during
CloudEvent processing, except for the child element of a `<data>` element containing
[XML element data](#33-xml-element-data), where all nodes MUST be preserved.

## 2. Attributes

The CloudEvents type system is mapped to a set of CloudEvent specific
type designators as follows :

| CloudEvents Type  |  XML Format Type | XML Schema Type | Notes |
| :-----------------| :----------------| :--------------- | :---- |
| Boolean       | ce:boolean | [xs:boolean][xml-primitives] | `true` or `false` |
| Integer       | ce:integer | [xs:int][xml-primitives] | |
| String        | ce:string | [xs:string][xml-primitives] | |
| Binary        | ce:binary | [xs:base64Binary][xml-primitives] |  |
| URI           | ce:uri | [xs:anyURI][xml-primitives] following [RFC 3986][rfc3986]| |
| URI-reference | ce:uriRef | [xs:anyURI][xml-primitives] following [RFC 3986][rfc3986] | |
| Timestamp     | ce:timestamp | [xs:dateTime][xml-primitives] following [RFC 3339][rfc3339] | |

Each CloudEvent context attribute MUST be represented as an XML element whose local
name exactly matches that of the attribute.

See the [envelope](#4-envelope) for special handing of the `specversion` context attribute.

Extension context attributes MUST be decorated with the appropriate CloudEvent type format
designators using an `xsi:type` XML attribute, this allows them to be exchanged
without loss of type information.

An XML element representing a core context attribute MAY be decorated with
an `xsi:type` XML attribute. If present, this designator MUST match that of the type specified
by the [CloudEvent context attributes][ce-attrs].

An XML element representing a context attribute MUST NOT contain any child elements. The text
within an XML element representing a context attribute MUST NOT contain any line breaks.
When processing the text, the attribute value MUST be parsed without discarding any other
whitespace. (For example, `<myextension xsi:type="ce:string">  text  </myextension>` represents
an extension attribute value with leading and trailing whitespace, whereas
`<myextension xsi:type="ce:integer">  10  </myextension>` is invalid as the textual representation
of an Integer attribute never contains whitespace.)

No other XML element attributes are expected, if present they MUST be ignored during
processing.

``` xml
    ...
    <id>AAABBBCCCNNN0000</id>
    ..
    <time>2021-08-14T14:30:22-08:00</time>
    ..
    <myextension xsi:type="ce:string">my extension value</myextension>
    <myboolean xsi:type="ce:boolean">false</myboolean>
```

## 3. Data

The data portion of a CloudEvent follows a similar model to that employed by
the [JSON Format specification][json-format]. A `<data>` element MUST be used to
encapsulate the payload.

An `xsi:type` is used to discrimate the payload type and MUST be present.

The `<data>` element MUST NOT occur more than once within an `<event>` element.

The following data representations are supported:

### 3.1 Binary Data

Binary data MUST be carried in an element with a defined type of `xs:base64Binary`
and encoded appropriately. The element MUST NOT contain any child elements.

Example:

``` xml
<data xsi:type="xs:base64Binary">.........</data>
```

### 3.2 Text Data

Text MUST be carried in an element with a defined type of `xs:string`.
The element MUST NOT contain any child elements.

Example:

``` xml
<data xsi:type="xs:string">This is text</data>
```

### 3.3 XML Element Data

XML element data MUST be carried in an element with a defined type of `xs:any` with
exactly one child XML element (with any mandatory namespace definitions).

All XML nodes (including comments and CDATA nodes) within the child XML element MUST
be preserved during processing.

The `<data>` XML element MUST NOT contain any direct child text nodes with
non-whitespace content. There are no restrictions on the content of the
child XML element.

Example:

``` xml
<data xsi:type="xs:any">
    <myData xmlns="http://my.org/namespace">
        ....
    </myData>  
</data>
```

## 4. Envelope

Each CloudEvent is wholly represented as an `<event>` XML element that
MUST carry the `specversion` as an XML attribute value.

Such a representation MUST use the media type `application/cloudevents+xml`.

The enveloping element contains:

* A set of CloudEvent context attribute XML elements.
* An OPTIONAL `<data>` XML element.

The `<event>` element MUST NOT contain any direct child text nodes with non-whitespace
content.

Example _(XML preamble and namespace definitions omitted for brevity)_:

``` xml
<event specversion="1.0">
    <time>2020-03-19T12:54:00-07:00</time>
    <datacontenttype>text/plain</datacontenttype>
    <id>000-1111-2222</id>
    <source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</source>
    <type>SOME.EVENT.TYPE</type>
    <myboolean xsi:type="ce:boolean">false</myboolean>
    <data xsi:type="xs:string">Now is the winter of our discount tents...</data>
</event>
```

## 5. XML Batch Format

In the _XML Batch Format_ several CloudEvents are batched into a single XML
`<batch>` element. The element comprises a list of elements in the XML Format.

The `<batch>` element MUST NOT contain any direct child text nodes with non-whitespace
content.

The `<batch>` element MUST NOT contain any direct child elements in
the namespace `http://cloudevents.io/xmlformat/V1` except `<event>`
elements.

An XML Batch of CloudEvents MUST use the media type
`application/cloudevents-batch+xml`.

Example _(XML preamble and namespace definitions omitted for brevity)_:

```xml
<batch>
    <event specversion="1.0">
       ....
    </event>
    <event specversion="1.0">
       ....
    </event>
    ....
</batch>
```

## 6. Examples

### 6.1 CloudEvent with PNG image data

```xml
<?xml version="1.0" encoding="UTF-8"?>
<event xmlns="http://cloudevents.io/xmlformat/V1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
       xmlns:xs="http://www.w3.org/2001/XMLSchema" specversion="1.0" >
    <time>2020-03-19T12:54:00-07:00</time>
    <datacontenttype>image/png</datacontenttype>
    <id>000-1111-2222</id>
    <source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</source>
    <type>SOME.EVENT.TYPE</type>
    <data xsi:type="xs:base64Binary">... Base64 encoded data...</data>
</event>
```

### 6.2 CloudEvent with JSON event data

```xml
<?xml version="1.0" encoding="UTF-8"?>
<event xmlns="http://cloudevents.io/xmlformat/V1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
       xmlns:xs="http://www.w3.org/2001/XMLSchema" specversion="1.0" >
    <time>2020-03-19T12:54:00-07:00</time>
    <datacontenttype>application/json</datacontenttype>
    <id>000-1111-2222</id>
    <source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</source>
    <type>SOME.EVENT.TYPE</type>
    <data xsi:type="xs:string">{ "salutation": "Good Morning", "text": "hello world" }</data>
</event>
```

### 6.3 CloudEvent with XML event data

#### 6.3.1 Locally namespaced event data

```xml
<?xml version="1.0" encoding="UTF-8"?>
<event xmlns="http://cloudevents.io/xmlformat/V1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
       xmlns:xs="http://www.w3.org/2001/XMLSchema" specversion="1.0" >
    <time>2020-03-19T12:54:00-07:00</time>
    <datacontenttype>application/xml</datacontenttype>
    <id>000-1111-2222</id>
    <source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</source>
    <type>SOME.EVENT.TYPE</type>
    <data xsi:type="xs:any">
        <geo:Location xmlns:geo="http://someauthority.example/">
            <geo:Latitude>51.509865</geo:Latitude>
            <geo:Longitude>-0.118092</geo:Longitude>
        </geo:Location>
    </data>
</event>
```

#### 6.3.2 Explicit namespacing

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ce:event xmlns:ce="http://cloudevents.io/xmlformat/V1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:geo="http://someauthority.example/"
          specversion="1.0" >
    <ce:time>2020-03-19T12:54:00-07:00</ce:time>
    <ce:datacontenttype>application/xml</ce:datacontenttype>
    <ce:id>000-1111-2222</ce:id>
    <ce:source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</ce:source>
    <ce:type>SOME.EVENT.TYPE</ce:type>
    <ce:data xsi:type="xs:any">
        <geo:Location>
            <geo:Latitude>51.509865</geo:Latitude>
            <geo:Longitude>-0.118092</geo:Longitude>
        </geo:Location>
    </ce:data>
</ce:event>
```

#### 6.3.3 ISO 20022 Usage Example

[ISO 20022][iso-20022] is an XML based messaging standard used in the financial industry; this is a
non-normative example.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<event xmlns="http://cloudevents.io/xmlformat/V1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
       xmlns:xs="http://www.w3.org/2001/XMLSchema" specversion="1.0" >
    <time>2022-02-22T15:12:00-08:00</time>
    <datacontenttype>application/xml</datacontenttype>
    <id>000-1111-2222</id>
    <source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</source>
    <type>com.mybank.pain.001.001.03</type>
    <data xsi:type="xs:any">
        <Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03">
            <CstmrCdtTrfInitn>
            <GrpHdr>
                <MsgId>ABC/060928/CCT001</MsgId>
                <CreDtTm>2022-02-22T14:07:00</CreDtTm>
                <NbOfTxs>3</NbOfTxs>
                <CtrlSum>2400.56</CtrlSum>
                <InitgPty>
                    <Nm>Cobelfac</Nm>
                    <Id>
                        <OrgId>
                            <Othr>
                                <Id>0468651441</Id>
                                <Issr>KBO-BCE</Issr>
                            </Othr>
                        </OrgId>
                    </Id>
                </InitgPty>
            </GrpHdr>
            <PmtInf>
                <PmtInfId> ABC/4560/2008-09-25</PmtInfId>
                <PmtMtd>TRF</PmtMtd>
                <BtchBookg>false</BtchBookg>

            <!-- Content omitted for brevity -->

            </PmtInf>
        </Document>
    </data>
</event>
```

#### 6.3.4 Batch Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<batch xmlns="http://cloudevents.io/xmlformat/V1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
       xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <event specversion="1.0" >
        <time>2020-03-19T12:54:00-07:00</time>
        <datacontenttype>image/png</datacontenttype>
        <id>000-1111-2222</id>
        <source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</source>
        <type>SOME.EVENT.TYPE</type>
        <data xsi:type="xs:base64Binary">... Base64 encoded data...</data>
    </event>
    <event specversion="1.0" >
        <time>2020-03-19T12:59:00-07:00</time>
        <datacontenttype>image/png</datacontenttype>
        <id>000-1111-3333</id>
        <source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</source>
        <type>SOME.EVENT.TYPE</type>
        <data xsi:type="xs:base64Binary">... Base64 encoded data...</data>
    </event>
    .....
</batch>
```

[ce-spec]: ../spec.md
[ce-types]: ../spec.md#type-system
[ce-attrs]: ../spec.md#context-attributes
[xml-format]: ./xml-format.md
[json-format]: ../formats/json-format.md
[xml-spec]: https://www.w3.org/TR/2008/REC-xml-20081126/
[xml-primitives]: https://www.w3.org/TR/xmlschema-2/#built-in-primitive-datatypes
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3339]: https://www.ietf.org/rfc/rfc3339.txt
[rfc3986]: https://tools.ietf.org/html/rfc3986
[iso-20022]: https://www.iso20022.org
