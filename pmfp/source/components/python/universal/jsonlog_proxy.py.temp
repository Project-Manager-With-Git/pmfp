import sys
import logging
import structlog

class LogProxy:
    __slots__ = ('app_name', 'log_level', 'log', "_callbacks")

    def __init__(self, app_name=None, log_level=None):
        self._callbacks = []
        self.app_name = app_name
        self.log_level = log_level
        self.log = None
        if app_name and log_level:
            self.initialize(app_name, log_level)

    def initialize(self, app_name, log_level):
        """初始化log对象.
        Args:
            url ([type]): [description]
        """
        self.app_name = app_name
        self.log_level = log_level

        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,  # 判断是否接受某个level的log消息
                structlog.stdlib.add_logger_name,  # 增加字段logger
                structlog.stdlib.add_log_level,  # 增加字段level
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(
                    fmt="iso"),  # 增加字段timestamp且使用iso格式输出
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,  # 捕获异常的栈信息
                structlog.processors.StackInfoRenderer(),  # 详细栈信息
                structlog.processors.JSONRenderer()  # json格式输出,第一个参数会被放入event字段
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        handler = logging.StreamHandler(sys.stdout)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(self.log_level)  # 设置最低log等级

        self.log = structlog.get_logger(self.app_name)

        for callback in self._callbacks:
            callback(self.log)

    def attach_callback(self, callback):
        self._callbacks.append(callback)

    def __getattr__(self, attr):
        if self.log is None:
            raise AttributeError('Cannot use uninitialized Proxy.')
        return getattr(self.log, attr)

    def __setattr__(self, attr, value):
        if attr not in self.__slots__:
            raise AttributeError('Cannot set attribute on proxy.')
        return super().__setattr__(attr, value)


log = LogProxy()