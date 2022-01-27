# CloudEvents 中文规范

<!-- no verify-specs -->

![CloudEvents logo](https://github.com/cncf/artwork/blob/master/projects/cloudevents/horizontal/color/cloudevents-horizontal-color.png)

## Purpose/规范目的

This Chinese spec aims to provide a fast and brief introduction of CloudEvents
in Chinese for people who are new to CloudEvents.
Most of the content is translated from the original English version.
It is strongly recommended to read the English version if you find anything lost in translation.

这份中文规范是为了让更多刚接触CloudEvents的中国开发者，能在最短时间内对CloudEvents有一个全局的认识。本文档中的大多内容翻译自英文版的CloudEvents规范，如果你在阅读中发现一些难以理解的翻译，请参阅英文版文档。

## CloudEvents

事件(Events)在现代系统中无处不在。但不同的事件生产者往往用不同的规范来描述自己的事件。

对事件的统一描述的匮乏意味着开发者必须不断重新学习如何消费不同定义的事件。它同样限制了那些用来帮助事件数据完成跨环境传输的库(如SDKs)、工具(如事件路由器)和基础设施(如事件追踪系统)的发展。总体来看，这种匮乏严重阻碍了事件数据的可移植性和生产力。

CloudEvents是一个以通用格式来描述事件数据的标准。它提供了事件在服务、平台和系统中的互操作性。

从主流云厂商到SaaS公司，工业界对CloudEvents兴趣浓烈。CloudEvents项目由[云原生计算基金会](https://cncf.io)托管，于[2018/05/15](https://docs.google.com/presentation/d/1KNSv70fyTfSqUerCnccV7eEC_ynhLsm9A_kjnlmU_t0/edit#slide=id.g37acf52904_1_41) 成为云原生沙箱级项目。

## CloudEvents 文件

现有文件如下:

|                               |                                 最新版本                                 |                                      工作草案                                      |
| :---------------------------- | :-----------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------: |
| **核心标准:**       |
| CloudEvents                   |          [v1.0.2](../../spec.md)          |            [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md)             |
|                               |
| **可选标准:**  |
| AMQP Protocol Binding         | [v1.0.2](../../bindings//amqp-protocol-binding.md)  |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/amqp-protocol-binding.md)    |
| AVRO Event Format             |      [v1.0.2](../../formats/avro-format.md)       |         [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/avro-format.md)         |
| HTTP Protocol Binding         | [v1.0.2](../../bindings/http-protocol-binding.md)  |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/http-protocol-binding.md)    |
| JSON Event Format             |      [v1.0.2](../../formats/json-format.md)       |         [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/json-format.md)         |
| Kafka Protocol Binding        | [v1.0.2](../../bindings/kafka-protocol-binding.md) |   [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/kafka-protocol-binding.md)    |
| MQTT Protocol Binding         | [v1.0.2](../../bindings/mqtt-protocol-binding.md)  |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/mqtt-protocol-binding.md)    |
| NATS Protocol Binding         | [v1.0.2](../../bindings/nats-protocol-binding.md)  |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/nats-protocol-binding.md)    |
| WebSockets Protocol Binding   |                                        -                                        | [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/bindings/websockets-protocol-binding.md) |
| Protobuf Event Format         |                                                                                 | [v1.0-rc1](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/protobuf-format.md)                                  |
| Web hook                      |      [v1.0.2](../../http-webhook.md)      |        [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/http-webhook.md)         |
|                               |
| **附加文件:** |
| CloudEvents Adapters          |                                        -                                        |          [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/adapters.md)           |
| CloudEvents SDK Requirements  |                                        -                                        |             [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/SDK.md)             |
| Documented Extensions         |                                        -                                        |    [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/documented-extensions.md)    |
| Primer                        |         [v1.0.2](../../primer.md)         |           [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/primer.md)            |
| Proprietary Specifications    |                                        -                                        |      [WIP](https://github.com/cloudevents/spec/blob/main/cloudevents/proprietary-specs.md)      |

推荐先行阅读[入门文档](primer_CN.md)了解CloudEvents规范的目标和设计理念，再阅读[核心规范](spec_CN.md)。

由于并非所有事件生产者都默认生产符合CloudEvents规范的事件，因此可以用[CloudEvents适配器](https://github.com/cloudevents/spec/blob/main/cloudevents/adapters.md)
来将现有的事件与CloudEvents做适配。

## SDKs

除了上述文档，我们还提供了[SDK 提议](../../SDK.md)以及一些编程语言的SDK：

- [CSharp](https://github.com/cloudevents/sdk-csharp)
- [Go](https://github.com/cloudevents/sdk-go)
- [Java](https://github.com/cloudevents/sdk-java)
- [Javascript](https://github.com/cloudevents/sdk-javascript)
- [PHP](https://github.com/cloudevents/sdk-php)
- [PowerShell](https://github.com/cloudevents/sdk-powershell)
- [Python](https://github.com/cloudevents/sdk-python)
- [Ruby](https://github.com/cloudevents/sdk-ruby)
- [Rust](https://github.com/cloudevents/sdk-rust)

## 社区

在社区里，你可以了解到更多致力于搭建一个动态、云原生的生态系统的成员和组织。
他们不断尝试提升现有系统和CloudEvents间的互操作性和兼容性。

- 我们的 [管理](../../../community/GOVERNANCE.md) 文档。
- 如何通过 issues 和 PR 为我们做[贡献](../../../community/CONTRIBUTING.md) 。
- [贡献者](../../../community/contributors.md):
  是指那些帮助我们制定规范或是积极活跃在CloudEvents规范相关工作的成员和组织。
- [Demos & open source](../../../community/README.md)
  -- 如果你希望向我们分享关于你对CloudEvents的使用，请通过提交PR让我们看到。

## 步骤

CloudEvents项目 [旨在](primer_CN.md#design-goals)制定一个能够提升不同事件系统(如生产者和消费者)之间互操作性和兼容性
的[标准](spec_CN.md)。

为了完成这个目标，这个项目必须描述：

- 一系列能够提升互操作性的用来描述事件的属性
- 一个或多个通用架构，这些架构必须是当下活跃的或是正在计划被完成的
- 事件是如何在一种或多种协议下从生产者传输到消费者的
- 识别并解决任何能提升互操作性的问题

## 联系方式

邮件联系方式如下:

- 发送EMail至: [cncf-cloudevents](mailto:cncf-cloudevents@lists.cncf.io)
- 订阅地址: https://lists.cncf.io/g/cncf-cloudevents
- 存档地址: https://lists.cncf.io/g/cncf-cloudevents/topics

添加一个 #cloudevents Slack 频道：
[CNCF's Slack workspace](http://slack.cncf.io/).

SDK相关的评论和问题:

- 发送EMail至: [cncf-cloudevents-sdk](mailto:cncf-cloudevents-sdk@lists.cncf.io)
- 订阅地址: https://lists.cncf.io/g/cncf-cloudevents-sdk
- 存档地址: https://lists.cncf.io/g/cncf-cloudevents-sdk/topics
- Slack: #cloudeventssdk on [CNCF's Slack workspace](http://slack.cncf.io/)

## 会议时间

会议日期请查看[CNCF 公开活动日历](https://www.cncf.io/community/calendar/).
CloudEvents规范由
[CNCF Serverless Working Group](https://github.com/cncf/wg-serverless) 开发完成。
这个工作组每周四的上午9点(美国-太平洋时间)通过Zoom开展视频会议。
([World Time Zone Converter](http://www.thetimezoneconverter.com/?t=9:00%20am&tz=San%20Francisco&)):

查看
[meeting minutes doc](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
获得如何加入会议的最新信息。

历史会议录像在
[here](https://www.youtube.com/playlist?list=PLj6h78yzYM2Ph7YoBIgsZNW_RGJvNlFOt).

工作组会定期举办与主流会议一致的线下会议。查看
[meeting minutes doc](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
了解更多未来计划。

