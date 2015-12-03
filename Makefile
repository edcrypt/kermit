.PHONY: clean help kermit test

PYTHON = python
RPYTHON = rpython

OPTS = "--output=bin/kermit"
TARGET = "kermit/main.py"

all: clean test build

help:
	@echo "clean    Remove build artifacts"
	@echo "build    Build the interpreter"
	@echo "test     Run unit and integration tests"

clean:
	@rm -rf bin/kermit

build:
	$(RPYTHON) $(OPTS) $(TARGET)

test:
	$(PYTHON) setup.py test
