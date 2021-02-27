from setuptools import setup

from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext

extension = Extension(
           "helloworld",
           sources=["helloworld.pyx"],
           #include_dirs=[numpy.get_include()], # 如果用到numpy
           language="c++"
)
setup(

)