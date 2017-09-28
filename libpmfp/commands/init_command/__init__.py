from .core import InitCore
from .mixins.init_python_mixin import InitPythonMixin
from .mixins.init_cython_mixin import InitCythonMixin
from .mixins.init_cpp_mixin import InitCppMixin
from .mixins.init_node_mixin import InitNodeMixin


class Init(InitCore, InitPythonMixin, InitCythonMixin, InitCppMixin, InitNodeMixin):
    pass
