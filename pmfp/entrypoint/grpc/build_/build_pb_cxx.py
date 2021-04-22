"""编译c++语言模块.

和其他不同为了照顾windows下的使用,cpp的grpc使用docker编译.
由于使用cpp写grpc一定是作为计算密集型任务的处理终端使用的,所以只提供了同步服务端
"""
import pkgutil
import warnings
from pathlib import Path
from typing import List
from pmfp.utils.template_utils import template_2_content

MainSource = ""
ServSource = ""
ServHeadSource = ""
DockerfileSource = ""
FindGRPCCmakeSource = ""
FindProtobufCmakeSource = ""

# cmake
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'FindGRPC.cmake.jinja')
if source_io:
    FindGRPCCmakeSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载FindGRPC.cmake.jinja模板失败")
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'FindProtobuf.cmake.jinja')
if source_io:
    FindProtobufCmakeSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载FindProtobuf.cmake.jinja模板失败")


# main
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'rpc.cc.jinja')
if source_io:
    MainSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载rpc.cc.jinja模板失败")

# serv
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'rpc_serv.cc.jinja')
if source_io:
    ServSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载rpc_serv.cc.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'rpc_serv.h.jinja')
if source_io:
    ServHeadSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载rpc_serv.h.jinja模板失败")


# dockerfile
source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'Dockerfile.jinja')
if source_io:
    DockerfileSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载Dockerfile.jinja模板失败")


def gen_serv(service_name_lower: str, service_name: str, to: Path) -> None:
    # 先创建cmake的grpc工具
    if not to.joinpath("cmake").exists():
        to.joinpath("cmake").mkdir(parents=True)
    if to.joinpath("cmake/FindGRPC.cmake").exists():
        warnings.warn("cmake/FindGRPC.cmake已经存在,不生成")
    else:
        content = FindGRPCCmakeSource
        with open(to.joinpath("cmake/FindGRPC.cmake"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    if to.joinpath("cmake/FindProtobuf.cmake").exists():
        warnings.warn("cmake/FindProtobuf.cmake已经存在,不生成")
    else:
        content = FindProtobufCmakeSource
        with open(to.joinpath("cmake/FindProtobuf.cmake"), "w", newline="", encoding="utf-8") as f:
            f.write(content)

    # 再创建dockerfile
    if to.joinpath("Dockerflie").exists():
        warnings.warn("Dockerflie已经存在,不生成")
    else:
        content = template_2_content(
            DockerfileSource,
            service_name_lower=service_name_lower,
            service_name=service_name)
        with open(to.joinpath("Dockerfile"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    # 再创建serv
    src_dir = to.joinpath("src")
    if not src_dir.exists():
        src_dir.mkdir(parents=True)
    if src_dir.joinpath(f"{service_name_lower}.cc").exists():
        warnings.warn(f"{service_name_lower}.cc已经存在,不生成")
    else:
        content = template_2_content(
            MainSource,
            service_name_lower=service_name_lower,
            service_name=service_name)
        with open(src_dir.joinpath(f"{service_name_lower}.cc"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    if src_dir.joinpath(f"{service_name_lower}_serv.cc").exists():
        warnings.warn(f"{service_name_lower}_serv.cc已经存在,不生成")
    else:
        content = template_2_content(
            ServSource,
            service_name_lower=service_name_lower,
            service_name=service_name)
        with open(src_dir.joinpath(f"{service_name_lower}_serv.cc"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    if src_dir.joinpath(f"{service_name_lower}_serv.h").exists():
        warnings.warn(f"{service_name_lower}_serv.h已经存在,不生成")
    else:
        content = template_2_content(
            ServHeadSource,
            service_name_lower=service_name_lower,
            service_name=service_name)
        with open(src_dir.joinpath(f"{service_name_lower}_serv.h"), "w", newline="", encoding="utf-8") as f:
            f.write(content)
    warnings.warn("""C++的grpc项目由cmake管理,请确保已经安装好了protobuf和grpc++.
    取消本工具cmake环境配置中protobuf和grpc部分的内容配置相应路径以激活对应支持.
    本项目只提供c++版本的服务端模板.
    同时提供一个dockerfile用于在docker中编译可执行文件.
    """)


def build_pb_cxx(files: List[str], cwd: Path) -> None:
    """为c++版本的grpc构造模板.

    由于使用cmake管理,而cmake难以解析所以只能给个大致

    Args:
        files (List[str]): 待编译的protobuffer文件
        cwd (Path): 执行时候的根目录
    """
    target = files[0]
    if target.endswith(".proto"):
        target = target.replace(".proto", "")
    service_name_lower = target.lower()
    service_name = target.upper()
    gen_serv(service_name_lower=service_name_lower, service_name=service_name, to=cwd)
