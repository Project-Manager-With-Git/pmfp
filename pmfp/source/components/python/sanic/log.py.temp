"""
+ `SET_LOG_MAIL_LOG:bool`,可以设置app的logger是否要支持发送错误信息到邮箱,相关的其他参数还有:
    + `SET_LOG_MAILHOST:str` 默认为None,设置发送邮箱的地址
    + `SET_LOG_MAILPORT:int` 默认为25,设置发送邮箱的端口
    + `SET_LOG_MAILSSL:bool` 默认为False,设置发送邮箱是否使用ssl加密发送(25端口一般不加密,465端口一般加密)
    + `SET_LOG_MAILUSERNAME:str` 默认为None,设置发送邮箱的用户名
    + `SET_LOG_MAILPASSWORD:str` 默认为None,设置发送邮箱的密码
    + `SET_LOG_MAILFROMADDR:str` 默认为None,设置发送邮箱的地址
    + `SET_LOG_MAILTOADDRS:List[str]` 默认为None,设置要发送去的目标,注意是字符串列表
    + `SET_LOG_MAILSUBJECT:str` 默认为`Application Error`,设置发送去邮件的主题
"""
import time
import sys
import logging
from logging.handlers import (
    SMTPHandler
)
from sanic.log import logger
logging.Formatter.converter = time.gmtime


LOGGING_CONFIG_JSON = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console"]},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access",
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout,
        },
    },
    formatters={
        "generic": {
            "format": '''{"time":"%(asctime)s","process":"%(process)d", "level":"%(levelname)s","msg":"%(message)s"}''',
            "datefmt": "%Y-%m-%dT%H:%M:%S Z",
            "class": "logging.Formatter",
        },
        "access": {
            "format": '''{"time":"%(asctime)s","name":"%(name)s", "level":"%(levelname)s","host":"%(host)s","status":"%(status)d","byte":"%(byte)d","request":"%(request)s",%(message)s}''',
            "datefmt": "%Y-%m-%dT%H:%M:%S Z",
            "class": "logging.Formatter",
        },
    },
)
def emit(self, record):
    try:
        import smtplib
        from email.message import EmailMessage
        import email.utils

        port = self.mailport
        if not port:
            port = smtplib.SMTP_PORT
        smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=self.timeout)
        msg = EmailMessage()
        msg['From'] = self.fromaddr
        msg['To'] = ','.join(self.toaddrs)
        msg['Subject'] = self.getSubject(record)
        msg['Date'] = email.utils.localtime()
        msg.set_content(self.format(record))
        if self.username:
            if self.secure is not None:
                smtp.ehlo()
                smtp.starttls(*self.secure)
                smtp.ehlo()
            smtp.login(self.username, self.password)
        smtp.send_message(msg)
        smtp.quit()
    except Exception:
        self.handleError(record)

def set_mail_log(app):
    SET_LOG_MAILHOST = app.config.get("SET_LOG_MAILHOST")
    SET_LOG_MAILPORT= app.config.get("SET_LOG_MAILPORT")
    SET_LOG_MAILSSL= app.config.get("SET_LOG_MAILSSL")
    SET_LOG_MAILUSERNAME= app.config.get("SET_LOG_MAILUSERNAME")
    SET_LOG_MAILPASSWORD= app.config.get("SET_LOG_MAILPASSWORD")
    SET_LOG_MAILFROMADDR= app.config.get("SET_LOG_MAILFROMADDR")
    SET_LOG_MAILTOADDRS= app.config.get("SET_LOG_MAILTOADDRS")
    SET_LOG_MAILSUBJECT= app.config.get("SET_LOG_MAILSUBJECT")
    if not SET_LOG_MAILHOST:
        raise AttributeError("必须指定邮件主机")
    if not SET_LOG_MAILFROMADDR:
        raise AttributeError("必须指定邮件发出邮箱")

    if not SET_LOG_MAILTOADDRS:
        raise AttributeError("必须指定邮件接收邮箱")
    if not SET_LOG_MAILSUBJECT:
        raise AttributeError("必须指定邮件主题")

    if SET_LOG_MAILPORT:
        SET_LOG_MAILHOST = (SET_LOG_MAILHOST,SET_LOG_MAILPORT)
    if SET_LOG_MAILSSL:
        SMTPHandler.emit = emit
    if SET_LOG_MAILUSERNAME:
        if SET_LOG_MAILPASSWORD:
            credentials = (SET_LOG_MAILUSERNAME, SET_LOG_MAILPASSWORD)
        else:
            credentials = (SET_LOG_MAILUSERNAME,)
        mail_handler = SMTPHandler(
            mailhost=SET_LOG_MAILHOST,
            fromaddr=SET_LOG_MAILFROMADDR,
            toaddrs=SET_LOG_MAILTOADDRS,
            credentials=credentials,
            subject=SET_LOG_MAILSUBJECT
        )
    else:
        mail_handler = SMTPHandler(
            mailhost=SET_LOG_MAILHOST,
            fromaddr=SET_LOG_MAILFROMADDR,
            toaddrs=SET_LOG_MAILTOADDRS,
            subject=SET_LOG_MAILSUBJECT
        )
    mail_handler.setLevel("ERROR")
    if not app.debug:
        logger.addHandler(mail_handler)
