from pmfp.utils.endpoint import EndPoint
from ..core import http


class Stress(EndPoint):
    """对一个http资源做压测."""
    argparse_noflag = "url"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["url"],
        "properties": {
            "url": {
                "type": "string",
                "description": "要访问的http资源的地址"
            },
            "method": {
                "type": "string",
                "title": "m",
                "description": "访问资源的方法",
                "default": "GET",
                "enum": ["GET", "POST", "DELETE", "PUT"]
            },
            "requests": {
                "type": "integer",
                "title": "n",
                "description": "请求的总次数",
                "default": 100
            },
            "concurrency": {
                "title": "b",
                "type": "integer",
                "description": "并发量",
                "default": 10
            },
            "duration": {
                "type": "integer",
                "title": "u",
                "description": "间隔时间,单位s",
                "default": 0
            },
            "data": {
                "type": "string",
                "title": "d",
                "description": "请求的负载"
            },
            "ct": {
                "type": "string",
                "title": "t",
                "description": "请求的负载类型",
                "enum": ["text/plain", "application/json"],
                "default": "text/plain"
            },
            "quiet": {
                "type": "boolean",
                "title": "q",
                "description": "安静执行",
                "default": False
            },
            "config_file": {
                "type": "string",
                "title": "f",
                "description": "配置文件"
            }
        }
    }


http_stress = http.regist_sub(Stress)
