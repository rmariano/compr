.. compressor documentation master file, created by
   sphinx-quickstart on Wed Nov 16 20:14:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: https://img.shields.io/travis/rmariano/compr.svg?style=flat-square
   :target: https://travis-ci.org/rmariano/compr
   :alt: CI Status

.. image:: https://codecov.io/gh/rmariano/compr/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/rmariano/compr
   :alt: coverage


PyCompressor
============

``Pycompressor`` is a tool for compressing text files into smaller ones, as
well as extracting compressed files back into the original content.

For example, in order to compress one file:

.. code:: bash

    $ pycompress -c -d /tmp/compressed.zf /usr/share/dict/words

The original file, in this example has a size of ``~4.8M``, and the tool left
the resulting file at ``/tmp/compressed.zf``, with a size of ``~2.7M``.

In order to extract it:

.. code:: bash

    $ pycompress -x -d /tmp/original /tmp/compressed.zf

You can specify the name of the resulting file with the ``-d`` flag. If you
don't indicate a name for the resulting file, the default will be
``<original-file>.comp``.

For the full options, run:

.. code:: bash

    $ pycompress -h


Contents:

.. toctree::
   :maxdepth: 2

   using-the-cli
   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
