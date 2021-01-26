import warnings
from pathlib import Path
from pmfp.utils.run_command_utils import run_command


def upx(target: str, cwd: Path) -> None:
    command = f"upx --best --lzma -o {target}_upx {target}"
    run_command(command, cwd=cwd).catch(
        lambda e: warnings.warn(f"""upx加壳失败
        {str(e)}
        """)
    ).get()
