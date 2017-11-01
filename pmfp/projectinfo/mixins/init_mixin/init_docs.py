import subprocess
from pathlib import Path
from string import Template

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
url_doc_root = "xxxx"#
def setup(app):
    app.add_config_value('recommonmark_config', {
        'url_resolver': lambda url: url_doc_root + url,
        'auto_toc_tree_section':'Contents',
         'enable_math':True,
        'enable_inline_math':True
    }, True)
    app.add_transform(AutoStructify)
""")


class InitDocsMixin:
    def _init_docs(self):
        """初始化sphinx文档
        
        """
        KY = {
            "python": ("sys.path.insert(0, str(p.parent.parent))",
                       "'sphinx.ext.autodoc'"),
            "cython": ("sys.path.insert(0, str(p.parent.parent))",
                       "'sphinx.ext.autodoc'")
        }

        print('building document')
        path = Path("document")
        if path.exists():
            print("document exists")
            return False
        else:
            if self.with_docs:
                if self.form.compiler in ["python", "cython"]:
                    package_name = self.meta.project_name
                    if Path(package_name).exists():
                        command = ["sphinx-apidoc", "-F", "-H", self.meta.project_name, '-A', self.author.author,
                                   '-V', self.meta.version, "-a", '-o', 'document', package_name]
                    else:
                        command = ["sphinx-apidoc", "-F", "-H", self.meta.project_name, '-A', self.author.author,
                                   '-V', self.meta.version, "-a", '-o', 'document', '.']
                else:
                    package_name = self.meta.project_name
                    command = ["sphinx-apidoc", "-F", "-H", self.meta.project_name, '-A', self.author.author,
                               '-V', self.meta.version, '-o', 'document', '.']

            subprocess.check_call(command)
            with open("document/conf.py", "w") as f:
                f.write(CONF.substitute(
                    project_name=self.meta.project_name,
                    author=self.author.author,
                    version=self.meta.version,
                    ky0=KY.get(
                        self.form.compiler, ("", ""))[0],
                    ky1=KY.get(
                        self.form.compiler, ("", ""))[1]
                ))
        print('building apidoc done')
        return True


__all__ = ["InitDocsMixin"]
