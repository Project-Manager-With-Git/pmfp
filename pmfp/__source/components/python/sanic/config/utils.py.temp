import os
import copy
import json
from pathlib import Path
from .verify import config_schema
from .default import DEFAULT_SETTING


def _load_conf_from_json(path):
    """指定地址加载配置文件为配置字典."""
    with open(path) as f:
        result = json.load(f)

    return config_schema(result)


def _load_conf_from_args(args):
    """通过命令行参数创建配置字典."""
    result = {}
    if args.port:
        result["PORT"] = args.port
    if args.host:
        result['HOST'] = args.host
    if args.nodebug:
        result['DEBUG'] = False
    return config_schema(result)


def _load_conf_from_env():
    result = {}
    if os.getenv('PORT'):
        result["PORT"] = os.getenv('PORT')
    if os.getenv('HOST'):
        result["HOST"] = os.getenv('HOST')
    if os.getenv('DEBUG'):
        result["DEBUG"] = os.getenv('DEBUG')
    return config_schema(result)


def load_conf(args):
    """加载配置.

    加载顺序优先级是`环境变量>命令行参数>指定位置配置文件>启动目录下的`config.json`配置文件>默认配置

    Args:
        args ([type]): [description]
        path ([type]): [description]
    """
    config = copy.deepcopy(DEFAULT_SETTING)
    p = Path("./config.json")
    if p.exists():
        config.update(**_load_conf_from_json(str(p)))
    if args.config:
        config.update(**_load_conf_from_json(args.config))
    config.update(**_load_conf_from_args(args))
    config.update(**_load_conf_from_env())
    return config
