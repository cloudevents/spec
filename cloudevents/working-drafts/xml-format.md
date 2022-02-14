# XML Event Format for CloudEvents

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
[Extensible Markup Language (XML)](xml-spec) documents.

* The [Attributes](#2-attributes) section describes the representation and
data type mappings for CloudEvents context attributes.

* The [Data](#3-data) section defines the container for the data portion of a
CloudEvent.

* The [Envelope](#4-envelope) section defines an XML element for CloudEvents
attributes and an associated media type.

* The [Batch](#5-xml-batch-format) section describes how multiple CloudEvents
can be packaged into a single XML document.

### 1.1. Conformance

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [RFC2119][rfc2119].

### 1.2 Approach

This XML representation used is deliberately verbose in favor of readability
and deterministic processing.

Preservation of type information for CloudEvent attributes is supported allowing
custom extensions to be communicated without type loss.

A schema-less approach has been taken favoring convention over rigid document
structure.

The namespace `http://cloudevents.io/xmlformat/V1` MUST be used.

When namespace prefixes are used a prefix of `ce` is preferred but MUST NOT
be expected from an XML document processing perspective.

An XML document preamble SHOULD be included to ensure deterministic processing.

## 2. Attributes

The CloudEvents type system is mapped to the XML schema types as follows :

| CloudEvents   |  XML Schema Type | Notes |
| :-------------| :--------------- | :---- |
| Boolean       | [xs:boolean][xml-primitives] | |
| Integer       | [xs:int][xml-primitives] | |
| String        | [xs:string][xml-primitives] | |
| Binary        | [xs:base64Binary][xml-primitives] | |
| URI           | [xs:anyURI][xml-primitives] following [RFC 3986][rfc3986]| |
| URI-reference | [xs:anyURI][xml-primitives] following [RFC 3986][rfc3986] | |
| Timestamp     | [xs:dateTime][xml-primitives] following [RFC 3339][rfc3339] | |

Each context attribute is represented as an XML element whose name MUST exactly match
that of a REQUIRED or OPTIONAL CloudEvent attribute, extension attribute names MUST
adhere to, and align with, the conventions in defined in the [cloud event specification][ce-spec].

See the [envelope](#4-envelope) for special handing of the `specversion` context attribute.

Extension attributes SHOULD be expressed with the appropriate `xsi:type` to allow them
to be exchanged without loss of type information. Extension attributes with no `xsi:type`
discriminator SHOULD be interpreted with an implied type of `xs:string`

``` xml
    ...
    <id>AAABBBCCCNNN0000</id>
    ..
    <time>2021-08-14T14:30:22-08:00</time>
    ..
    <myextension xsi:type="xs:string">my extension value</myextension>
    <myboolean xsi:type="xs:boolean">false</myboolean>
```

## 3. Data

The data portion of a CloudEvent follows a similar model to that employed by
the [JSON Format specification][json-format]. A `data` element is used to
encapsulate the payload and an `xsi:type` used to discrimate the payload
type.

### 3.1 Binary Data

MUST be carried in an element with an defined type of `xs:base64Binary`

``` xml
<data xsi:type="xs:base64Binary">.........</data>
```

### 3.2 Text Data

MUST be carried in an element with an defined type of `xs:string`

``` xml
<data xsi:type="xs:string">This is text</data>
```

### 3.3 XML Data

XML data MUST be carried in an element with a defined type of `xs:any`
allowing a single XML element (with any required namespace definitions)
to be represented.

``` xml
<data xsi:type="xs:any">
    <myData>
        ....
    </myData>  
</data>
```

## 4. Envelope

Each CloudEvent is wholly represented as an XML element `<event>` that
carries the `specversion` as an XML attribute value.

Such a representation MUST use the media type `application/cloudevents+xml`.

The enveloping element contains:

* A set of context attribute elements.
* An optional `data` element.

eg _(XML preamble and namespace definitions omitted for brevity)_:

``` xml
<event specversion="1.0">
    <time>2020-03-19T12:54:00-07:00</time>
    <datacontenttype>text/plain</datacontenttype>
    <id>000-1111-2222</id>
    <source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</source>
    <type>SOME.EVENT.TYPE</type>
    <myboolean xsi:type="xs:boolean">false</myboolean>
    <data xsi:type="xs:string">Now is the winter of our discount tents...</data>
</event>
```

## 5. XML Batch Format

In the _XML Batch Format_ several CloudEvents are batched into a single XML
element. The element comprises a list of elements in the XML Format.

Although the _XML Batch Format_ builds on top of the _XML Format_, it is
considered as a separate format: a valid implementation of the _XML Format_
doesn't need to support it. The _XML Batch Format_ MUST NOT be used when only
support for the _XML Format_ is indicated.

An XML Batch of CloudEvents MUST use the media type
`application/cloudevents-batch+xml`.

Example _(XML preamble and namespace definitions omitted for brevity)_:

``` xml
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

An example of an empty batch of CloudEvents (typically used in a response, but also valid in a request):

```xml
<batch />
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

[ce-spec]: ../spec.md
[ce-types]: ../spec.md#type-system
[xml-schema]: ./cloudevents.xsd
[xml-format]: ./xml-format.md
[json-format]: ../formats/json-format.md
[xml-spec]: https://www.w3.org/TR/2008/REC-xml-20081126/
[xml-primitives]: https://www.w3.org/TR/xmlschema-2/#built-in-primitive-datatypes
[rfc2119]: https://tools.ietf.org/html/rfc2119
[rfc3339]: https://www.ietf.org/rfc/rfc3339.txt
[rfc3986]: https://tools.ietf.org/html/rfc3986
