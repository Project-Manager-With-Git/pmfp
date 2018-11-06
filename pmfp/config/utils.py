import os
import copy
import json
from pathlib import Path
from pmfp.const import PMFPRC_PATH
from .verify import config_schema


def load_conf(path):
    """指定地址加载配置文件为配置字典."""
    with open(str(path)) as f:
        result = json.load(f)
    return config_schema(result)


def load_rc():
    if PMFPRC_PATH.is_file():
        config = load_conf(PMFPRC_PATH)
        return config
    else:
        return False


def write_rc(config):
    old_conf = load_rc()
    if old_conf:
        old_conf.update(config)
        config = old_conf
    config = config_schema(config)
    with open(str(PMFPRC_PATH), "w") as f:
        result = json.dump(config, f)
    print("配置文件")
