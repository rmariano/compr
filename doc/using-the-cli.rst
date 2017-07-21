Using the Application
---------------------

This section explains how the application is used from the command line
interface (``cli``), detailing which parameters are accepted and how they work.


Basic usage
^^^^^^^^^^^

Compressing a File
******************

You can start using the program by just running it, and telling
``pycompressor`` the name of the file you'd like to compress, for example::

    $ pycompress -c /usr/share/dict/words

The `-c` parameter stands for "compress", and if nothing else is specified, the
resulting file will be left on the current directory, with the base name of the
provided file and the ``.comp`` suffix. In this example, the result of will be a
file named ``words.comp``.

You can change the name of the resulting file, by passing the `-d`
(destination) flag, like in::

    $ pycompress -c -d /tmp/compressed.zf /usr/share/dict/words

In this case the resulting file (after compressed) will be
``/tmp/compressed.zf``.

Extracting a file
*****************

If you want to recover the original file from a binary, compressed one, use the
``-x`` (extract) flag::

    $ pycompress -x /tmp/compressed.zf

If a name for the resulting file is not specified, it'll assume the base name
provided with the ``.extr`` suffix, in the local path of where the command is
being applied. In this case, it would be ``compressed.zf.extr``.


You can also indicate the name of the destination file, again with the ``-d``
parameter::

    $ pycompress -x -d /tmp/original /tmp/compressed.zf

The destination file in this case, indicates that after extracted the file is
written in ``/tmp/original``.
