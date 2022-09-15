all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip external links
	@python tools/verify-links.py .
	@echo Running the spec phrase checker:
	@tools/verify-specs.sh -v .
	@echo Running the doc phrase checker:
	@tools/verify-docs.sh -v .
