"""编译js语言模块."""
import os
import warnings
from pathlib import Path
from typing import List, Optional
from pmfp.utils.run_command_utils import run


def build_pb_js(serv_file: str, includes: List[str], to: str, cwd: Path,
                js_import_style: str, web_import_style: str, web_mode: str,
                files: Optional[List[str]] = None, web: bool = False, ** kwargs: str) -> None:
    """编译grpc的protobuf定义文件为js语言模块.

    Args:
        serv_file (str): 定义grpc service的目标proto文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        cwd (Path): 执行目录.
        js_import_style (str): 生成的js/ts文件类型
        web_import_style (str): 使用grpc-web时的导入模式
        web_mode (str): 使用grpc-web时的
        files (List[str]): 待编译的protobuffer文件
        web (bool): 是否使用grpc-web编译
    """
    includes_str = " ".join([f"-I {include}" for include in includes])

    target_str = serv_file
    if files:
        target_str += " " + " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])

    if web:
        PROTOC_GEN_GRPC_WEB_PATH = os.getenv('PROTOC_GEN_GRPC_WEB_PATH')
        if PROTOC_GEN_GRPC_WEB_PATH:
            command = f"protoc {includes_str} --js_out=import_style={js_import_style},binary:{to} --grpc-web_out=import_style={web_import_style},mode={web_mode}:{to} {target_str}"
        else:
            raise AttributeError("需要先设定环境变量`PROTOC_GEN_GRPC_NODE_PATH`")
        try:
            run(command, cwd=cwd, visible=True)
        except Exception as err:
            warnings.warn(
                f"""编译grpc项目 {target_str} 为python模块失败:

            {str(err)}

            编译grpc-js-web需要安装protoc-gen-grpc-web <https://github.com/grpc/grpc-web/releases>,将其放入`PATH`
            并将protoc-gen-grpc-web`的路径指定到环境变量`PROTOC_GEN_GRPC_WEB_PATH"""
            )
        else:
            print(f"编译grpc项目 {target_str} 为js语言模块为grpc-web使用完成!")

    else:
        PROTOC_GEN_GRPC_NODE_PATH = os.getenv('PROTOC_GEN_GRPC_NODE_PATH')
        if PROTOC_GEN_GRPC_NODE_PATH:
            command = f"protoc {includes_str} --plugin=protoc-gen-grpc={PROTOC_GEN_GRPC_NODE_PATH} --js_out=import_style={js_import_style},binary:{to} --grpc_out=grpc_js:{to} {target_str}"
        else:
            raise AttributeError("需要先设定环境变量`PROTOC_GEN_GRPC_NODE_PATH`")
        try:
            run(command, cwd=cwd, visible=True)
        except Exception as err:
            warnings.warn(
                f"""编译grpc项目 {target_str} 为python模块失败:

            {str(err)}

            编译grpc-js需要安装grpc-tools <https://www.npmjs.com/package/grpc-tools>,
            并将插件grpc_node_plugin`的路径指定到环境变量`PROTOC_GEN_GRPC_NODE_PATH"""
            )
        else:
            print(f"编译grpc项目 {target_str} 为js语言模块完成!")
