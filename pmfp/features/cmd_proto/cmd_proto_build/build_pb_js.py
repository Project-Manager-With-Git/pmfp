"""编译js语言模块."""
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
        warnings.warn("""编译grpc-js需要安装`grpc-tools`<https://www.npmjs.com/package/grpc-tools>""")
        task = "grpc"
        #--grpc_out=grpc_js:{to}
        command = f"protoc {includes_str} --js_out=import_style=commonjs,binary:{to} --grpc_js_out=import_style=commonjs,binary:{to} {target_str}"
        res = subprocess.run(command, capture_output=True, shell=True)
        
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