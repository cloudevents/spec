all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip external links
	@misc/tools/verify-links.sh -t -v .
	@echo Running the spec phrase checker:
	@misc/tools/verify-specs.sh -v \
		cloudevents/bindings/amqp-protocol-binding.md \
		cloudevents/formats/avro-format.md \
		cloudevents/documented-extensions.md \
		cloudevents/bindings/http-protocol-binding.md \
		cloudevents/http-webhook.md \
		cloudevents/formats/json-format.md \
		cloudevents/bindings/kafka-protocol-binding.md \
		cloudevents/bindings/mqtt-protocol-binding.md \
		cloudevents/bindings/nats-protocol-binding.md \
		cloudevents/formats/protobuf-format.md \
		cloudevents/spec.md \
		cloudevents/bindings/websockets-protocol-binding.md \
		\
		discovery/spec.md \
		pagination/spec.md \
		subscriptions/spec.md 
	@echo Running the doc phrase checker:
	@misc/tools/verify-docs.sh -v .
