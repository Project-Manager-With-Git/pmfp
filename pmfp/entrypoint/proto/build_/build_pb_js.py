"""编译js语言模块."""
import warnings
from pathlib import Path
from typing import List
from pmfp.utils.run_command_utils import run


def build_pb_js(files: List[str], includes: List[str], to: str, cwd: Path, js_import_style: str,
                **kwargs: str) -> None:
    """编译js语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        js_import_style (str): 编译出来的js模块形式

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    
    command = f"protoc {includes_str} --js_out=import_style={js_import_style},binary:{to} {target_str}"
    try:
        run(command, cwd=cwd, visible=True)
    except Exception as err:
        lambda err: warnings.warn(f"""编译protobuf项目 {target_str} 为python模块失败:

        {str(err)}

        编译为js模块需要安装`protoc-gen-js`<https://www.npmjs.com/package/protoc-gen>
        """)
    else:
        print(f"编译protobuf项目 {target_str} 为js语言模块完成!")
