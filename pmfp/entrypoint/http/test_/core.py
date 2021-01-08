from schema_entry import EntryPoint

from ..core import http


class Test(EntryPoint):
    """检查http请求返回的数据是否满足json schema定义的模式."""
    argparse_noflag = "url"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["url", "schema", "serialization"],
        "properties": {
            "schema": {
                "type": "string",
                "description": "用于验证的json schema,可以是路径也可以是url"
            },
            "url": {
                "type": "string",
                "description": "要访问的http资源的地址"
            },
            "method": {
                "type": "string",
                "description": "访问资源的方法",
                "default": "GET",
                "enum": ["GET", "POST", "DELETE", "PUT"]
            },
            "serialization": {
                "type": "string",
                "description": "请求的返回值序列化协议.默认json",
                "default": "json",
                "enum": ["json", "yaml"]
            },
            "auth": {
                "type": "string",
                "description": "认证字符串,多字段的使用,分隔"
            },
            "auth_type": {
                "type": "string",
                "description": "认证类型",
                "enum": ["basic", "digest", "jwt", "oauth1"]
            },
            "payload": {
                "type": "string",
                "description": "请求负载"
            },
            "payload_type": {
                "type": "string",
                "description": "请求的负载类型",
                "enum": ["json", "form", "url", "stream"]
            },
            "stream": {
                "type": "boolean",
                "description": "返回是否为流数据",
                "default": False
            },
            "verify": {
                "type": "boolean",
                "description": "https请求是否验证",
                "default": False
            },
            "cert": {
                "type": "string",
                "description": "https请求的客户端认证文件位置"
            }
        }
    }


http_test = http.regist_sub(Test)
