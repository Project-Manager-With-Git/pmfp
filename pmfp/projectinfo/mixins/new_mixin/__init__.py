"""项目初始化使用的mixin汇总."""
import traceback
from .init_cython import InitCythonMixin
from .init_docker import InitDockerMixin
from .init_docs import InitDocsMixin
from .init_main import InitMainMixin
from .init_setup import InitSetupMixin


class NewMixin(InitCythonMixin, InitDockerMixin, InitDocsMixin, InitMainMixin, InitSetupMixin):
    """创建一些非关键组件的混入.

    包括创建dockerfile,创建入口文件,创建setup.py文件,创建sphinx的文档项目.
    """

    pass


__all__ = ["NewMixin"]
