from pmfp.utils.endpoint import EndPoint
from ..core import schema


class Check(EndPoint):
    """检查请求结果是否符合指定的json schema模式.
    这个schema文件可以是文件地址或者http/fiil的url
    """
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
            "schema": {
                "type": "string",
                "title": "s",
                "description": "用于验证的json schema,可以是路径也可以是url",
            },
            "method": {
                "type": "string",
                "title": "m",
                "description": "访问资源的方法",
                "default": "GET",
                "enum": ["GET", "POST", "DELETE", "PUT"]
            },
            "serialization": {
                "type": "string",
                "title": "z",
                "description": "请求的返回值序列化协议.默认json",
                "default": "json",
                "enum": ["json", "yaml"]
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
                "enum": ["json", "form", "url", "stream"]
            },
            "stream": {
                "type": "boolean",
                "title": "r",
                "description": "返回是否为流数据",
                "default": False
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


schema_check = schema.regist_sub(Check)
