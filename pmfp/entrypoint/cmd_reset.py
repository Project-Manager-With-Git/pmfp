"""reset命令的处理."""
import argparse
import json
from typing import Sequence
from pmfp.const import DEFAULT_PMFPRC, PMFP_CONFIG_PATH, PMFP_CONFIG_HOME
from .core import ppm


@ppm.regist_subcmd
def reset(argv: Sequence[str]) -> None:
    """重置pmfp的配置.

    ppm reset [--flags]
    """
    parser = argparse.ArgumentParser(
        prog='ppm reset',
        description='重置pmfp的配置',
        usage=ppm.subcmds.get("reset").__doc__
    )
    parser.add_argument("--python", type=str, help="指定全局python路径")
    parser.add_argument("--cc", type=str, help="指定全局c编译器")
    parser.add_argument("--cache_dir", type=str, help="指定缓存的存储位置")
    parser.set_defaults(func=cmd_reset)
    args = parser.parse_args(argv)
    args.func(args)


def cmd_reset(args: argparse.Namespace) -> None:
    """重置pmfp工具的配置."""
    config = {}
    config.update(DEFAULT_PMFPRC)
    if args.python:
        config.update(python=args.python)
    if args.cc:
        config.update(cc=args.cc)
    if args.cache_dir:
        config.update(cache_dir=args.cache_dir)

    if not PMFP_CONFIG_HOME.exists():
        PMFP_CONFIG_HOME.mkdir(parents=True)

    if PMFP_CONFIG_HOME.is_dir():
        with open(PMFP_CONFIG_PATH, "w") as f:
            json.dump(config, f, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        print(f"配置保存路径{str(PMFP_CONFIG_HOME)}已被占用")
