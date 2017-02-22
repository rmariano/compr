all:

.PHONY: test
test: dev
	py.test --cov-report=html --cov=compressor tests/

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
	make -C doc/ html
	@xdg-open doc/_build/html/index.html
