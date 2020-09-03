import sys
import argparse
import functools
from typing import Callable,Sequence,Dict

class EntryPoint:
    prog:str
    epilog:str
    description:str
    subcmds: Dict[str, Callable[[Sequence[str]],None]]
    __name__: str
    def __init__(self,name:str)->None:
        """初始化复杂入口."""
        self.__name__ = name
        self.subcmds = {}
        self.prog = ""
        self.epilog = ''
        self.description = ''
        

    def __call__(self,argv:Sequence[str])->None:
        self.parse_args(argv)

    def regist_subcmd(self,func:Callable[[Sequence[str]],None])->Callable[[Sequence[str]],None]:
        """注册子命令.

        Args:
            func (Callabel[[Sequence[str]],]): 子命令的处理函数

        Returns:
            Callabel[[Sequence[str]],]: 包装后的子命令处理函数

        """
        @functools.wraps(func)
        def warp(argv:Sequence[str])->None:
            func(argv)
        self.subcmds[func.__name__] = func
        return warp

    def parse_args(self,argv:Sequence[str])->None:
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
            print(f'未知的子命令 {argv[1:]}')
            parser.print_help()
            sys.exit(1)
            

ppm = EntryPoint("ppm")
ppm.__doc__= """ppm <subcmd> [<args>]
    ppm工具的子命令有:

    工具自身相关:
    help              展示ppm的帮助说明
    version           展示ppm的版本
    reset             将ppm工具的设置初始化
    cache             管理ppm的缓存             

    项目管理类:
    template          管理模板项目
    project           管理项目
    stack             管理项目组
    
    常用工具类:
    proto             管理protobuffer文件
    schema            管理json schema文件
    http              http服务相关的工具
    test              执行测试
    """

ppm.prog = "ppm"
ppm.epilog = ''
ppm.description = '项目脚手架'