"""tools_info_utils

获取功能依赖工具信息的工具组
"""
import sys
import json
import warnings
from pathlib import Path
from typing import Optional, Dict, Any
from jsonschema import validate
from pmfp.utils.run_command_utils import run
from pmfp.const import (
    GOLBAL_CC,
    GOLBAL_CXX,
    GOLBAL_PYTHON_VERSION,
    PMFP_CONFIG_HOME,
    PMFP_CONFIG_PATH,
    GLOBAL_CONFIG_PATH,
    DEFAULT_PMFPRC,
    GOLBAL_PYTHON,
    GOLBAL_CC
)
from pmfp.protocol import PMFP_CONFIG_SCHEMA


def get_global_python() -> str:
    """获取全局python."""
    with open(PMFP_CONFIG_PATH, "r") as f:
        pmfprc = json.load(f)
        return pmfprc.get("python", GOLBAL_PYTHON)


def get_global_cc() -> str:
    """获取全局c编译器."""
    with open(GLOBAL_CONFIG_PATH, "r") as f:
        pmfprc = json.load(f)
        return pmfprc.get("cc", GOLBAL_CC)


def get_global_cxx() -> str:
    """获取全局c++编译器."""
    with open(GLOBAL_CONFIG_PATH, "r") as f:
        pmfprc = json.load(f)
        return pmfprc.get("cxx", GOLBAL_CXX)


def get_node_version() -> Optional[str]:
    """获取系统中node的版本."""
    try:
        x = run("node -v")
    except Exception:
        warnings.warn("系统中未找到node环境,如有需要请安装")
        sys.exit(1)
    else:
        return x[1:]


def get_golang_version() -> Optional[str]:
    """获取本地golang的版本."""
    try:
        content = run("go version")
    except Exception as e:
        warnings.warn("系统中未找到golang环境,如有需要请安装")
        sys.exit(1)
    else:
        return [i for i in content.split(" ") if "." in i][0][2:]


def get_protoc_version() -> Optional[str]:
    """获取本地protoc的版本."""
    try:
        content = run("protoc --version")
    except Exception as e:
        warnings.warn("系统中未找到protoc环境,如有需要请安装")
        sys.exit(1)
    else:
        return [i for i in content.split(" ") if "." in i][0]


def init_pmfprc() -> None:
    """初始化pmfp的配置."""
    if not PMFP_CONFIG_PATH.exists():
        if not PMFP_CONFIG_HOME.exists():
            PMFP_CONFIG_HOME.mkdir(parents=True)
        config = {}
        config.update(DEFAULT_PMFPRC)
        with open(PMFP_CONFIG_PATH, "w", encoding="utf-8") as fw:
            json.dump(config, fw, ensure_ascii=False, indent=4, sort_keys=True)


def init_global_config() -> None:
    """初始化pmfp项目的全局配置."""
    if not GLOBAL_CONFIG_PATH.exists():
        if not PMFP_CONFIG_HOME.exists():
            PMFP_CONFIG_HOME.mkdir(parents=True)
        config = {
            "python_version": GOLBAL_PYTHON_VERSION,
            "cc": GOLBAL_CC,
            "cxx": GOLBAL_CXX
        }
        node_version = get_node_version()
        if node_version:
            config["node_version"] = node_version
        golang_version = get_golang_version()
        if golang_version:
            config["golang_version"] = golang_version
        with open(GLOBAL_CONFIG_PATH, "w", encoding="utf-8") as fw:
            json.dump(config, fw, ensure_ascii=False, indent=4, sort_keys=True)


def get_config_info() -> Dict[str, Any]:
    """获取配置信息."""
    with open(PMFP_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    try:
        validate(instance=config, schema=PMFP_CONFIG_SCHEMA)
    except Exception:
        warnings.warn(f"配置文件{PMFP_CONFIG_PATH}不符合规范,使用默认")
        return DEFAULT_PMFPRC
    else:
        conf = {}
        conf.update(DEFAULT_PMFPRC)
        conf.update(config)
        return conf


def get_cache_dir() -> Path:
    """获取缓存根目录."""
    config = get_config_info()
    return Path(config["cache_dir"])


def get_local_python(cwdp: Path) -> str:
    """获取本地环境python解释器的地址.

    Args:
        cwdp (Path): python本地环境目录.

    Returns:
        str: python位置字符串
    """

    env_path = cwdp.joinpath(get_config_info()["python_local_env_dir"])
    python_path = env_path.joinpath("bin/python")
    if not python_path.exists():
        python_path = env_path.joinpath("Scripts/python.exe")
        if not python_path.exists():
            python_path = env_path.joinpath("python")
            if not python_path.exists():
                warnings.warn("目录中未找到python环境.使用全局python")
                return get_global_python()
    return str(python_path)


init_pmfprc()
init_global_config()
