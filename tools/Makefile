all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip external links
	@tools/verify-links.sh -t -v .
	@echo Running the spec phrase checker:
	@tools/verify-specs.sh -v .
	@echo Running the doc phrase checker:
	@tools/verify-docs.sh -v .
	@echo Running the languages phrase checker:
	@python tools/verify-languages.py -v .
