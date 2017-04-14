.PHONY: dev
dev:
	pip install -e .

.PHONY: typehint
typehint: testdeps
	mypy compressor/

.PHONY: testdeps
testdeps:
	pip install -U -e .[tests]

.PHONY: test
test:
	pytest

.PHONY: lint
lint:
	@./tests/checklist/linting.sh

.PHONY: checklist
checklist: testdeps lint test

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
