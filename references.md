# References

Examples of current event formats that exist today.

### Microsoft - Event Grid
```
{
    "topic":"/subscriptions/{subscription-id}",        "subject":"/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.EventGrid/eventSubscriptions/LogicAppdd584bdf-8347-49c9-b9a9-d1f980783501",
    "eventType":"Microsoft.Resources.ResourceWriteSuccess",
    "eventTime":"2017-08-16T03:54:38.2696833Z",
    "id":"25b3b0d0-d79b-44d5-9963-440d4e6a9bba",
    "data": {
        "authorization":"{azure_resource_manager_authorizations}",
        "claims":"{azure_resource_manager_claims}",
        "correlationId":"54ef1e39-6a82-44b3-abc1-bdeb6ce4d3c6",
        "httpRequest":"",
        "resourceProvider":"Microsoft.EventGrid",
        "resourceUri":"/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.EventGrid/eventSubscriptions/LogicAppdd584bdf-8347-49c9-b9a9-d1f980783501",
        "operationName":"Microsoft.EventGrid/eventSubscriptions/write",
        "status":"Succeeded",
        "subscriptionId":"{subscription-id}",
        "tenantId":"72f988bf-86f1-41af-91ab-2d7cd011db47"
    }
}
```
[Documentation](https://docs.microsoft.com/en-us/azure/event-grid/event-schema)

### Google - Cloud Functions (potential future)
```
{
  "data": {
    "@type": "types.googleapis.com/google.pubsub.v1.PubsubMessage",
    "attributes": {
      "foo": "bar",
     },
     "messageId": "12345",
     "publishTime": "2017-06-05T12:00:00.000Z",
     "data": "somebase64encodedmessage"
  },
  "context": {
    "eventId": "12345",
    "timestamp": "2017-06-05T12:00:00.000Z",
    "eventTypeId": "google.pubsub.topic.publish",
    "resource": {
      "name": "projects/myProject/topics/myTopic",
      "service": "pubsub.googleapis.com"
    }
  }
}
```

### AWS - SNS
```
{
  "Records": [
    {
      "EventVersion": "1.0",
      "EventSubscriptionArn": eventsubscriptionarn,
      "EventSource": "aws:sns",
      "Sns": {
        "SignatureVersion": "1",
        "Timestamp": "1970-01-01T00:00:00.000Z",
        "Signature": "EXAMPLE",
        "SigningCertUrl": "EXAMPLE",
        "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
        "Message": "Hello from SNS!",
        "MessageAttributes": {
          "Test": {
            "Type": "String",
            "Value": "TestString"
          },
          "TestBinary": {
            "Type": "Binary",
            "Value": "TestBinary"
          }
        },
        "Type": "Notification",
        "UnsubscribeUrl": "EXAMPLE",
        "TopicArn": topicarn,
        "Subject": "TestInvoke"
      }
    }
  ]
}
```
[Documentation](http://docs.aws.amazon.com/lambda/latest/dg/eventsources.html)

### AWS - Kinesis
```
{
  "Records": [
    {
      "eventID": "shardId-000000000000:49545115243490985018280067714973144582180062593244200961",
      "eventVersion": "1.0",
      "kinesis": {
        "partitionKey": "partitionKey-3",
        "data": "SGVsbG8sIHRoaXMgaXMgYSB0ZXN0IDEyMy4=",
        "kinesisSchemaVersion": "1.0",
        "sequenceNumber": "49545115243490985018280067714973144582180062593244200961"
      },
      "invokeIdentityArn": identityarn,
      "eventName": "aws:kinesis:record",
      "eventSourceARN": eventsourcearn,
      "eventSource": "aws:kinesis",
      "awsRegion": "us-east-1"
    }
  ]
}
```

### IBM - OpenWhisk - Web Action Event
```
{
  "__ow_method": "post",
  "__ow_headers": {
    "accept": "*/*",
    "connection": "close",
    "content-length": "4",
    "content-type": "text/plain",
    "host": "172.17.0.1",
    "user-agent": "curl/7.43.0"
  },
  "__ow_path": "",
  "__ow_body": "Jane"
}
```

### OpenStack - Audit Middleware - Event
```
{
  "typeURI": "http://schemas.dmtf.org/cloud/audit/1.0/event",
  "id": "d8304637-3f63-5092-9ab3-18c9781871a2",
  "eventTime": "2018-01-30T10:46:16.740253+00:00",
  "action": "delete",
  "eventType": "activity",
  "outcome": "success",
  "reason": {
    "reasonType": "HTTP",
    "reasonCode": "204"
  },
  "initiator": {
    "typeURI": "service/security/account/user",
    "name": "user1",
    "domain": "domain1",
    "id": "52d28347f0b4cf9cc1717c00adf41c74cc764fe440b47aacb8404670a7cd5d22",
    "host": {
      "address": "127.0.0.1",
      "agent": "python-novaclient"
    },
    "project_id": "ae63ddf2076d4342a56eb049e37a7621"
  },
  "target": {
    "typeURI": "compute/server",
    "id": "b1b475fc-ef0a-4899-87f3-674ac0d56855"
  },
  "observer": {
    "typeURI": "service/compute",
    "name": "nova",
    "id": "1b5dbef1-c2e8-5614-888d-bb56bcf65749"
  },
  "requestPath": "/v2/ae63ddf2076d4342a56eb049e37a7621/servers/b1b475fc-ef0a-4899-87f3-674ac0d56855"
}
```
[Documentation](https://github.com/openstack/pycadf/blob/master/doc/source/event_concept.rst)
