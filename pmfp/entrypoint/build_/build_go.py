"""编译go语言模块."""
import os
# from pmfp.entrypoint.build_ import build
import warnings
from typing import Optional
from pathlib import Path
from pmfp.utils.run_command_utils import run
from pmfp.utils.fs_utils import path_to_str
from pmfp.const import PLATFORM
from .utils import upx_process, zip_pack


def build_exec(code: str, project_name: str, *,
               output_dir: Path,
               cwd: Path,
               upx: bool = False,
               mini: bool = False,
               for_linux_arch: Optional[str] = None) -> None:
    if not cwd.joinpath("go.mod").exists():
        warnings.warn("go语言项目需要先有go.mod")
        return
    default_environ = dict(os.environ)
    env = {"GO111MODULE": "on", "GOPROXY": "https://goproxy.io"}
    env.update(default_environ)
    command = "go build"
    if mini:
        command += ' -ldflags "-s -w"'

    bin_name = project_name
    if PLATFORM == 'Windows' and not for_linux_arch:
        bin_name = f"{project_name}.exe"
    target_str = path_to_str(output_dir.joinpath(bin_name))
    command += f" -o {target_str} {code}"
    if for_linux_arch:
        env.update({
            "GOARCH": for_linux_arch,
            "GOOS": "linux"
        })
    run(command, cwd=cwd, env=env, visible=True, fail_exit=True)
    if upx:
        upx_process(target_str, cwd=cwd)


def build_alib(code: str, project_name: str, *,
               output_dir: Path,
               cwd: Path,
               for_linux_arch: Optional[str] = None) -> None:
    if not cwd.joinpath("go.mod").exists():
        warnings.warn("go语言项目需要先有go.mod")
        return
    default_environ = dict(os.environ)
    env = {"GO111MODULE": "on", "GOPROXY": "https://goproxy.io"}
    env.update(default_environ)
    command = "go build"
    bin_name = f"{project_name}.a"
    target_str = path_to_str(output_dir.joinpath(bin_name))
    command += f" -o {target_str} {code}"
    if for_linux_arch:
        env.update({
            "GOARCH": for_linux_arch,
            "GOOS": "linux"
        })
    run(command, cwd=cwd, env=env, visible=True, fail_exit=True)


def build_dlib(code: str, project_name: str, *,
               output_dir: Path,
               cwd: Path,
               for_linux_arch: Optional[str] = None) -> None:
    if not cwd.joinpath("go.mod").exists():
        warnings.warn("go语言项目需要先有go.mod")
        return
    default_environ = dict(os.environ)
    env = {"GO111MODULE": "on", "GOPROXY": "https://goproxy.io"}
    env.update(default_environ)
    command = "go build -buildmode=plugin"
    bin_name = f"{project_name}.plugin"
    target_str = path_to_str(output_dir.joinpath(bin_name))
    command += f" -o {target_str} {code}"
    if for_linux_arch:
        env.update({
            "GOARCH": for_linux_arch,
            "GOOS": "linux"
        })
    run(command, cwd=cwd, env=env, visible=True, fail_exit=True)


def go_build(code: str, project_name: str, *,
             output_dir: Path,
             cwd: Path,
             upx: bool = False,
             mini: bool = False,
             build_as: str = "exec",
             for_linux_arch: Optional[str] = None,
             ) -> None:
    if build_as == "exec":
        build_exec(code=code,
                   project_name=project_name,
                   output_dir=output_dir,
                   cwd=cwd,
                   upx=upx,
                   mini=mini,
                   for_linux_arch=for_linux_arch)
    elif build_as == "zip":
        zip_pack(code=code, output_dir=output_dir, cwd=cwd, project_name=project_name)

    elif build_as == "alib":
        build_alib(code=code,
                   project_name=project_name,
                   output_dir=output_dir,
                   cwd=cwd,
                   for_linux_arch=for_linux_arch)
    elif build_as == "dlib":
        build_dlib(code=code,
                   project_name=project_name,
                   output_dir=output_dir,
                   cwd=cwd,
                   for_linux_arch=for_linux_arch)
