"""使用flask的默认http服务器`Werkzeug`运行服务.

可以设置
+ `"SERVER_CONFIG_THREADED":true`来允许多线程服务
+ `"SERVER_CONFIG_USE_RELOADER":true`来允许修改文件后重载服务
+ `"SERVER_CONFIG_PROFILE":true`来允许收集优化数据.
+ `"SERVER_CONFIG_PROFILE":"profile"`来指定存放收集到数据的路径

注意Werkzeug服务器目前不支持websocket;同时不要在生产环境使用这个服务器.它启动时的log无法被消除,设置或转化为json格式
"""
from pathlib import Path
from typing import Any
from flask import Flask
from werkzeug.contrib.profiler import ProfilerMiddleware


def run(app: Flask, *,
        host: str="0.0.0.0",
        port: int=5000,
        threaded: bool=True,
        use_reloader: bool=True,
        profile: bool= True,
        profile_dir: str="profile")->None:
    if profile == True:
        p = Path(profile_dir)
        if not p.is_dir():
            p.mkdir()
        app.wsgi_app = ProfilerMiddleware(
            app.wsgi_app,
            restrictions=[25],
            profile_dir=profile_dir
        )
    return app.run(
        host=host,
        port=port,
        debug=app.debug,
        threaded=threaded,
        use_reloader=use_reloader
    )


__all__ = ["run"]
