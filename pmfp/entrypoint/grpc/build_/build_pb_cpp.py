"""编译python语言模块."""
import os
import warnings
from pathlib import Path
from typing import List, Optional
from pmfp.utils.run_command_utils import run


def build_pb_cpp(serv_file: str, includes: List[str], to: str, cwd: Path,
                 files: Optional[List[str]] = None, **kwargs: str) -> None:
    """编译grpc的protobuffer定义文件为C++语言模块.

    Args:
        serv_file (str): 定义grpc service的目标proto文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        cwd (Path): 执行目录.
        files (Optional[List[str]]): 其他待编译的protobuffer文件

    """
    PROTOC_GEN_GRPC_CXX_PATH = os.getenv('PROTOC_GEN_GRPC_CXX_PATH')
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = serv_file
    serv_name = serv_file.replace(".proto", "")
    to = f"{to}/{serv_name}_pb"
    if files:
        target_str += " " + " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    if PROTOC_GEN_GRPC_CXX_PATH:
        command = f"protoc  {includes_str} {flag_str} --grpc_out={to} --plugin=protoc-gen-grpc={PROTOC_GEN_GRPC_CXX_PATH} --cpp_out={to} {target_str}"
    else:
        raise AttributeError("需要先设定环境变量`PROTOC_GEN_GRPC_CXX_PATH`")

    try:
        run(command, cwd=cwd, visible=True)
    except Exception as err:
        warnings.warn(f"""编译protobuf项目 {target_str} 为c++语言模块失败:

        {str(err)}
        """)
    else:
        print(f"编译protobuf项目{target_str}为c++语言模块完成!")
