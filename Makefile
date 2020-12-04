all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip external links
	@tools/verify-links.sh -t -v .
	@echo Running the spec phrase checker:
	@tools/verify-specs.sh -v \
		amqp-protocol-binding.md \
		avro-format.md \
		documented-extensions.md \
		http-protocol-binding.md \
		http-webhook.md \
		json-format.md \
		kafka-protocol-binding.md \
		mqtt-protocol-binding.md \
		nats-protocol-binding.md \
		protobuf-format.md \
		spec.md \
		websockets-protocol-binding.md \
		\
		discovery.md \
		pagination.md \
		subscriptions-api.md 
	@echo Running the doc phrase checker:
	@tools/verify-docs.sh -v .
