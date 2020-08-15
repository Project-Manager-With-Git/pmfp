import argparse
from pmfp.update import update
from pmfp.config import load_rc, write_rc


def update_cmd(args: argparse.Namespace):
    config = load_rc()
    if config:
        if args.version:
            config.update({
                "version": args.version
            })
        if args.status:
            config.update({
                "status": args.status
            })
        write_rc(config)
        update(config)
        print("项目版本更新了")
    else:
        print("命令需要在pmfp项目中执行")
