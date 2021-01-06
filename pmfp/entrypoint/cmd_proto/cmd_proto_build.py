"""ppm proto build命令的处理."""
from schema_entry import EntryPoint
from .core import proto


class Build(EntryPoint):
    """创建protobuf文件."""
    argparse_noflag = "files"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required":["env","grpc","source_relative","includes","files"],
        "properties": {
            "env": {
                "description": "proto文件名,也是package名",
                "type": "array",
                "items": {
                    "type": "string",
                    "enum":["py","js","go","web"]
                }
            },
            "grpc": {
                "type": "boolean",
                "description": "是否是grpc",
                "default": False
            },
            "to": {
                "type": "string",
                "description": "存放的地方",
                "default": "."
            },
            "source_relative": {
                "type": "boolean",
                "description": "使用路径作为包名,只针对go语言",
                "default": False
            },
            "includes":{
                "type": "array",
                "description": "待编译的文件的依赖所在的文件夹",
                "items": {
                    "type": "string"
                },
                "default":["pbschema"]
            },
            "kwargs":{
                "type": "string",
                "description": "其他键值对的额外参数,使用`key::value,key::value`的形式"
            },
            "files":{
                "type": "array",
                "description": "待编译的文件名",
                "items": {
                    "type": "string"
                }
            }
        }
    }


proto_build = proto.regist_sub(Build)