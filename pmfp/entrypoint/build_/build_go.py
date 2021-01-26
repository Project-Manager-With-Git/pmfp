"""编译go语言模块."""
import warnings
from typing import Optional
from pathlib import Path
from pmfp.const import PLATFORM
from pmfp.utils.run_command_utils import run_command
from .utils import upx


def go_build(code: str, project_name: str, *,
             output_dir: Path,
             cwd: Path,
             upx: bool = False,
             mini: bool = False,
             build_as: str = "exec",
             for_linux_arch: Optional[str] = False,
             ) -> None:
    if build_as != "exec":
        warnings.warn("go语言只支持编译为可执行文件")
        return
    env = {"GO111MODULE": "on", "GOPROXY": "https://goproxy.io"}
    command = "go build"
    if mini:
        command += ' -ldflags "-s -w"'
    output_dir_str = ""
    if PLATFORM == 'Windows':
        output_dir_str = str(output_dir).replace("\\", "\\\\")
    else:
        output_dir_str = str(output_dir)
    target_str = f"{output_dir_str}/{project_name}"
    command += " -o {target_str} {code}"
    if for_linux_arch:
        env.update({
            "GOARCH": for_linux_arch,
            "GOOS": "linux"
        })
    run_command(
        command, cwd=cwd, env=env
    ).catch(
        lambda err: warnings.warn(f"""编译失败
            {str(err)}
            """)
    ).then(
        lambda _: upx(target_str, cwd=cwd)
    ).get()
