all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip external links
	@tools/verify-links.sh -t -v .
	@echo Running the spec phrase checker:
	@tools/verify-specs.sh -v \
		cloudevents/amqp-protocol-binding.md \
		cloudevents/avro-format.md \
		cloudevents/documented-extensions.md \
		cloudevents/http-protocol-binding.md \
		cloudevents/http-webhook.md \
		cloudevents/json-format.md \
		cloudevents/kafka-protocol-binding.md \
		cloudevents/mqtt-protocol-binding.md \
		cloudevents/nats-protocol-binding.md \
		cloudevents/protobuf-format.md \
		cloudevents/spec.md \
		cloudevents/websockets-protocol-binding.md \
		\
		discovery/discovery.md \
		pagination/pagination.md \
		subscriptions/subscriptions-api.md 
	@echo Running the doc phrase checker:
	@tools/verify-docs.sh -v .
