"""创建protobuf的schema."""
import subprocess
import warnings
import pkgutil
from pathlib import Path
from typing import Dict, Any, List, Optional

from pmfp.utils.template_utils import template_2_content
from pmfp.utils.fs_utils import get_abs_path

from .core import proto_new

proto_template = ""
grpc_template = ""
proto_template_io = pkgutil.get_data('pmfp.entrypoint.proto.new.source_temp', 'proto.jinja')
if proto_template_io:
    proto_template = proto_template_io.decode('utf-8')
else:
    raise AttributeError("加载proto模板失败")


@proto_new.as_main
def new_pb(name: str, pb_include: str, *, parent_package: Optional[str] = None, cwd: str = ".") -> None:
    """新建一个protpbuf文件.

    Args:
        name (str): 文件名,文件名也为package名,如果是grpc,则其大写也是rpc的服务名
        pb_include (str): protobuf文件存放的文件夹路径
        parent_package (Optional[str], optional): 父包名. Defaults to None.
        cwd (str, optional): 执行位置. Defaults to `.`.
    """
    try:
        to_path = get_abs_path(pb_include, Path(cwd))
        if not to_path.exists():
            to_path.mkdir(parents=True)
        package_go = name
        if parent_package:
            if parent_package.endswith("."):
                package_go = parent_package[:-1].replace(".", "_") + "/" + name
            else:
                package_go = parent_package.replace(".", "_") + "/" + name
                parent_package = parent_package + "."
        else:
            parent_package = ""

        content = template_2_content(
            template=proto_template,
            parent_package=parent_package,
            name=name,
            package_go=package_go)
        with open(str(to_path.joinpath(f"{name}.proto")), "w", newline="", encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        warnings.warn(f"""构造protobuffer文件失败:

        Error: {str(e)}
        """)
    else:
        print("构造protobuffer文件成功")
