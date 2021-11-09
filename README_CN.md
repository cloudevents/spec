# CloudEvents 中文手册

![CloudEvents logo](https://github.com/cncf/artwork/blob/master/projects/cloudevents/horizontal/color/cloudevents-horizontal-color.png)

Declaration： This manual aims to provide a fast and brief introduction of CloudEvents 
in Chinese for people who are new to CloudEvents. 
Most of the content is translated from the original English version. 
It is strongly recommended to read the English version if you find anything lost in translation.

事件(Events)在现代系统中无处不在。但不同的事件生产者往往用不同的规范来描述自己的事件。

对事件的统一描述的匮乏意味着开发者必须不断重新学习如何消费不同定义的事件。它同样限制了那些用来帮助事件数据完成
跨环境传输的库(如SDKs)，工具(如事件路由器)和基础设施(如事件追踪系统)的发展。总体来看，这种匮乏严重阻碍了事件数据的
可移植性和生产力。

CloudEvents是一个以通用格式来描述事件数据的标准。它提供了事件在服务、平台和系统中的互操作性。

CloudEvents 收获了从主流云厂商到SaaS公司的广泛关注。CloudEvents被[云原生计算基金会](https://cncf.io) (CNCF)持有，
在[2018/05/15](https://docs.google.com/presentation/d/1KNSv70fyTfSqUerCnccV7eEC_ynhLsm9A_kjnlmU_t0/edit#slide=id.g37acf52904_1_41)
被选为云原生沙箱级项目。

## CloudEvents 文件

现有文件如下:

|                               |                                 最新版本                                 |                                    工作草稿                                    |
| :---------------------------- | :----------------------------------------------------------------------------: | :---------------------------------------------------------------------------------: |
| **核心标准:**       |
| CloudEvents                   |         [v1.0](https://github.com/cloudevents/spec/blob/v1.0/spec.md)          |          [master](https://github.com/cloudevents/spec/blob/master/spec.md)          |
|                               |
| **可选标准:**  |
| AMQP Protocol Binding         | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/amqp-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/amqp-protocol-binding.md)  |
| AVRO Event Format             | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/avro-format.md)           | [master](https://github.com/cloudevents/spec/blob/master/avro-format.md)            |
| HTTP Protocol Binding         | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/http-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/http-protocol-binding.md)  |
| JSON Event Format             |      [v1.0](https://github.com/cloudevents/spec/blob/v1.0/json-format.md)      |      [master](https://github.com/cloudevents/spec/blob/master/json-format.md)       |
| Kafka Protocol Binding        | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/kafka-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/kafka-protocol-binding.md) |
| MQTT Protocol Binding         | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/mqtt-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/mqtt-protocol-binding.md)  |
| NATS Protocol Binding         | [v1.0](https://github.com/cloudevents/spec/blob/v1.0/nats-protocol-binding.md) | [master](https://github.com/cloudevents/spec/blob/master/nats-protocol-binding.md)  |
| Web hook                      |     [v1.0](https://github.com/cloudevents/spec/blob/v1.0/http-webhook.md)      |      [master](https://github.com/cloudevents/spec/blob/master/http-webhook.md)      |
|                               |
| **附加文件:** |
| CloudEvents Adapters          |                                       -                                        |        [master](https://github.com/cloudevents/spec/blob/master/adapters.md)        |
| CloudEvents SDK Requirements  |                                       -                                        |          [master](https://github.com/cloudevents/spec/blob/master/SDK.md)           |
| Documented Extensions         |                                       -                                        | [master](https://github.com/cloudevents/spec/blob/master/documented-extensions.md)  |
| Primer                        |        [v1.0](https://github.com/cloudevents/spec/blob/v1.0/primer.md)         |         [master](https://github.com/cloudevents/spec/blob/master/primer.md)         |
| Proprietary Specifications    |                                       -                                        |   [master](https://github.com/cloudevents/spec/blob/master/proprietary-specs.md)    |

对于初次接触CloudEvents的同学，可以通过阅读[入门文档](primer.md)增加对CloudEvents规范的目标和设计理念
的总体理解，
希望在最短时间内使用CloudEvents 规范的同学，可以直接阅读[核心规范](spec.md)。

由于并非所有事件生产者都默认生产符合CloudEvents规范的事件，因此可以用[CloudEvents适配器](https://github.com/cloudevents/spec/blob/master/adapters.md)
来将现有的事件与CloudEvents做适配。

## SDKs

除了上述文档，我们还提供了[SDK 提议](SDK.md)以及一些编程语言的SDK：

- [CSharp](https://github.com/cloudevents/sdk-csharp)
- [Go](https://github.com/cloudevents/sdk-go)
- [Java](https://github.com/cloudevents/sdk-java)
- [Javascript](https://github.com/cloudevents/sdk-javascript)
- [Python](https://github.com/cloudevents/sdk-python)

## 社区

在社区里，你可以了解到更多致力于搭建一个动态、云原生的生态系统的成员和组织。
他们不断尝试提升现有系统和CloudEvents间的互操作性和兼容性。

- [贡献者](community/contributors.md): 
  是指那些帮助我们制定规范或是积极活跃在CloudEvents规范相关工作的成员和组织。
- 即将推出: [demos & open source](community/README.md) -- 
  如果你希望向我们分享关于你对CloudEvents的使用，请通过提交PR让我们看到。

## 步骤

CloudEvents项目 [旨在](primer.md#设计目标)制定一个能够提升不同事件系统(如生产者和消费者)之间互操作性和兼容性
的[标准](spec.md)。

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

## 会议时间

会议日期请查看 [CNCF 公开活动日历](https://www.cncf.io/community/calendar/).
CloudEvents规范由
[CNCF Serverless 工作组](https://github.com/cncf/wg-serverless) 开发完成。
这个工作组每周四的上午9点(美国-太平洋时间)通过Zoom开展视频会议。 
通过 PC, Mac, Linux, iOS or Android来参加活动: https://zoom.us/my/cncfserverlesswg

或者通过 iPhone one-tap :

    US: +16465588656,,3361029682#  or +16699006833,,3361029682#

或者电话接入:

    Dial:
        US: +1 646 558 8656 (US Toll) or +1 669 900 6833 (US Toll)
        or +1 855 880 1246 (Toll Free) or +1 877 369 0926 (Toll Free)

会议 ID: 336 102 9682

国际号码接入:
https://zoom.us/zoomconference?m=QpOqQYfTzY_Gbj9_8jPtsplp1pnVUKDr

世界时区转化器:
http://www.thetimezoneconverter.com/?t=9:00%20am&tz=San%20Francisco&

## 会议记录

历史会议记录在
[这里](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#)
查看。

历史会议录像在
[这里](https://www.youtube.com/playlist?list=PLj6h78yzYM2Ph7YoBIgsZNW_RGJvNlFOt)
查看。

工作组会定期举办与主流会议一致的线下会议。查看[这里](https://docs.google.com/document/d/1OVF68rpuPK5shIHILK9JOqlZBbfe91RNzQ7u_P7YCDE/edit#) 
了解更多未来计划。

