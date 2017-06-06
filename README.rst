
pmfp
===============================

version: 0.2.4

author: hsz

email: hsz1273327@gmail.com

Feature
----------------------

* python's package manager support venv and conda

* code template with test, document, requirements and virtual environment for
different situation such as script, model, GUI, web.

* easy to build a python application or model

* easy to test a python application or model, include static type check

* project status manager

* run script with virtual env  in project's root

* upload project to git repository

* upload model to pypi

* docker support


Example
-------------------------------

.. code:: shell
    ppm init
    ppm install
    ppm build
    ppm doc
    ppm test
    ppm clean
    ppm status
    ppm update
    ppm rename
    ppm upload
    ppm run
    ppm docker





Install
--------------------------------

- ``python -m pip install pmfp``


Documentation
--------------------------------

`Documentation on Readthedocs <https://github.com/Python-Tools/pmfp>`_.



TODO
-----------------------------------
* more tests



Limitations
-----------
* only support python3.5+
