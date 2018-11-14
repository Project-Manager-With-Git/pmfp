from pmfp.clean import clean
from pmfp.config import load_rc

def clean_cmd(args):
    config = load_rc()
    if config is False:
        print("freeze命令需要目录下有.pmfprc.json配置文件.")
        return
    else:
        clean(args.all)
