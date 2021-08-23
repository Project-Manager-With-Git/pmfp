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
        "required": ["language", "pb_includes", "serv_file"],
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
            "go_source_relative": {
                "type": "boolean",
                "title": "r",
                "description": "使用路径作为包名,只针对go语言",
                "default": False
            },
            "js_import_style": {
                "type": "string",
                "description": "编译出来的js模块形式",
                "enum": ["commonjs", "closure"],
                "default": "commonjs"
            },
            "web": {
                "type": "boolean",
                "description": "只针对js,是否编译为grpc-web使用的js模块,grpc-web是针对浏览器用的",
                "default": False
            },
            "web_import_style": {
                "type": "string",
                "description": "js编译出来的模块形式,只针对js",
                "enum": ["commonjs", "closure", "commonjs+dts", "typescript"],
                "default": "commonjs"
            },
            "web_mode": {
                "type": "string",
                "description": "传输的形式",
                "enum": ["grpcwebtext", "grpcweb"],
                "default": "grpcwebtext"
            },
            "serv_file": {
                "type": "string",
                "description": "待编译的文件名",
            },

        }
    }


grpc_build = grpc.regist_sub(Build)
