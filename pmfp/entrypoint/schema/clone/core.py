from pmfp.utils.endpoint import EndPoint
from ..core import schema


class Clone(EndPoint):
    """克隆json schema模式文本."""
    argparse_noflag = "url"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["url", "schema"],
        "properties": {
            "url": {
                "type": "string",
                "description": "请求的路径,可以是http/file的url或者文件系统的路径",
            },
            "out": {
                "type": "string",
                "title": "o",
                "description": "输出位置",
                "default": "."
            },
            "method": {
                "type": "string",
                "title": "m",
                "description": "访问资源的方法",
                "default": "GET",
                "enum": ["GET", "POST"]
            },
            "auth": {
                "type": "string",
                "title": "a",
                "description": "认证字符串,多字段的使用,分隔"
            },
            "auth_type": {
                "type": "string",
                "title": "t",
                "description": "认证类型",
                "enum": ["basic", "digest", "jwt", "oauth1"]
            },
            "payload": {
                "type": "string",
                "title": "d",
                "description": "请求负载"
            },
            "payload_type": {
                "type": "string",
                "title": "p",
                "description": "请求的负载类型",
                "enum": ["json", "form", "url"]
            },
            "verify": {
                "type": "boolean",
                "title": "v",
                "description": "https请求是否验证",
                "default": False
            },
            "cert": {
                "type": "string",
                "title": "e",
                "description": "指定一个本地证书用作客户端证书,如果是证书加key的形式,可以用','隔开"
            }
        }
    }


schema_clone = schema.regist_sub(Clone)
