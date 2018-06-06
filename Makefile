.PHONY: build
build:
	python setup.py bdist_wheel

.PHONY: dev
dev:
	pipenv install --dev -e .

.PHONY: typehint
typehint:
	@./tests/checklist/typehint.sh

.PHONY: testdeps
testdeps:
	pipenv install --dev -e .[tests]
	touch testdeps

.PHONY: unit
unit: testdeps
	pipenv run pytest -sv tests/unit/

.PHONY: functional
functional:
	pipenv run pytest -sv tests/functional/

.PHONY: test
test: unit functional

.PHONY: lint
lint:
	@./tests/checklist/linting.sh

.PHONY: checklist
checklist: testdeps lint typehint test

.PHONY: clean
clean:
	rm -fr .coverage .cache/ .tox/ build/ .mypy_cache/ *.comp
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -fr {} +

.PHONY: doc
doc:
	pipenv install --dev -e .[docs]
	pipenv run make -C doc/ html
	@xdg-open doc/_build/html/index.html

.PHONY: tox
tox:
	pip install -U tox
	tox

# use; make release VERSION=<version>
.PHONY: release
release:
	git tag -s $(VERSION)
