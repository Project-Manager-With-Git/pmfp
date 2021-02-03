"""编译go语言模块."""
import os
import warnings
from typing import Optional
from pathlib import Path
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.fs_utils import path_to_str
from pmfp.const import PLATFORM
from .utils import upx_process


def go_build(code: str, project_name: str, *,
             output_dir: Path,
             cwd: Path,
             upx: bool = False,
             mini: bool = False,
             build_as: str = "exec",
             for_linux_arch: Optional[str] = None,
             ) -> None:
    default_environ = dict(os.environ)
    if build_as != "exec":
        warnings.warn("go语言只支持编译为可执行文件")
        return
    if not cwd.joinpath("go.mod").exists():
        warnings.warn("go语言项目需要先有go.mod")
        return
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
    rc = run_command(
        command, cwd=cwd, env=env, visible=True
    ).catch(
        lambda err: warnings.warn(f"""编译失败
            {str(err)}
            """)
    )
    if upx:
        rc.then(
            lambda _: upx_process(target_str, cwd=cwd)
        ).get()
    else:
        rc.get()
