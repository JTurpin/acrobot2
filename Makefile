.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style with flake8
	flake8 acrobot tests

test: ## run tests quickly with the default Python
	py.test tests --cov=acrobot --cov-fail-under=100 --cov-branch --cov-report term-missing

test-all: lint test test-security

coverage: ## check code coverage quickly with the default Python
	coverage run --source acrobot -m pytest
	coverage report -m

install: clean ## install the package to the active Python's site-packages
	pip install -r requirements_dev.txt

install-dev: clean
	pip install -e . -r requirements_dev.txt --upgrade

install-local: clean
	pip install -e . -r requirements.txt --upgrade

routes:
	env FLASK_APP=run.py flask routes

run:
	env SERVICE_LOG_LEVEL=DEBUG FLASK_APP=run.py flask run

run-local:
	env SERVICE_LOG_LEVEL=DEBUG FLASK_ENV=development FLASK_APP=run.py flask run

shell:
	env FLASK_APP=run.py flask shell

db-init:
	python manage.py db init

db-upgrade:
	python manage.py db upgrade

db-migrate:
	python manage.py db migrate

db-migrate-prod:
	zappa invoke prod manage.run_upgrade
