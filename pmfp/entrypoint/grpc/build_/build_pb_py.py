"""编译python语言模块."""
from pathlib import Path
import warnings
from typing import List
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.tools_info_utils import get_global_python
from pmfp.utils.python_package_find_utils import find_pypackage_string


def find_py_grpc_pb2_import_string(name: str) -> str:
    """python的grpc模块as的内容."""
    return "__".join(name.split("_"))


def _build_grpc_py(files: List[str], includes: List[str], to: str,
                   **kwargs: str) -> None:
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    python = get_global_python()
    command = f"{python} -m grpc_tools.protoc {includes_str} {flag_str} --python_out={to} --grpc_python_out={to} {target_str}"
    print(f"编译命令:{command}")

    def _(_: str) -> None:
        print(f"编译grpc项目 {target_str} 为python模块完成!")
        trans_grpc_model_py(to)

    run_command(
        command
    ).catch(
        lambda content: warnings.warn(f"""编译grpc项目 {target_str} 为python模块失败:

        {content}

        编译grpc的python项目依赖如下插件,请检查是否安装:

        `pip install grpcio`
        `pip install grpcio-tools`
        """)
    ).then(
        _
    ).catch(
        lambda content: warnings.warn(f"""转换python的grpc输出为一个模块失败:

        {content}
        """)
    ).get()


def trans_grpc_model_py(to: str) -> None:
    """转换python的grpc输出为一个python模块.

    Args:
        to (str): 目标地址

    """
    to_path = get_abs_path(to)
    for p in to_path.iterdir():
        if p.is_file() and p.suffix == ".py" and p.name != "__init__.py":
            x = p.name.split("_")
            if x[-1] == "grpc.py":
                grpc_file = p
                grpc_name = p.name
                grpc_package = grpc_name.split(".")[0]
                pb_package = "_".join(x[:-1])
                to_path.joinpath("__init__.py").open("a", encoding="utf-8").write(
                    f"""
from .{pb_package} import *
from .{grpc_package} import *
""")

                with open(str(grpc_file), "r", encoding='utf-8') as f:
                    lines = f.readlines()
                new_lines = []
                packstr = find_pypackage_string(to)
                as_package = find_py_grpc_pb2_import_string(pb_package)
                for line in lines:
                    if f"import {pb_package} as {as_package}" in line:
                        t = f"import {packstr}.{pb_package} as {as_package}\n"
                        new_lines.append(t)
                    else:
                        new_lines.append(line)
                with open(str(grpc_file), "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                print(f"转换python项目的grpc文件{grpc_name}为python模块完成!")


def build_pb_py(files: List[str], includes: List[str], to: str,
                **kwargs: str) -> None:
    """编译python语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径

    """
    _build_grpc_py(files, includes, to, **kwargs)
