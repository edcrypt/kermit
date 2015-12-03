.. _Python: https://www.python.org/
.. _virtualenv: https://pypy.python.org/pypi/virtualenv
.. _virtualenvwrapper: https://pypy.python.org/pypi/virtualenvwrapper
.. _Docker: https://docker.com/
.. _Latest Release: https://github.com/prologic/kermit/releases
.. _example interpreter: https://bitbucket.org/pypy/example-interpreter

Kermit - An example interpreter
===============================

.. image:: https://travis-ci.org/prologic/kermit.svg
   :target: https://travis-ci.org/prologic/kermit
   :alt: Build Status

.. image:: https://coveralls.io/repos/prologic/kermit/badge.svg
   :target: https://coveralls.io/r/prologic/kermit
   :alt: Coverage

.. image:: https://landscape.io/github/prologic/kermit/master/landscape.png
   :target: https://landscape.io/github/prologic/kermit/master
   :alt: Quality

This is an example interpreter written using PyPy. A preferred way to walk
through it is to follow the history of commits. Interesting tags are

- parser-boilerplate    -- just cruft to make parser run
- first-parse-test      -- enough support to make the first test of parser pass
- parser-complete       -- implement enough of parser to run simple ifs and whiles
- compiler-start        -- pass the first compiler test


.. note:: This is a fork of PyPy's `example interpreter`_ Kermit.
          You may still follow the commit history as a learning
          guide, however; this fork is a divergent from PyPy's
          version of Kermit and is not compatible.


Prerequisites
-------------

It is recommended that you do all development using a Python Virtual
Environment using `virtualenv`_ and/or using the nice `virtualenvwrapper`_.

::
   
    $ mkvirtualenv kermit


Installation
------------

Grab the source from https://github.com/prologic/kermit and either
run ``python setup.py develop`` or ``pip install -e .``

::
    
    $ git clone https://github.com/prologic/kermit.git
    $ cd kermit
    $ pip install -e .

You can also download the `Latest Release`_


Building
--------

To build the interpreter simply run ``kermit/main.py`` against the RPython
Compiler. There is a ``Makefile`` that has a default target for building
and translating the interpreter.

::
    
    $ make

You can also use `Docker`_ to build the interpreter:

::
    
    $ docker build -t kermit .


Usage
-----

You can either run the interpreter using `Python`_ itself or by running the
compiled interpreter ``kermit`` in ``./bin/kermit``.

::
    
    $ ./bin/kermit examples/hello.ker

Untranslated running on top of `Python`_ (*CPython*):

::
    
    $ kermit examples/hello.ker


Grammar
-------

The grammar of kermit is currently as follows:

::
   
   main: statement* [EOF];

   statement: expr ";"
              | VARIABLE "=" expr ";"
              | "while" "(" expr ")" "{" statement* "}"
              | "if" "(" expr ")" "{" statement* "}"
              | "print" expr ";";

   expr: atom ADD_SYMBOL expr | atom;

   atom: DECIMAL | FLOAT | STRING | VARIABLE;
