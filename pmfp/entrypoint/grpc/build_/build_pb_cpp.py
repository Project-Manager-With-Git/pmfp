"""编译python语言模块."""
import re
import sys
import shutil
import pkgutil
import warnings
from pathlib import Path
from typing import List, Optional, Tuple
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run
from pmfp.utils.tools_info_utils import get_global_python
from pmfp.utils.python_package_find_utils import find_pypackage_string
from pmfp.utils.template_utils import template_2_content

TRANS_GRPC_MODEL_IMPORT_TEMP = """
from .{pb_package} import *
from .{grpc_package} import *
"""

HanddlerSource = ""
AioHanddlerSource = ""

CliExampleSource = ""
AioCliExampleSource = ""


ServSource = ""
AioServSource = ""


CliSource = ""
AioCliSource = ""

# handdler
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'handdler.py.temp')
if source_io:
    HanddlerSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载handdler.py.temp模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aiohanddler.py.temp')
if source_io:
    AioHanddlerSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aiohanddler.py.temp模板失败")


# example
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'cli_example.py.temp')
if source_io:
    CliExampleSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载cli_example.py.temp模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aiocli_example.py.temp')
if source_io:
    AioCliExampleSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aiocli_example.py.temp模板失败")

# serv
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'serv.py.temp')
if source_io:
    ServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载serv.py.temp模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aioserv.py.temp')
if source_io:
    AioServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aioserv.py.temp模板失败")


# cli
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'cli.py.temp')
if source_io:
    CliSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载cli.py.temp模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aiocli.py.temp')
if source_io:
    AioCliSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aiocli.py.temp模板失败")


def find_py_grpc_pb2_import_string(name: str) -> str:
    """python的grpc模块as的内容."""
    return "__".join(name.split("_"))


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
                to_path.joinpath("__init__.py").open(
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
    """生成cpp模块."""
    command = f"protoc {includes_str} {flag_str} --grpc_out={to} --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` {target_str}"
    
    print(f"编译命令:{command}")

    def _(_: str) -> None:
        print(f"编译grpc项目 {target_str} 为c++模块完成!")
        trans_grpc_model_py(to)
        print("转换python项目的grpc文件为c++模块完成!")

    try:
        run(command, cwd=cwd, visible=True)
    except Exception as err:
        warnings.warn(f"""编译grpc项目 {target_str} 为python模块失败:

        {str(err)}

        编译grpc的cpp项目依赖`grpc_cpp_plugin`,请检查是否安装,如果未安装,请去
        <>下载最新插件后编译

        `grpc_cpp_plugin`需要源码安装
        """)
        sys.exit(1)
    else:
        try:
            print(f"编译grpc项目 {target_str} 为python模块完成!")
            trans_grpc_model_py(to)
        except Exception as e:
            warnings.warn(f"""转换python的grpc输出为一个模块失败:
                {str(e)}
            """)
            sys.exit(1)
        else:
            print("转换python项目的grpc文件为python模块完成!")


def gen_serv(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建handdler
    if to.joinpath("handdler.py").exists():
        print("handdler已经存在,不生成")
    else:
        content = template_2_content(
            HanddlerSource,
            service_name_lower=service_name_lower,
            service_name=service_name)
        with open(to.joinpath("handdler.py"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    # 再创建serv
    content = template_2_content(
        ServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("serv.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .serv import Serv\n")
    print("""grpc serv需要安装依赖:
    grpcio --no-binary grpcio
    grpcio-reflection
    grpcio-health-checking
    schema-entry

    通常还会使用到依赖:
    grpcio-tools
    """)


def gen_aio_serv(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建handdler
    content = template_2_content(
        AioHanddlerSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aiohanddler.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    # 再创建serv
    content = template_2_content(
        AioServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aioserv.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .aioserv import Serv\n")

    print("""grpc serv需要安装依赖:
    grpcio --no-binary grpcio
    grpcio-reflection
    grpcio-health-checking
    schema-entry

    通常还会使用到依赖:
    grpcio-tools
    uvloop
    """)


def gen_cli(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建cli
    content = template_2_content(
        CliSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("cli.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .cli import client\n")

    # 再创建example
    content = template_2_content(
        CliExampleSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("cli_example.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    print("""grpc cli需要安装依赖:
    grpcio
    pyproxypattern

    通常还会使用到依赖:
    grpcio-tools
    """)


def gen_aio_cli(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建cli
    content = template_2_content(
        AioCliSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aiocli.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .aiocli import aio_client\n")
    # 再创建example
    content = template_2_content(
        AioCliExampleSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aiocli_example.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    print("""grpc cli需要安装依赖:
    grpcio
    pyproxypattern

    通常还会使用到依赖:
    grpcio-tools
    uvloop
    """)


# def _build_grpc_cpp_more(to: str, target: str, as_type: Optional[List[str]]) -> None:
#     if not as_type:
#         return
#     path = Path(to)
#     service_name_lower, service_name = find_grpc_package(path)
#     if "serv" in as_type:
#         if "aio" in as_type:
#             gen_aio_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
#         else:
#             gen_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
#     if "cli" in as_type:
#         if "aio" in as_type:
#             gen_aio_cli(service_name_lower=service_name_lower, service_name=service_name, to=path)
#         else:
#             gen_cli(service_name_lower=service_name_lower, service_name=service_name, to=path)


def build_pb_cpp(files: List[str], includes: List[str], to: str, as_type: Optional[List[str]], cwd: Path,
                 **kwargs: str) -> None:
    """编译grpc的protobuf定义文件为python语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        as_type (str): 执行的目的. Default: "source"

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])

    gen_code(includes_str=includes_str, to=to, flag_str=flag_str, target_str=target_str, cwd=cwd)
    _build_grpc_cpp_more(to=to, target=target_str, as_type=as_type)
