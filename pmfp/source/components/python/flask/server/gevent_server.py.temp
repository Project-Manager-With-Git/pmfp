"""使用gevent运行服务.

可以设置
+ `"SERVER_CONFIG_PROFILE":true`来允许收集优化数据.
+ `"SERVER_CONFIG_PROFILE":"profile"`来指定存放收集到数据的路径

注意gevent服务器目前不支持reload.
"""
import logging
from typing import Any
from pathlib import Path
from flask import Flask
from werkzeug.debug import DebuggedApplication
from werkzeug.contrib.profiler import ProfilerMiddleware
from flask_sockets import SocketMiddleware

serverlogger = logging.getLogger('werkzeug')


def log_request(self):
    self.server.log.write(self.format_request())


def format_request(self):
    length = self.response_length or '-'
    if self.time_finish:
        delta = '%.6f' % (self.time_finish - self.time_start)
    else:
        delta = '-'
    client_address = self.client_address[0] if isinstance(self.client_address, tuple) else self.client_address
    return 'client:%s, query:%s, status:%s, length:%s, used:%ss' % (
        client_address or '-',
        self.requestline or '',
        # Use the native string version of the status, saved so we don't have to
        # decode. But fallback to the encoded 'status' in case of subclasses
        # (Is that really necessary? At least there's no overhead.)
        (self._orig_status or self.status or '000').split()[0],
        length,
        delta)


def run(app: Flask,
        host: str="0.0.0.0",
        port: int=5000,
        profile: bool=False,
        profile_dir: str="profile")->None:
    from gevent import pywsgi
    from gevent import monkey
    from geventwebsocket.handler import WebSocketHandler
    monkey.patch_all()
    pywsgi.WSGIHandler.log_request = log_request
    pywsgi.WSGIHandler.format_request = format_request
    if isinstance(app.wsgi_app, SocketMiddleware):
        server = pywsgi.WSGIServer(
            (host, port),
            app,
            handler_class=WebSocketHandler,
            log=serverlogger
        )
    else:
        server = pywsgi.WSGIServer(
            (host, port),
            app,
            log=serverlogger
        )
    if app.debug is True:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
    if profile is True:
        p = Path(profile_dir)
        if not p.is_dir():
            p.mkdir()
        app.wsgi_app = ProfilerMiddleware(
            app.wsgi_app,
            restrictions=[25],
            profile_dir=profile_dir
        )
    return server.serve_forever()


__all__ = ["run"]
