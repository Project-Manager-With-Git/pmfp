from pmfp.build_ import build
from pmfp.config import load_rc


def build_cmd(args):
    """编译项目中需要编译的源码."""
    config = load_rc()
    if config:
        cross = args.cross if args.cross else None
        build(config, args.inplace, cross)
    else:
        print("命令需要在pmfp项目中执行")
