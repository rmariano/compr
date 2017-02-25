.PHONY: dev
dev:
	pip install -e .

.PHONY: test
test: dev
	python setup.py test

.PHONY: clean
clean:
	rm .coverage
	rm -fr .cache/
	find . -type f -name "*.pyc" -delete

.PHONY: dev
dev:
	pip install -e .

.PHONY: doc
doc:
	pip install -e .[docs]
	make -C doc/ html
	@xdg-open doc/_build/html/index.html
