.PHONY: dev
dev:
	pip install -e .

.PHONY: test
test:
	pip install -e .[tests]
	pytest

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
