from pmfp.build_ import build
from pmfp.config import load_rc


def build_cmd():
    config = load_rc()
    if config:
        build(config)
    else:
        print("命令需要在pmfp项目中执行")
