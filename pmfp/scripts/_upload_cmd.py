import argparse
from pmfp.upload import upload
from pmfp.config import load_rc


def upload_cmd(args: argparse.Namespace):
    config = load_rc()
    if config:
        kwargs = _parser_args(args)
        upload(config, kwargs)
    else:
        print("命令需要在pmfp项目中执行")


def _parser_args(args: argparse.Namespace):
    kwargs = {
        "msg": None,
        "tag": False
    }
    if args.message:
        kwargs.update({
            "msg": args.message
        })
    if args.with_tag:
        kwargs.update({
            "tag": args.with_tag
        })
    return kwargs
