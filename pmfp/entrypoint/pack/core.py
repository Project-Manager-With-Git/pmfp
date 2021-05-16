"""ppm pack命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import ppm


class Pack(EndPoint):
    """打包指定位置项目.
    
    
    """
    argparse_noflag = "code"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["code", "project_name"],
        "properties": {
            "language": {
                "type": "string",
                "title": "l",
                "description": "打包的代码语言",
                "enum": ["py"]
            },
            "code": {
                "description": "语言源码位置",
                "title": "s",
                "type": "string",
            },
            "output_dir": {
                "type": "string",
                "title": "d",
                "description": "打包结果目录",
                "default": "dist"
            },
            "project_name": {
                "type": "string",
                "title": "n",
                "description": "项目名"
            },
            "pack_as": {
                "type": "string",
                "title": "a",
                "description": "打包的目标,可选有exec,lib",
                "enum": ["exec", "lib"],
                "default": "exec"
            },
            "pypi_mirror": {
                "type": "string",
                "title": "m",
                "description": "pypi的镜像源,比如https://pypi.tuna.tsinghua.edu.cn/simple",
            },
            "cwd": {
                "type": "string",
                "description": "执行编译操作时的执行位置",
                "default": "."
            }
        }
    }


pack_cmd = ppm.regist_sub(Pack)
