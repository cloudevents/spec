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
CloudEvent context attributes must look like, ways to extract information from them, and
how to interact with them.

Although JSON Schema is used to validate JSON Documents, Attrschema provides an
algorithm to validate non-JSON formatted CloudEvents (XML, Protobuf, etc.) as well.

### Validation Algorithm
To validated a given CloudEvent the attrschema implementation MUST:

1. Create a map of all attributes of a given event, where the keys are the attribute
    names and the values are the attribute values
2. Strip all `null` OPTIONAL attributes from the event if present
3. Map all attribute values into the string canonical string representation as
   defined in the [CloudEvent spec](../spec.md#type-system) corresponding to 
   the attribute type.
4. Validate the given dictionary using Attrschema document and the rules defined by the
    [JSON Schema Spec][json-schema-spec] 
5. Attributes are considered adhering to the attrschema document if the JSON schema
   validation succeeded.

Note: in addition to the attribute schema, the usual CloudEvent attribute constraints
still apply, even though they are not expressed in the schema explicitly. 

#### Examples
Here is an example attrschema
```json
{
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^A[0-9]{3}-[0-9]{4}-[0-9]{4}$"
    },
    "comexampleothervalue": {
      "type": "string"
    },
    "datacontenttype": {
      "const": "text/xml"
    }
  }
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
   
### JSON Schema Version
This document does not specify exact json schema version to be used in the attrschema
definition.

[json-schema]: https://json-schema.org/
[json-schema-spec]: https://json-schema.org/draft/2020-12/json-schema-core.html