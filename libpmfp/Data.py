from string import Template

Dockerfile = Template("""
FROM python:$v1:$v2
ADD requirements/requirements.txt /code/requirements.txt
ADD $project_name.$suffix /code/$project_name.$suffix
WORKDIR /code
RUN pip install -r requirements.txt
""")


MANIFEST = Template("""
include LICENSE
include README.rst
recursive-include $project_name *.py
""")


SCRIPT = """
def main():
    pass

if __name__=="__main__":
    main()
"""

PACKAGEJSON = Template("""
{
  "name": "$project_name",
  "version": "$version",
  "description": "$description",
  "main": "index.js",
  "scripts": {
    "test": "echo \\\"Error: no test specified\\\" && exit 1"
  },
  "author": "$author",
  "license": "$license_"
}
""")

READMERST = Template("""
$project_name
===============================

version: $version

author: $author

email: $author_email

Feature
----------------------
* Feature1
* Feature2

Example
-------------------------------

.. code:: python





Install
--------------------------------

- ``python -m pip install $project_name``


Documentation
--------------------------------

`Documentation on Readthedocs <$url>`_.



TODO
-----------------------------------
* todo



Limitations
-----------
* limit


""")

SETUPPY = Template("""from codecs import open
from setuptools import setup, find_packages
from os import path

REQUIREMETS_DEV_FILE = 'requirements_dev.txt'
REQUIREMETS_TEST_FILE = 'requirements_test.txt'
REQUIREMETS_FILE = 'requirements.txt'
PROJECTNAME = '$project_name'
VERSION = '$version'
DESCRIPTION = '$description'
URL = '$url'
AUTHOR = '$author'
AUTHOR_EMAIL = '$author_email'
LICENSE = '$license_'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: $license_ License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Documentation :: Sphinx',
]
KEYWORDS = [$keywords]
PACKAGES = find_packages(exclude=['contrib', 'docs', 'test'])
ZIP_SAFE = False

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()
REQUIREMETS_DIR = path.join(HERE,"requirements")

with open(path.join(REQUIREMETS_DIR, REQUIREMETS_FILE), encoding='utf-8') as f:
    REQUIREMETS = f.readlines()

with open(path.join(REQUIREMETS_DIR, REQUIREMETS_DEV_FILE), encoding='utf-8') as f:
    REQUIREMETS_DEV = f.readlines()

with open(path.join(REQUIREMETS_DIR, REQUIREMETS_TEST_FILE), encoding='utf-8') as f:
    REQUIREMETS_TEST = f.readlines()
setup(
    name=PROJECTNAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=PACKAGES,
    include_package_data=True,
    install_requires=REQUIREMETS,
    extras_require={
        'dev': REQUIREMETS_DEV,
        'test': REQUIREMETS_TEST
    },
    $entry_points
    zip_safe=ZIP_SAFE,
    data_files=[('requirements', ['requirements/requirements.txt', 'requirements/requirements_dev.txt', 'requirements/requirements_test.txt'])]
)
""")


COMMAND_MAIN = """
#!/usr/bin/env python3
import sys

if __name__ == '__main__':
    from {project_name}.main import main
    sys.exit(main(sys.argv[1:]))

"""

CONF = Template("""
import os
import sys
from pathlib import Path
import recommonmark
from recommonmark.transform import AutoStructify
from recommonmark.parser import CommonMarkParser
p = Path(__file__).absolute()
$ky0

extensions = [$ky1,
              'sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'sphinx.ext.napoleon',
              'sphinx.ext.mathjax']

templates_path = ['_templates']

source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}
source_suffix = ['.rst', '.md']

master_doc = 'index'

project = '$project_name'
copyright = '2017, $author'
author = '$author'

version = '$version'

release = ''

language = 'en'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

todo_include_todos = True

html_theme = 'alabaster'

html_static_path = ['_static']

htmlhelp_basename = 'score_card_modeldoc'

latex_elements = {

}

latex_documents = [
    (master_doc, 'score_card_model.tex', 'score\\_card\\_model Documentation',
     'Author', 'manual'),
]

man_pages = [
    (master_doc, 'score_card_model', 'score_card_model Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'score_card_model', 'score_card_model Documentation',
     author, 'score_card_model', 'One line description of project.',
     'Miscellaneous'),
]

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

epub_exclude_files = ['search.html']

todo_include_todos = True

def setup(app):
    app.add_config_value('recommonmark_config', {
        'url_resolver': lambda url: url_doc_root + url,
        'auto_toc_tree_section':'Contents',
         'enable_math':True,
        'enable_inline_math':True
    }, True)
    app.add_transform(AutoStructify)
""")
