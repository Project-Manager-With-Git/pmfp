"""编译go语言模块."""
import re
import pkgutil
import warnings
from typing import List
from pathlib import Path
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.template_utils import template_2_content

ServiceSource = ""
HanddlerSource = ""
LocalresolverSource = ""
SDKSource = ""

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'serv.go.temp')
if source_io:
    ServiceSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载handdler.go.temp模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'handdler.go.temp')
if source_io:
    HanddlerSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载handdler.go.temp模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'localresolver.go.temp')
if source_io:
    LocalresolverSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载localresolver.go.temp模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'sdk.go.temp')
if source_io:
    SDKSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载sdk.go.temp模板失败")


def find_grpc_package(to: str) -> List[str]:
    path = Path(to)
    package = ""
    registservice = ""
    registclient = ""
    registclient_new = ""
    for file in path.iterdir():
        if file.name.endswith(".pb.go"):
            with open(file) as f:
                content = f.read()
                p = re.search(r"package \w+\s", content)
                if p is not None:
                    package = p.group(0)
                m = re.search(r"Register\w+Server", content)
                if m is not None:
                    registservice = m.group(0)
                n = re.search(r"New\w+Client", content)
                if n is not None:
                    registclient_new = n.group(0)
                    registclient = registclient_new.replace("New", "")
    return package, registservice, registclient, registclient_new


def _build_grpc(includes: str, flag: str, to: str, target: str) -> None:
    topath = Path(to)
    init = True
    for file in topath.iterdir():
        if file.suffix == ".go":
            init = False
            break

    def _make_server_temp(package: str, registservice: str) -> None:
        servcontent = template_2_content(ServiceSource, package=package, registservice=registservice)
        with open(Path(to).joinpath("serv.go"), "w", encoding="utf-8") as f:
            f.write(servcontent)
        handdlercontent = template_2_content(HanddlerSource, package=package)
        with open(Path(to).joinpath("handdler.go"), "w", encoding="utf-8") as f:
            f.write(handdlercontent)

    def _make_client_temp(package: str, registclient: str, registclient_new: str) -> None:
        Localresolvercontent = template_2_content(LocalresolverSource, package=package)
        with open(Path(to).joinpath("localresolver.go"), "w", encoding="utf-8") as f:
            f.write(Localresolvercontent)
        sdkcontent = template_2_content(SDKSource, package=package, registclient=registclient, registclient_new=registclient_new)
        with open(Path(to).joinpath("sdk.go"), "w", encoding="utf-8") as f:
            f.write(sdkcontent)

    def _build_pb_succ_cb(_: str) -> None:
        print(f"编译grpc项目 {target} 为go语言模块完成!")
        if init:
            print("初次创建项目,根据模板构造grpc项目")
            package, registservice, registclient, registclient_new = find_grpc_package(to)
            _make_server_temp(package, registservice)
            print(f"为grpc项目 {target} 构造服务端模板!")
            _make_client_temp(package, registclient, registclient_new)
            print(f"为grpc项目 {target} 构造客户端端模板!")

    command = f"protoc {includes} {flag} --go_out=plugins=grpc:{to} {target}"
    print(f"编译命令:{command}")
    run_command(
        command
    ).catch(
        lambda content: warnings.warn(f"""编译grpc项目 {target} 为go语言模块失败:

            {content}

            编译为go语言依赖如下插件,请检查是否安装:
            "google.golang.org/protobuf/cmd/protoc-gen-go"
            "google.golang.org/grpc/cmd/protoc-gen-go-grpc"
            """)
    ).then(
        _build_pb_succ_cb
    ).catch(
        lambda content: warnings.warn(f"""根据模板构造grpc项目失败:

            {content}
            """)
    ).get()


def build_pb_go(files: List[str], includes: List[str], to: str,
                source_relative: bool, **kwargs: str) -> None:
    """编译protobuffer为go语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        source_relative (bool): 是否使用路径作为包名,只针对go语言

    """
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if source_relative:
        flag_str += " --go_opt=paths=source_relative"
    if kwargs:
        if flag_str:
            flag_str += " "
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    _build_grpc(includes_str, flag_str, to, target_str)
