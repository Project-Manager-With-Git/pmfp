"""编译go语言模块."""
import warnings
from typing import List
from pathlib import Path
from pmfp.utils.run_command_utils import run


def _build_pb(includes: str, flag: str, to: str, target: str, cwd: Path) -> None:
    command = f"protoc  {includes} {flag} --go_out={to} {target}"
    try:
        run(command, cwd=cwd, visible=True)
    except Exception as err:
        warnings.warn(f"""编译protobuf项目 {target} 为go语言模块失败:

            {str(err)}

            需要安装额外插件"google.golang.org/protobuf/cmd/protoc-gen-go"
            """)
    else:
        print(f"编译protobuf项目 {target} 为go语言模块完成!")


def build_pb_go(files: List[str], includes: List[str], to: str, cwd: Path,
                source_relative: bool = False, **kwargs: str) -> None:
    """编译protobuffer为go语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        source_relative (bool): 是否使用路径作为包名,只针对go语言

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if source_relative:
        flag_str += " --go_opt=paths=source_relative"
    if kwargs:
        if flag_str:
            flag_str += " "
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])

    _build_pb(includes=includes_str, flag=flag_str, to=to, target=target_str, cwd=cwd)
