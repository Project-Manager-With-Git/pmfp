# """ppm proto new命令的处理."""
# import argparse
# from typing import Sequence
# from pmfp.features.cmd_project.cmd_project_init import init_project
# from pmfp.const import DEFAULT_AUTHOR
# from .core import ppm_project


# @ppm_project.regist_subcmd
# def init(argv: Sequence[str]) -> None:
#     """创建一个新项目.

#     ppm proto init [-flag]
#     """
#     parser = argparse.ArgumentParser(
#         prog='ppm proto init',
#         description='创建pb文件',
#         usage=ppm_project.subcmds.get("new").__doc__
#     )
#     parser.add_argument("--root", type=str, default=".", help="创建环境的位置")
#     parser.add_argument("--project_name", type=str, default="example", help="环境对应的项目名")
#     parser.add_argument("--project_version", type=str, default="0.0.0", help="环境对应的项目版本")
#     parser.add_argument("--project_license", type=str, default="MIT", help="环境对应的项目的协议")
#     parser.add_argument("--author", type=str, default=DEFAULT_AUTHOR, help="环境对应的项目的作者")
#     parser.add_argument("--author_email", type=str, default="MIT", help="环境对应的项目的作者email")
#     parser.add_argument("--keywords", type=str, default="MIT", help="环境对应的项目的关键字")
#     parser.add_argument("--description", type=str, default="MIT", help="环境对应的项目的说明")
#     parser.set_defaults(func=cmd_new_pb)
#     args = parser.parse_args(argv)
#     args.func(args)


# def cmd_new_pb(args: argparse.Namespace) -> None:
#     """新建一个protobuf."""
#     new_pb(name=args.name, to=args.to, grpc=args.grpc, parent_package=args.parent_package)
