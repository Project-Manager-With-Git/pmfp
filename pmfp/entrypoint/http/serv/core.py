from pmfp.utils.endpoint import EndPoint
from ..core import http


class Serv(EndPoint):
    """以指定位置作为http服务的根目录启动一个静态http服务器."""
    argparse_noflag = "port"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["port"],
        "properties": {
            "bind": {
                "type": "string",
                "title": "b",
                "description": "绑定的网址",
                "default": "localhost"
            },
            "port": {
                "type": "integer",
                "title": "p",
                "description": "端口号"
            },
            "root": {
                "type": "string",
                "title": "r",
                "description": "http服务的根目录",
                "default": "."
            }
        }
    }


http_serv = http.regist_sub(Serv)
