all: verify

verify:
	@echo Running href checker:
	@# Use "-x" if you want to skip exernal links
	@tools/verify-links.sh -v .
