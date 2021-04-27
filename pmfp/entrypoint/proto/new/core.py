from pmfp.utils.endpoint import EndPoint
from ..core import proto


class New(EndPoint):
    """创建protobuf文件."""
    argparse_noflag = "name"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "proto文件名,也是package名"
            },
            "pb_include": {
                "type": "string",
                "title": "t",
                "description": "protobuffer文件存放的路径",
                "default": "pbschema"
            },
            "parent_package": {
                "type": "string",
                "title": "p",
                "description": "package父package"
            },
            "cwd": {
                "type": "string",
                "description": "",
                "default": "."
            }
        }
    }


proto_new = proto.regist_sub(New)
