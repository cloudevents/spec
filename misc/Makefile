all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip external links
	@misc/tools/verify-links.sh -v .
	@echo Running the spec phrase checker:
	@misc/tools/verify-specs.sh -v 
	    cloudevents/spec.md \
		cloudevents/documented-extensions.md \
		cloudevents/formats/json-format.md \
		cloudevnets/bindings/http-protocol-binding.md \
		cloudevents/http-webhook.md \
		cloudevents/bindings/mqtt-protocol-binding.md \
		cloudevents/bindings/nats-protocol-binding.md \
		cloudevents/bindings/kafka-protocol-binding.md \
		cloudevents/formats/avro-format.md
	@echo Running the doc phrase checker:
	@misc/tools/verify-docs.sh -v .
