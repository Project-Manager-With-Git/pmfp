"""flask插件形式的服务器设置组件.

目前支持的服务器有:

+ `werkzeug`
+ `gevent`
+ `gunicorn`

每个服务的参数不尽相同吗,除了host和端口则通过`HOST和`PORT`来设置外,都是通过flask app中的配置`SERVER_CONFIG_xxxx`来设置的.

## 基本的使用方法

```python
from server import FlaskRunApplication
app = Flask(__name__)
run_aplication = FlaskRunApplication(app)
```

或者使用默认的实例:
```python
from server import run_aplication

app = Flask(__name__)
run_aplication.init_app(app)
```

## 使用flask的默认http服务器`Werkzeug`运行服务.

可以设置
+ `"SERVER_CONFIG_THREADED":true`来允许多线程服务
+ `"SERVER_CONFIG_USE_RELOADER":true`来允许修改文件后重载服务
+ `"SERVER_CONFIG_PROFILE":true`来允许收集优化数据.
+ `"SERVER_CONFIG_PROFILE":"profile"`来指定存放收集到数据的路径

注意Werkzeug服务器目前不支持websocket;同时不要在生产环境使用这个服务器.它启动时的log无法被消除,设置或转化为json格式

## 使用gevent运行服务.

可以设置
+ `"SERVER_CONFIG_PROFILE":true`来允许收集优化数据.
+ `"SERVER_CONFIG_PROFILE":"profile"`来指定存放收集到数据的路径

注意gevent服务器目前不支持reload.

## 使用gunicorn运行服务.

注意,使用本项目的flask的log组件不能改变其log的format,但可以在配置文件中以`SERVER_CONFIG_`+[官方页面](http://docs.gunicorn.org/en/latest/settings.html#settings)
写出的配置项的大写来设置gunicorn的配置.从而修改log的形式.

推荐的设置有:

+ `"SERVER_CONFIG_ACCESS_LOG_FORMAT":"{\"remote_address\":\"%(h)s\",\"request_time\":\"%(t)s\",\"request\":\"%(m)s %(U)s\",\"status\":\"%(s)s\"}"`
    用于将access+log信息转为json形式.
+ `"SERVER_CONFIG_LOGLEVEL":"warning"`
    用于将服务器的系统信息log信息打印的等级提高.
+ `"SERVER_CONFIG_ERRORLOG": "gunicorn.log"`
    用于将服务器的log输出转移到文件中

需要注意如果要使用websocket,那么需要先安装`flask_sockets`,然后设置`"SERVER_CONFIG_WORKER_CLASS":"flask_sockets.worker"`
"""
from .extension import FlaskRunApplication

run_aplication = FlaskRunApplication()
