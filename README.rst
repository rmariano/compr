PyCompress - Text compression tool
==================================

.. image:: https://img.shields.io/travis/rmariano/compr.svg?style=flat-square
   :target: https://travis-ci.org/rmariano/compr
   :alt: CI Status


.. image:: https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square
   :target: LICENSE
   :alt: MIT license


.. image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=flat-square
   :target: http://compr.readthedocs.io/en/latest/
   :alt: `Check the online documentation <http://compr.readthedocs.io/en/latest/>`_


.. contents ::


Introduction
------------

``PyCompress`` is a package that implements a text compression algorithm.

This project entails both a command line application, and a library.

The command line application is able to compress source files into smaller
ones, saving disk space, and also extracting the compressed files into the
original ones.

It can also be used as a library, imported from python, that achieve the same
functionality.


Installation
------------

.. code:: bash

   pip install trenzalore


Will install the package and leave an application named ``pycompress`` for
using the command line utility.


Development
-----------

Running tests:

.. code:: bash

    make test
