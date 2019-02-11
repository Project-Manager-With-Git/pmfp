from pmfp.run import run
from pmfp.config import load_rc


def run_cmd(args):
    config = load_rc()
    if config:
        if args.script:
            cmd = " ".join(args.script)
        else:
            cmd = None
        run(config, cmd)
    else:
        print("命令需要在pmfp项目中执行")
