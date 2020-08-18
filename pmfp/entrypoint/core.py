import os
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
            prog='ppm',
            epilog='除show命令,init命令,build_pb命令外每个子命令都需要在根目录下有名为.pmfp.json的配置文件.',
            description='Python用户的项目脚手架',
            usage=self.__doc__)
        parser.add_argument('subcmd', help='执行子命令')
        args = parser.parse_args(argv[0:1])
        if self.subcmds.get(args.subcmd):
            self.subcmds[args.subcmd](argv[1:])
        else:
            print('未知的子命令')
            parser.print_help()
            os.exit(1)
            

ppm = EntryPoint()
ppm.__doc__= """ppm <subcmd> [<args>]
    ppm工具的子命令有:

    help              展示ppm的帮助说明
    version           展示ppm的版本
    template          管理模板
    project           管理项目
    stack             管理项目组
    build_pb          代理protoc编译protobuffer
    """