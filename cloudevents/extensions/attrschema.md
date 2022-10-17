# Attrschema Extension

## Attributes

#### attrschema

- Type: `URI`
- Description: Identifies the [Attrschema](#attrschema-document) that attributes of
  the current CloudEvent adhere to.
 
  Incompatible changes to the schema SHOULD be reflected by a different URI. See
  [Versioning of CloudEvents in the Primer](../primer.md#versioning-of-cloudevents)
  for more information.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty URI

<!--
If the future will require schema languages other than JSON Schema,
we can add an "attrschematype" attribute which will be defaulted to 
"jsonschema" and MAY hold additional types such as "xsd" which will indicate
different validation algorithms
-->
 
## Attrschema Document

Attrschema is a [JSON Schema][json-schema] document. This document asserts what the
CloudEvent context attributes MUST look like, ways to extract information from them, and
how to interact with them.

Although JSON Schema is used to validate JSON Documents, Attrschema provides an
algorithm to validate non-JSON formatted CloudEvents (XML, Protobuf, etc.) as well.

### Validation Algorithm
To validate a given CloudEvent the attrschema implementation MUST:

1. Create a map of all attributes of a given event, where the keys are the attribute
    names and the values are the attribute values
2. Strip all `null` OPTIONAL attributes from the event if present
3. All assumed values MUST be evaluated as-if the event was translated to another
   format. (`datacontenttype` assumptions of the JSON format for example)
4. Map all attribute values into the string canonical string representation as
   defined in the [CloudEvent spec](../spec.md#type-system) corresponding to 
   the attribute type.
5. Validate the given dictionary using Attrschema document and the rules defined by the
    [JSON Schema Spec][json-schema-spec] 
6. Attributes are considered adhering to the attrschema document if the JSON schema
   validation succeeded.

Note: in addition to the attribute schema, the usual CloudEvent attribute constraints
still apply, even though they are not expressed in the schema explicitly. 

### Type Annotation
Attrschema provides a way to annotate the defined attributes with the CloudEvent type
information using the `cetype` keyword.

This keyword indicates which of the standard CloudEvent types this attribute holds.

This keyword MUST be one of `boolean`, `integer`, `string`, `binary`, `uri`,
`uri-reference`, or `timestamp`.

When `uri` is used the `format` keyword MUST be set to `uri`
When `uri-reference` is used the `format` keyword MUST be set to `uri-reference`
When `timestamp` is used the `format` keyword MUST be set to `date-time`

#### Examples
Here is an example attrschema document
```json
{
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^A[0-9]{3}-[0-9]{4}-[0-9]{4}$"
    },
    "myattr": {
      "type": "string"
    },
    "datacontenttype": {
      "type": "string",
      "enum": [
         "text/xml",
         "application/json"
      ],
    }
  },
  "required": ["myattr"]
}
```
##### Json Event
```json
{
    "specversion" : "1.0",
    "type" : "com.github.pull_request.opened",
    "source" : "https://github.com/cloudevents/spec/pull",
    "id" : "A234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "myattr" : 5,
    "yourattr" : true ,
    "datacontenttype" : "text/xml",
    "data" : "<much wow=\"xml\"/>"
}
```
Notice that this event is adhering to the example attrschema even though the
`myattr` is of type `integer` and not `string`. The reason for it is
that the `myattr` value MUST be converted to the string representation
before validation. 

This is the actual JSON object which is being validated

```json
{
    "specversion" : "1.0",
    "type" : "com.github.pull_request.opened",
    "source" : "https://github.com/cloudevents/spec/pull",
    "id" : "A234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "myattr" : "5",
    "yourattr" : "true",
    "datacontenttype" : "text/xml",
}
```
Pay attention that the `data` property is missing from this object, and `myattr` and
`yourattr` were converted to the string representation.
 
#### XML Event
 ```xml
<?xml version="1.0" encoding="UTF-8"?>
<event xmlns="http://cloudevents.io/xmlformat/V1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
       xmlns:xs="http://www.w3.org/2001/XMLSchema" specversion="1.0" >
    <time>2020-03-19T12:54:00-07:00</time>
    <datacontenttype>application/json</datacontenttype>
    <id>A000-1111-2222</id>
    <source>urn:uuid:123e4567-e89b-12d3-a456-426614174000</source>
    <type>SOME.EVENT.TYPE</type>
    <data xsi:type="xs:string">{ "salutation": "Good Morning", "text": "hello world" }</data>
</event>
```
This event will be transformed to 
```json
{
    "specversion" : "1.0",
    "time" : "2020-03-19T12:54:00-07:00",
    "datacontenttype" : "application/json",
    "id" : "A000-1111-2222",
    "source" : "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
    "type" : "SOME.EVENT.TYPE",
}
```
But will fail validation because `myattr` is not present

### JSON Schema Version
This document does not specify exact json schema version to be used in the attrschema
definition.

[json-schema]: https://json-schema.org/
[json-schema-spec]: https://json-schema.org/draft/2020-12/json-schema-core.html