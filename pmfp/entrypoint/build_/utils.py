import warnings
from pathlib import Path
from pmfp.utils.run_command_utils import run


def upx_process(target: str, cwd: Path) -> None:
    command = f"upx --best --lzma -o {target}_upx {target}"
    run(command, cwd=cwd, visible=True, fail_exit=True)
