.PHONY: pip-install virtualenv

pip-install:
	pip install -r requirements.txt

virtualenv:
	python3 -m venv venv

lint:
	pylint src

