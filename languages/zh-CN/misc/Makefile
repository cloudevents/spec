all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip external links
	@misc/tools/verify-links.sh -t -v .
	@echo Running the spec phrase checker:
	@misc/tools/verify-specs.sh -v .
	@echo Running the doc phrase checker:
	@misc/tools/verify-docs.sh -v .
