import asyncio


class SanicHook:
    def __init__(self, app=None):
        self.HOOK_FUNCS = {}
        if app:
            self.init_app(app)

    def register(self, hook_type: str):
        if self.HOOK_FUNCS.get(hook_type) is None:
            self.HOOK_FUNCS[hook_type] = []

        def wrap(cfunc):
            if not asyncio.iscoroutinefunction(cfunc):
                raise AttributeError("类型错误")
            self.HOOK_FUNCS[hook_type].append(cfunc)
            return cfunc
        return wrap

    def init_app(self, app):
        if not self.HOOK_FUNCS:
            raise AttributeError("no hooks registed")
        for k, cfuncs in self.HOOK_FUNCS.items():
            if k == 'request':
                for cfunc in cfuncs:
                    app.middleware('request')(cfunc)
            elif k == 'response':
                for cfunc in cfuncs:
                    app.middleware('response')(cfunc)

            elif k == 'before_server_start':
                for cfunc in cfuncs:
                    app.listener('before_server_start')(cfunc)

            elif k == 'after_server_start':
                for cfunc in cfuncs:
                    app.listener('after_server_start')(cfunc)

            elif k == 'before_server_stop':
                for cfunc in cfuncs:
                    app.listener('before_server_stop')(cfunc)

            elif k == 'after_server_stop':
                for cfunc in cfuncs:
                    app.listener('after_server_stop')(cfunc)
            else:
                print("unknown hook type")


hooks = SanicHook()

__all__ = ["SanicHook", "hooks"]
