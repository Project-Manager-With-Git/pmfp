"""编译go语言模块."""
import warnings
from typing import List, Optional
from pathlib import Path
from pmfp.utils.run_command_utils import run


def _build_grpc(includes: str, flag: str, to: str, target: str, cwd: Path) -> None:
    command = f"protoc {includes} {flag} --go_out=plugins=grpc:{to} {target}"
    try:
        run(command, cwd=cwd, visible=True)
    except Exception as e:
        warnings.warn(f"""根据模板构造grpc项目失败

        {str(e)}

        编译为go语言依赖如下插件,请检查是否安装:
        "google.golang.org/protobuf/cmd/protoc-gen-go"
        "google.golang.org/grpc/cmd/protoc-gen-go-grpc"
        """)
    else:
        print(f"编译grpc项目 {target} 为go语言模块完成!")


def build_pb_go(serv_file: str, includes: List[str], to: str,
                source_relative: bool, cwd: Path, files: Optional[List[str]] = None, **kwargs: str) -> None:
    """编译grpc的protobuffer定义文件为go语言模块.

    Args:
        serv_file (str): 定义grpc service的目标proto文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        source_relative (bool): 是否使用路径作为包名,只针对go语言
        cwd (Path): 执行目录.
        files (Optional[List[str]]): 其他待编译的protobuffer文件

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = serv_file
    if files:
        target_str += " " + " ".join(files)
    flag_str = ""
    if source_relative:
        flag_str += " --go_opt=paths=source_relative"
    if kwargs:
        if flag_str:
            flag_str += " "
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    _build_grpc(includes_str, flag_str, to, target_str, cwd)
