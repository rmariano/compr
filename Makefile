PYTHON:=$(VIRTUAL_ENV)/bin/python
PIP:=$(VIRTUAL_ENV)/bin/pip

.PHONY: build
build:
	$(VIRTUAL_ENV)/bin/pip install wheel
	$(PYTHON) setup.py sdist bdist_wheel

.PHONY: typehint
typehint:
	@./tests/checklist/typehint.sh

.PHONY: testdeps
testdeps:
	$(PIP) install -e .[tests]

.PHONY: tox
tox: testdeps
	$(PIP) install tox
	tox

.PHONY: unit
unit:
	pytest -sv tests/unit/ $(ARGS)

.PHONY: functional
functional:
	pytest -sv tests/functional/ $(ARGS)

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
	$(PIP) install --dev -e .[docs]
	$(MAKE) -C doc/ html
	@xdg-open doc/_build/html/index.html


# use; make release VERSION=<version>
.PHONY: release
release:
	git tag -s $(VERSION)
