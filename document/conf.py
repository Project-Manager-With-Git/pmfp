# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify
project = 'pmfp'
copyright = '2022, hsz'
author = 'hsz'

# The short X.Y version
version = '4.1.9'

# The full version, including alpha/beta/rc tags
release= '4.1.9'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'zh_CN'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
# 不进行编译的文件/文件夹
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# 设置不同后缀的文件使用不同解析器(这个需要后加)
source_suffix = {
    '.rst': 'restructuredtext'
}
# 主题
extensions.append('sphinx_rtd_theme')
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    'logo_only': True,
    'navigation_depth': 5,
}

# 使用插件支持markdowm
extensions.append('recommonmark')
# 针对`.md`为后缀的文件做markdown渲染
source_suffix[".md"] = 'markdown'

# 设置markdown渲染器的自定义项


def setup(app):
    github_doc_root = 'https://localhost:5000'
    app.add_config_value('recommonmark_config', {
        # 'url_resolver': lambda url: github_doc_root + url,
        "enable_auto_toc_tree": True,
        "auto_toc_tree_section": "目录",
        'auto_toc_maxdepth': 2,
        "enable_math": True,
        'enable_eval_rst': True
    }, True)

    app.add_transform(AutoStructify)


# autoapi-python
extensions.append('autoapi.extension')
extensions.append("sphinx.ext.napoleon")
autoapi_type = 'python'
autoapi_dirs = ["/Users/mac/WORKSPACE/GITHUB/ProjectManagerWithGit/pmfp/pmfp"]
