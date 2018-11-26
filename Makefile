all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip external links
	@tools/verify-links.sh -v .
	@echo Running the spec phrase checker:
	@tools/verify-specs.sh -v spec.md documented-extensions.md json-format.md \
		http-transport-binding.md http-webhook.md mqtt-transport-binding.md \
		nats-transport-binding.md protobuf-format.md \
		rocketmq-transport-binding.md
	@echo Running the doc phrase checker:
	@tools/verify-docs.sh -v .
