"""编译js语言模块."""
import os
import warnings
from pathlib import Path
from typing import List, Optional
from pmfp.utils.run_command_utils import run


def build_pb_js(files: List[str], includes: List[str], to: str, as_type: Optional[List[str]], cwd: Path,
                ** kwargs: str) -> None:
    """编译grpc的protobuf定义文件为js语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        as_type (str): 执行的目的. Default: "source"

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])

    warnings.warn("""""")
    PROTOC_GEN_GRPC_JS_PATH = os.getenv('PROTOC_GEN_GRPC_JS_PATH')
    print(PROTOC_GEN_GRPC_JS_PATH)
    if PROTOC_GEN_GRPC_JS_PATH:
        command = f"protoc {includes_str} --plugin=protoc-gen-grpc={PROTOC_GEN_GRPC_JS_PATH} --js_out=import_style=commonjs,binary:{to} --grpc_out=grpc_js:{to} {target_str}"
    else:
        raise AttributeError("需要先设定环境变量`PROTOC_GEN_GRPC_JS_PATH`")
    try:
        run(command, cwd=cwd, visible=True)
    except Exception as err:
        warnings.warn(
            f"""编译grpc项目 {target_str} 为python模块失败:

        {str(err)}

        编译grpc-js需要安装grpc-tools <https://www.npmjs.com/package/grpc-tools>,
        并将插件grpc_node_plugin`的路径指定到环境变量`PROTOC_GEN_GRPC_JS_PATH"""
        )
    else:
        print(f"编译grpc项目 {target_str} 为js语言模块完成!")
