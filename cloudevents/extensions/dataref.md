# Dataref (Claim Check Pattern)

As defined by the term [Data](../spec.md#data), CloudEvents MAY include
domain-specific information about the occurrence. When present, this information
will be encapsulated within `data`.
The `dataref` attribute MAY be used to reference another location where this
information is stored. The information, whether accessed via `data` or `dataref`
MUST be identical.

Both `data` and the `dataref` attribute MAY exist at the same time. A middleware
MAY drop `data` when the `dataref` attribute exists, it MAY add
the `dataref` attribute and drop the `data` attribute, or it MAY add the `data`
attribute by using the `dataref` attribute.

## Attributes

### dataref

- Type: `URI-reference`
- Description: A reference to a location where the event payload is stored. The
  location MAY not be accessible without further information (e.g. a pre-shared
  secret).

  Known as the "Claim Check Pattern", this attribute MAY be used for a variety
  of purposes, including:

  - If the [Data](../spec.md#data) is too large to be included in the
    message, the `data` is not present, and the consumer can retrieve it using
    this attribute.
  - If the consumer wants to verify that the [Data](../spec.md#data)
    has not been tampered with, it can retrieve it from a trusted source using
	this attribute.
  - If the [Data](../spec.md#data) MUST only be viewed by trusted
    consumers (e.g. personally identifiable information), only a trusted
	consumer can retrieve it using this attribute and a pre-shared secret.

  If this attribute is used, the information SHOULD be accessible long enough
  for all consumers to retrieve it, but MAY not be stored for an extended period
  of time.

- Constraints:
  - OPTIONAL

# Examples

The following example shows a CloudEvent in which the event producer has included
both `data` and `dataref` (serialized as JSON):

```JSON
{
    "specversion" : "1.0",
    "type" : "com.github.pull_request.opened",
    "source" : "https://github.com/cloudevents/spec/pull/123",
    "id" : "A234-1234-1234",
    "datacontenttype" : "text/xml",
    "data" : "<much wow=\"xml\"/>",
    "dataref" : "https://github.com/cloudevents/spec/pull/123/events/A234-1234-1234.xml"
}
```

The following example shows a CloudEvent in which a middleware has replaced the
`data` with a `dataref` (serialized as JSON):

```JSON
{
    "specversion" : "1.0",
    "type" : "com.github.pull_request.opened",
    "source" : "https://github.com/cloudevents/spec/pull/123",
    "id" : "A234-1234-1234",
    "datacontenttype" : "text/xml",
    "dataref" : "https://tenant123.middleware.com/events/data/A234-1234-1234.xml"
}
```
