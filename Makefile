all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip exernal links
	@tools/verify-links.sh -v .
	@echo Running the spec phrase checker:
	@tools/verify-specs.sh -v spec.md extensions.md serialization.md
	@echo Running the doc phrase checker:
	@tools/verify-docs.sh -v .
