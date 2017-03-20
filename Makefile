.PHONY: dev
dev:
	pip install -e .

.PHONY: typehint
typehint: testdeps
	mypy compressor/

.PHONY: testdeps
testdeps:
	pip install -e .[tests]

.PHONY: test
test: testdeps
	pytest

.PHONY: checklist
checklist: typehint test

.PHONY: clean
clean:
	rm .coverage
	rm -fr .cache/
	find . -type f -name "*.pyc" -delete

.PHONY: doc
doc:
	pip install -e .[docs]
	make -C doc/ html
	@xdg-open doc/_build/html/index.html
