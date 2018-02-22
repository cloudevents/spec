all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip exernal links
	@tools/verify-links.sh -v .
	@echo Running the RFC2119 keyword checker:
	@tools/verify-phrases.sh -v spec.md
