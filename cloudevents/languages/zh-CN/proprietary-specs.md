# CloudEvent 专有协议与编码规范

免责声明：CloudEvents并不支持这些协议或规范，也不能保证它们能与CloudEvents的当前版本保持一致。使用这些协议的项目维护者应该保证这些协议与CloudEvents的最新版本的兼容性。

- [Apache RocketMQ Transport Binding](https://github.com/apache/rocketmq-externals/blob/master/rocketmq-cloudevents-binding/rocketmq-transport-binding.md)
- [Google Cloud Pub/Sub Protocol Binding](https://github.com/google/knative-gcp/blob/master/docs/spec/pubsub-protocol-binding.md)

**想要添加一个专属的传输层协议绑定？**

- 根据现有的绑定规范的格式来创建自己的规范 (如 [http](../../bindings/http-protocol-binding.md) or [amqp](../../bindings/amqp-protocol-binding.md)) - 这会对相应的SDKs开发有帮助。
  - **注意：**
    - 这个新建的规范必须能被公开访问，同时它必须被提出它的组织所管理。
    - 这个新建的规范必须明确地指出它支持的CloudEvents版本.
- 为这个新建的规范创立一个PR。
- 回复在这个PR下的相关评论，可能会被要求加入到工作组的常规会话中。
