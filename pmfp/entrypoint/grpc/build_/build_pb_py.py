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
NogenHanddlerSource = ""
AioHanddlerSource = ""
AioNogenHanddlerSource = ""

CliExampleSource = ""
NogenCliExampleSource = ""
AioCliExampleSource = ""
AioNogenCliExampleSource = ""

ServSource = ""
MpServSource = ""
NogenServSource = ""
NogenMpServSource = ""
AioServSource = ""
AioMpServSource = ""
AioNogenServSource = ""
AioNogenMpServSource = ""

CliSource = ""
NogenCliSource = ""
AioCliSource = ""
AioNogenCliSource = ""

# handdler
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'handdler.py.jinja')
if source_io:
    HanddlerSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载handdler.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aiohanddler.py.jinja')
if source_io:
    AioHanddlerSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aiohanddler.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'nogenhanddler.py.jinja')
if source_io:
    NogenHanddlerSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载nogenhanddler.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aionogenhanddler.py.jinja')
if source_io:
    AioNogenHanddlerSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aionogenhanddler.py.jinja模板失败")

# example
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'cli_example.py.jinja')
if source_io:
    CliExampleSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载cli_example.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'nogencli_example.py.jinja')
if source_io:
    NogenCliExampleSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载nogencli_example.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aiocli_example.py.jinja')
if source_io:
    AioCliExampleSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aiocli_example.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aionogencli_example.py.jinja')
if source_io:
    AioNogenCliExampleSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aionogencli_example.py.jinja模板失败")


# serv
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'serv.py.jinja')
if source_io:
    ServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载serv.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'mpserv.py.jinja')
if source_io:
    MpServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载mpserv.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'nogenserv.py.jinja')
if source_io:
    NogenServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载nogenserv.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'nogenmpserv.py.jinja')
if source_io:
    NogenMpServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载nogenmpserv.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aioserv.py.jinja')
if source_io:
    AioServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aioserv.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aiompserv.py.jinja')
if source_io:
    AioMpServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aiompserv.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aionogenserv.py.jinja')
if source_io:
    AioNogenServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aionogenserv.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aionogenmpserv.py.jinja')
if source_io:
    AioNogenMpServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aionogenmpserv.py.jinja模板失败")

# cli
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'cli.py.jinja')
if source_io:
    CliSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载cli.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'nogencli.py.jinja')
if source_io:
    NogenCliSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载nogencli.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aiocli.py.jinja')
if source_io:
    AioCliSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aiocli.py.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'aionogencli.py.jinja')
if source_io:
    AioNogenCliSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载aionogencli.py.jinja模板失败")


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
    """生成python模块."""
    python = get_global_python()
    command = f"{python} -m grpc_tools.protoc {includes_str} {flag_str} --python_out={to} --grpc_python_out={to} {target_str}"
    print(f"编译命令:{command}")

    def _(_: str) -> None:
        print(f"编译grpc项目 {target_str} 为python模块完成!")
        trans_grpc_model_py(to)
        print("转换python项目的grpc文件为python模块完成!")

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


def gen_mp_serv(service_name_lower: str, service_name: str, to: Path) -> None:
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
        MpServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("mpserv.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .mpserv import Serv\n")
    print("""grpc serv需要安装依赖:
    grpcio --no-binary grpcio
    grpcio-reflection
    grpcio-health-checking
    schema-entry

    通常还会使用到依赖:
    grpcio-tools
    """)


def gen_nogen_mp_serv(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建handdler
    if to.joinpath("handdler.py").exists():
        print("handdler已经存在,不生成")
    else:
        content = template_2_content(
            NogenHanddlerSource,
            service_name_lower=service_name_lower,
            service_name=service_name)
        with open(to.joinpath("nogenhanddler.py"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    # 再创建serv
    content = template_2_content(
        NogenMpServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("nogenmpserv.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .nogenmpserv import Serv\n")
    print("""grpc serv需要安装依赖:
    grpcio --no-binary grpcio
    grpcio-reflection
    grpcio-health-checking
    schema-entry

    通常还会使用到依赖:
    grpcio-tools
    """)


def gen_nogen_serv(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建handdler
    if to.joinpath("handdler.py").exists():
        print("handdler已经存在,不生成")
    else:
        content = template_2_content(
            NogenHanddlerSource,
            service_name_lower=service_name_lower,
            service_name=service_name)
        with open(to.joinpath("nogenhanddler.py"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    # 再创建serv
    content = template_2_content(
        NogenMpServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("nogenserv.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .nogenserv import Serv\n")
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


def gen_aio_mp_serv(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建handdler
    content = template_2_content(
        AioHanddlerSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aiohanddler.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    # 再创建serv
    content = template_2_content(
        AioMpServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aiompserv.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .aiompserv import Serv\n")

    print("""grpc serv需要安装依赖:
    grpcio --no-binary grpcio
    grpcio-reflection
    grpcio-health-checking
    schema-entry

    通常还会使用到依赖:
    grpcio-tools
    uvloop
    """)


def gen_aio_nogen_serv(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建handdler
    content = template_2_content(
        AioNogenHanddlerSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aiohanddler.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    # 再创建serv
    content = template_2_content(
        AioNogenServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aionogenserv.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .aionogenserv import Serv\n")

    print("""grpc serv需要安装依赖:
    grpcio --no-binary grpcio
    grpcio-reflection
    grpcio-health-checking
    schema-entry

    通常还会使用到依赖:
    grpcio-tools
    uvloop
    """)


def gen_aio_nogen_mp_serv(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建handdler
    content = template_2_content(
        AioNogenHanddlerSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aiohanddler.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    # 再创建serv
    content = template_2_content(
        AioNogenMpServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aionogenmpserv.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .aionogenmpserv import Serv\n")

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


def gen_nogen_cli(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建cli
    content = template_2_content(
        NogenCliSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("nogencli.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .nogencli import client\n")

    # 再创建example
    content = template_2_content(
        NogenCliExampleSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("nogencli_example.py"), "w", newline="", encoding="utf-8") as f:
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


def gen_aio_nogen_cli(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建cli
    content = template_2_content(
        AioNogenCliSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aionogencli.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    with open(to.joinpath("__init__.py"), "a", encoding="utf-8") as f:
        f.write("from .aionogencli import aio_client\n")
    # 再创建example
    content = template_2_content(
        AioNogenCliExampleSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("aionogencli_example.py"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    print("""grpc cli需要安装依赖:
    grpcio
    pyproxypattern

    通常还会使用到依赖:
    grpcio-tools
    uvloop
    """)


def _build_grpc_py_more(to: str, target: str, as_type: Optional[List[str]]) -> None:

    if not as_type:
        return
    path = Path(to)
    service_name_lower, service_name = find_grpc_package(path)
    if "serv" in as_type:
        if "aio" in as_type:
            if "mp" in as_type:
                if "nogen" in as_type:
                    pass
                    # gen_aio_nogen_mp_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
                else:
                    gen_aio_mp_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
            else:
                if "nogen" in as_type:
                    gen_aio_nogen_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
                else:
                    gen_aio_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
        else:
            if "mp" in as_type:
                if "nogen" in as_type:
                    gen_nogen_mp_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
                else:
                    gen_mp_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
            else:
                if "nogen" in as_type:
                    gen_nogen_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
                else:
                    gen_serv(service_name_lower=service_name_lower, service_name=service_name, to=path)
    if "cli" in as_type:
        if "aio" in as_type:
            if "nogen" in as_type:
                gen_aio_nogen_cli(service_name_lower=service_name_lower, service_name=service_name, to=path)
            else:
                gen_aio_cli(service_name_lower=service_name_lower, service_name=service_name, to=path)
        else:
            if "nogen" in as_type:
                gen_nogen_cli(service_name_lower=service_name_lower, service_name=service_name, to=path)
            else:
                gen_cli(service_name_lower=service_name_lower, service_name=service_name, to=path)


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
    if as_type and "nogen" in as_type:
        topp = cwd.joinpath(to).parent
        for include_dir in includes:
            include_dirp = cwd.joinpath(include_dir)
            for file in files:
                file_p = include_dirp.joinpath(file)
                if file_p.exists():
                    shutil.copyfile(file_p, topp.joinpath(file))
    else:
        gen_code(includes_str=includes_str, to=to, flag_str=flag_str, target_str=target_str, cwd=cwd)
    _build_grpc_py_more(to=to, target=target_str, as_type=as_type)
