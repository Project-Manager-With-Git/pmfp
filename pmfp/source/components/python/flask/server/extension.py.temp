"""插件形式的服务器组件."""
import time
import logging
import traceback
from flask import Flask
from flask_sockets import SocketMiddleware
from .werkzeug_server import run as werkzeug_runner

from .gevent_server import run as gevent_runner
from .gunicorn_server import run as gunicorn_runner


SERVERS = {
    "werkzeug": werkzeug_runner,
    "gevent": gevent_runner,
    "gunicorn": gunicorn_runner
}


def _run_application(app: Flask, host: str="0.0.0.0", port: int= 5000, server: str="werkzeug", **kwargs):
    """执行flask项目服务的入口.

    Args:
        app ([Flask]): flask项目
        port (int): 服务启动的端口
        host (str, optional): Defaults to "0.0.0.0". 服务启动的host
        server (str, optional): Defaults to "werkzeug". 指定的服务器类型

    Raises:
        AttributeError: 当服务器类型不可用或者特定条件不支持时抛出
    """
    server_range = list(SERVERS.keys())
    if server not in server_range:
        raise AttributeError(f"未知的服务器类型,支持{server_range}")
    if isinstance(app.wsgi_app, SocketMiddleware) and server == "werkzeug":
        raise AttributeError("websocket的服务器类型不能是werkzeug,可以设置SERVER_CONFIG_SERVER来指定不同的服务器")
    return SERVERS.get(server)(app=app, host=host, port=port, **kwargs)


class FlaskRunApplication:
    """配置服务器的插件.
    可以通过配置`SERVER_CONFIG_xxxx`来设置参数.但host和端口则通过`HOST和`PORT`来设置."""

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app.run_application = self.run_application
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['run_application'] = self

    def run_application(self, **kwargs):
        """执行flask项目服务的入口.

        优先使用app中的config项,然后才是代码中的参数.
        """
        serverlogger = logging.getLogger('werkzeug')
        server_config = dict(kwargs)
        server_config.update(self.app.config.get_namespace('SERVER_CONFIG_'))
        try:
            host = self.app.config["HOST"]
        except:
            pass
        else:
            server_config.update({"host": host})
        try:
            port = self.app.config["PORT"]
        except:
            pass
        else:
            server_config.update({"port": port})
        try:
            serverlogger.info(f'{server_config["server"]} start @ {server_config["host"]}:{server_config["port"]}')
            _run_application(
                app=self.app,
                **server_config
            )
        except KeyboardInterrupt as ki:
            formatted_lines = "/n".join(traceback.format_exc().splitlines())
            serverlogger.info(f'"msg":"server stoped by Ctrl+C","traceback":"{formatted_lines}"')
        except Exception as e:
            formatted_lines = "/n".join(traceback.format_exc().splitlines())
            serverlogger.info(f'"msg":"server stoped by error","error":"{type(e)}","error_msg":"{str(e)}","traceback":"{formatted_lines}"')


__all__ = ["FlaskRunApplication"]
