# CloudEvents 入门文档 -  1.0.3 版本（制作中）

## 摘要

这份非技术规范文档用来为你提供关于 CloudEvents 规范的总体概览。它补充了 CloudEvents 规范的相关背景以及在制定本规范时的历史和设计理念。这样，CloudEvents 的核心规范就只需要关注 Events 规范的技术细节，而不用过多地关心背景相关内容。

## 文档状态

这份文档是一份仍在制作中的工作草案。

## 目录

- [历史](#history历史)
- [CloudEvents 概念](#cloudevents-concepts概念)
- [设计目标](#design-goals设计目标)
- [架构](#architecture架构)
- [属性版本控制](#versioning-of-cloudevents属性版本控制)
- [CloudEvent 属性](#cloudevent-core-attributes核心属性)
- [CloudEvent 属性扩展](#cloudevent-attribute-extensions属性扩展)
- [生产 CloudEvents](#creating-cloudevents生产-cloudevents)
- [合格的协议与编码](#qualifying-protocols-and-encodings合理化协议与编码)
- [专有的协议和编码](#proprietary-protocols-and-encodings专有的协议与编码)
- [现有技术](#prior-art现有技术)
- [角色](#roles角色)
- [价值主张](#value-proposition价值主张)
- [现有的数据格式](#existing-event-formats现有的数据格式)

## History/历史

[CNCF Serverless 工作组](https://github.com/cncf/wg-serverless) 是由 CNCF的[技术监管委员会](https://github.com/cncf/toc) 成立，用于研究 Serverless 相关技术并为 CNCF 推荐相关领域的未来发展计划的工作组。工作组其中一项建议就是研究创建一种通用事件格式，用于提升不同云厂商间函数的可移植性和事件流处理的互操作性。就此，CloudEvents 应运而生。

尽管 CloudEvents 起初是作为 Serverless 工作组的项目进行的，但随着 CloudEvents 规范完成它v0.1版本的里程碑，技术监管委员会批准了 CloudEvents 作为一个新的独立的 CNCF 沙箱级项目。

## Cloudevents Concepts/概念

一个[事件](spec.md#event事件)包含了[事件发生](spec.md#occurrence事件发生)的上下文和相关数据。
事件的相关数据可以用来唯一标识一件事件的发生。

事件代表了已发生的事实，因此它并不包含任何目的地相关信息，但消息能够传达事件内容，从而将事件数据
从源头传输到指定的目的地。

### Eventing/事件

事件通常在服务器端代码中使用来连接不同的系统，其中一个系统中的状态变化会导致代码在另一个系统中执行。
比如，一个事件源，可能会在收到某个外部信号(如 HTTP 或 RPC )或观察到状态变化(如 IoT/ 物联网传感器数据变化或不活跃)
时，生产一个事件。

为了更好地解释一个系统如何使用 CloudEvents，下图展示了一个从事件源生产的事件是如何触发一个行为的。

![alt text](../../source-event-action.png "A box representing the source with
arrow pointing to a box representing the action. The arrow is annotated with
'e' for event and 'protocol'.")

事件源生产了一条封装了基于某种协议的事件数据的消息。
当载有事件的消息到达目的地时，会触发一个使用了事件数据的行为函数。

一个事件源是那些允许暂存和测试实例的源类型的特定实例。
某个特定源类型的开源软件可能由多个公司或提供商部署。

事件可以通过各种行业标准协议（如 HTTP、AMQP、MQTT、SMTP）、开源协议（例如 Kafka、NATS）或
平台/供应商专有协议（AWS Kinesis、Azure Event Grid）传输。

一个操作函数能够处理那些定义了行为或影响的事件，这些行为和效果由来自特定源的特定事件触发而来。
虽然超出了规范的范围，但生成事件的目的通常是让其他系统能够轻松地对它们无法控制的源中的更改做出反应。
源和操作通常由不同的开发人员构建。
通常，源是托管服务，而操作是 serverless 函数（如 AWS Lambda 或 Google Cloud Functions）中
的自定义代码。

## Design Goals/设计目标

CloudEvents 通常用于分布式系统，以允许服务在开发过程中松耦合，独立部署，方便之后连接以创建新的应用程序。

CloudEvents 规范的目标是定义允许服务生产或消费事件的事件系统的互操作性，
其中生产者和消费者可以独立开发和部署。 生产者可以在没有消费者监听时就生成事件，
消费者也可以表达对尚未生成的事件或事件类的兴趣。值得注意的是，这项工作产生的规范侧重于事件格式的互操作性
以及它在通过各种协议（例如 HTTP）发送时的显示方式。我们不关注事件生产者或事件消费者的处理模型。

CloudEvents 的核心规范中定义了一组称之为属性的元数据，
它们描述了在系统之间传输的事件以及这些元数据片段应如何显示在该消息中。
这些元数据是，将请求路由到适当组件并帮助该组件正确处理事件所需的最小信息集。
因此，某些事件本身的数据可能会作为 CloudEvent 属性集的一部分而被复制，
但这样做仅是为了能够正确传递和处理消息。那些不用于该目的的数据应放置在事件（数据）本身中。

此外，本规范中假设协议层所需的用来将消息传递到目标系统的元数据应完全由协议处理，
因此不包含在 CloudEvents 属性中。 有关更多详细信息，请参阅[非目标](#non-goals非目标)部分。

除了这些属性的定义之外，规范还描述了关于如何序列化
不同格式（例如 JSON）和协议（例如 HTTP、AMQP、Kafka）的事件。

一些协议本身支持将多个事件批处理到单个 API 的调用中。
为了提升系统间的互操作性，是否以及如何实现批处理将由协议自己决定。
相关详细信息可以在协议绑定或协议规范中找到。
成批的CloudEvents并没有语义，也没有排序。
[中间人](spec.md#intermediary中间人)可以添加或删除批处理以及将事件分配给不同的批处理。

事件的目的或语义含义超出了 CloudEvents 规范的范围。
只要发送的消息符合规范，那么它就是一个有效的 CloudEvent。
很多人不容易意识到一件事，错误和异常是可以作为CloudEvents来传输的。
接下来应由事件生产者定义将使用的 CloudEvents 属性值，就像它可能生成的任何其他事件一样。

由于并非所有事件生产者都将其事件以CloudEvents的形式发布，
因此我们定义了一组 [适配器](../../adapters.md)
来展示如何将事件从一些流行的事件生产者映射到 CloudEvents。
这些适配器是非规范的，
但它们是规范作者对 CloudEvents 属性如何在其它生产者本地生成事件并映射到CloudEvents时的最佳猜测。

### Non Goals/非目标

以下内容不在本规范的范围之内：

- 函数的构建和调用过程
- 特定语言的运行时 APIs
- 选择单一身份认证或访问控制的系统
- 包含协议级路由信息
- 事件持久化过程
- 授权、数据完整性和保密机制

就连那些刚接触 CloudEvents 概念的人都会建议
CloudEvents 规范不应包括协议级路由信息（例如，将事件发送到的目标的URL）。
经过深思熟虑，工作组得出的结论是，CloudEvents规范中不需要路由信息：
因为任何现有的协议（例如 HTTP、MQTT、XMPP 或 Pub/Sub 总线）都已经定义了路由语义。
例如，CloudEvents [HTTP 绑定](../../bindings/http-protocol-binding.md) 规定了头部和请求正文内容。
CloudEvents 不需要在规范中包含目标 URL 即可与 HTTP 兼容；HTTP 规范已经在
[请求行](https://tools.ietf.org/html/rfc2616#section-5.1) 中包含了所需的目标URL。

路由信息不仅是多余的，而且是有害的。
CloudEvents 应该增加互操作性并解耦事件的生产者和消费者。
禁止来自事件格式的路由信息允许将 CloudEvents 重新传送到新的行为，或通过包含多个通道的复杂中继传送。
例如，如果 Webhook 地址不可用，则用于 Webhook 的 CloudEvent 应可传送到死信队列。
死信队列应该能够将事件传送给原始事件发射者从未想象过的新的行为上。

在系统内和跨系统生产和消费的 CloudEvent 能够触发产生价值的行为。
因此，对于调试或复制的目的而言，存档和或重放事件可能很有价值。
但是，持久化事件会删除传输期间可用的上下文信息，例如生产者的身份和权利、保真验证机制或机密性保护。
此外，持久化会增加满足用户需求的复杂性和挑战。
例如，出于加密或签名目的重复使用私钥会增加攻击者可用的信息，从而降低安全性。
因此我们推测，可以定义有助于满足持久性要求的属性，但这些属性可能随着行业最佳实践和进步而不断发展。

CloudEvents 规范目前不强制或提倡任何有关授权、数据完整性和保密的专有机制和原则，
因为当前规范的目的不是定义有关 CloudEvents 的安全原则。
每个实现者都有一个增强其安全模型的不同原则。
我们把它留给规范的实现者去提供额外的细节来通过扩展字段的方式强化他们的安全模型，
这样可以更好地被实现者为规范而自己实现的组件所解释。
但是，如果社区观察到一种扩展字段的模式，作为处理数据完整性主题的标准方法。
在这种情况下，此类扩展字段可能被声明为对 CloudEvent 规范的官方扩展。

## Architecture/架构

CloudEvents 规范集定义了四种有助于形成分层架构模型的不同类型的协议元素。

1. [基本规范](spec.md) 定义了一个抽象信息模型，
   该模型由属性（键值对）和构成 CloudEvent 的相关规则组成。此规范包含了*核心属性*的定义。有些核心属性必须出现在所有的 CloudEvents 中，有些则是可选的。
2. [扩展属性](spec.md#extension-context-attributes扩展上下文属性)
   添加了特定于用例且可能重叠的扩展属性集和相关规则，如支持不同的追踪标准的规则。
3. 事件格式编码,如 [JSON](../../formats/json-format.md), 定义了基本规范的信息模型与所选扩展的编码方式，
   以将其映射到应用程序协议的头部和负载元素。
4. 协议绑定, 如. [HTTP协议绑定](../../bindings/http-protocol-binding.md),
   在HTTP to HTTP的情况下，
   定义了 CloudEvent 如何绑定到应用程序协议的传输层。
   协议绑定不限制传输层的使用方式，这意味着 HTTP绑定可用于任何 HTTP方法以及请求和响应消息。

为了确保更广泛的互操作性，CloudEvents 规范集为使用专有应用协议的事件传输提供了特定约束。
[HTTP Webhook](../../http-webhook.md) 规范并非特定于 CloudEvents，
而是可用于将任何类型的单向事件和通知发布到符合标准的 HTTP 端点。
但是，由于其他地方缺乏此类规范，因此 CloudEvents 需要对其进行定义。

### Interoperability Constraints/互操作性约束条件

如 [设计目标](#design-goals设计目标) 部分所述，互操作性是本规范的一个关键目标。
因此，本协议中有地方被建议有所约束条件。
例如，在[大小限制](spec.md#size-limits大小限制) 部分提示事件大小应该不超过 64KiB。
重要的是要注意诸如这些约束，在没有通过“必须”强制执行的情况下，
是对增加多个实现和部署之间互操作性的可能性的一种建议。
具体使用规范可以随意忽略这些建议，
但这些环境有责任确保所有参与 CloudEvents 传输的组件能够远离这些建议的边界。

### Protocol Error Handling/协议错误处理

CloudEvents 规范在很大程度上并未规定与 CloudEvents 的创建或处理相关联的处理模型。
因此，如果在处理 CloudEvent 过程中出现错误，
请使用正常的协议级错误处理机制进行处理。

## Versioning of CloudEvents/属性版本控制

对于某些 CloudEvents 属性，由其值引用的实体或数据模型可能会随时间变化。
CloudEvents 规范不强制要求要使用的特定模式，甚至不要求必须考虑用到版本控制。
这个决定取决于每个事件生产者。

然而，鼓励事件生产者考虑他们如何在不破坏消费者的情况下发展他们的scheme。
两个具体的上下文属性`type` 和 `dataschema`在这方面尤为重要，但是预期用法有所不同。
两者间在版本控制方面的差异在下面介绍。

鼓励事件生产者从一开始就考虑版本问题，尤其是在首先声明一个特定的 CloudEvent
是“稳定的”之前。
所选版本控制方案的文档，包括其背后的原理，都会是消费者所喜欢的。

### `type` 属性在版本控制方面的作用

`type` 属性应该是消费者识别他们收到的事件类型的主要方式。
这可以通过订阅特定的 CloudEvent 类型来实现，或者通过本地过滤所有收到的 CloudEvent实现。
但确定了 CloudEvent 类型的消费者通常会期望该类型的数据
仅以向后兼容的方式更改，除非另有明确说明。
“向后兼容”的确切含义将因数据内容类型而异。

当 CloudEvent 的数据以向后兼容的方式更改时，`type` 属性的值通常应保持不变。

当 CloudEvent 的数据以向后不兼容的方式更改时，`type` 属性的值通常应更改。
我们鼓励事件生产者在一段时间内（可能永远）同时生产旧事件和新事件，以避免干扰消费者。

在考虑 `type` 属性的值时，事件生产者可以选择他们希望的任何版本控制方案，
例如版本号 (v1, v2) 或日期 (2018-01-01) 作为值的一部分。
他们还可能使用 `type` 属性来表示特定版本尚未稳定，可能会经历重大更改。
或者，他们可以选择根本不在类型值中包含版本。

### `dataschema` 属性在版本控制方面的作用

我们预计 `dataschema` 属性是信息性的，主要在开发过程中使用，并通过工具使用时，
该工具能够通过其理解的数据内容类型提供任意 CloudEvents 的诊断信息。

当 CloudEvent 的数据以向后兼容的方式更改时，
`dataschema` 属性的值通常应更改以反映这一点。
另一种方法是让 URI 保持不变，但从该 URI 提供的内容要更改以反映更新的架构。
后一种方法对于事件生产者来说可能更容易实现，
但对于希望通过 URI 缓存schema内容的消费者来说不太方便。

当 CloudEvent 的数据以向后不兼容的方式更改时，`dataschema` 属性的值通常应更改，
就像上述的 `type` 属性的情况一样。

## CloudEvent Core Attributes/核心属性

本节介绍了与 CloudEvent 核心属性相关的其它背景和设计要点。

### id

`id` 属性是一个在同一事件源下所有事件中用来标识事件唯一的值
（其中每个事件源由其 CloudEvents `source`属性唯一标识）。
虽然`id`使用的确切值是生产者定义的，
但必须要确保来自单个事件源的 CloudEvents 消费者不会有两个事件共享相同的 id 值。
我们在这里隐含地声明没有两个事件将共享相同的 id 值，但不提供关于如何保证这一点的解释，
因为这超出了本规范的范围。
唯一的例外是如果支持事件的重播，在这些情况下，可以使用 id 来检测这一点。

由于一次事件的发生可能导致生成多个事件，
在所有这些事件都来自同一事件源的情况下，
生成的每个 CloudEvent 将具有唯一的 `id`。
以创建数据库条目为例，这一事件的发生可能会生成一个类型为 `create` 的 CloudEvent
和一个类型为 `write` 的 CloudEvent。
这两个 CloudEvents 各自都有一个唯一的 ID。
如果需要在这两个 CloudEvent 之间建立某种关联以表明它们都与同一事件相关，
那么可以使用 CloudEvent 中的一些附加数据来实现该目的。

从这方面来看，虽然事件生产者对`id`的使用可能是某个随机字符串，
或者在其它上下文中具有某种语义的字符串，
但对于此 CloudEvent 属性而言，这些含义并不成立，
因此本规范不建议将 `id` 用于除了唯一性检查之外的其它目的。

## CloudEvent Attribute Extensions/属性扩展

为了实现规范的设计目标，
规范作者将尝试限制他们在 CloudEvents 中定义的元数据属性的数量。
为此，该项目定义的属性将分为以下两类：

- 核心属性
- 扩展属性

本规范中定义了核心属性。核心属性又被分为必要和可选两种。
正如类别名称所暗示的那样，“必要”属性是工作组认为在任何情况下，对所有事件都至关重要的属性，
而“可选”属性将在大多数情况下使用。

工作组考虑到某些属性不够常见而不能归入上述两个类别，
但此类属性的良好定义仍会使系统间的互操作性级别受益，
因此将这些属性放入了“扩展”类别并记录在[扩展文档](../../extensions/README.md)中，
本规范定义了这些扩展属性在 CloudEvent 中的显示方式。

在确定提议的属性属于哪个类别时，
工作组使用现有的用例和用户故事来解释它们的基本原理和需求。
相关信息将添加到本文档的[现有技术](#prior-art现有技术)部分。

CloudEvent 规范的扩展属性是需要包含的附加元数据，它们能确保正确的路由和正确处理CloudEvent。
用于其它目的的附加元数据，
即那些与事件本身相但在 CloudEvent 的传输或处理中不需要的元数据，
应改为放置在事件 (`data`)的扩展点内。

扩展属性应保持最少，以确保 CloudEvent 可以正确序列化和传输。
事件生产者应该考虑在向 CloudEvent 添加扩展时可能遇到的技术限制。
例如，[HTTP Binary Mode](../../bindings/http-protocol-binding.md#31-binary-content-mode)
使用 HTTP 头来传输元数据；
大多数 HTTP 服务器会拒绝包含过多 HTTP 头部数据的请求，要求限制其低至 8 KiB。
因此，扩展属性的大小和数量应保持最小。

如果扩展变得流行，那么规范作者可能会考虑将其作为核心属性移入规范。
这意味着在正式将新属性添加到规范之前，扩展机制/过程可用作审查新属性的一种方式。

### JSON Extensions/JSON 扩展

如 [CloudEvents JSON 事件格式](../../formats/json-format.md)中
[属性](../../formats/json-format.md#2-attributes)部分所述，
CloudEvent 扩展属性与已定义属性(必要属性、可选属性)在序列化时处于同一等级 -
也就是说，它们都是 JSON 对象的顶层属性。
CloudEvent 的作者花了很长时间考虑所有选项，并认为这是最好的选择。
理由如下：

由于 CloudEvents 规范遵循 [semver](https://semver.org/) ，
这意味着只要新属性是可选属性，它们可以在核心规范的未来版本定义，而无需更改当前主要版本。
在这样的情况下，请考虑现有消费者将如何使用新的（未知的）顶级属性。
虽然消费者可以随意忽略它，因为它是可选的，
但在大多数情况下，这些属性仍然希望向接收这些事件的应用程序公开。
这可能导致这些应用程序在基础设施不支持的情况下，支持这些属性。
这意味着未知的顶级属性（无论是谁定义的——规范的未来版本或事件生产者）可能不会被忽略。
因此，虽然其它一些规范定义了放置扩展的特定属性（例如顶级 `extensions` 属性），
但作者认为在传入事件中具有两个不同位置的未知属性可能会导致互操作性问题和开发人员的混淆。

扩展属性通常用于测试那些被规范正式采用之前的潜在属性。
如果有一个 `extensions` 类型的属性，这个新属性已经被序列化，
那么如果该属性被核心规范采用，它将从`extensions`属性提升（从序列化的角度）为顶级属性。
如果我们假设这个新属性是可选的，那么当它被核心规范采用时，
它只是一个小版本增量，所有现有的消费者仍然会继续工作。
但是，消费者将不知道此属性将出现在何处 - 在扩展属性中还是作为顶级属性。
这意味着他们可能需要同时查看两个地方。
如果属性出现在两个地方但具有不同的值怎么办？
生产者是否需要将它放在两个地方，因为他们可能同时有新、老消费者？
虽然可以为如何解决出现的每个潜在问题而制定明确的规则，
但作者认为一个避免这些问题的更好的办法是在序列化中只有一个位置来放置未知的甚至是新的属性。
作者还注意到 HTTP 规范现在遵循类似的模式，不再建议扩展 HTTP 头部以 `X-` 为前缀。

## Creating CloudEvents/生产 CloudEvents

CloudEvents 规范有意避免将 CloudEvents 的创建方式设计的过于死板。
例如，它不假定原始事件源必须是该事件生产对应 CloudEvent 的同一实体。
这允许多种实现方式。
但是，对于规范的实现者来说，理解规范作者心中的期望还是有帮助的，因为这将有助于确保互操作性和一致性。

如上所述，生成初始事件的实体是否与创建相应 CloudEvent 的实体相同是由实现决定的。
但是，当构建/填充 CloudEvents 属性的实体代表事件源进行操作时，这些属性的值是用来描述事件或事件源，
而不是计算 CloudEvent 属性值的实体的。
换句话说，当事件源和 CloudEvents 生产者之间的分离对事件使用者没有实质性意义时，
规范定义的属性通常不会包含任何值来指示这种职责分离。

这并不是说 CloudEvents 生产者不能向 CloudEvent 添加一些额外的属性，
但这些属性超出了规范的互操作性定义属性的范围。
这类似于 HTTP 代理通常如何最大限度地减少对传入消息的明确定义的 HTTP 头部的更改，
但它可能会添加一些额外的头部，其中包括一些特定代理的元数据。

还值得注意的是，原始事件源和 CloudEvents 生产者之间的这种分离可大可小。
意思是，即使 CloudEvent 生产者不是原始事件源生态系统的一部分，
如果它代表事件源行事，并且它在事件流中的存在对事件消费者没有意义，那么上述指导仍然适用。

当实体同时充当 CloudEvents 的接收者和发送者以转发或转换传入事件时，
出站 CloudEvent 与入站 CloudEvent 匹配的程度将根据该实体的处理语义而有所不同。
在它充当代理的情况下，它只是将 CloudEvents 转发给另一个事件消费者，
那么出站 CloudEvent 通常看起来与入站 CloudEvent 就规范定义的属性相同
- 请参阅上一段有关添加其他属性的内容。

但是，如果此实体正在执行 CloudEvent 的某种类型的语义处理，
通常会导致 `data` 属性值发生更改，
则可能需要将其视为与原始事件源不同的“事件源”。
因此，与事件生产者相关的 CloudEvents 属性（例如`source` and `id`）
将从传入的 CloudEvent 中更改。

可能存在需要创建包含另一个 CloudEvent 的 CloudEvent 的特殊情况。
虽然规范没有明确定义嵌套，但它是可能的。
虽然内部事件将始终以[独立的事件格式](spec.md#event-format事件格式) 编码，
但外部事件可能是二进制或结构化模式的。
外部事件的 `datacontenttype` 属性不得设置为 `application/cloudevents+json`
或任何其它用于表示使用结构化模式的媒体类型。
事件嵌套的正确示例是：

```
Content-Type: application/json
ce-specversion: 1.0
ce-type: myevent
ce-id: 1234-1234-1234
ce-source: example.com

{
  "specversion": "1.0",
  "type": "coolevent",
  "id": "xxxx-xxxx-xxxx",
  "source": "bigco.com",
  "data": { ... }
}
```

## Qualifying Protocols and Encodings/合理化协议与编码

正如规范中所表达的，CloudEvents 工作的明确目标是
“以通用方式描述事件数据”且
“定义允许服务产生或消费事件的事件系统的互操作性，其中生产者和消费者可以被独立开发和部署”。

这种互操作性的基础是开放的数据格式和协议，
CloudEvents 旨在提供这种开放的数据格式，并将其数据格式映射到常用协议和常用编码上。

虽然每个软件或服务产品和项目都可以自己选择自己喜欢的通信形式，
但毫无疑问，这种产品或项目私有的专有协议无法进一步实现跨生产者和消费者的广泛互操作性的目标。

特别是在消息传递和事件处理领域，该行业在过去十年中开发出了强大且受到广泛支持的协议
例如 HTTP 1.1 和 HTTP/2 以及 WebSockets 或 Web 上的事件，或者 MQTT 和 AMQP
用于面向连接的消息传递和遥测传输的协议。

一些广泛使用的协议已经成为事实上的标准，这些协议来自三个或更多公司的顶级财团打造的强大生态系统，
还有一些来自单个公司发布的强大项目生态系统，在任何一种情况下都与前面提到的标准栈的演变相一致。

CloudEvents 的努力不应成为认可或推广项目或产品专有协议的工具，
因为这与CloudEvents 的原始目标背道而驰。

要使协议或编码符合核心 CloudEvents 事件格式或协议绑定的条件，它必须属于以下任一类别：

- 该协议具有广泛认可的多供应商协议标准化机构（例如 W3C、IETF、OASIS、ISO）的正式标准地位
- 该协议在其生态系统类别中具有“事实上的标准”地位。
  这意味着它被广泛使用，甚至被认为是给定应用程序的标准。
  实际上，我们希望在供应商中立的开源组织（例如 Apache、Eclipse、CNCF、.NET 基金会）的保护伞下
  看到至少一个开源实现，
  并且至少有十几个独立供应商在他们的产品中使用它的产品或服务。

除了正式状态之外，协议或编码是否符合核心 CloudEvents 事件格式或协议绑定的一个关键标准是，
该组织是否认为协议或编码出现后，该规范对与产品或项目无关的任何一方具有持续的实际利益。
对此的基本要求是协议或编码的定义方式允许独立于产品或项目代码的替代实现。

欢迎将 CloudEvents 的所有其他协议和编码格式
包含在指向相应项目自己的公共仓库，或站点中的 CloudEvents binding信息的列表中。

## Proprietary Protocols and Encodings/专有的协议与编码

为了鼓励更多人采用 CloudEvents，本仓库将自动收集专有协议和编码。
本仓库的维护人员不负责创建、维护或通知专有规范的维护人员有关专有规范和 CloudEvents 规范间的偏差。

专有规范将托管在他们自己的仓库或文档站点中，并记录在[专有规范](../../proprietary-specs.md)
文件中。 专有规范应遵循与核心协议和编码相关的其他规范相同的格式。

专有规范将比核心规范受到更少的审查，并且随着 CloudEvents 规范的发展，
相应协议和编码的维护者有责任使规范与 CloudEvents 规范保持同步。
如果专有规范过时太多，CloudEvents 可能会将指向该规范的链接标记为已弃用或将其删除。

如果为同一个协议创建了多个不兼容的规范，存储库维护者将不知道哪个规范是正确的，并列出所有规范的链接。

## Prior Art/现有技术

本节介绍了工作组在 CloudEvent 规范开发过程中使用的一些输入材料。

### Roles/角色

下面列举了可能涉及事件的产生、管理或消费的各种参与者和场景。

在这些中，事件生产者和事件消费者的角色保持不同。 单个应用程序上下文始终可以同时承担多个角色，包括既是事件的生产者又是事件的消费者。

1. 应用程序生成供他人使用的事件，
   如为消费者提供有关终端用户活动、状态变化或环境观察的见解，
   或允许通过事件驱动的扩展来补充应用程序的功能。

   生产的事件通常与上下文或生产者选择的分类相关。
   例如，房间中的温度传感器可能被安装位置、房间、楼层和建筑物等上下文限定。
   运动结果可以按联赛和球队分类。

   生产者应用程序可以在任何地方运行，例如在服务器或设备上。

   生产的事件可能由生产者或中间人直接提供和发出；
   作为后者的示例，请考虑设备通过负载大小受限的网络（如 LoRaWAN 或 ModBus）传输的事件数据，
   并且符合此规范的事件将由网络网关代表生产者提供。

   例如，气象站每 5 分钟通过 LoRaWAN 传输一次 12 字节的专有事件 payload 用于指示天气状况。
   然后使用 LoRaWAN 网关以 CloudEvents 格式将事件发布到 Internet 目标。
   LoRaWAN 网关是事件生产者，代表气象站发布事件，并将设置一定的元数据以反映事件的来源(气象站)。

2. 应用程序可能以以下目的：
   如显示、存档、分析、工作流处理、监控状态或提供业务解决方案及其基本构建模块的透明化
   来消费事件。

   消费者应用程序可以在任何地方运行，例如在服务器或设备上。

   消费应用程序通常对以下内容感兴趣：

    - 区分事件，使得完全相同的事件不会被处理两次。
    - 识别和选择源上下文或生产者指定的分类。
    - 确定事件相对于原始上下文或相对于时钟的时间顺序。
    - 了解事件中携带的上下文相关的详细信息。
    - 关联来自多个事件生产者的事件实例并将它们发送到相同的消费者上下文。

   在某些情况下，消费应用程序可能对以下内容感兴趣：

    - 从原始上下文中获取有关事件主题的更多详细信息，例如获取有关需要特权访问授权的已更改对象的详细信息。
      例如，出于隐私原因，HR 解决方案可能仅在事件中发布非常有限的信息，
      任何需要更多数据的事件消费者都必须在其自己的授权上下文背景下从 HR 系统获取与事件相关的详细信息
    - 在原始上下文中与事件的主题进行交互，例如在被告知该数据块刚刚创建后读取存储该数据块。

   消费者的兴趣激发了信息生产者应该包括事件的需求。

3. 中间件将事件从生产者路由到消费者，或转发到其他中间件。
   产生事件的应用程序可能会将根据消费者需求产生的某些任务委托给中间件：

    - 管理同时对大量类别和上下文背景中的某个事件感兴趣的消费者。
    - 代表消费者在类或事件的原始上下文上处理过滤条件。
    - 转码，比如从 JSON 解码后在 MsgPack 中编码。
    - 更改事件结构的转换，例如从专有格式映射到 CloudEvents，同时保留事件的身份和语义完整性。
    - 即时“推送式”传输给感兴趣的消费者。
    - 存储最终传输的事件，用于由消费者发起的“拉”请求，或延迟后由中间件发起“推”请求。
    - 观察事件内容或事件流以进行监控或诊断。

   为了满足这些需求，中间件将对以下方面感兴趣：

    - 一种元数据鉴别器，可用于事件的分类或上下文化，以便消费者可以表达对一个或多个类或上下文的兴趣。
      例如，消费者可能对文件存储帐户内的特定目录相关的所有事件感兴趣。
    - 一种元数据鉴别器，允许区分该类或上下文的特定事件的主题。例如，消费者可能希望过滤掉与以“.jpg”结尾的
      新文件相关的所有事件（文件名是“新文件”事件的主题），以此表示它对感兴趣的文件存储账户下某个目录的
      上下文环境。
    - 一个事件及其数据编码的指示器。
    - 一个事件及其数据的结构布局（模式）的指示器。

   事件是否可通过中间件消费取决于生产者的选择。

   在实践中，当中间件改变事件的语义时可以扮演[生产者](spec.md#producer生产者)的角色，
   当它根据事件采取行动时可以扮演[消费者](spec.md#consumer消费者)的角色，
   或者当它路由事件而不进行语义改变时可以扮演[中间人](spec.md#intermediary中间人)的角色。

4. 框架和其他抽象使与事件平台基础设施间的交互更简单，
   并且通常为多个事件平台基础设施提供公共 API 区域。

   框架通常用于将事件转换为对象图，并将事件分派给某些特定的处理逻辑或用户规则，
   这些用户逻辑或用户规则允许消费应用程序对原始上下文和特定主题中的特定类型的事件做出反应。

   框架最感兴趣的是跨抽象平台的语义元数据通用性，以便可以统一处理类似的活动。

   对于体育应用程序，使用该框架的开发人员可能对联盟中一支球队今天的比赛（主题）
   的所有事件感兴趣，但希望以不同于“换人”事件的方式处理“得分”事件。
   为此，框架将需要一个合适的元数据鉴别器，使其不必了解事件细节。
   需要明确的是，合适的元数据鉴别器应该由生产者填充，而不是框架的责任。

### Value Proposition/价值主张

本节介绍了一些能够展示 CloudEvents 价值主张的用例。

#### 跨服务和平台规范化事件

主要事件发布者（例如 AWS、Microsoft、Google 等）都在各自的平台上以不同的格式发布事件。
甚至在少数情况下，同一提供商的服务以不同格式（例如 AWS）发布事件。
这迫使事件消费者实现自定义逻辑以跨平台读取或处理事件数据，有时甚至需要跨单个平台的多个服务处理。

CloudEvents 可以为那些跨平台和服务处理事件的使用者提供单一体验。

#### 促进跨服务和平台的集成

跨环境传输的事件数据越来越普遍。
然而，如果没有描述事件的通用方式，跨环境的事件传递就会受到阻碍。
CloudEvents之前没有单一的方法可以确定事件的来源和可能的去向。
这对研究成功传输事件事件工具和消费者知道如何处理事件数据形成了巨大阻碍。

CloudEvents 提供有用的元数据，中间件和消费者可以依赖这些元数据来促进事件路由、日志记录、传输和接收。

#### 提高功能即服务的可移植性

功能即服务( FaaS )（也称为 serverless 计算）是 IT 中增长最快的趋势之一，它主要是由事件驱动的。
然而，FaaS 的一个主要问题是供应商锁定。
这种锁定部分是由函数 API 和供应商之间签名的差异引起的，
锁定同样也是由函数内接收的事件数据格式的差异引起的。

CloudEvents 提供描述事件数据的通用方式提高了功能即服务的可移植性。

#### 改进事件驱动/serverless架构的开发和测试

缺乏通用事件格式使事件驱动和 serverless 架构的开发和测试变得复杂。
没有简单的方法可以准确地为开发和测试目的模拟事件，并帮助在开发环境中模拟事件驱动的工作流。

CloudEvents 可以提供更好的开发工具来构建、测试和处理事件驱动和无服务器架构的端到端生命周期。

#### 事件数据发展

大多数平台和服务对其事件的数据模型进行不同的版本控制（如果他们这样做的话）。
随着这些数据模型的发展，这会为发布和使用事件的数据模型带来不一致的体验。

CloudEvents 可以提供一种通用的方式来版本化和演化事件数据的发展。
这将帮助事件发布者根据最佳实践安全地对其数据模型进行版本控制，
并且这有助于事件消费者随着事件数据的发展安全地使用它。

#### 规范化 Webhook

Webhooks 是一种不使用通用格式的来发布事件的模式。
Webhook 的使用者没有一致的方式来开发、测试、识别、验证和整体处理通过 Webhook 传输的事件数据。

CloudEvents 可以提供 Webhook 发布和消费事件的一致性。

#### 安全策略

出于安全和策略考虑，可能需要过滤、转换或阻止系统之间的事件传输。
比如可能需要防止事件的进入或退出，如包含敏感信息的事件数据或想要禁止发送方和接收方之间的信息流。

通用事件格式将允许更容易地推理正在传输的数据，并提供更好的数据自查。

#### 事件追踪

从源发送的事件可能会出现在一系列附加事件序列之中，
这些附加事件序列从各种中间件设备（例如事件代理和网关）发出。
CloudEvents 在事件中包含元数据以将这些事件关联为事件序列的一部分，以便进行事件跟踪和故障排除。

#### IoT/物联网

物联网设备会发送和接收与其功能相关的事件。
例如，连接的恒温器将发送有关当前温度的遥测数据，
并可以接收改变温度的事件。
这些设备通常具有受限的操作环境（cpu、内存），需要明确定义的事件消息格式。
在很多情况下，这些消息是二进制编码的，而不是文本的。
无论是直接来自设备还是通过网关转换，CloudEvents 都可以更好地描述消息的来源和消息中包含的数据格式。

#### 事件关联

一个 serverless 应用或工作流可能与来自不同事件源或事件生产者的多个事件相关联。
例如，盗窃检测应用程序/工作流可能涉及运动事件和门/窗打开事件。
一个 serverless 平台可能接收每种类型事件的许多实例，例如 它可以接收来自不同房屋的运动事件和开窗事件。

serverless 平台需要将一种类型的事件实例与其他类型的事件实例正确关联，
并将接收到的事件实例映射到正确的应用/工作流实例。
CloudEvents 将为任何事件使用者（例如 serverless 平台）提供一种标准方式，
以在事件数据中定位事件关联信息/令牌并将接收到的事件实例映射到正确的应用/工作流实例。

### Existing Event Formats/现有的数据格式

与上一节一样，对当前现状的调查（和理解）对 CloudEvents 小组来说非常重要。
为此，下面列出了在实践中被广泛使用的当前事件格式的样本。

#### Microsoft - Event Grid/微软 - 事件网格

```json
{
  "topic": "/subscriptions/{subscription-id}",
  "subject": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.EventGrid/eventSubscriptions/LogicAppdd584bdf-8347-49c9-b9a9-d1f980783501",
  "eventType": "Microsoft.Resources.ResourceWriteSuccess",
  "eventTime": "2017-08-16T03:54:38.2696833Z",
  "id": "25b3b0d0-d79b-44d5-9963-440d4e6a9bba",
  "data": {
    "authorization": "{azure_resource_manager_authorizations}",
    "claims": "{azure_resource_manager_claims}",
    "correlationId": "54ef1e39-6a82-44b3-abc1-bdeb6ce4d3c6",
    "httpRequest": "",
    "resourceProvider": "Microsoft.EventGrid",
    "resourceUri": "/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.EventGrid/eventSubscriptions/LogicAppdd584bdf-8347-49c9-b9a9-d1f980783501",
    "operationName": "Microsoft.EventGrid/eventSubscriptions/write",
    "status": "Succeeded",
    "subscriptionId": "{subscription-id}",
    "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47"
  }
}
```

[Documentation](https://docs.microsoft.com/en-us/azure/event-grid/event-schema)

#### Google - Cloud Functions (potential future)/谷歌 - 云函数 (潜在的未来)

```json
{
  "data": {
    "@type": "types.googleapis.com/google.pubsub.v1.PubsubMessage",
    "attributes": {
      "foo": "bar"
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

#### AWS - CloudWatch Events/亚马逊 - CloudWatch 事件

AWS 上的很大一部分事件处理系统都在使用这种格式。

```json
{
  "version": "0",
  "id": "6a7e8feb-b491-4cf7-a9f1-bf3703467718",
  "detail-type": "EC2 Instance State-change Notification",
  "source": "aws.ec2",
  "account": "111122223333",
  "time": "2017-12-22T18:43:48Z",
  "region": "us-west-1",
  "resources": [
    "arn:aws:ec2:us-west-1:123456789012:instance/i-1234567890abcdef0"
  ],
  "detail": {
    "instance-id": "i-1234567890abcdef0",
    "state": "terminated"
  }
}
```

#### IBM - OpenWhisk - Web Action Event/IBM - OpenWhisk - Web Action事件

```json
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

#### OpenStack - Audit Middleware - Event /OpenStack - 审计中间件 - 事件

```json
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

#### Adobe - I/O Events/Adobe - I/O 事件

```json
{
  "event_id": "639fd17a-d0bb-40ca-83a4-e78612bce5dc",
  "event": {
    "@id": "82235bac-2b81-4e70-90b5-2bd1f04b5c7b",
    "@type": "xdmCreated",
    "xdmEventEnvelope:objectType": "xdmAsset",
    "activitystreams:to": {
      "xdmImsUser:id": "D13A1E7053E46A220A4C86E1@AdobeID",
      "@type": "xdmImsUser"
    },
    "activitystreams:generator": {
      "xdmContentRepository:root": "https://cc-api-storage.adobe.io/",
      "@type": "xdmContentRepository"
    },
    "activitystreams:actor": {
      "xdmImsUser:id": "D13A1E7053E46A220A4C86E1@AdobeID",
      "@type": "xdmImsUser"
    },
    "activitystreams:object": {
      "@type": "xdmAsset",
      "xdmAsset:asset_id": "urn:aaid:sc:us:4123ba4c-93a8-4c5d-b979-ffbbe4318185",
      "xdmAsset:asset_name": "example.jpg",
      "xdmAsset:etag": "6fc55d0389d856ae7deccebba54f110e",
      "xdmAsset:path": "/MyFolder/example.jpg",
      "xdmAsset:format": "image/jpeg"
    },
    "activitystreams:published": "2016-07-16T19:20:30+01:00"
  }
}
```

[Documentation](https://developer.adobe.com/events/docs/)
