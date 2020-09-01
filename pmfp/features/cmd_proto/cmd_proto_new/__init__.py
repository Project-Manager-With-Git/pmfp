"""创建protobuf的schema."""
import subprocess
import warnings
from pathlib import Path
import pkgutil
from typing import Dict, Any,List,Optional
import chardet
from pmfp.utils.template_utils import template_2_content
from pmfp.utils.fs_utils import get_abs_path

proto_template = ""
grpc_template = ""
proto_template_io= pkgutil.get_data('pmfp.features.cmd_proto.cmd_proto_new.prototemp', 'proto.temp')
if proto_template_io:
    proto_template = proto_template_io.decode('utf-8')
else:
    raise AttributeError("加载proto模板失败")

grpc_template_io = pkgutil.get_data('pmfp.features.cmd_proto.cmd_proto_new.grpctemp', 'grpc.temp')
if grpc_template_io:
    grpc_template = grpc_template_io.decode('utf-8')
else:
    raise AttributeError("加载grpc模板失败")

def new_pb(name: str, to: str,*,parent_package:Optional[str]=None, grpc: bool=False) -> None:
    """新建一个protpbuf文件.

    Args:
        name (str): 文件名,文件名也为package名,如果是grpc,则其大写也是rpc的服务名
        to (str): protobuf文件路径
        parent_package (Optional[str], optional): 父包名. Defaults to None.
        grpc (bool, optional): 是否是grpc. Defaults to False.

    """
    to_path =get_abs_path(to)
    package_go = name
    if parent_package:
            package_go = parent_package.replace(".","_") + "/"+ name
    if grpc:
        content = template_2_content(template=grpc_template,parent_package=parent_package,name=name,package_go=package_go,name_upper=name.upper())
    else:
        content = template_2_content(template=proto_template,parent_package=parent_package,name=name,package_go=package_go)
    with open(str(to_path.joinpath(f"{name}.proto")),"w", encoding='utf-8') as f:
        f.write(content)


    
    
