"""编译python语言模块."""
from pathlib import Path
from pmfp.utils.run_command_utils import run_command
from typing import List, Optional,NoReturn,Dict

def _find_pypackage(final_path: Path, packs: List[Optional[str]]):
    has_init = False
    for i in final_path.iterdir():
        if i.name == "__init__.py":
            has_init = True
    if not has_init:
        return
    else:
        lates_p = final_path.name
        packs.append(lates_p)
        _find_pypackage(final_path.parent, packs)


def find_pypackage_string(to_path: str) -> str:
    """find_pypackage_string.

    Args:
        to_path (str): 目标地址
    Returns:
        str: package地址

    """
    packs = []
    tp = Path(to_path)
    if tp.is_absolute():
        final_path = tp
    else:
        final_path = Path(".").absolute().joinpath(to_path)
    _find_pypackage(final_path, packs)
    packs = ".".join(reversed(packs))
    return packs


def find_py_grpc_pb2_import_string(name: str)->str:
    """python的grpc模块as的内容."""
    return "__".join(name.split("_"))

def _build_pb_py(files: List[str], includes: List[str], to: str, **kwargs: Dict[str, str]) -> NoReturn:
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    task = "protobuf"
    command = f"protoc  {includes_str} {flag_str} --python_out={to} {target_str}"
    print(f"编译命令:{command}")
    run_command(
        command,
        succ_cb=lambda : print(f"编译{task}项目{target_str}为python语言模块完成!"),
        fail_cb=lambda : print(f"编译{task}项目{target_str}为python语言模块失败!"))


def _build_grpc_py(files: List[str], includes: List[str], to: str, **kwargs: Dict[str, str])->NoReturn:
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    task = "grpc"
    command = f"python -m grpc_tools.protoc {includes_str} {flag_str} --python_out={to} --grpc_python_out={to} {target_str}"
    print(f"编译命令:{command}")
    def _():
        print(f"编译{task}项目 {target_str} 为python模块完成!")
        trans_grpc_model_py(to)

    run_command(
        command,
        succ_cb=_,
        fail_cb=lambda : print(f"编译{task}项目 {target_str} 为python模块失败!"))

def trans_grpc_model_py(to:str):
    """转换python的grpc输出为一个python模块.

    Args:
        to (str): 目标地址

    """
    tp = Path(to)
    if tp.is_absolute():
        to_path = tp
    else:
        to_path = Path(".").absolute().joinpath(to)

    for p in to_path.iterdir():
        if p.is_file() and p.suffix==".py" and p.name != "__init__.py":
            x = p.name.split("_")
            if x[-1]=="grpc.py":
                grpc_file = p
                grpc_name = p.name
                grpc_package = grpc_name.split(".")[0]
                pb_package = "_".join(x[:-1])
                pb_name = pb_package + ".py"         
                to_path.joinpath("__init__.py").open("a").write(
f"""
from .{pb_package} import *
from .{grpc_package} import *
""")

                with open(str(grpc_file), "r") as f:
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
                with open(str(grpc_file), "w") as f:
                    f.writelines(new_lines)
                print(f"转换python项目的grpc文件{grpc_name}为python模块完成!")


def build_pb_py(files: List[str], includes: List[str], to: str,grpc:bool, **kwargs: Dict[str, str]) -> NoReturn:
    """编译python语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        grpc (bool): 是否编译为grpc

    """
    if grpc:
        _build_grpc_py(files, includes, to, **kwargs)

    else:
        _build_pb_py(files, includes, to, **kwargs)