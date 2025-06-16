# OPC Unified Architecture

This extension defines the mapping of [OPC UA](https://reference.opcfoundation.org/Core/Part1/v105/docs/)
[PubSub](https://reference.opcfoundation.org/Core/Part14/v105/docs/) dataset to
CloudEvents to allow seamless routing of OPC UA dataset messages via different
protocols, it therefore provides a recommendation to map known REQUIRED and
OPTIONAL attributes using other extensions as well as defines its own extension
attributes.

## Notational Conventions

As with the main [CloudEvents specification](../spec.md), the key words "MUST",
"MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT",
"RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as
described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

However, the scope of these key words is limited to when this extension is used.
For example, an attribute being marked as "REQUIRED" does not mean it needs to
be in all CloudEvents, rather it needs to be included only when this extension
is being used.

## Attributes

### opcuametadatamajorversion

- Type: `Integer`
- Description: Links dataset message to the current version of the metadata.
- Constraints
  - OPTIONAL but MUST NOT be present if `dataschema` is used

### opcuametadataminorversion

- Type: `Integer`
- Description: Links dataset message to the current version of the metadata.
- Constraints
  - OPTIONAL but MUST NOT be present if `dataschema` is used

### opcuastatus

- Type: `Integer`
- Description: Defines the overall status of the data set message.
- Constraints
  - OPTIONAL
  - REQUIRED if status is not _Good_
  - MAY be omitted if status is _Good_
