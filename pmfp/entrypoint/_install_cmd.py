import argparse
from pmfp.install import install
from pmfp.config import load_rc


def install_cmd(args: argparse.Namespace):
    config = load_rc()
    if config is False:
        print("install命令需要目录下有.pmfprc.json配置文件.")
    else:
        kwargs = _parser_args(args)
        install(config, kwargs)


def _parser_args(args: argparse.Namespace):
    result = {
        "dev": False,
        "package": None
    }
    if args.dev:
        result.update({
            "dev": True
        })
    if args.packages != "DEFAULT":
        result.update({
            "package": args.packages
        })
    return result
