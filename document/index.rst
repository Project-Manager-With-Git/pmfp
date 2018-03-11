.. pmfp documentation master file, created by
   sphinx-quickstart on Mon Oct  9 15:03:44 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pmfp's documentation!
================================

* version: 2.0.3
* status: dev
* author: hsz
* email: hsz1273327@gmail.com

Desc
--------------------------------

a simple scaffold for pythoner


keywords:scaffold,tool,python,js


Feature
----------------------
* python's scaffold for model, command-line tool, flask, sanic, tk
* javascript's scaffold for vue.js, simple frontend/node.js project

Example
-------------------------------

.. code:: shell

    usage: ppm <command> [<args>]

    The most commonly used ppm commands are:
    init        initialise a project
    clean       clean a project
    install     install a package
    status      see the project's info
    update      update the project's version and status
    upload      upload your project to a git repository, a docker repository,
                a pypi server
    search      search for a package
    run         run scripts for python and node
    build       build your python project to a pyz file, wheel,egg,docker image,
                build your cpp project to a lib or a executable file
    test        test your project
    doc         build your project's document
    new         new a document,setup.py,test,dockerfile for a project

    shortcut:
    flask       init flask
    sanic       init sanic
    vue         init vue
    celery      init celery



Install
--------------------------------

- ``python -m pip install pmfp``



BUG
--------------------------------

1. if you can not init your project,you should try to create the env by yourself first

`python3 -m venv env`

then run the `ppm init` 

2. ppm test now can run correctly.

3. init cython commandline now can run correctly. 1.0.9
Change
------------------------------

* a better celery template with test

TODO
-----------------------------------

* C/C++ support
* more js template
* template for tensorflow
* template for cuda,opencv,opencl
* template for gitbook

API:
---------------------------

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
