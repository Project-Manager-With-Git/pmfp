import shutil
import warnings
from pathlib import Path
from pmfp.utils.fs_utils import get_abs_path, path_to_str
from pmfp.utils.run_command_utils import run
from ..utils import no_jekyll


def move_doc(sourcep: Path, outputp: Path) -> None:
    p = None
    for i in sourcep.iterdir():
        if i.name.startswith("generated-"):
            p = i
            break
    if p is None:
        raise AttributeError("not generated")
    shutil.rmtree(path_to_str(outputp))
    shutil.move(path_to_str(p), outputp)
    shutil.rmtree(path_to_str(sourcep))
    no_jekyll(outputp)
    print("文档更新成功")


def doc_build_go(output: str, *, source_dir: str, is_web: bool = False, cwd: str = ".") -> None:
    """为go项目更新api文档.
    Args:
        output (str): html文档位置
        source_dir (str): 文档源码位置
        version (str): 项目版本
        is_web (bool): 为真时执行`swag init --parseDependency --parseInternal`
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
    if is_web:
        if source_dir:
            command = f"swag init --parseDependency --parseInternal --output {outputp} --dir {source_dir}"
        else:
            command = f"swag init --parseDependency --parseInternal --output {outputp}"
        try:
            run(command, cwd=cwdp, visible=True)
        except Exception as e:
            warnings.warn(f"""gen doc get error {str(e)}
            you need to install swaggo first

            `go install github.com/swaggo/swag/cmd/swag@latest`""")
            return
        else:
            print("文档构建成功")
    else:
        if source_dir:
            command = f"golds -gen -dir={outputp} -source-code-reading=rich -wdpkgs-listing=solo -nouses {source_dir}"
        else:

            command = f"golds -gen -dir={outputp} -source-code-reading=rich -wdpkgs-listing=solo -nouses ./..."
        try:
            run(command, cwd=cwdp, visible=True)
        except Exception as e:
            warnings.warn(f"""gen doc get error {str(e)}
            you need to install golds first

            `go get -v -u go101.org/golds`""")
            return
        else:
            print("文档构建成功")