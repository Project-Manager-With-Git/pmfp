"""编译c++语言模块.

和其他不同为了照顾windows下的使用,cpp的grpc使用docker编译.
由于使用cpp写grpc一定是作为计算密集型任务的处理终端使用的,所以只提供了同步服务端
"""
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
from pmfp.utils.template_utils import template_2_content

ServSource = ""
MakefileSource = ""
DockerfileSource = ""


# serv
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'serv.cc.temp')
if source_io:
    ServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载serv.cc.temp模板失败")

# makefile
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'makefile.temp')
if source_io:
    MakefileSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载makefile.temp模板失败")

# dockerfile
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'Dockerfile.temp')
if source_io:
    DockerfileSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载Dockerfile.temp模板失败")


def gen_serv(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建makefile
    if to.joinpath("makeflie").exists():
        print("makefile已经存在,不生成")
    else:
        content = template_2_content(
            MakefileSource,
            service_name_lower=service_name_lower,
            service_name=service_name)
        with open(to.joinpath("makeflie"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    # 再创建dockerfile
    if to.joinpath("Dockerflie").exists():
        print("Dockerflie已经存在,不生成")
    else:
        content = template_2_content(
            MakefileSource,
            service_name_lower=service_name_lower,
            service_name=service_name)
        with open(to.joinpath("DockerfileSource"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    # 再创建serv
    content = template_2_content(
        ServSource,
        service_name_lower=service_name_lower,
        service_name=service_name)
    with open(to.joinpath("serv.cc"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
    print("""grpc serv需要在docker环境下编译""")


def build_pb_cpp(files: List[str], includes: List[str], to: str, as_type: Optional[List[str]], cwd: Path,
                 **kwargs: str) -> None:
    """编译grpc的protobuf定义文件为python语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        as_type (str): 执行的目的. Default: "source"

    """
    target = files[0]
    if target.endswith(".proto"):
        target = target.replace(".proto", "")
    service_name_lower = target.lower()
    service_name = target.upper()
    gen_serv(service_name_lower=service_name_lower, service_name=service_name, to=cwd)
