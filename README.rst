============
uncythonize
============

This script strips cython code (.pyx files) down to python code, by
replacing cython declarations (cdef) with python equivalents
and stripping away type annotations.

Limitations
--------------

This is a simple script working based on text substitutions.
It does not handle, or even claim to handle, all valid cython syntax.

Python 3.5 and above is required.

UTF-8 input is required.

Installation
--------------

::

	$ pip install uncythonize

Usage
---------

::

	$ uncythonize.py filename.pyx

will produce a corresponding file filename.pyx.py

That file can then be run through various syntax checkers and linters,
such as pyflakes, pydocstyle, pylint, vulture, pystrict3.

It is useful to substitute in output of these tools back the original
filename, filename.pyx.py -> filename.pyx

Line numbering is preserved by this tool.

More than one file can be processed.


Contributing
--------------

Contributions are welcome! Please open pull requests.

If you adapt the script to handle your use case, please add
example scripts as test cases.

TODO
----------

* setup CI testing

Licence
---------

This code was originally developed at https://github.com/guyskk/validr
by guyskk, and is redistributed here under the GPL-3 licence.

Some modifications were made by JohannesBuchner to support testing 
the UltraNest repository.
