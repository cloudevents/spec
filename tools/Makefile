all: verify

verify:
	@echo Running href checker:
	@python tools/verify-links.py .
	@echo Running the doc phrase checker:
	@python tools/verify-docs.py -v .
