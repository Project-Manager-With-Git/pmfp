"""维护常量."""
import sys
import platform
import getpass
from pathlib import Path

# PLATFORM 执行平台
PLATFORM = platform.system()
# GOLBAL_PYTHON 全局python
GOLBAL_PYTHON = "python" if PLATFORM == 'Windows' else "python3"
# GOLBAL_CC 全局c编译器
GOLBAL_CC = "MSVC" if PLATFORM == 'Windows' else "gcc"
# GOLBAL_CXX 全局c++编译器
GOLBAL_CXX = "MSVC" if PLATFORM == 'Windows' else "g++"
# GOLBAL_PYTHON_VERSION 全局python的版本
GOLBAL_PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1])
# PMFP_CONFIG_DEFAULT_NAME
PMFP_CONFIG_DEFAULT_NAME = "pmfprc.json"

# PMFP_CONFIG_HOME pmfp工具的默认缓存和配置位置
PMFP_CONFIG_HOME = Path.home().resolve().joinpath(".pmfprc")
# PMFP_CONFIG_PATH pmfp工具的配置项
PMFP_CONFIG_PATH = PMFP_CONFIG_HOME.joinpath("config.json")
GLOBAL_CONFIG_PATH = PMFP_CONFIG_HOME.joinpath(PMFP_CONFIG_DEFAULT_NAME)


PY_ENV_PATH = "env"
JS_ENV_PATH = "package.json"
GO_ENV_PATH = "go.mod"
DOC_PATH = "document"
TEST_PATH = "test"
TYPECHECK_PATH = "typecheck"

DEFAULT_PMFPRC = {
    "cache_dir": str(PMFP_CONFIG_HOME.joinpath("cache")),
    "default_template_host": "github.com",
    "default_template_namespace": "Project-Manager-With-Git",
    "template_config_name": ".pmfp_template.json",
    "python": GOLBAL_PYTHON,
    "python_local_env_dir": "env",
    "default_typecheck_doc_dir": "doc_typecheck",
    "default_unittest_doc_dir": "doc_unittest"
}
DEFAULT_AUTHOR = getpass.getuser()
