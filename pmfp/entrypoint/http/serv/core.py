from schema_entry import EntryPoint

from ..core import http


class Serv(EntryPoint):
    """以指定位置作为http服务的根目录启动一个静态http服务器."""
    argparse_noflag = "port"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["port"],
        "properties": {
            "bind": {
                "type": "string",
                "description": "绑定的网址",
                "default": "localhost"
            },
            "port": {
                "type": "integer",
                "description": "端口号"
            },
            "root": {
                "type": "string",
                "description": "http服务的根目录",
                "default": "."
            }
        }
    }


http_serv = http.regist_sub(Serv)
