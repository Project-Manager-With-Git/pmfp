import argparse
from pmfp.run import run
from pmfp.config import load_rc


def run_cmd(args: argparse.Namespace):
    config = load_rc()
    if config:
        if args.cmd:
            cmd = " ".join(args.cmd)
        else:
            cmd = None
        if args.entry:
            entry = args.entry
        else:
            entry = None
        run(config, entry, cmd)
    else:
        print("命令需要在pmfp项目中执行")
