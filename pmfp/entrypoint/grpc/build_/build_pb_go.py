"""编译go语言模块."""
import re
import pkgutil
import warnings
from typing import List, Optional, Tuple
from pathlib import Path
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run
from pmfp.utils.template_utils import template_2_content

ServiceSource = ""
HanddlerSource = ""
ExampleSource = ""
SDKSource = ""

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'serv.go.jinja')
if source_io:
    ServiceSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载serv.go.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'handdler.go.jinja')
if source_io:
    HanddlerSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载handdler.go.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'example.go.jinja')
if source_io:
    ExampleSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载localresolver.go.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.grpc.build_.source_temp', 'sdk.go.jinja')
if source_io:
    SDKSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载sdk.go.jinja模板失败")


def find_grpc_package(to: str) -> Tuple[str, str, str, str]:
    path = Path(to)
    package = ""
    registservice = ""
    registclient = ""
    registclient_new = ""
    for file in path.iterdir():
        if file.name.endswith(".pb.go"):
            with open(file, encoding="utf-8") as f:
                content = f.read()
                p = re.search(r"package \w+\s", content)
                if p is not None:
                    package_new = p.group(0)
                    package = package_new.replace("package ", "")
                m = re.search(r"Register\w+Server", content)
                if m is not None:
                    registservice = m.group(0)
                n = re.search(r"New\w+Client", content)
                if n is not None:
                    registclient_new = n.group(0)
                    registclient = registclient_new.replace("New", "")
    return package, registservice, registclient, registclient_new


def _build_grpc(includes: str, flag: str, to: str, as_type: Optional[List[str]], target: str, cwd: Path) -> None:
    topath = get_abs_path(to, cwd)

    def _make_server_temp(package: str, registservice: str) -> None:
        """如果已经存在`serv.go则不会执行`"""
        # 创建serv.go
        target_path = topath.joinpath("serv.go")
        if target_path.exists():
            print("项目已存在serv.go,不会重复初始化")
        else:
            servcontent = template_2_content(ServiceSource, package=package, registservice=registservice)
            with open(target_path, "w", newline="", encoding="utf-8") as f:
                f.write(servcontent)

        # 创建hanndler.go
        target_path = topath.joinpath("handdler.go")
        if target_path.exists():
            print("项目已存在handdler.go,不会重复初始化")
        else:
            package_upper = package.upper()
            handdlercontent = template_2_content(HanddlerSource, package=package, package_upper=package_upper)
            with open(target_path, "w", newline="", encoding="utf-8") as f:
                f.write(handdlercontent)

    def _make_client_temp(package: str, registclient: str, registclient_new: str) -> None:
        """如果已经存在`sdk.go则不会执行`"""
        # 创建sdk.go
        target_path = topath.joinpath("sdk.go")
        if target_path.exists():
            print("项目已存在sdk.go,不会重复初始化")
        else:
            sdkcontent = template_2_content(
                SDKSource,
                package=package,
                registclient=registclient,
                registclient_new=registclient_new
            )
            with open(target_path, "w", newline="", encoding="utf-8") as f:
                f.write(sdkcontent)

        # 创建example.go
        target_path = topath.joinpath("example.go")
        if target_path.exists():
            print("项目已存在example.go,不会重复初始化")
        else:
            examplecontent = template_2_content(
                ExampleSource,
                package=package,
                registclient=registclient,
                registclient_new=registclient_new
            )
            with open(target_path, "w", newline="", encoding="utf-8") as f:
                f.write(examplecontent)
        # Localresolvercontent = template_2_content(LocalresolverSource, package=package)
        # with open(topath.joinpath("localresolver.go"), "w", newline="", encoding="utf-8") as f:
        #     f.write(Localresolvercontent)

    command = f"protoc {includes} {flag} --go_out=plugins=grpc:{to} {target}"
    try:
        run(command, cwd=cwd, visible=True)
    except Exception as e:
        warnings.warn(f"""根据模板构造grpc项目失败{str(e)}""")
    else:
        try:
            print(f"编译grpc项目 {target} 为go语言模块完成!")
            if as_type is not None:
                print("根据模板构造grpc项目")
                package, registservice, registclient, registclient_new = find_grpc_package(to)
                print(f"{package}, {registservice}, {registclient}, {registclient_new}")
                for t in as_type:
                    if t == "serv":
                        _make_server_temp(package, registservice)
                        print(f"为grpc项目 {target} 构造{t}模板成功!")
                    elif t == "cli":
                        _make_client_temp(package, registclient, registclient_new)
                        print(f"为grpc项目 {target} 构造{t}端模板成功!")
                    else:
                        print(f"为grpc项目 {target} 构造{t}模板失败,go语言不支持")
        except Exception as e:
            warnings.warn(f"""编译grpc项目 {target} 为go语言模块失败:

            {str(e)}

            编译为go语言依赖如下插件,请检查是否安装:
            "google.golang.org/protobuf/cmd/protoc-gen-go"
            "google.golang.org/grpc/cmd/protoc-gen-go-grpc"
            """)


def build_pb_go(files: List[str], includes: List[str], to: str, as_type: Optional[List[str]],
                source_relative: bool, cwd: Path, **kwargs: str) -> None:
    """编译grpc的protobuffer定义文件为go语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        as_type (str): 执行的目的.
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
    _build_grpc(includes_str, flag_str, to, as_type, target_str, cwd)
