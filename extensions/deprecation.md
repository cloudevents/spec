# Deprecation

This extension defines two attributes that can be included within a CloudEvent
to indicate the deprecation of the event, delivery method, format or other
properties, such as the `schemaUrl`.

The `deprecated` attribute indicates deprecation of the event delivery. The
exact value and meaning of this attribute can be defined by the
`deprecatedType` attribute. As the specification of the attributes is left
intentionally open-ended, event consumers will need to have some out-of-band
communication with the event producer to understand how to interpret the value
of the attribute.

Event producers should use established or well-known patterns to facilitate
integration. In addition to or instead of integrating specific patterns,
consumers can also choose to alert on deprecation and rely on human
intervention.

## Attributes

### deprecated
* Type: `String`
* Description: Value indicating the deprecation of the delivery of these events
* Constraints
  * REQUIRED
  * MUST be a non-empty string
  * RECOMMENDED to provide information on type and timeline of deprecation and
    a way to find more information

### deprecatedType
* Type: `String`
* Description: Used to specify the format and meaning of the `deprecated`
  attribute
* Constraints:
  * OPTIONAL
  * If present, MUST be a non-empty string
