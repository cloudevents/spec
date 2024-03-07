# CloudEvents

<!-- no verify-specs -->

![CloudEvents logo](https://github.com/cncf/artwork/blob/master/projects/cloudevents/horizontal/color/cloudevents-horizontal-color.png)

[![CLOMonitor](https://img.shields.io/endpoint?url=https://clomonitor.io/api/projects/cncf/cloudevents/badge)](https://clomonitor.io/projects/cncf/cloudevents)
[![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/6770/badge)](https://bestpractices.coreinfrastructure.org/projects/6770)


事件(Events)在现代系统中无处不在。但不同的事件生产者往往用不同的规范来描述自己的事件。

对事件的统一描述的匮乏意味着开发者必须不断重新学习如何消费不同定义的事件。
它同样限制了那些用来帮助事件数据完成跨环境传输的库(如 SDKs)、工具(如事件路由器)和基础设施(如事件追踪系统)的发展。
总体来看，这种匮乏严重阻碍了事件数据的可移植性和生产力。

CloudEvents 是一个以通用格式来描述事件数据的规范。它提供了事件在服务、平台和系统中的互操作性。

从主流云厂商到SaaS公司，工业界对 CloudEvents 兴趣浓烈。CloudEvents 项目由[云原生计算基金会](https://cncf.io)托管，
于[2018/05/15](https://docs.google.com/presentation/d/1KNSv70fyTfSqUerCnccV7eEC_ynhLsm9A_kjnlmU_t0/edit#slide=id.g37acf52904_1_41)
成为 CNCF 沙箱级项目，于[2019/10/24](https://github.com/cncf/toc/pull/297) CNCF 孵化项目。

## CloudEvents 文件

|                               |                                 最新发行版本                                  |                                      工作草案                                       |
| :---------------------------- | :-----------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------: |
| **核心规范：**       |
| CloudEvents                   | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md)   | [WIP](../../cloudevents/languages/zh-CN/spec.md) |
|                               |
| **可选规范：**  |
| AMQP 协议绑定         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/amqp-protocol-binding.md)  | [WIP](../../cloudevents/languages/zh-CN/bindings/amqp-protocol-binding.md)       |
| AVRO 事件格式             | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/avro-format.md)             | [WIP](../../cloudevents/languages/zh-CN/formats/avro-format.md)                  |
| HTTP 协议绑定         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/http-protocol-binding.md)  | [WIP](../../cloudevents/languages/zh-CN/bindings/http-protocol-binding.md)       |
| JSON 事件格式             | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/formats/json-format.md)             | [WIP](../../cloudevents/languages/zh-CN/formats/json-format.md)                  |
| Kafka 协议绑定        | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/kafka-protocol-binding.md) | [WIP](../../cloudevents/languages/zh-CN/bindings/kafka-protocol-binding.md)      |
| MQTT 协议绑定         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/mqtt-protocol-binding.md)  | [WIP](../../cloudevents/languages/zh-CN/bindings/mqtt-protocol-binding.md)       |
| NATS 协议绑定         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/nats-protocol-binding.md)  | [WIP](../../cloudevents/languages/zh-CN/bindings/nats-protocol-binding.md)       |
| WebSockets 协议绑定   | -                                                                                                        | [WIP](../../cloudevents/languages/zh-CN/bindings/websockets-protocol-binding.md) |
| Protobuf 事件格式         | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/bindings/nats-protocol-binding.md)  | [WIP](../../cloudevents/languages/zh-CN/formats/protobuf-format.md)              |
| XML 事件格式              | -                                                                                                        | [WIP](../../cloudevents/languages/zh-CN/working-drafts/xml-format.md)            |
| Web hook                      | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/http-webhook.md)                    | [WIP](../../cloudevents/languages/zh-CN/http-webhook.md)                         |
|                               |
| **附加文件：** |
| CloudEvents 入门文档                                             | [v1.0.2](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/primer.md) | [WIP](../../cloudevents/languages/zh-CN/primer.md)                          |
| [CloudEvents 适配器](../../cloudevents/languages/zh-CN/adapters.md)                | -                                                                               | [无版本工作草案](../../cloudevents/languages/zh-CN/adapters.md)              |
| [CloudEvents SDK 必要条件](../../cloudevents/languages/zh-CN/SDK.md)             | -                                                                               | [无版本工作草案](../../cloudevents/languages/zh-CN/SDK.md)                   |
| [记录的扩展属性](../../cloudevents/languages/zh-CN/extensions/README.md)  | -                                                                               | [无版本工作草案](../../cloudevents/languages/zh-CN/extensions/README.md) |
| [专有规范](../../cloudevents/languages/zh-CN/proprietary-specs.md) | -                                                                               | [无版本工作草案](../../cloudevents/languages/zh-CN/proprietary-specs.md)     |

## 其它规范
|                 | 最新发行版本 | 工作草案                 |
| :-------------- | :------------: | :---------------------------: |
| CE SQL          |       -        | [WIP](../../cesql/languages/zh-CN/spec.md)          |
| Subscriptions   |       -        | [WIP](../../subscriptions/languages/zh-CN/spec.md)  |

其它发行相关信息可以在
[历史发行版本及变化内容中](../../docs/languages/zh-CN/RELEASES.md)查看。

如果你初次接触 CloudEvents 并且希望对它有全面认识，可以阅读[入门文档](../../cloudevents/languages/zh-CN/primer.md)了解 CloudEvents 规范的目标和设计理念。
如果你希望快速了解并使用 CloudEvents ，可以直接阅读[核心规范](../../cloudevents/languages/zh-CN/spec.md)。

由于并非所有事件生产者都默认生产符合CloudEvents规范的事件，因此可以用[CloudEvents适配器](../../cloudevents/languages/zh-CN/adapters.md)
来将现有的事件与CloudEvents做适配。

## SDKs

除了上述文档，我们还提供了[SDK 提议](../../cloudevents/languages/zh-CN/SDK.md)以及一些编程语言的SDK：

- [C#/.NET](https://github.com/cloudevents/sdk-csharp)
- [Go](https://github.com/cloudevents/sdk-go)
- [Java](https://github.com/cloudevents/sdk-java)
- [Javascript](https://github.com/cloudevents/sdk-javascript)
- [PHP](https://github.com/cloudevents/sdk-php)
- [PowerShell](https://github.com/cloudevents/sdk-powershell)
- [Python](https://github.com/cloudevents/sdk-python)
- [Ruby](https://github.com/cloudevents/sdk-ruby)
- [Rust](https://github.com/cloudevents/sdk-rust)

## 社区和文件

在 CloudEvents 社区里，你能够认识更多致力于搭建一个动态、云原生的生态系统的成员和组织。
他们不断尝试利用 CloudEvents 来提升现有系统间的互操作性和兼容性。

- 我们的 [社区管理](../../docs/languages/zh-CN/GOVERNANCE.md) 文档。
- 我们的 [贡献指南](../../docs/languages/zh-CN/CONTRIBUTING.md) 文档。
- [CloudEvents 路线图](../../docs/languages/zh-CN/ROADMAP.md)。
- [CloudEvents 采用者](https://cloudevents.io/) 可在官网"集成"版块中找到。
- [CloudEvents 贡献者](../../docs/languages/zh-CN/contributors.md):
  是指那些帮助我们制定规范或是积极活跃在 CloudEvents 规范相关工作的成员和组织。
- [Demos & 开源](../../docs/languages/zh-CN/README.md)
  -- 如果你希望向我们分享关于你对CloudEvents的使用，请通过提交PR让我们看到。
- [CloudEvents 行为准则](https://github.com/cncf/foundation/blob/master/code-of-conduct.md)

### 安全问题

如果对本仓库中任意规范有安全方面的担忧，请[提交一个issue](https://github.com/cloudevents/spec/issues) ，告知我们。

[Trail of Bits](https://www.trailofbits.com/) 于 2022 年 10 月对本项目进行了安全评估。详情参见[完整报告](../../docs/CE-SecurityAudit-2022-10.pdf)。

## 联系方式

邮件联系方式如下:

- 发送EMail至: [cncf-cloudevents](mailto:cncf-cloudevents@lists.cncf.io)
- 订阅地址: https://lists.cncf.io/g/cncf-cloudevents
- 存档地址: https://lists.cncf.io/g/cncf-cloudevents/topics

在[CNCF's Slack 工作空间](http://slack.cncf.io/) 中添加 #cloudevents Slack 频道。

SDK相关的评论和问题:

- 发送EMail至: [cncf-cloudevents-sdk](mailto:cncf-cloudevents-sdk@lists.cncf.io)
- 订阅地址: https://lists.cncf.io/g/cncf-cloudevents-sdk
- 存档地址: https://lists.cncf.io/g/cncf-cloudevents-sdk/topics
- Slack: 在[CNCF's Slack 工作空间](http://slack.cncf.io/) 中 添加 #cloudeventssdk 频道

## 会议时间

会议日期请查看[CNCF 公开活动日历](https://www.cncf.io/community/calendar/).
CloudEvents 规范由
[CNCF Serverless Working Group](https://github.com/cncf/wg-serverless) 开发完成。
这个工作组每周四的上午9点(美国-太平洋时间)通过Zoom开展视频会议。
([World Time Zone Converter](http://www.thetimezoneconverter.com/?t=9:00%20am&tz=San%20Francisco&)):

通过查看
[会议纪要文档](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
来获得如何加入会议的最新信息。

你可以在[这里](https://www.youtube.com/playlist?list=PLj6h78yzYM2Ph7YoBIgsZNW_RGJvNlFOt)
观看以往的历史会议录像。

工作组会定期举办与主流会议一致的线下会议。查看
[会议纪要文档](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
了解更多未来会议的计划。
