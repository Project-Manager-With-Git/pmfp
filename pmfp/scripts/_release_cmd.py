import argparse
from pmfp.config import load_rc
from pmfp.release import release

def release_cmd():
    freeze_range = ("Python","Javascript")
    config = load_rc()
    if config is False:
        print("release命令需要目录下有.pmfprc.json配置文件.")
        return
    else:
        if config['project-language'] not in freeze_range:
            print(f"freeze命令只有{freeze_range}中的编程语言支持")
        else:
            release(config)
