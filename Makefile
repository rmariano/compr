all:

test:
	py.test --cov-report=html --cov=compressor tests/

clean:
	rm .coverage
	rm -fr .cache/
	find . -type f -name "*.pyc" -delete

.PHONY: all test clean
