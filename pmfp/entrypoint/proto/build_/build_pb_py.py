"""编译python语言模块."""
import warnings
from pathlib import Path
from typing import List
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run
from pmfp.utils.tools_info_utils import get_global_python


def _build_pb_py(files: List[str], includes: List[str], to: str, cwd: Path, **kwargs: str) -> None:
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    command = f"protoc  {includes_str} {flag_str} --python_out={to} {target_str}"
    try:
        run(command, cwd=cwd, visible=True)
    except Exception as err:
        warnings.warn(f"""编译protobuf项目 {target_str} 为python模块失败:

        {str(err)}
        """)
    else:
        print(f"编译protobuf项目{target_str}为python语言模块完成!")


def build_pb_py(files: List[str], includes: List[str], to: str, cwd: Path,
                **kwargs: str) -> None:
    """编译python语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径

    """
    _build_pb_py(files, includes, to, cwd, **kwargs)
