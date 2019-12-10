import argparse
from pmfp.doc import doc
from pmfp.config import load_rc


def doc_cmd(args: argparse.Namespace):
    config = load_rc()
    if config:
        kwargs = _parser_args(args)
        doc(config, kwargs)
    else:
        print("命令需要在pmfp项目中执行")


def _parser_args(args: argparse.Namespace):
    kwargs = {
        "serve": False,
        "build": False,
        "update": False,
        "locale": None
    }
    if args.serve:
        kwargs.update({
            "serve": args.serve
        })
    if args.build:
        kwargs.update({
            "build": args.build
        })
    if args.update:
        kwargs.update({
            "update": args.update
        })

    if args.locale:
        kwargs.update({
            "locale": args.locale
        })
    return kwargs
