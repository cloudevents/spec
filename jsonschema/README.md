# CloudEvents JSONSchema

This directory contains [JSONSchema](http://json-schema.org) for the
spec.

## Main

The core spec JSONSchema document is in [spec.json](spec.json) and
contains the core definitions for the json schema.

## Testing

The testing is done using a JSONSchema validator for the language of
your choice. Some examples are as follows.

### Python

The Python JSONSchema validator is the `jsonschema` package.

```
pip install jsonschema
jsonschema -i example.json spec.json
jsonschema -i missingdata.json spec.json
{u'eventID': u'B234-1234-1234', u'eventTime': u'2018-04-05T17:31:00Z', u'contentType': u'application/vnd.apache.thrift.b
inary', u'eventType': u'com.example.someevent', u'cloudEventsVersion': u'0.1', u'source': u'/mycontext', u'extensions':
{u'comExampleExtension': u'value'}}: u'data' is a required property
```
