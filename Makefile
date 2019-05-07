.PHONY: build
build:
	$(VIRTUAL_ENV)/bin/pip install wheel
	python setup.py sdist bdist_wheel

.PHONY: dev
dev:
	pip install -e .

.PHONY: typehint
typehint:
	@./tests/checklist/typehint.sh

.PHONY: testdeps
testdeps:
	pip install -Ue .[tests]

.PHONY: test
test:
	pytest

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
	pip install -e .[docs]
	make -C doc/ html
	@xdg-open doc/_build/html/index.html

.PHONY: tox
tox:
	pip install -U tox
	tox

# use; make release VERSION=<version>
.PHONY: release
release:
	git tag -s $(VERSION)
