"""创建protobuf文件."""
import shutil
import warnings
from typing import Dict, Any
from pmfp.const import PMFP_PB_TEMP, PROJECT_HOME
from pmfp.utils import (
    get_protoc_version
)
from .utils import template_2_file, iter_template_2_file


def new_pb(c_name: str, rename: str, to: str = "pbschema", project_name: str = ""):
    """创建protobuf文件.

    Args:
        c_name (str): 组件名,只能是pb或grpc
        rename (str): 项目中组件的名字
        to (str, optional): Defaults to "pbschema". 文件放到哪个文件夹.
    """
    if get_protoc_version() is None:
        warnings.warn("""本机没有安装protoc,请去<https://developers.google.com/protocol-buffers/docs/downloads>下载安装.
        
        如果要使用python环境,请安装python模块<grpc-tools>和<protobuf>
        要使用grpc的话请再安装python模块<grpcio>;

        如果使用go语言环境,请额外安装go包<github.com/golang/protobuf/protoc-gen-go>和<google.golang.org/genproto>
        要使用grpc的话请再安装go包<google.golang.org/grpc>;

        如果使用javascript的话,请额外安装js包<grpc>和<@grpc/proto-loader>
        """)
    t_path = PROJECT_HOME.joinpath(to)
    if not t_path.exists():
        print(f"找不到目标目录{str(t_path)},新建")
        t_path.mkdir(parents=True, exist_ok=False)
    if c_name == "grpc-web-proxy":
        c_path = PMFP_PB_TEMP.joinpath("grpc-web-proxy")
        to_path = t_path.joinpath(rename)
        if t_path.joinpath(rename).exists():
            print(f"存在同名组件{rename}")
            return
        else:
            shutil.copytree(
                str(c_path),
                str(to_path)
            )
            iter_template_2_file(project_name, to_path)
    else:
        if c_name == "pb":
            c_path = PMFP_PB_TEMP.joinpath("pbschema/data.proto.temp")
        elif c_name == "grpc":
            c_path = PMFP_PB_TEMP.joinpath("grpc-pbschema/data.proto.temp")
        elif c_name == "grpc-streaming":
            c_path = PMFP_PB_TEMP.joinpath(
                "grpc-streaming-pbschema/data.proto.temp")
        else:
            return
        to_path = t_path.joinpath(rename + ".proto")
        if to_path.exists():
            print(f"存在同名文件{rename}.proto")
            return
        else:
            shutil.copy(
                str(c_path),
                str(to_path)
            )
            template_2_file(to_path, rename=rename, project_name=project_name)
