from pmfp.utils.endpoint import EndPoint
from ..core import grpc


class Build(EndPoint):
    """根据grpc的定义protobuf文件编译指定语言的模块.

    需要本地有`protoc`,可以在`https://github.com/protocolbuffers/protobuf/releases`下载安装
    """
    argparse_noflag = "serv_file"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["language", "source_relative", "pb_includes", "serv_file"],
        "properties": {
            "cwd": {
                "type": "string",
                "description": "执行命令的根目录",
                "default": "."
            },
            "language": {
                "description": "编译成的目标语言",
                "title": "l",
                "type": "string",
                "enum": ["py", "cython", "go", "js", "CXX"]
            },
            "to": {
                "type": "string",
                "title": "t",
                "description": "存放的地方",
                "default": "."
            },
            "source_relative": {
                "type": "boolean",
                "title": "r",
                "description": "使用路径作为包名,只针对go语言",
                "default": False
            },
            "pb_includes": {
                "type": "array",
                "title": "i",
                "description": "待编译的文件的依赖所在的文件夹",
                "items": {
                    "type": "string"
                },
                "default": ["pbschema"]
            },
            "kwargs": {
                "type": "string",
                "description": "其他键值对的额外参数,使用`key::value,key::value`的形式"
            },
            "files": {
                "type": "array",
                "title": "f",
                "description": "待编译的文件名",
                "items": {
                    "type": "string"
                }
            },
            "serv_file": {
                "type": "string",
                "description": "待编译的文件名",
            }
        }
    }


grpc_build = grpc.regist_sub(Build)
