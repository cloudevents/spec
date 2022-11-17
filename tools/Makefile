all: test_tools verify

deps:
	@python -m pip install -qq -r tools/requirements.txt

verify:
	@python tools/verify.py .

test_tools:
	@pytest tools/

docker:
	@docker run -ti -v $(PWD):/tmp/spec -w /tmp/spec python:latest \
	    make -f tools/Makefile deps test_tools verify
