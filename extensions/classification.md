# Information Classification

As part of ISO27001 control objective A8.2 aims to address 'Information Classification' whereby information and data in an organisation is properly managed, including classifcation in relation to sensitivity of the data, legislation etc. A.8.2.2 requires that electronic assets should be 'labelled', and this extension allows the `data` of cloudevents to be appropriately labelled with the `classification` of the event being shared.

Organisations will typically have their own internal Information Management policies and standards that might address these control objectives differently, however this extension should provide a consistent framework for labelling events, where organisation can use their own internal values for `classification`.

This extension is not opinionated on how this classification will be used and does for example imply different encryption schemes etc.

## Attributes

### classification

- Type: `String`
- Description: The `classification` of the `data`. The value SHOULD be expressed in uppercase.
- Constraints:
  - REQUIRED
  - MUST be a non-empty string (TBD)

# Examples

The following example shows a CloudEvent the producer has labelled as PUBLIC:

```JSON
{
    "specversion" : "1.0",
    "type" : "com.github.pull_request.opened",
    "source" : "https://github.com/cloudevents/spec/pull/123",
    "id" : "A234-1234-1234",
    "datacontenttype" : "text/xml",
    "classification" : "PUBLIC",
    "data" : "<much wow=\"xml\"/>",
}
```
