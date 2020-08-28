import sys
import argparse
import functools
from typing import Callable,Sequence,NoReturn

class EntryPoint:
    

    def __init__(self):
        """初始化复杂入口."""
        self.subcmds = {}

    def __call__(self,argv:Sequence[str])->NoReturn:
        self.parse_args(argv)

    def regist_subcmd(self,func:Callable[[Sequence[str]],NoReturn])->Callable[[Sequence[str]],NoReturn]:
        """注册子命令.

        Args:
            func (Callabel[[Sequence[str]],NoReturn]): 子命令的处理函数

        Returns:
            Callabel[[Sequence[str]],NoReturn]: 包装后的子命令处理函数

        """
        @functools.wraps(func)
        def warp(argv:Sequence[str])->NoReturn:
            return func(argv)
        self.subcmds[func.__name__] = func
        return warp

    def parse_args(self,argv:Sequence[str])->NoReturn:
        """解析复杂命令行."""
        parser = argparse.ArgumentParser(
            prog=self.prog if hasattr(self,"prog") else None,
            epilog=self.epilog if hasattr(self,"epilog") else None,
            description=self.description if hasattr(self,"description") else None,
            usage=self.__doc__ if hasattr(self,"__doc__") else None)
        parser.add_argument('subcmd', help='执行子命令')
        args = parser.parse_args(argv[0:1])
        if self.subcmds.get(args.subcmd):
            self.subcmds[args.subcmd](argv[1:])
        else:
            print('未知的子命令')
            parser.print_help()
            sys.exit(1)
            

ppm = EntryPoint()
ppm.__doc__= """ppm <subcmd> [<args>]
    ppm工具的子命令有:

    工具自身相关:
    help              展示ppm的帮助说明
    version           展示ppm的版本

    项目管理类:
    template          管理模板项目
    project           管理项目
    stack             管理项目组
    
    常用工具类:
    proto             管理protobuffer文件
    schema            管理json schema文件
    http              http服务相关的工具
    """

ppm.prog = "ppm"
ppm.epilog = ''
ppm.description = '项目脚手架'