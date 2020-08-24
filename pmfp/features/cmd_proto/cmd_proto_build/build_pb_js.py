"""编译js语言模块."""
import os
import warnings
import subprocess
import chardet
from typing import NoReturn, List, Dict


def build_pb_js(files: List[str], includes: List[str], to: str, grpc: bool, **kwargs: Dict[str, str]) -> NoReturn:
    """编译js语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        grpc (bool): 是否编译为grpc

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])


    if grpc:
        warnings.warn("""编译grpc-js需要安装`grpc-tools`<https://www.npmjs.com/package/grpc-tools>,并将插件`grpc_node_plugin`的路径指定到环境变量`PROTOC_GEN_GRPC_JS_PATH`""")
        task = "grpc"
        PROTOC_GEN_GRPC_JS_PATH = os.getenv('PROTOC_GEN_GRPC_JS_PATH')
        print(PROTOC_GEN_GRPC_JS_PATH)
        if PROTOC_GEN_GRPC_JS_PATH:
            #--grpc_out=grpc_js:{to}
            #command = f"protoc {includes_str} --js_out=import_style=commonjs,binary:{to} --grpc_js_out=import_style=commonjs,binary:{to} {target_str}"
            command = f"protoc {includes_str} --plugin=protoc-gen-grpc={PROTOC_GEN_GRPC_JS_PATH} --js_out=import_style=commonjs,binary:{to} --grpc_out=grpc_js:{to} {target_str}"
            res = subprocess.run(command, capture_output=True, shell=True)
        else:
            raise AttributeError("需要先设定环境变量`PROTOC_GEN_GRPC_JS_PATH`")
        
    else:
        warnings.warn("""编译为js模块需要安装`protoc-gen-js`<https://www.npmjs.com/package/protoc-gen>""")
        task = "protobuf"
        command = f"protoc {includes_str} --js_out=import_style=commonjs,binary:{to} {target_str}"
    print(f"编译命令:{command}")
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode == 0:
        print(f"编译{task}项目 {target_str} 为js语言模块完成!")
    else:
        print(f"编译{task}项目 {target_str} 为js语言模块失败!")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))