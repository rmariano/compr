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
