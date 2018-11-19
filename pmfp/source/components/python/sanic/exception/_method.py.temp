import asyncio
from sanic.exceptions import SanicException


class SanicExcept:
    def __init__(self, app=None):
        self.EXC_FUNCS = {}
        if app:
            self.init_app(app)

    def register(self, exc_type: SanicException):
        if not issubclass(exc_type, SanicException):
            raise AttributeError("注册的错误类型必须是SanicException的子类")
        def wrap(cfunc):
            if not asyncio.iscoroutinefunction(cfunc):
                raise AttributeError("类型错误")
            self.EXC_FUNCS[exc_type] = (cfunc)
            return cfunc
        return wrap

    def init_app(self, app):
        if not self.EXC_FUNCS:
            raise AttributeError("no exception registed")
        for k, cfunc in self.EXC_FUNCS.items():
            app.exception(k)(cfunc)


excep = SanicExcept()

__all__ = ["SanicExcept", "excep"]
