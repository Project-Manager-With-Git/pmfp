"""编译js语言的grpc-web模块."""
import warnings
import subprocess
import chardet


def build_pb_web(name: str, dir_: str, to: str, grpc: bool) -> None:
    """编译js语言的grpc-web模块.

    Args:
        name (str): 要编译的pb文件
        dir_ (str): 要编译的pb文件所在文件夹
        to (str): 将模块文件编译到目标位置
        grpc (bool): 编译grpc
    """
    if grpc:
        warnings.warn(
            """编译grpc-web需要安装`protoc-gen-grpc-web`<https://github.com/grpc/grpc-web/releases>"""
        )
        command = f"protoc -I {dir_} {dir_}/{name} --js_out=import_style=commonjs:{to} \
            --grpc-web_out=import_style=commonjs,mode=grpcwebtext:{to}"
        print(command)
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"编译grpc的protobuf项目<{name}>为go语言模块完成!")
        else:
            print(f"编译grpc的protobuf项目{name}为go语言模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
    else:
        warnings.warn("""编译为js模块需要安装`protoc-gen-js`<https://www.npmjs.com/package/protoc-gen>""")
        command = f"protoc -I={dir_} --js_out=import_style=commonjs,binary:{to} {dir_}/{name}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"编译protobuf项目<{name}>为js语言模块完成!")
        else:
            print(f"编译protobuf项目{name}为js语言模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
