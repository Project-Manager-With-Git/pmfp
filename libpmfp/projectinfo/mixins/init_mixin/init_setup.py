from pathlib import Path
from string import Template

MANIFEST = Template("""
include LICENSE
include README.rst
recursive-include requirements *.txt
recursive-include $project_name *.pyx *.pxd *.pxi *.py *.c *.h
""")

PY_SETUP = Template("""from codecs import open
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
KEYWORDS = $keywords
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
    data_files=[('requirements', ['requirements/requirements.txt',
        'requirements/requirements_dev.txt',
        'requirements/requirements_test.txt'])]
)
""")

CYTHON_SETUP = Template("""from codecs import open
from setuptools import setup, find_packages
from os import path
from Cython.Build import cythonize
from Cython.Compiler import Options

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
KEYWORDS = $keywords
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

extensions = [
    Extension("$project_name.lib$project_name",
          sources = ["$project_name/lib$project_name.pyx"],
          $numpy_include
          language = "c++")
]
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
    ext_modules=cythonize(extensions),
    $entry_points
    zip_safe=ZIP_SAFE,
    data_files=[('requirements', ['requirements/requirements.txt', 'requirements/requirements_dev.txt', 'requirements/requirements_test.txt'])]
)
""")


class InitSetupMixin:
    def _init_manifest(self):
        """初始化setup.py上传用的manifest文件"""
        print('create MANIFEST.in')
        with open("MANIFEST.in", "w") as f:
            f.write(MANIFEST.substitute(
                project_name=self.meta.project_name))
        print('create MANIFEST.in done!')
        return 1

    def _init_cython_setuppy(self):
        """初始化cython的setup.py
        """
        path = Path("setup.py")
        if path.exists():
            print("already have setup.py")
            return False
        if self.form.project_type == "command":
            entry_points_T = Template(
                "entry_points={'console_scripts': ['$project_name = lib$project_name.main:main']},")
            entry_points = entry_points_T.substitute(project_name=project_name)
        else:
            entry_points = ""
        if self.form.template == "math":
            numpy_include = "include_dirs=[numpy.get_include()],"
        else:
            numpy_include = ""

        setup = CYTHON_SETUP.substitute(
            project_name=self.meta.project_name,
            author=self.author.author,
            author_email=self.author.author_email,
            license_=self.meta.license_,
            keywords="(" + ",".join(
                ['"' + i + '"' for i in self.desc.keywords]) + ",)",
            version=self.meta.version,
            description=self.desc.description,
            url=self.meta.url,
            numpy_include=numpy_include,
            entry_points=entry_points
        )

        with open(str(path), "w") as f:
            f.write(setup)
        print("writing setup.py for cython done!")
        return True

    def _init_python_setuppy(self):
        """初始化python的setup.py
        """
        path = Path("setup.py")
        if path.exists():
            print("already have setup.py")
            return False
        if self.form.project_type == "command":
            entry_points_T = Template(
                "entry_points={'console_scripts': ['$project_name = lib$project_name.main:main']},")
            entry_points = entry_points_T.substitute(project_name=project_name)
        else:
            entry_points = ""

        setup = PY_SETUP.substitute(
            project_name=self.meta.project_name,
            author=self.author.author,
            author_email=self.author.author_email,
            license_=self.meta.license_,
            keywords="(" + ",".join(
                ['"' + i + '"' for i in self.desc.keywords]) + ",)",
            version=self.meta.version,
            description=self.desc.description,
            url=self.meta.url,
            entry_points=entry_points
        )

        with open(str(path), "w") as f:
            f.write(setup)
        print("writing setup.py for python done!")
        return True

    def _init_setuppy(self):
        """初始化python/cython的setup.py"""
        if self.form.compiler == "python":
            self._init_manifest()
            self._init_python_setuppy()
            return True
        elif self.form.compiler == "cython":
            self._init_manifest()
            self._init_cython_setuppy()
            return True
        else:
            print(self.form.compiler, "not need a setup.py file !")
            return False


__all__ = ["InitSetupMixin"]
