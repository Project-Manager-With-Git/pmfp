import shutil
import warnings
from pathlib import Path
from typing import Optional
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.run_command_utils import run_command
from ..utils import no_jekyll
from pmfp.const import PLATFORM


def move_doc(sourcep: Path, outputp: Path) -> None:
    p = None
    for i in sourcep.iterdir():
        if i.name.startswith("generated-"):
            p = i
            break
    if p is None:
        raise AttributeError("not generated")
    shutil.rmtree(outputp)
    shutil.move(p, outputp)
    shutil.rmtree(sourcep)
    no_jekyll(outputp)
    print("文档更新成功")


def doc_build_go(output: str, source_dir: str, *, version: Optional[str] = None, cwd: str = ".") -> None:
    """为go项目更新api文档.
    Args:
        output (str): html文档位置
        source_dir (str): 文档源码位置
        version (str): 项目版本
        cwd (str): 执行命令的根目录

    """
    if cwd:
        cwdp = get_abs_path(cwd)
    else:
        cwdp = Path(".")
    outputp = get_abs_path(output, cwd=cwdp)
    if not outputp.exists():
        warnings.warn("文档目录不存在!")
        return
    source_dirp = get_abs_path(source_dir, cwd=cwdp)
    if PLATFORM == 'Windows':
        source_dirp_str = str(source_dirp).replace("\\", "\\\\")
    else:
        source_dirp_str = str(source_dirp)

    command = f"golds -gen -dir={source_dirp_str} -wdpkgs-listing=solo -nouses ./..."
    run_command(command).catch(
        lambda e: warnings.warn(f"""gen doc get error {str(e)}
        you need to install golds first

        `go get -v -u go101.org/golds`
        """)
    ).then(
        lambda _: move_doc(source_dirp, outputp)
    ).catch(
        lambda e: warnings.warn(f"move doc get error {str(e)}")
    )
