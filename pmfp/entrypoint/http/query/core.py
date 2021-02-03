from pmfp.utils.endpoint import EndPoint
from ..core import http


class Query(EndPoint):
    """使用http请求获取资源."""
    argparse_noflag = "url"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["url", "method"],
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
            "payload": {
                "type": "string",
                "title": "d",
                "description": "请求负载"
            },
            "auth": {
                "type": "string",
                "title": "a",
                "description": "用户身份验证字符串"
            },
            "auth_type": {
                "type": "string",
                "title": "t",
                "description": "用户身份的验证类型",
                "enum": ["basic", "digest", "jwt", "oauth1"]
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
                "description": "https请求的客户端认证文件位置"
            }
        }
    }


http_query = http.regist_sub(Query)
