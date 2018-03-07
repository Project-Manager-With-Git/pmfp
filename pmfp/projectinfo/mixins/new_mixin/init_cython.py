from pathlib import Path
CYTHON_NUMPY_BUILD = """from distutils.core import setup
from Cython.Build import cythonize
import numpy


setup(
    name = '{name}',
    ext_modules = cythonize("src/*.pyx", include_path = [numpy.get_include()]),
)
"""
CYTHON_BUILD = """from distutils.core import setup
from Cython.Build import cythonize


setup(
    name = '{name}',
    ext_modules = cythonize("src/*.pyx"),
)
"""


class InitCythonMixin:
    @staticmethod
    def init_cython(name, dir_path=".", math=False):
        path = Path(dir_path)
        name_path = path.joinpath(name)
        if name_path.exists():
            print('path already exist!')
            return
        name_path.mkdir()
        setup_path = name_path.joinpath("setup.py")
        src_path = name_path.joinpath("src")
        src_path.mkdir()
        with open(str(setup_path), "w") as f:
            if math:
                f.write(CYTHON_NUMPY_BUILD.format(name=name))
            else:
                f.write(CYTHON_BUILD.format(name=name))
