"""ppm build命令的处理."""
from pmfp.utils.endpoint import EndPoint
from ..core import ppm


class Build(EndPoint):
    """打包指定位置项目为便于分发的形式.

    需要指定形式为: 
        exec--可执行程序,可以通过static来指定是否为纯静态可执行程序
        alib--静态库
        dlib--动态库
        zip--将文件打包为zip包

    go语言:
        exec--可执行程序,可以通过static来指定是否为纯静态可执行程序
        alib--静态库
        dlib--动态库
        zip--将文件打包为zip包

    cython语言:
        可以编译为exec和dlib

    python语言:
        由于python本身为脚本语言所以其打包只是将源码放入zip包中
        exec--打包为.pyz文件,如果声明为`static`则将依赖也放入zip中,如果声明`mini`则代码先编译为pyc再打包
        zip--wheel打包

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
                "description": "编译的代码语言,如果language为`cython则只能编译为动态链接库`",
                "enum": ["go", "cython", "py"]
            },
            "code": {
                "description": "语言源码位置或者入口文件位置",
                "type": "string",
            },
            "output_dir": {
                "type": "string",
                "title": "t",
                "description": "编译结果目录",
                "default": "dist"
            },
            "project_name": {
                "type": "string",
                "title": "n",
                "description": "项目名"
            },
            "upx": {
                "type": "boolean",
                "title": "u",
                "description": "是否使用upx给可执行文件加壳(`build_as`为`exec`有效)"
            },
            "static": {
                "type": "boolean",
                "title": "s",
                "description": "是否编译为无依赖的静态文件(`build_as`为`exec`有效)",
                "default": True
            },
            "mini": {
                "type": "boolean",
                "title": "m",
                "description": "是否最小化编译"
            },
            "includes": {
                "type": "array",
                "title": "i",
                "description": "包含的头文件路径",
                "items": {
                    "type": "string"
                }
            },
            "libs": {
                "type": "array",
                "title": "b",
                "description": "使用的库名",
                "items": {
                    "type": "string"
                }
            },
            "lib_dir": {
                "type": "array",
                "title": "d",
                "description": "使用的库的位置",
                "items": {
                    "type": "string"
                }
            },
            "build_as": {
                "type": "string",
                "title": "a",
                "description": "编译为的目标,可选有exec,alib,dlib",
                "enum": ["exec", "alib", "dlib", "zip"],
                "default": "exec"
            },
            "for_linux_arch": {
                "type": "string",
                "title": "f",
                "description": "是否交叉编译支持其他指令集版本的linux",
                "enum": ["arm64", "amd64"]
            },
            "pypi_mirror": {
                "type": "string",
                "description": "pypi的镜像源,比如https://pypi.tuna.tsinghua.edu.cn/simple",
            },
            "requires": {
                "type": "array",
                "title": "r",
                "description": "依赖,只有python打包时有效,注意有c扩展的依赖时打包出来的pyz也无法执行",
                "items": {
                    "type": "string"
                }
            },
            "cwd": {
                "type": "string",
                "description": "执行编译操作时的执行位置",
                "default": "."
            }
        }
    }


build_cmd = ppm.regist_sub(Build)
