import sys
import argparse
from .show_cmd import (
    show_template_cmd,
    show_component_cmd
)
from pmfp.config.verify import STATUS_RANGE
from .install_cmd import install_cmd
from .freeze_cmd import freeze_cmd
from .new_cmd import new_cmd
from .init_cmd import init_cmd
from .clean_cmd import clean_cmd
from .status_cmd import status_cmd
from .update_cmd import update_cmd
from .upload_cmd import upload_cmd
from .build_cmd import build_cmd
from .run_cmd import run_cmd
from .test_cmd import test_cmd
from .doc_cmd import doc_cmd
from .release_cmd import release_cmd
from .build_pb_cmd import build_pb_cmd

class PPM:
    """ppm命令的第一级子命令定义."""

    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            prog='ppm',
            epilog='除show命令和init命令外每个子命令都需要在根目录下有名为.pmfp.json的配置文件.',
            description='Python用户的项目脚手架',
            usage='''ppm <command> [<args>]

ppm工具的子命令有:
   show        展示已有的模板和组件

   install     安装依赖
   freeze      (python专用)将依赖保存到requirements.txt

   new         新增一个组件
   init        初始化一个项目
   clean       清空一个项目

   status      查看项目状态
   update      更新项目版本
   upload      将项目上传至git仓库

   run         执行项目,需要在配置文件中指定入口文件
   build       将项目打包
   release     将项目发表出去,app型的发表到docker的镜像仓库,module型的发表到包管理仓库
               
   test        执行测试
   doc         编译文档

   build_pb    将pb编译为对应项目语言的文件
''')
        parser.add_argument('command', help='执行子命令')
        self.argv = argv
        args = parser.parse_args(argv[0:1])
        if not hasattr(self, args.command):
            print('未知的子命令')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def show(self):
        parser = argparse.ArgumentParser(
            prog='ppm show',
            description='展示已有的模板和组件',
            epilog='子命令show可以用来查看模板和组件'
        )
        parser.set_defaults(func=lambda x: parser.print_help())

        subparsers = parser.add_subparsers(
            title='show命令的子命令',
            description='支持查看模板(template)和组件(component)',
            help='子解析模板(template)和组件(component)')

        template_parsers = subparsers.add_parser(
            "template", aliases=["T"], help="查看已有的模板")
        template_parsers.add_argument("-n", "--name", type=str, help="查看对应名字的模板", default="")
        template_parsers.add_argument("-l", "--language", type=str, help="查看对应语言的模板", default="")
        template_parsers.add_argument("-c", "--category", type=str, help="查看对应分类的模板", default="")
        template_parsers.set_defaults(func=show_template_cmd)

        component_parsers = subparsers.add_parser(
            "component", aliases=["C"], help="查看已有的组件")
        component_parsers.add_argument("-n", "--name", type=str, help="查看对应名字的组件", default="")
        component_parsers.add_argument("-l", "--language", type=str, help="查看对应语言的组件", default="")
        component_parsers.add_argument("-c", "--category", type=str, help="查看对应分类的组件", default="")
        component_parsers.set_defaults(func=show_component_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def install(self):
        """为项目安装依赖.如果有参数就是安装到固定环境,没有就是按固定环境安装其中写的内容."""

        parser = argparse.ArgumentParser(
            prog='ppm install',
            description='为项目安装依赖',
            epilog='子命令install用于安装依赖'
        )
        parser.add_argument('packages', nargs='?', type=str, default="DEFAULT")
        parser.add_argument(
            '--dev', action='store_true')
        parser.set_defaults(func=install_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def freeze(self):
        freeze_cmd()

    def new(self):
        """新增一个组件"""
        parser = argparse.ArgumentParser(
            prog='ppm new',
            description='为项目新增组件',
            epilog='''
子命令new用于新增组件,其中特殊的有:
document, doc            新建文档
env                      创建虚拟环境
readme                   创建markdown和rst格式的readme文件
setup                    python的安装脚本
cmd_setup                python的带命令行的安装脚本
cython_setup             cython的安装脚本
cython_numpy_setup       cython的安装脚本,带上numpy依赖
pb                       创建一个protobuf 文件
grpc                     创建一个grpc用的protobuf文件
''')
        parser.add_argument("component_name", type=str)
        parser.add_argument("-l", "--language", type=str, help="指定组件的语言", default="-")
        parser.add_argument("-t", "--to", type=str, help="指定一个存放的位置", default="-")
        parser.add_argument("-r", "--rename", type=str, help="重命名为", default="-")
        parser.add_argument('--test', action="store_true", default=False)
        parser.set_defaults(func=new_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def init(self):
        """创建对应模板项目的子命令"""
        print('Running ppm init')
        parser = argparse.ArgumentParser(
            prog='ppm init',
            description='基于模板创建一个项目',
            epilog='子命令init用于新建一个项目'
        )
        parser.add_argument("project_name", nargs='?', type=str, help="项目命名")
        parser.add_argument("-l", "--language", type=str, help="指定一个项目语言", default="")
        parser.add_argument("-t", "--template", type=str, help="指定一个项目模板", default="")
        parser.add_argument('--test', action="store_true", default=False, help="是否有测试用的对应组件")
        parser.add_argument('--doc', action="store_true", default=False, help="是否带着文档")
        parser.set_defaults(func=init_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def clean(self):
        """清理项目,删除文件."""
        parser = argparse.ArgumentParser(
            prog='ppm clean',
            description='清理项目')
        parser.add_argument(
            '-A', '--all', action='store_true', help="清理到只留下项目配置")
        parser.set_defaults(func=clean_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)

    def status(self):
        """查看项目状态的命令."""
        return status_cmd()

    def update(self):
        """更新项目元数据."""
        parser = argparse.ArgumentParser(
            prog='ppm update',
            description="更新项目的版本号和开发状态")
        parser.add_argument('-v', '--version', type=str)
        parser.add_argument('-s', "--status", type=str,
                            choices=STATUS_RANGE)
        parser.set_defaults(func=update_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("update done!")

    def upload(self):
        """上传数据流到git仓库."""
        parser = argparse.ArgumentParser(
            prog='ppm upload',
            description='upload project to a remote git repository')
        parser.add_argument('-m', '--message', type=str, default="", help="commit的信息")
        parser.add_argument('-t', '--with_tag', action="store_true", default=False, help="是否打标签")
        parser.set_defaults(func=upload_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("upload done!")

    def build(self):
        """按需求编译项目为二进制文件.

        包括编译dockerfile
        python可以选择将包编译为egg或者wheel用于发布,或者编译为pyz文件用于部署.
        node和c暂时不支持.
        """
        build_cmd()
        print("build package done!")

    def run(self):
        """执行命令的命令."""
        parser = argparse.ArgumentParser(
            prog='ppm run',
            description='执行脚本,脚本的入口由配置文件中的entry字段指定')
        parser.add_argument('script', type=str,
                            nargs='*')
        parser.set_defaults(func=run_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("run script done!")

    def release(self):
        release_cmd()
        print("release done!")

    def test(self):
        """测试命令的参数设置."""
        parser = argparse.ArgumentParser(
            prog='ppm test',
            description='test project')
        parser.add_argument('-H', '--html', action="store_true", default=False,
                            help="export the html report")
        parser.add_argument('-g', action="store_true", default=False,
                            help="use global env")
        parser.add_argument(
            '-T', '--typecheck', action="store_true", help="check python's typehints")
        parser.add_argument('--source', type=str, nargs='*', help="coverage source")
        parser.set_defaults(func=test_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("test done!")

    def doc(self):
        """用于构建文档"""
        parser = argparse.ArgumentParser(
            prog='ppm doc',
            description="build project's document")
        parser.add_argument('-s', '--serve', action="store_true")
        parser.set_defaults(func=doc_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)
        print("doc done!")

    def build_pb(self):
        parser = argparse.ArgumentParser(
            prog='ppm build_pb',
            description='编译pb文件',
            epilog='子命令build_pb可以用来编译.proto文件对应语言'
        )
        parser.add_argument("-n", "--name", type=str, help="待编译的文件名", default="data.proto")
        parser.add_argument("-d", "--dir", type=str, help="待编译的文件所在的地址", default="pbschema")
        parser.add_argument("-l", "--language", type=str, help="编译为什么语言", default="")
        parser.add_argument("--grpc", action="store_true", help="是否是grpc")
        parser.add_argument("-t", "--to", type=str, help="存放的", default="")
        parser.set_defaults(func=build_pb_cmd)
        args = parser.parse_args(self.argv[1:])
        args.func(args)


def main(argv=sys.argv[1:]):
    """服务启动入口.

    设置覆盖顺序`环境变量>命令行参数`>`'-c'指定的配置文件`>`项目启动位置的配置文件`>默认配置.
    """
    PPM(argv)
