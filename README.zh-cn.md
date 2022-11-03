# CloudEvents

<!-- no verify-specs -->

![CloudEvents logo](https://github.com/cncf/artwork/blob/master/projects/cloudevents/horizontal/color/cloudevents-horizontal-color.png)

[![CLOMonitor](https://img.shields.io/endpoint?url=https://clomonitor.io/api/projects/cncf/cloudevents/badge)](https://clomonitor.io/projects/cncf/cloudevents)

语言: [English](README.md) | [简体中文](README.zh-cn.md)

事件到处都是。然而，事件生产者倾向于描述事件
不同。

缺乏描述事件的通用方法意味着开发人员必须不断地
重新学习如何使用事件。这也限制了图书馆的潜力，
辅助跨界传递事件数据的工具和基础设施
环境，如 sdk、事件路由器或跟踪系统。可移植性和
我们可以从事件数据中获得的生产力总体上受到了阻碍。

CloudEvents 是以通用格式描述事件数据的规范
提供跨服务、平台和系统的互操作性。

CloudEvents 已经收到了大量的行业兴趣，从主要的
为流行的 SaaS 公司提供云服务。CloudEvents 由
[云原生计算基础](https://cncf.io) (CNCF) 被批准为
一个云原生沙盒级别的项目
[2018 年 5 月 15 日](https://docs.google.com/presentation/d/1KNSv70fyTfSqUerCnccV7eEC_ynhLsm9A_kjnlmU_t0/edit#slide=id.g37acf52904_1_41) 作为一个
孵化器项目 [2019 年 10 月 24 日](https://github.com/cncf/toc/pull/297).

## CloudEvents 文档

|                                                  |                                                 最新版本                                                 |                          工作草案                          |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------: |
| **核心规范:**                                    |
| CloudEvents                                      |              [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md)               |                 [WIP](cloudevents/spec.md)                 |
|                                                  |
| **可选规格:**                                    |
| AMQP 协议绑定                                    | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/amqp-protocol-binding.md)  |    [WIP](cloudevents/bindings/amqp-protocol-binding.md)    |
| AVRO 事件格式                                    |       [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md)       |         [WIP](cloudevents/formats/avro-format.md)          |
| HTTP 协议绑定                                    | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md)  |    [WIP](cloudevents/bindings/http-protocol-binding.md)    |
| JSON 事件格式                                    |       [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md)       |         [WIP](cloudevents/formats/json-format.md)          |
| Kafka 协议绑定                                   | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md) |   [WIP](cloudevents/bindings/kafka-protocol-binding.md)    |
| MQTT 协议绑定                                    | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/mqtt-protocol-binding.md)  |    [WIP](cloudevents/bindings/mqtt-protocol-binding.md)    |
| NATS 协议绑定                                    | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/nats-protocol-binding.md)  |    [WIP](cloudevents/bindings/nats-protocol-binding.md)    |
| WebSockets 协议绑定                              |                                                    -                                                     | [WIP](cloudevents/bindings/websockets-protocol-binding.md) |
| Protobuf 事件格式                                |     [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/protobuf-format.md)     |       [WIP](cloudevents/formats/protobuf-format.md)        |
| XML 事件格式                                     |                                                    -                                                     |      [WIP](cloudevents/working-drafts/xml-format.md)       |
| Web hook                                         |          [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/http-webhook.md)           |             [WIP](cloudevents/http-webhook.md)             |
|                                                  |
| **附加的文档:**                                  |
| CloudEvents Primer                               |             [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/primer.md)              |                [WIP](cloudevents/primer.md)                |
| [CloudEvents Adapters](cloudevents/adapters.md)  |                                                    -                                                     |            [不是版本](cloudevents/adapters.md)             |
| [CloudEvents SDK 要求](cloudevents/SDK.md)       |                                                    -                                                     |               [不是版本](cloudevents/SDK.md)               |
| [记录扩展](cloudevents/documented-extensions.md) |                                                    -                                                     |      [不是版本](cloudevents/documented-extensions.md)      |
| [专有的规范](cloudevents/proprietary-specs.md)   |                                                    -                                                     |        [不是版本](cloudevents/proprietary-specs.md)        |

## 其他规范

|                 | 最新版本 |           工作草案            |
| :-------------- | :------: | :---------------------------: |
| CE SQL          |    -     |     [WIP](cesql/spec.md)      |
| Discovery       |    -     |   [WIP](discovery/spec.md)    |
| Pagination      |    -     |   [WIP](pagination/spec.md)   |
| Schema Registry |    -     | [WIP](schemaregistry/spec.md) |
| Subscriptions   |    -     | [WIP](subscriptions/spec.md)  |

其他发布相关信息:

[历史版本和更新日志](docs/RELEASES.md)

如果您是 CloudEvents 的新手，建议您从阅读

[Primer](cloudevents/primer.md)查看规范目标的概述

设计决策，然后继续[核心规范](cloudevents/spec.md)。

因为不是所有的事件生成器都默认生成 CloudEvents，所以存在这样的情况
描述改编一些流行的推荐过程的文档

事件进入 CloudEvents，参见
[CloudEvents 适配器](cloudevents/adapters.md)。

## SDKs

除了上面提到的文档，还有一个
[SDK 的提议](cloudevents/SDK.md)。一组 sdk 也正在开发中:

- [CSharp](https://github.com/cloudevents/sdk-csharp)
- [Go](https://github.com/cloudevents/sdk-go)
- [Java](https://github.com/cloudevents/sdk-java)
- [Javascript](https://github.com/cloudevents/sdk-javascript)
- [PHP](https://github.com/cloudevents/sdk-php)
- [PowerShell](https://github.com/cloudevents/sdk-powershell)
- [Python](https://github.com/cloudevents/sdk-python)
- [Ruby](https://github.com/cloudevents/sdk-ruby)
- [Rust](https://github.com/cloudevents/sdk-rust)

## 社区和文档

了解更多关于创建动态云的人员和组织的信息
使我们的系统与 CloudEvents 可互操作。

- 我们的[治理](docs/GOVERNANCE.md)文档。
- [贡献](docs/CONTRIBUTING.md)指导。

- [路线图](docs/ROADMAP.md)

- [采用者](https://cloudevents.io/) -参见“集成”。

- [Contributors](docs/contributors.md):提供帮助的个人和组织

我们已经开始或正在积极地致力于 CloudEvents 规范。

-[演示和开源](docs/README.md)——如果你有东西要分享

关于您使用 CloudEvents 的信息，请提交 PR!

-[行为守则](https://github.com/cncf/foundation/blob/master/code-of-conduct.md)

### 安全问题

如果其中一个规范存在安全问题
请存储库[打开一个问题](https://github.com/cloudevents/spec/issues)。

### 通信

用于电子邮件通信的主要邮件列表:

- 发送电子邮件到: [cncf-cloudevents](mailto:cncf-cloudevents@lists.cncf.io)
- 订阅看到: https://lists.cncf.io/g/cncf-cloudevents
- 档案在: https://lists.cncf.io/g/cncf-cloudevents/topics

下面还有一个#cloudevents Slack 频道
[CNCF's Slack workspace](http://slack.cncf.io/).

SDK 相关评论和问题:

-电子邮件到:[cncf-cloudevents-sdk](mailto:cncf-cloudevents-sdk@lists.cncf.io)

-订阅请参见:https://lists.cncf.io/g/cncf-cloudevents-sdk

—档案:https://lists.cncf.io/g/cncf-cloudevents-sdk/topics

- Slack: #cloudeventssdk on [CNCF's Slack workspace](http://slack.cncf.io/)

### 会议时间

会议日期请查看[CNCF 公开活动日历](https://www.cncf.io/community/calendar/).
CloudEvents 规范由
[CNCF Serverless Working Group](https://github.com/cncf/wg-serverless) 开发完成。
这个工作组每周四的上午 9 点(美国-太平洋时间)通过 Zoom 开展视频会议。
([World Time Zone Converter](http://www.thetimezoneconverter.com/?t=9:00%20am&tz=San%20Francisco&)):

通过查看
[会议纪要文档](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
来获得如何加入会议的最新信息。

你可以在[这里](https://www.youtube.com/playlist?list=PLj6h78yzYM2Ph7YoBIgsZNW_RGJvNlFOt)
观看以往的历史会议录像。

工作组会定期举办与主流会议一致的线下会议。查看
[会议纪要文档](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
了解更多未来会议的计划。
