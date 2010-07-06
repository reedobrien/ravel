ZPUGDC deform demo website
==========================

Definition
----------

:strong:`rav·el`: [rav-*uhl*]

verb. rav·eled also rav·elled, rav·el·ing also rav·el·ling, rav·els also rav·els

verb tr.
 1. To separate the fibers or threads of (cloth, for example); unravel.
 2. To clarify by separating the aspects of.
 3. To tangle or complicate.
verb intr.
 1. To become separated into its component threads; unravel or fray.
 2. To become tangled or confused.
noun
 1. A raveling.
 2. A broken or discarded thread.
 3. A tangle.


No, Really What is it?
----------------------

An app demonstrating the use of `deform <http://docs.repoze.org/deform>`_ with `repoze.bfg <http://docs.repoze.org/bfg>`_ and `MongoDB <http://www.mongodb.org>`_. It may or may not be of any use beyond that of demonstration.


Installation
------------

At the time if this writing I am running on development eggs for `colander <http://svn.repoze.org/colander/>`_, `deform src <http://svn.repoze.org/deform/>`_, `perppercorn <http://svn.repoze.org/peppercorn/>`_, `pymongo <http://github.com/mongodb/mongo-python-driver/>`_ and `lumin <http://github.com/koansys/lumin.git>`_ and of course this package `ravel <http://github.com/reedobrien/ravel.git>`_. You can get whatever you are comfortabel with. (I think all of the relased packages should work at the time of this writing).

Installation should theoretically be as simple as getting the `source <http://github.com/reedobrien/ravel>`_ and perfroming setup.py [install|develop] on it.

I will elicit the steps performed by me:

1. Setup a `virtualenv <http://pypi.python.org/pypi/virtualenv>`_ and activate it (activation azzumes you are using bash or a bash compatible shell)

  ``$ /usr/local/python/2.7.0/bin/virtualenv /usr/local/dev/zpug_demo_env --no-site-packages --distribute``
  ``$ . /usr/local/dev/zpug_demo_env/bin/activate``

2. Make development eggs for the src you have checked out

  ``$ for dir in peppercorn colander deform mongo-python-driver repoze.bfg lumin ravel; do cd ../$dir && /usr/local/dev/zpug_demo_env/bin/python setup.py develop; done``

3. See if it runs

  ``$ paster serve ravel.ini``


You call this documentation?
----------------------------

No. There may or may not ever be more documentation in docs/index.rst.
