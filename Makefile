.PHONY: clean-pyc clean-build clean lint test coverage sync-data release dist
SHELL := /bin/bash

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with ruff"
	@echo "test - run the test suite with pytest"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "sync-data - regenerate bundled datasets from data/parquet"
	@echo "release - package and upload a release"
	@echo "dist - package"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	ruff check russiannames tests

test:
	pytest

coverage:
	coverage run --source russiannames -m pytest
	coverage report -m
	coverage html
	python3 -m webbrowser htmlcov/index.html

sync-data:
	cp data/parquet/names.parquet data/parquet/surnames.parquet data/parquet/midnames.parquet russiannames/data/

release: dist
	python3 -m twine upload dist/*

dist: clean sync-data
	python3 -m build
	ls -l dist
