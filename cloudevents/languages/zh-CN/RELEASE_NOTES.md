# CloudEvents Release Notes

<!-- no verify-specs -->

## v1.0.2 - 2022/02/05

- 添加 C# 命名空间选项到 proto (#937)
- 调整 SDK 需求措辞 (#915)
- 重组 repo 目录结构 (#904/#905)
- 将 CE 规范翻译成中文 (#899/#898)
- 序列化时明确声明 application/json 默认值 (#881)
- 添加 PowerShell SDK 到 SDK 列表 (#875)
- WebHook "Origin" header 概念与 RFC6454 冲突 (#870)
- 使用 JSON 数据内容类型澄清 JSON 格式的数据编码 (#861)
- Webhook-Allowed-Origin 代替 Webhook-Request-Origin (#836)
- 将 Sampling 扩展修改为 Sampled Rate (#832)
- 移除 Kafka Binding 中的冲突语句 (#823/#813)
- 修复 Kafka Binding 中的语句冲突 (#814)
- 阐明 HTTP header 值编码和解码要求 (#793)
- 在入门文档中，增加版本控制相关建议 (#799)
- 添加对protobuf批处理格式的支持 (#801)
- 阐明 HTTP header 值编码和解码要求 (#816)
- 处理错误的入门指南 (#763)
- 信息分类扩展 (#785)
- 阐明分区扩展在 Kafka 中的作用 (#727)

## v1.0.1 - 2020/12/12

- 添加 protobuf 格式作为子协议 (#721)
- 允许 JSON 值为 null，即未设置 (#713)
- 在入门文档中将安全性相关内容定为规范的非目标内容 (#712)
- WebSockets 协议绑定 (#697)
- 阐明消息模式和 HTTP 内容模式之间的区别 (#672)
- 添加缺少的 sdks 到 readme (#666)
- 新的 sdk 维护者规则 (#665)
- 转移 sdk 治理和清理 (#663)
- 使 'datadef' 定义符合规范 (#658)
- 添加 CoC 并将一些治理文档移动到“社区” (#656)
- 添加有关理解 Cloud Events 交互的博客文章 (#651)
- SDK 治理草案 (#649)
- docs:为 SDK 维护者和贡献者添加通用进程  (#648)
- 为 Cloud Events 编排添加 Demo (#646)
- 明确 JSON 格式的 MUST 要求 (#644)
- 重新引入协议缓冲区表示 (#626)
- 关闭 #615 (#616)
- 重写分布式跟踪扩展 (#607)
- Cloud Events Primer 的小更新 (#600)
- Kafka 说明 (#599)
- 专有绑定规范包含指南 (#595)
- 添加链接到 Pub/Sub 绑定 (#588)
- 添加一些关于 SDK 里程碑的清晰度 (#584)
- 如何确定二进制 CE 与随机非 CE 消息 (#577)
- 添加 Visual Studio Code 扩展到社区开源文档 (#573)
- 指定 kafka 标头键、值以及消息键的编码 (#572)
- 修复分布式跟踪示例 (#569)
- 关于入门嵌套事件的段落 (#567)
- 添加更改管理员的规则-#564
- 更新 JSON 架构 (#563)
- 可以忽略非必须的建议 - 风险自负 (#562)
- 更新分布式跟踪扩展规范链接 (#550)
- 将 Ruby SDK 添加到 SDK 列表 (#548)

## v1.0.0 - 2019/10/24

- 使用“生产者”和“消费者”而不是“发送者”和“接收者”
- 阐明中介应转发可选属性
- 删除属性名称必须以字母开头的限制
- 删除属性名称应具有描述性和简洁性的建议
- 阐明一次事件可能导致多个事件
- 
  添加 Event Data 部分（替换`data`），使事件数据成为顶级概念而不是属性
- 介绍一个事件格式部分
- 定义结构化模式和二进制模式消息
- 定义协议绑定
- 添加扩展属性到 "context attributes" 描述中
- 将属性序列化机制的提名从 "context attributes" 描述移至 "type system"
- 将 “transport” 普遍更改为 “protocol”
- 为属性引入 Boolean 、URI 和 URI-reference 类型
- 删除属性的 Any 和 Map 类型
- 明确字符串属性中允许使用哪些 Unicode 字符
- 要求所有 context attribute 值都是列出的类型之一，并声明它们可以显示为原生类型或字符串。
- 要求`source`非空；推荐一个绝对URI
- 版本号从 0.3 更新到 1.0
- 阐明 `type` 与 "the originating occurrence" 有关
- 删除 `datacontentencoding` 部分
- 阐明缺失 `datacontenttype` 属性的处理
- 重命名 `schemaurl` 为 `dataschema`, 并将类型从 URI-reference 更改为 URI
- 限制 `dataschema` 为非空（如果存在）
- 添加一些关于 `time` 如何在无法确定的情况下产生的细节，
  特别是在一个源内的一致性
- 添加扩展 context attribute 处理的细节
- 添加 CloudEvent 接收器传递非 CloudEvent 元数据的建议
- Sample CloudEvent 不再使用JSON对象作为示例扩展值

## v0.3 - 2019/06/13

- 更新标题格式。 (#447)
- 删除空白部分
- Misc. 排版错误修复
- 添加一些关于如何构建 CloudEvents 的指导 (#404)
- 尺寸限制 (#405)
- 类型系统更改 // 规范字符串表示 (#432)
- 为 ID 添加一些额外的设计点 (#403)
- 添加 "Subject" context attribute 定义
- 补充术语 Source, Consumer, Producer and Intermediary (#420)
- 添加了分区扩展 (#218)
- Issue #331: 阐明 source and id 唯一性的范围
- 添加了 dataref.md 的链接
- 对属性部分排序
- 为我们的图像修复错误的 href (#424)
- Master表示规范的未来版本，在文本中使用未来版本。 (#415)
- 调整示例以包含 AWS CloudWatch 事件、我们事实上的中心事件格式，并删除有效但不是非常相关的 SNS 和 Kinesis 示例。
- 添加 dataref 属性并描述 Claim Check Pattern (#377)
- 为 PR 406 做一些遗漏的清理项目
- 介绍 "subject" (#406)
- 添加了数据内容编码 (#387)
- 添加与 cloudevents 的 Apache RocketMQ 专有绑定
- 在所有markdown上执行 https://prettier.io/ 命令。 (#411)
- 隐私与安全 (#399)
- 阐明 OPTIONAL 的含义
- 扩展遵循 #321 中引入的属性命名方案
- 添加 README
- 修复排版错误
- inter 不能接受占位符链接 🙄
- 在专用文件中收集专有的规范
- 将 "extension attributes" 部分下移到 context attributes 的末尾
- 修复了入门中的断开链接
- 修复断开的链接
- 一致性：schemaurl 使用 URI-reference，protobuf 使用 URI-reference
- 用于批处理 JSON 的 HTTP 传输绑定 (#370)
- minLength 用于非空属性，添加 schemaurl (#372)
- 修复描述中的类型引用
- 数据格式与上述段落保持一致
- 删除重复段落
- 在变量类型的描述中添加任何允许的整数
- s/内容类型/数据类型/g
- 在我们的发版过程中添加一个公告
- Transports 负责批处理消息 (#360)
- 准确指定 Integer 类型的范围 (#361)
- 修复 http 传输中的 TOC
- 添加 KubeCon 演示信息

## v0.2 - 2018/12/06

- 添加了 HTTP WebHook 规范 (#155)
- 添加了 AMQP 1.0 传输和 AMQP 类型系统映射 (#157)
- 添加了 MQTT 3.1.1 和 5.0 传输绑定 (#158)
- 添加了 NATS 传输绑定 (#215)
- 添加了分布式跟踪扩展 (#227)
- 添加了入门 (#238)
- 添加了 Sampling 扩展 (#243)
- 为新协议/编码定义 minimum bar (#254)
- 删除 eventTypeVersion (#256)
- 将扩展的序列化更改为顶级JSON属性 (#277)
- 添加了序列扩展 (#291)
- 添加了 Protobuf 传输 (#295)
- 为新扩展定义了 minimum bar (#308)
- 要求所有属性为小写并限制字符集 (#321)
- 简化/缩短属性名称 (#339)
- 添加了 SDK 设计文档的初稿 (#356)

## v0.1 - 2018/04/20

- 规范的初稿发布！