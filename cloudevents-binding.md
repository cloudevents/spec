<!--
---
linkTitle: "CloudEvents Binding"
weight: 100
hide_summary: true
icon: "fa-solid fa-arrow-right-arrow-left"
description: >
   CloudEvents Binding for CDEvents
---
-->
# CloudEvents Binding for CDEvents  <!-- omit in toc -->

## Abstract <!-- omit in toc -->

The CloudEvents Binding for CDEvents defines how CDEvents are mapped to CloudEvents headers and body.

## Table Of Contents <!-- omit in toc -->

<!-- toc -->
- [CloudEvents Context](#cloudevents-context)
  - [specversion](#specversion)
  - [id](#id)
  - [source](#source)
  - [type](#type)
  - [subject](#subject)
  - [time](#time)
  - [datacontenttype](#datacontenttype)
  - [dataschema](#dataschema)
- [CloudEvents Data](#cloudevents-data)
  - [Examples](#examples)
<!-- /toc -->

## CloudEvents Context

The CloudEvents context is built by the event producer using some of the data
from the [CDEvents context](spec.md#context).

### specversion

The [CloudEvents `specversion`][ce-version] MUST be set to `1.0`.

### id

The [CloudEvents `id`][ce-id] MUST be set to the CDEvents [`id`](spec.md#id).

### source

The [CloudEvents `source`][ce-source] MUST be set to the CDEvents [`source`](spec.md#source).

### type

The [CloudEvents `type`][ce-type] MUST be set to the [`type`](spec.md#type) of the CDEvent.

### subject

The [CloudEvents `subject`][ce-subject] MUST be set to the [subject `id`](spec.md#subjectid) of the CDEvent.
__Note__: since the *subject* is mandatory in CDEvents, the `subject` in the CloudEvents format will always be set - even if it's not mandated by the CloudEvents specification.

### time

The [CloudEvents `time`][ce-time] MUST be set to the [`timestamp`](spec.md#timestamp) of the CDEvent. The CloudEvents specification allows for `time` to be set to either the current time or the time of the occurrence, but it requires all producers to be chose the same option. CDEvents requires all producers to use the `timestamp` from the CDEvent to meet the CloudEvents specification.

### datacontenttype

The [CloudEvents `datacontenttype`][ce-contenttype] is optional, its use depends on the specific CloudEvents binding and mode in use. See the [event data](#cloudevents-data) section for more details.

### dataschema

The [CloudEvents `dataschema`][ce-dataschema] is MAY be set to a URL that points to the event data schema included in this specification.

## CloudEvents Data

The content and format of the event data depends on the specific CloudEvents binding in use. All the examples, unless otherwise stated, refer to the[HTTP binding][ce-http-binding] in [binary content mode][ce-binary]. In this format, the CloudEvents context is stored in HTTP headers.

The [CloudEvents Event Data][ce-eventdata] MUST include the full CDEvents, i.e.
[`context`](spec.md#cdevents-context), [`subject`](spec.md#cdevents-subject)
and any [custom data](spec.md#cdevents-custom-data), rendered as JSON in the
format specified by the [schema](./schemas/) for the event type.

[Custom data](spec.md#cdevents-custom-data) of type "application/json" MUST be
embedded as is in the [`customData`](spec.md#customdata) field. Data with any other
content-type MUST be base64 encoded and set as value for the
[`customData`](spec.md#customdata) field.

In CloudEvents HTTP binary mode, the `Content-Type` HTTP header MUST be set to `application/json`. In CloudEvents HTTP structured mode, the same information is carried in the CloudEvents context field `datacontenttype`.

### Examples

Full example of a CDEvents transported through a CloudEvent in HTTP *binary* mode:

```json
POST /sink HTTP/1.1
Host: cdevents.example.com
ce-specversion: 1.0
ce-type: dev.cdevents.taskrun.started.0.1.1
ce-time: 2018-04-05T17:31:00Z
ce-id: A234-1234-1234
ce-source: /staging/tekton/
ce-subject: /namespace/taskrun-123
Content-Type: application/json; charset=utf-8
Content-Length: nnnn

{
   "context": {
      "specversion": "0.6.0-draft",
      "id" : "A234-1234-1234",
      "source" : "/staging/tekton/",
      "type" : "dev.cdevents.taskrun.started.0.1.1",
      "timestamp" : "2018-04-05T17:31:00Z",
   }
   "subject" : {
      "id": "/namespace/taskrun-123",
      "content": {
         "task": "my-task",
         "uri": "/apis/tekton.dev/v1beta1/namespaces/default/taskruns/my-taskrun-123"
         "pipelineRun": {
            "id": "/somewherelse/pipelinerun-123",
            "source": "/staging/jenkins/"
         }
      }
   }
}
```

[ce-id]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id
[ce-version]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#specversion
[ce-source]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#source-1
[ce-type]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#type
[ce-subject]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#subject
[ce-time]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#time
[ce-contenttype]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#datacontenttype
[ce-dataschema]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#dataschema
[ce-http-binding]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md
[ce-binary]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md#31-binary-content-mode
[ce-eventdata]: https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#event-data
