# CloudEvents SDK 要求

本文档旨在描述对新建CloudEvents软件开发工具（SDKs）的最低要求集。开发者设计并实现这些SDKs来增强并加速CloudEvents的集成。以下SDKs作为社区的重要成果将会被CloudEvents团队支持并维护下去：

- [C#/.NET SDK](https://github.com/cloudevents/sdk-csharp)
- [Go SDK](https://github.com/cloudevents/sdk-go)
- [Java SDK](https://github.com/cloudevents/sdk-java)
- [JavaScript SDK](https://github.com/cloudevents/sdk-javascript)
- [PHP SDK](https://github.com/cloudevents/sdk-php)
- [PowerShell](https://github.com/cloudevents/sdk-powershell)
- [Python SDK](https://github.com/cloudevents/sdk-python)
- [Ruby SDK](https://github.com/cloudevents/sdk-ruby)
- [Rust SDK](https://github.com/cloudevents/sdk-rust)

本文档为CloudEvents 的SDK开发者提供了指导和要求。它将伴随着ClodEvents核心规范不断更新下去。

## 贡献被接受的条件

CloudEvents团队作为一个开源的社区十分欢迎新的成员以及他们的贡献。但为了确保新贡献的SDK能够被支持和维护，CloudEvents小组要求必须确保以下内容：

- 每个SDK都需要活跃的联系人或组织支持。
- 每个SDK都必须支持最新版（N）以及前一（N-1）大版本的[CloudEvents规范](spec.md)\*。
- 在一个大版本中，SDK只需要支持它最新的小版本即可。

我们不强制要求SDK对候选版本提供支持，但强烈建议作者这样做。

\* 注意：v1.0是一个特殊的情况，因此我们建议只要v1.0还是最新版本，SDKs在支持它的同时也应该支持v0.3。

## 技术性要求

每个SDK都必须满足以下要求：

- 同时支持CloudEvents规范的里程碑版本和正在开发中的版本。
  - 将CloudEvents标准事件经过编码存在特定传输协议的消息中。
  - 将特定的传输层消息解码成为CloudEvents标准格式事件。
- 使用常用的编程语言实现SDK。
  - 使用这些编程语言的流行版本。
- 同时支持HTTP传输中的`structured` 和 `binary` 两种模型。

### 对象模型结构建议

每个SDK都应该提供一种用来表示标准事件的通用格式，这种格式是类/对象/结构这样的形式。

SDK应使用户能够绕过 CloudEvents 事件传输协议的特定编码和解码。事件对象的一般传输流程应该是：

```
事件 (-> 消息) -> 网络传输
```

以及

```
网络传输 (-> 消息) -> 事件
```
开发者不需要为SDK实现一个传输层的包装类，重点应该是实现当前编程语言与高等级的`事件`对象的交互，并提供工具来获取`事件`，以及将`事件`转换为你选择的传输实现能使用的格式。

Event作为一个高层级的概念，它的SDK需要能帮助以下任务：

1. 构造一个事件.
1. 将一个事件以给定的传输协议和编码方式进行编码（如果有需要的话将事件编写入传输消息中）。
1. 将一个事件以给定传输协议的消息、请求或响应格式进行解码。

#### 构建一个事件

SDK应该提供一个方便的方法来通过单条或多条消息构建事件。SDK的使用者需要一种方法来快速地构建CloudEvents格式的事件或是将他们的事件数据转换为CloudEvents格式的事件。在实践中事件构建通常有两种形式。

1. 事件创建

- "我有一些还不是CloudEvent的数据，我希望将它们变成CloudEvent。"
2. 事件转换

- "我有一个CloudEvent格式的事件，我希望它变成不同的事件。"
- "我有一个CloudEvent格式的事件，我希望它转换不同的格式。"

事件的创建是SDK中最常见的用法。

事件转换可以通过存取模式实现，比如添加getter或setter方法。 但是直接的key访问或者是named-key访问函数也是可以利用的。

无论是那种情况，必须要有一个根据参数集来验证最终事件对象的方法，在参数集中，CloudEvents规范的版本是至关重要的。

#### 编码/解码一个事件

每个SDK应该支持在传输协议和编码方面对一个事件进行编码和解码。结构化的编码是最容易支持的，因为它就是`json`格式。但是`Binary`对于不同的传输协议而言就可能完全不同了。

#### 数据

事件数据的访问则有很多种情况需要考虑，比如事件可能被编码为`base64`格式的结构化数据，或是`json`这种传输格式。SDK必须要提供方法将事件数据从这些格式中转换为本地的格式。

#### 扩展

SDK支持CloudEvents的扩展也是很常见的，但是提供一个能镜像数据访问的方法也可以实现。

#### 验证

对于每个事件的验证都必须是可行的。同时验证功能必须要将CloudEvents规范的版本考虑在内。对于SDK的所有要求都要根据不同版本的规范一一实现。

## 文档

每个SDK必须提供不同的例子，最少需要提供一个基于HTTP传输并实现以下功能的例子：

- 构建一个事件。
- 编码并发送一个构建好的事件。
- 接收并解码一个事件。
