from pmfp.freeze import freeze
from pmfp.config import load_rc


def freeze_cmd():
    freeze_range = ("Python",)
    config = load_rc()
    if config is False:
        print("freeze命令需要目录下有pmfprc.json配置文件.")
        return
    else:
        if config['project-language'] not in freeze_range:
            print(f"freeze命令只有{freeze_range}中的编程语言支持")
        else:
            freeze(config)
