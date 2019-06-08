# Tenant Identifier 

This extension defines an attributes that can be included within a CloudEvent
to describe a tenant identifier for the event produced by an event source in 
multi-tenant systems. This attribute allow intermediaries to apply functional 
tenant-based logic, such as routing, scheduling or processing priorities, etc. 
without a need to understand the event body.   

The `tenantid` attribute represents the value of this event's Tenant Identifier 
attribute. 

## Attributes

### tenantid

- Type: `String`
- Description: Value expressing the tenant identifier of the event. 
- Examples:
  - A UUID  
- Constraints:
  - REQUIRED
  - MUST be a non-empty string in the format defined by the event producer. 

## Encoding

### In-memory formats

The Tenant Identifier extension uses the key `tenantid` for in-memory formats.

### Transport bindings

The Tenant Identifier extension does not customize any transport binding's 
storage for extensions.



