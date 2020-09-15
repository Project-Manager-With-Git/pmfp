"""编译go语言模块."""
from typing import List
from pmfp.utils.run_command_utils import run_command


def build_pb_go(files: List[str], includes: List[str], to: str, grpc: bool,
                source_relative: bool, **kwargs: str) -> None:
    """编译protobuffer为go语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        grpc (bool): 是否编译为grpc
        source_relative (bool): 是否使用路径作为包名,只针对go语言

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if source_relative:
        flag_str += "--go_opt=paths=source_relative"
    if kwargs:
        if flag_str:
            flag_str += " "
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    task = "protobuf"
    if grpc:
        command = f"protoc {includes_str} {flag_str} --go_out=plugins=grpc:{to}  {target_str}"
        task = "grpc"
    else:
        command = f"protoc  {includes_str} {flag_str} --go_out={to} {target_str}"
    print(f"编译命令:{command}")
    run_command(command,
                succ_cb=lambda x: print(f"编译{task}项目 {target_str} 为go语言模块完成!"))
