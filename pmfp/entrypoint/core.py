class EntryPoint:
    """复杂入口定义."""

    def __init__(self):
        """初始化复杂入口."""
        self.cmds = {}
        self.argv = None

    def regist_cmd(self,func):
        
        

    def parse_args(self,argv):
        """解析复杂命令行."""
        parser = argparse.ArgumentParser(
            prog='ppm',
            epilog='除show命令,init命令,build_pb命令外每个子命令都需要在根目录下有名为.pmfp.json的配置文件.',
            description='Python用户的项目脚手架',
            usage=PPM_HELP)
        parser.add_argument('command', help='执行子命令')
        self.argv = argv
        args = parser.parse_args(argv[0:1])
        
        if not hasattr(self, args.command):
            print('未知的子命令')
            parser.print_help()
            exit(1)
        else:
            getattr(self, args.command)()