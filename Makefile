.PHONY: pip-install virtualenv lint test

install:
	pip install -r requirements.txt

virtualenv:
	python3 -m venv venv

lint:
	pylint src

test: install
	pytest src
