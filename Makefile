PYTHON:=$(VIRTUAL_ENV)/bin/python
PIPENV:=$(VIRTUAL_ENV)/bin/pipenv
PIP:=$(VIRTUAL_ENV)/bin/pip

.PHONY: build
build:
	$(VIRTUAL_ENV)/bin/pip install wheel
	$(PYTHON) setup.py sdist bdist_wheel

.PHONY: dev
dev:
	$(PIP) install pipenv
	$(PIPENV) install --dev -e .

.PHONY: typehint
typehint:
	@./tests/checklist/typehint.sh

.PHONY: testdeps
testdeps:
	$(PIPENV) install --dev -e .[tests]
	touch testdeps

.PHONY: unit
unit:
	$(PIPENV) run pytest -sv tests/unit/

.PHONY: functional
functional:
	$(PIPENV) run pytest -sv tests/functional/

.PHONY: test
test: unit functional

.PHONY: lint
lint:
	@./tests/checklist/linting.sh

.PHONY: checklist
checklist: testdeps lint typehint test

.PHONY: clean
clean:
	rm -fr .coverage .cache/ .tox/ build/ .mypy_cache/ *.comp dist
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -fr {} +

.PHONY: doc
doc:
	$(PIPENV) install --dev -e .[docs]
	$(PIPENV) run make -C doc/ html
	@xdg-open doc/_build/html/index.html

.PHONY: tox
tox:
	$(PIPENV) install tox
	$(PIPENV) run tox

# use; make release VERSION=<version>
.PHONY: release
release:
	git tag -s $(VERSION)
