"""pmfp的常量."""

import sys
import platform
from pathlib import Path

PLATFORM = platform.system()
GOLBAL_PYTHON = "python" if PLATFORM == 'Windows' else "python3"
GOLBAL_PYTHON_VERSION = str(sys.version_info[0]) + "." + str(sys.version_info[1])
PROJECT_HOME = Path(".").absolute()
PMFPRC_PATH = PROJECT_HOME.joinpath("pmfprc.json")
PMFP_HOME = Path(__file__).parent.absolute()
ENV_PATH = PROJECT_HOME.joinpath("env")
JS_ENV_PATH = PROJECT_HOME.joinpath("package.json")
GO_ENV_PATH = PROJECT_HOME.joinpath("go.mod")
DOC_PATH = PROJECT_HOME.joinpath("document")
TEST_PATH = PROJECT_HOME.joinpath("test")
TYPECHECK_PATH = PROJECT_HOME.joinpath("typecheckhtml")

PMFP_SOURCE_HOME = PMFP_HOME.joinpath("source")
PMFP_TEMPLATES_HOME = PMFP_SOURCE_HOME.joinpath("templates")


PMFP_COMPONENTS_HOME = PMFP_SOURCE_HOME.joinpath("components")
PMFP_PB_TEMP = PMFP_SOURCE_HOME.joinpath("components/protobuf")
PMFP_DOC_TEMP = PMFP_SOURCE_HOME.joinpath("components/doc")
PMFP_README_TEMP = PMFP_SOURCE_HOME.joinpath("components/readme")
PMFP_SETUP_TEMP = PMFP_SOURCE_HOME.joinpath("components/setup")
PMFP_TEST_TEMP = PMFP_SOURCE_HOME.joinpath("components/test")
PMFP_GOLANG_ENV_TEMP = PMFP_SOURCE_HOME.joinpath("components/golang/universal/go.mod.temp")
