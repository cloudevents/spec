all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip external links
	@tools/verify-links.sh -t -v .
	@echo Running the spec phrase checker:
	@tools/verify-specs.sh -v spec.md documented-extensions.md json-format.md \
		http-protocol-binding.md http-webhook.md mqtt-protocol-binding.md \
		nats-protocol-binding.md \
		kafka-protocol-binding.md avro-format.md
	@echo Running the doc phrase checker:
	@tools/verify-docs.sh -v .
