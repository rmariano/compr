.PHONY: build
build:
	python setup.py bdist_wheel

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
	rm .coverage
	rm -fr .cache/ .tox/ build/
	find . -type f -name "*.pyc" -delete

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
