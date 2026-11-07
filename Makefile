PYTHON ?= python

.PHONY: help install test lint run demo clean

help:
	@printf '%s\n' 'install  Install the project and development tools' 'test     Run the test suite' 'lint     Run critical flake8 checks' 'run      Run the reasoning search CLI' 'demo     Run the DNA-like transformation demo' 'clean    Remove generated Python and pytest files'

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m flake8 . --count --select=E9,F63,F7,F82

run:
	$(PYTHON) -m infinity_algorithms_cli reason

demo:
	$(PYTHON) -m infinity_algorithms_cli demo

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache build dist *.egg-info
