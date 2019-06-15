# Correlation 

This extension defines two attributes that can be included within a CloudEvent
to describe an identifier for correlating multiple events produced by one or more  
event sources in order to identify related events for auditing purposes. 

The `correlationid` attribute represents the value of this event's correlation 
attribute. The exact value and meaning of this attribute is defined by the 
event producer.  

## Attributes

### correlationid

- Type: `String`
- Description: Value expressing the correlation identifier of the event.  
- Examples:
  - A UUID  
- Constraints:
  - REQUIRED;
  - MUST be a non-empty string. 

## Encoding

### In-memory formats

The Correlation extension uses the key `correlationid` for in-memory formats.

### Transport bindings

The Correlation extension does not customize any transport binding's storage for
extensions.


