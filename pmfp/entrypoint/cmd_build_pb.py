"""version命令的处理."""
import argparse
from .core import ppm
from typing import Sequence
from pmfp import VERSION

@ppm.regist_subcmd
def build_pb(argv:Sequence[str]):
    """ppm build_pb 

    获取pmfp工具的版本
    """
    parser = argparse.ArgumentParser(
        prog='ppm build_pb',
        description='编译pb文件',
        usage= ppm.subcmds.get("build_pb").__doc__
    )
    parser.add_argument("-n", "--name", type=str, help="待编译的文件名")
    parser.add_argument("-d", "--dir", type=str, help="待编译的文件所在的地址")
    parser.add_argument("-l", "--language", type=str, help="编译为什么语言")
    parser.add_argument("--grpc", action="store_true", help="是否是grpc")
    parser.add_argument("-t", "--to", type=str, help="存放的地方")
    parser.set_defaults(func=cmd_build_pb)
    args = parser.parse_args(argv)
    args.func(args)




def cmd_build_pb(args: argparse.Namespace):
    kwargs = _parser_args(args)
    build_pb(kwargs)


def _parser_args(args: argparse.Namespace):
    config = load_rc()
    kwargs = {}
    grpc = False
    name = ""
    if args.name:
        if args.name.endswith(".proto"):
            name = args.name
            kwargs.update({
                "name": name
            })
        else:
            name = f"{name}.proto"
            kwargs.update({
                "name": name
            })

    else:
        if not config:
            print("命令未在pmfp项目下执行,必须指定要编译的proto文件名")
            return
        else:
            project_name = config["project-name"]
            name = f"{project_name}.proto"
            kwargs.update({
                "name": name
            })
    if args.dir:
        kwargs.update({
            "dir": args.dir
        })
    else:
        if not config:
            print("命令未在pmfp项目下执行,必须指定要编译的proto文件所在的文件夹路径")
            return
        else:
            kwargs.update({
                "dir": "pbschema"
            })
    language = None
    if args.language:
        if args.language in ("go", "Go", "golang", "Golang"):
            language = "Golang"
        elif args.language in ("python", "py", "Python", "PY"):
            language = "Python"
        elif args.language in ("js", "javascript", "JS", "Javascript", "Js", "JavaScript"):
            language = "Javascript"
        elif args.language in ("web", "WEB", "Web"):
            language = "Web"
        elif args.language in ("asyncio", "Asyncio","aio"):
            language = "Asyncio"
        else:
            print("不支持的语言, 目前只支持Python,Golang和Javascript/Web")
            return
        kwargs.update({
            "language": language
        })
    else:
        if not config:
            print("命令未在pmfp项目下执行,必须指定要编译的proto文件所需要编译成模块的对应语言")
            return
        else:
            language = config["project-language"]
            env = config["env"]
            if language == "Javascript" and env not in ("node",):
                kwargs.update({
                    "language": "Web"
                })
            else:
                kwargs.update({
                    "language": language
                })

    if args.grpc:
        grpc = args.grpc
        kwargs.update({
            "grpc": grpc
        })
    else:
        kwargs.update({
            "grpc": grpc
        })

    if args.to:
        if args.to.startswith("/") or args.to.startswith(".."):
            print("请指定当前文件夹下的文件夹相对位置")
            return
        elif args.to == ".":
            to = "_".join(name.split("."))
            print(f"将在当前文件夹下创建{name}文件相应的模块{to}")
            kwargs.update({
                "to": to
            })
        elif args.to.startswith("./"):
            if language in ("Python","Asyncio") and grpc is True:
                to = args.to[2:] + "/" + "_".join(name.split("."))
            else:
                to = args.to[2:]
            kwargs.update({
                "to": to
            })
        elif args.to.startswith("grpc_cli"):

            if language in ("Python","Asyncio") and grpc is True:
                to = "grpc_cli/grpc_schema"
            else:
                to = "grpc_cli"
            kwargs.update({
                "to": to
            })
        else:
            if language in ("Python","Asyncio") and grpc is True:
                to = args.to + "/" + "_".join(name.split("."))
            else:
                to = args.to
            kwargs.update({
                "to": to
            })
    else:
        if not config:
            print("命令未在pmfp项目下执行,必须指定要编译的proto文件所需要编译成模块的位置")
            return
        else:
            project_name = config["project-name"]
            if language == "Golang":
                to = "grpc_schema"
            elif language in ("Python","Asyncio"):
                to = f"{project_name}/grpc_schema"
            elif language == "Javascript":
                to = f"es/grpc_schema"
            else:
                to = "_".join(name.split("."))
            kwargs.update({
                "to": to
            })

    return kwargs