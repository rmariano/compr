all:

test:
	py.test --cov-report=html --cov=compressor tests/

clean:
	rm .coverage
	rm -fr .cache/
	find . -type f -name "*.pyc" -delete

.PHONY: doc
doc:
	cd doc && make html && cd ..

.PHONY: all test clean
