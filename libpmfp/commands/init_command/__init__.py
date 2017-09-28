from .core import InitCore
from .mixins.init_python_mixin import InitPythonMixin


class Init(InitCore, InitPythonMixin):
    pass
