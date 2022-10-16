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

### JSON Schema Version
This document does not specify exact json schema version to be used in the attrschema
definition.

[json-schema]: https://json-schema.org/