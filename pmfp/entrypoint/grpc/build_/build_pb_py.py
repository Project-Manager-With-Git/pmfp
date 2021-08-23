"""编译python语言模块."""
import re
import sys
import warnings
from pathlib import Path
from typing import List, Optional, Tuple
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run
from pmfp.utils.tools_info_utils import get_global_python
from pmfp.utils.python_package_find_utils import find_pypackage_string

TRANS_GRPC_MODEL_IMPORT_TEMP = """
from .{pb_package} import *
from .{grpc_package} import *
"""


def find_py_grpc_pb2_import_string(name: str) -> str:
    """python的grpc模块as的内容."""
    return "__".join(name.split("_"))


def trans_grpc_model_py(to: str) -> None:
    """转换python的grpc输出为一个python模块.

    Args:
        to (str): 目标地址

    """
    to_path = get_abs_path(to)
    init_path = to_path.joinpath("__init__.py")
    init = False
    if not init_path.exists():
        init = True
    for p in to_path.iterdir():
        if p.is_file() and p.suffix == ".py" and p.name != "__init__.py":
            x = p.name.split("_")
            if x[-1] == "grpc.py":
                grpc_file = p
                grpc_name = p.name
                grpc_package = grpc_name.split(".")[0]
                pb_package = "_".join(x[:-1])
                if init is True:
                    init_path.open(
                        "a", encoding="utf-8", newline=""
                    ).write(
                        TRANS_GRPC_MODEL_IMPORT_TEMP.format(
                            pb_package=pb_package, grpc_package=grpc_package
                        )
                    )
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
                with open(str(grpc_file), "w", newline="", encoding="utf-8") as f:
                    f.writelines(new_lines)


def gen_code(includes_str: str, to: str, flag_str: str, target_str: str, cwd: Path) -> None:
    """生成python模块."""
    python = get_global_python()
    command = f"{python} -m grpc_tools.protoc {includes_str} {flag_str} --python_out={to} --grpc_python_out={to} {target_str}"
    print(f"编译命令:{command}")

    try:
        run(command, cwd=cwd, visible=True)
    except Exception as err:
        warnings.warn(f"""编译grpc项目 {target_str} 为python模块失败:

        {str(err)}

        编译grpc的python项目依赖如下插件,请检查是否安装:

        `pip install grpcio`
        `pip install grpcio-tools`
        """)
        sys.exit(1)
    else:
        print(f"编译grpc项目 {target_str} 为python模块完成!")
        try:
            trans_grpc_model_py(to)
        except Exception as e:
            warnings.warn(f"""转换python的grpc输出为一个模块失败:
                {str(e)}
            """)
            sys.exit(1)
        else:
            print("转换python项目的grpc文件为python模块完成!")


def find_grpc_package(to: Path) -> Tuple[str, str]:
    service_name_lower = ""
    service_name = ""
    for file in to.iterdir():
        if file.name.endswith("_pb2_grpc.py"):
            service_name_lower = file.name.replace("_pb2_grpc.py", "")
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                p = re.search(r"add_\w+Servicer_to_server", content)
                if p is not None:
                    c = p.group(0)
                    service_name = c.replace("add_", "").replace("Servicer_to_server", "")
    return service_name_lower, service_name


def build_pb_py(serv_file: str, includes: List[str], to: str, cwd: Path,
                files: Optional[List[str]] = None, **kwargs: str) -> None:
    """编译grpc的protobuf定义文件为python语言模块.

    Args:
        serv_file (str): 定义grpc service的目标proto文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        cwd (Path): 执行目录.
        files (List[str]): 待编译的protobuffer文件

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = serv_file
    serv_name = serv_file.replace(".proto", "")
    if files:
        target_str += " " + " ".join(files)
    flag_str = ""
    to = f"{to}/{serv_name}_pb"
    topath = Path(to)
    if not topath.exists():
        topath.mkdir(parents=True)
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    gen_code(includes_str=includes_str, to=to, flag_str=flag_str, target_str=target_str, cwd=cwd)
