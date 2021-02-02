"""编译python语言模块."""
import re
import pkgutil
import warnings
from pathlib import Path
from typing import List, Optional
from promise import Promise
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.tools_info_utils import get_global_python
from pmfp.utils.python_package_find_utils import find_pypackage_string
from pmfp.utils.template_utils import template_2_content

ServSource = ""
AioServSource = ""
CliSource = ""
AioCliSource = ""

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


def gen_code(includes_str: str, to: str, flag_str: str, target_str: str, cwd: Path) -> Promise:
    """生成python模块."""
    python = get_global_python()
    command = f"{python} -m grpc_tools.protoc {includes_str} {flag_str} --python_out={to} --grpc_python_out={to} {target_str}"
    print(f"编译命令:{command}")

    def _(_: str) -> None:
        print(f"编译grpc项目 {target_str} 为python模块完成!")
        trans_grpc_model_py(to)
        print("转换python项目的grpc文件为python模块完成!")

    return run_command(command, cwd=cwd).catch(
        lambda err: warnings.warn(f"""编译grpc项目 {target_str} 为python模块失败:

        {str(err)}

        编译grpc的python项目依赖如下插件,请检查是否安装:

        `pip install grpcio`
        `pip install grpcio-tools`
        `pip install grpcio-reflection`
        """)
    ).then(
        _
    ).catch(
        lambda content: warnings.warn(f"""转换python的grpc输出为一个模块失败:
        {str(content)}
        """)
    )


def find_grpc_package(to: Path) -> List[str]:
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


def gen_serv(service_name_lower: str, service_name: str, to: Path):
    content = template_2_content(
        ServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    to.joinpath("serv.py").write_text(content, encoding="utf-8")
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .serv import server\n")


def gen_cli(service_name_lower: str, service_name: str, to: Path):
    print(service_name_lower)
    print(service_name)
    content = template_2_content(
        CliSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    to.joinpath("cli.py").write_text(content, encoding="utf-8")
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .cli import client\n")


def gen_aio_serv(service_name_lower: str, service_name: str, to: Path):
    content = template_2_content(
        AioServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    to.joinpath("aioserv.py").write_text(content, encoding="utf-8")
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .aioserv import aio_server\n")


def gen_aio_cli(service_name_lower: str, service_name: str, to: Path):
    content = template_2_content(
        AioCliSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    to.joinpath("aiocli.py").write_text(content, encoding="utf-8")
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .aiocli import aio_client\n")


def _build_grpc_py_more(to: str, target: str, as_type: Optional[List[str]]) -> None:

    if not as_type:
        return
    path = Path(to)
    service_name_lower, service_name = find_grpc_package(path)
    for t in as_type:
        if t == "service":
            gen_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
            print("gen service code done")
        elif t == "client":
            gen_cli(service_name_lower=service_name_lower, service_name=service_name, to=path)
            print("gen client code done")
        elif t == "aiocli":
            gen_aio_cli(service_name_lower=service_name_lower, service_name=service_name, to=path)
            print("gen asyncio client code done")
        elif t == "aioserv":
            gen_aio_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
            print("gen asyncio service code done")
        else:
            print(f"为grpc项目 {target} 构造{t}模板失败,python语言不支持")


def build_pb_py(files: List[str], includes: List[str], to: str, as_type: Optional[List[str]], cwd: Path,
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
    gen_code(includes_str=includes_str, to=to, flag_str=flag_str, target_str=target_str, cwd=cwd).then(
        lambda _: _build_grpc_py_more(to=to, target=target_str, as_type=as_type)
    ).catch(
        lambda e: print(f"!!!!!!!!!!!!!!!!!!{e}$$$$$$$$$$$$$$$")
    )
