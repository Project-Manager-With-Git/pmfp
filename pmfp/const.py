"""维护常量."""
import sys
import platform
from pathlib import Path

# PLATFORM 执行平台
PLATFORM = platform.system()
# GOLBAL_PYTHON 全局python
GOLBAL_PYTHON = "python" if PLATFORM == 'Windows' else "python3"

# GOLBAL_CC 全局c编译器
GOLBAL_CC = "MSVC" if PLATFORM == 'Windows' else "gcc"

# GOLBAL_PYTHON_VERSION 全局python的版本
GOLBAL_PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1])
# PMFP_CONFIG_HOME pmfp工具的默认缓存和配置位置
PMFP_CONFIG_HOME = Path.Home().resolve().joinpath(".pmfprc")
# PMFP_CONFIG_PATH pmfp工具的配置项
PMFP_CONFIG_PATH = PMFP_CONFIG_HOME.joinpath("pmfprc.json")

PY_ENV_PATH ="env"
JS_ENV_PATH = "package.json"
GO_ENV_PATH = "go.mod"
DOC_PATH = "document"
TEST_PATH = "test"
TYPECHECK_PATH = "typecheck"

DEFAULT_PMFPRC = {
    "cache_dir":str(PMFP_CONFIG_HOME.joinpath("cache")),
    "python": GOLBAL_PYTHON,
    "cc": GOLBAL_CC
}