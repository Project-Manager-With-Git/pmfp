"""ppm docker image new命令的处理."""
import re
import pkgutil
import warnings
from pathlib import Path
from typing import List, Optional, Tuple
from pmfp.const import GOLBAL_PYTHON_VERSION
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.tools_info_utils import get_golang_version
from pmfp.utils.template_utils import template_2_content
from .core import dockerfile_new

PythonPureSource = ""
PythonExtendSource = ""
PipConfSource = ""

GoPureSource = ""
GoExtendSource = ""

CXXExtendSource = ""

source_io = pkgutil.get_data('pmfp.entrypoint.docker_.image.new.source_temp', 'python_pure.jinja')
if source_io:
    PythonPureSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载python_pure.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.docker_.image.new.source_temp', 'python_extend.jinja')
if source_io:
    PythonExtendSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载python_extend.jinja模板失败")
source_io = pkgutil.get_data('pmfp.entrypoint.docker_.image.new.source_temp', 'pip.conf.jinja')
if source_io:
    PipConfSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载pip.conf.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.docker_.image.new.source_temp', 'go_pure.jinja')
if source_io:
    GoPureSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载go_pure.jinja模板失败")

source_io = pkgutil.get_data('pmfp.entrypoint.docker_.image.new.source_temp', 'go_extend.jinja')
if source_io:
    GoExtendSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载go_extend.jinja模板失败")


source_io = pkgutil.get_data('pmfp.entrypoint.docker_.image.new.source_temp', 'cxx_extend.jinja')
if source_io:
    CXXExtendSource = source_io.decode('utf-8')
else:
    raise AttributeError("加载cxx_extend.jinja模板失败")


@dockerfile_new.as_main
def new_dockerfile(language: str, dockerfile_name: str = "Dockerfile",
                   cross_compiling: bool = False, extend: bool = False,
                   app_name: Optional[str] = None, project_name: Optional[str] = None,
                   cwd: str = ".") -> None:
    cwdp = get_abs_path(cwd)
    if app_name is None:
        if project_name is None:
            app_name = "app"
        else:
            app_name = project_name

    if language in ("py", "cython"):
        with open(cwdp.joinpath("pip.conf"), "w", newline="", encoding="utf-8") as f:
            f.write(PipConfSource)
        if extend or language == "cython":
            content = template_2_content(
                PythonExtendSource,
                python_version=GOLBAL_PYTHON_VERSION,
                cross_compiling="--platform=$TARGETPLATFORM " if cross_compiling else "",
                app_name=app_name)
        else:
            content = template_2_content(
                PythonPureSource,
                python_version=GOLBAL_PYTHON_VERSION,
                cross_compiling="--platform=$TARGETPLATFORM " if cross_compiling else "",
                app_name=app_name)
    elif language == "go":
        if extend:
            content = template_2_content(
                GoExtendSource,
                golang_version=get_golang_version(),
                cross_compiling="--platform=$TARGETPLATFORM " if cross_compiling else "",
                app_name=app_name)
        else:
            content = template_2_content(
                GoPureSource,
                golang_version=get_golang_version(),
                cross_compiling="--platform=$TARGETPLATFORM " if cross_compiling else "",
                app_name=app_name)
    elif language == "CXX":
        if extend:
            content = template_2_content(
                CXXExtendSource,
                cross_compiling="--platform=$TARGETPLATFORM " if cross_compiling else "",
                app_name=app_name)
        # else:
        #     content = template_2_content(
        #         GoPureSource,
        #         golang_version=get_golang_version(),
        #         cross_compiling="--platform=$TARGETPLATFORM " if cross_compiling else "",
        #         app_name=app_name)
    else:
        print(f"未知的环境类型{language}")
        return

    with open(cwdp.joinpath(dockerfile_name), "w", newline="", encoding="utf-8") as f:
        f.write(content)
