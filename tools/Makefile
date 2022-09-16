all: test verify 

verify:
	@echo Verifing Specification
	@python tools/verify.py .

test:
	@echo Testing Verification
	@pytest tools/ -q
