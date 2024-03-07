# CloudEvents 扩展属性

[CloudEvents 规范](../spec.md)定义了一系列用来将通用事件转换为CloudEvent的元数据属性。该文档中指定的属性列表代表了作者认为在大多数情况下最可能用到的属性最小集。

在本文档中定义了一些额外的属性。这些属性尽管不像[CloudEvents 规范](../spec.md)中的属性那样常见，但精准使用这些属性，仍能为提高互操作性的程度提供帮助。这种额外属性的机制，同样允许新属性在被纳入到[CloudEvents 规范](../spec.md)之前，能以试验的形式被定义。

[CloudEvents 规范](../spec.md)的实现中不会限制必须使用本文档中提到的那些扩展属性。本文档中定义的扩展属性并不是正式的、稳定的，相反它们可能随时被修改，甚至删除。因此，引入本文档中的这些属性并不需要满足像[CloudEvents 规范](../spec.md)中其它属性那样的成熟度和流行性。要想定义一个收录在本文档中的扩展属性，除了正常的PR检查流程外，还需要至少两名[有投票权的成员](../../../../docs/GOVERNANCE.md#membership)在PR中留言支持。如果这个PR的作者本身就具有投票权，那么只需要另一名成员投票支持即可。

## 使用

任何对扩展属性的支持都不是必要的。当一个扩展属性使用了[RFC 2199](https://www.ietf.org/rfc/rfc2119.txt) 中的关键词（如MUST、SHOULD、MAY等）时，对这些关键词的使用仅适用于使用了这个扩展属性的事件。

扩展属性尽管没有定义在CloudEvents的核心规范中，它们同样必须遵守格式和协议绑定规范中定义的序列化规则。详情请见[扩展上下文属性](../spec.md#extension-context-attributes扩展上下文属性)

## 现有的扩展

- [Dataref (Claim Check Pattern)](../../../extensions/dataref.md)
- [Distributed Tracing](../../../extensions/distributed-tracing.md)
- [Expiry Time](../../../extensions/expirytime.md)
- [Partitioning](../../../extensions/partitioning.md)
- [Recorded Time](../../../extensions/recordedtime.md)
- [Sampling](../../../extensions/sampledrate.md)
- [Sequence](../../../extensions/sequence.md)
