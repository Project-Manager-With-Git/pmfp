"""编译js语言模块."""
import os
import warnings
from typing import List
from pmfp.utils.run_command_utils import run_command


def build_pb_js(files: List[str], includes: List[str], to: str, cwd: Path,
                **kwargs: str) -> None:
    """编译js语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    command = f"protoc {includes_str} --js_out=import_style=commonjs,binary:{to} {target_str}"
    print(f"编译命令:{command}")
    run_command(command, cwd=cwd
                ).catch(
        lambda err: warnings.warn(f"""编译protobuf项目 {target_str} 为python模块失败:

        {str(err)}

        编译为js模块需要安装`protoc-gen-js`<https://www.npmjs.com/package/protoc-gen>
        """)
    ).then(
        lambda x: print(f"编译protobuf项目 {target_str} 为js语言模块完成!")
    ).get()
