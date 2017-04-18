IMAGE := inloop-integration-test
SUITE := tests

PYTHON := python3.5
PYTAG  := $(shell echo $(PYTHON) | sed 's/thon//;s/\.//')
VENV   := $(PWD)/.venvs/$(PYTAG)

OPEN_CMD := $(shell command -v gnome-open || command -v xdg-open || command -v open)

TEST_CMD := ./manage.py test --failfast $(SUITE)
WATCH_DIRS := inloop tests

## Run the test suite (takes an optional SUITE= argument)
test: .state/docker
	$(TEST_CMD)

## Like 'test', but additionally record code coverage
coveragetest: .state/docker
	coverage run $(TEST_CMD)

## Generate and show the HTML coverage report in your browser
report:
	coverage html
	$(OPEN_CMD) htmlcov/index.html

## Watch for changes in Python code and re-run tests
watchmedo:
	@watchmedo shell-command --patterns="*.py" --recursive --command "$(TEST_CMD)" $(WATCH_DIRS)

## Start a live-reload proxy watching for style changes
browsersync:
	@command -v browser-sync >/dev/null || echo "Please run 'npm install -g browser-sync'." 1>&2
	@browser-sync start --proxy localhost:8000 --files "assets,inloop/**/*.html"

## Run basic code convention and quality checks
lint:
	isort --quiet --check-only
	flake8

## Run extended code convention and quality checks (slower)
xlint: lint
	bandit --recursive inloop || true
	pylint inloop tests || true

## Install Python and npm dependencies needed for development
install-deps:
	pip install -r requirements/main.txt
	pip install -r requirements/test.txt
	pip install -r requirements/lint.txt
	npm install --production

## Install Python tools (e.g., ipython, watchmedo, etc.)
install-tools:
	pip install -r requirements/dev.txt

.state/docker: tests/functional/testrunner/Dockerfile
	docker build -t $(IMAGE) tests/functional/testrunner
	mkdir -p .state
	touch .state/docker

virtualenv:
	rm -rf $(VENV)
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -U pip setuptools

initdb:
	mkdir -p .state
	python manage.py migrate
	python manage.py loaddata about_pages staff_group
	python manage.py loaddata demo_accounts development_site

## Initialize a developer environment (takes an optional PYTHON= argument)
devenv: virtualenv
	-cp -i .env_develop .env
	PATH=$(VENV)/bin:$(PATH) make install-deps install-tools initdb
	@echo
	@echo "virtualenv created -- now run 'source $(VENV)/bin/activate'."
	@echo

## Update version pins in the requirements files
deps:
	pip-compile --no-annotate --no-header --upgrade requirements/main.in >/dev/null
	pip-compile --no-annotate --no-header --upgrade requirements/prod.in >/dev/null

## Tidy up dangling docker images/containers and *.pyc files
clean:
	docker ps -q -f status=exited | xargs docker rm
	docker images -q -f dangling=true | xargs docker rmi
	find inloop tests -name "*.pyc" -delete
	find inloop tests -name "__pycache__" -delete

## Remove everything that can be installed or generated by this Makefile
purge: clean
	rm -rf .state .venvs .env node_modules htmlcov
	-docker rmi $(IMAGE)

define PYHELPTEXT
import re
contents = open('Makefile').read()
pattern = re.compile(r'## (.+)\\n([a-z-]+):')
for desc, target in pattern.findall(contents):
	print('  {:15s} {}'.format(target, desc))
endef

export PYHELPTEXT
help:
	@echo "Please specify one of the following targets:"
	@echo
	@echo "$$PYHELPTEXT" | python3
	@echo

.DEFAULT_GOAL := help
.PHONY: test coveragetest report watchmedo lint install-deps install-tools virtualenv initdb devenv deps clean purge help
