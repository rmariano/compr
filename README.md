[![image](https://img.shields.io/travis/rmariano/compr.svg?style=flat-square)](https://travis-ci.org/rmariano/compr)

>   :alt: CI Status

[![Documentation Status](https://readthedocs.org/projects/compr/badge/?version=latest&style=flat-square)](http://compr.readthedocs.io/en/latest/?badge=latest)

[![coverage](https://codecov.io/gh/rmariano/compr/branch/master/graph/badge.svg)](https://codecov.io/gh/rmariano/compr)

[![image](https://img.shields.io/pypi/pyversions/trenzalore.svg?style=flat-square)](https://pypi.python.org/pypi/trenzalore)

# PyCompress

`Pycompressor` is a tool for compressing text files into smaller ones,
as well as extracting compressed files back into the original content.

It can be used as a program or imported as a package module, and use the
functions defined on it.

For example, in order to compress one file:

``` bash
$ pycompress -c /usr/share/dict/words -d /tmp/compressed.zf
```

The original file, in this example has a size of `~4.8M`, and the tool
left the resulting file at `/tmp/compressed.zf`, with a size of `~2.7M`.

In order to extract it:

``` bash
$ pycompress -x /tmp/compressed.zf -d /tmp/original
```

You can specify the name of the resulting file with the `-d` flag. If
you don\'t indicate a name for the resulting file, the default will be
`<original-file>.comp`.

For the full options, run:

``` bash
$ pycompress -h
```

## Installation

``` bash
pip install trenzalore
```

Will install the package and leave an application named `pycompress` for
using the command line utility.

## Development

To install the package in development mode, run:

    make testdeps

And run the tests with:

    make test

Before submitting a pull request, run the checklist to make sure all
dependencies are met (code style/linting, tests, pass, etc.). This is
automated with:

``` bash
make checklist
```

This will run the checks for the code style (`make lint`), as well as
the tests (`make test`).
