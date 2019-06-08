# Correlation 

This extension defines two attributes that can be included within a CloudEvent
to describe an identifier for correlating multiple events produced by one or more  
event sources in order to identify related events for auditing purposes. 

The `correlationid` attribute represents the value of this event's correlation 
attribute. The exact value and meaning of this attribute is defined by the 
`correlationtype` attribute. If the `correlationtype` is missing, event 
consumers MUST assume the default value of `uuid`. If the `correlationtype` is not 
defined in this specification, event consumers will need to have some out-of-band
communication with the event producer to understand how to interpret the value
of the attribute.

## Attributes

### correlationid

- Type: `String`
- Description: Value expressing the correlation identifier of the event. 
- Constraints:
  - REQUIRED, if this extension is used
  - MUST be a non-empty string in the format defined by the `correlationtype`. 

### correlationtype

- Type: `String`
- Description: Specifies the semantics of the `correlationid` attribute. See the
  [CorrelationType Values](#correlationtype-values) section for more information.
- Constraints:
  - OPTIONAL
  - If present, MUST be a non-empty string

## CorrelationType Values

This specification defines the following values for `correlationtype`. Additional
values MAY be defined by other specifications.

### UUID

If the `correlationtype` is set to `uuid`, the `correlationid` attribute has the
following semantics:

- The values of `correlationid` are string-encoded UUID. 

