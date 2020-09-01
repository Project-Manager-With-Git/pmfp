"""编译js语言的grpc-web模块."""
import warnings
from typing import List, Optional,Dict
from pmfp.utils.run_command_utils import run_command
def build_pb_web(files: List[str], includes: List[str], to: str,grpc:bool, **kwargs: Dict[str, str]) -> None:
    """编译js语言的grpc-web模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        grpc (bool): 是否编译为grpc

    """
    if grpc:
        warnings.warn("编译grpc-web需要安装`protoc-gen-grpc-web`<https://github.com/grpc/grpc-web/releases>")
        includes_str = " ".join([f"-I {include}" for include in includes])
        target_str = " ".join(files)
        flag_str = ""
        if kwargs:
            flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
        task = "grpc"
        command = f"protoc {includes_str} {flag_str} --js_out=import_style=commonjs:{to} --grpc-web_out=import_style=commonjs,mode=grpcwebtext:{to} {target_str}"
        print(f"编译命令:{command}")
        run_command(
            command,
            succ_cb=lambda : print(f"编译{task}项目 {target_str} 为web环境模块完成!"),
            fail_cb=lambda : print(f"编译{task}项目 {target_str} 为web环境模块失败!"))

    else:
        print("web环境只有grpc,如果需要编译普通protobuf文件,应该使用js环境")