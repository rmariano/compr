.. image:: https://img.shields.io/travis/rmariano/compr.svg?style=flat-square 
   :target: https://travis-ci.org/rmariano/compr
   :alt: CI Status

.. begin

PyCompress
==========

Pycompress is a package that implements a text compression algorithm. The program
that implements this algorithm, allows the user to compress a text file, in a resulting
one which a smaller size, as well as extracting a compressed file (that was created by
the same means), resulting in the original one.

It can be used as a program or imported as a package module,
and use the functions defined on it.

Installation
------------

.. code:: bash

   pip install trenzalore


Will install the package and leave an application named `pycompress` for using
the command line utility.


Development
-----------

.. code:: python

    python setup.py develop

Run tests
---------

.. code:: bash

    make test
