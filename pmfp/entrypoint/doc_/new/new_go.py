import shutil
import warnings
from pathlib import Path
from pmfp.utils.fs_utils import get_abs_path, path_to_str
from pmfp.utils.run_command_utils import run
from ..utils import no_jekyll


def doc_new_go(code: str, output: str, source_dir: str, *, project_name: str, author: str, version: str, is_web: bool = False, cwd: str = ".") -> None:
    """为go项目构造api文档.
    Args:
        code (str): 项目源码位置
        output (str): html文档位置
        source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本
        is_web (bool): 为真时执行`swag init --parseDependency --parseInternal`
        cwd (str): 执行命令的根目录
    """
    if cwd:
        cwdp = get_abs_path(cwd)
    else:
        cwdp = Path(".")
    outputp = get_abs_path(output, cwd=cwdp)
    if outputp.exists():
        warnings.warn("文档已存在!")
        return
    if is_web:
        if code != ".":
            command = f"swag init --parseDependency --parseInternal --output {outputp} --dir {code}"
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
        if code != "./...":
            command = f"golds -gen -dir={outputp} -source-code-reading=rich -wdpkgs-listing=solo -nouses {code}"
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
            no_jekyll(outputp)
            print("文档构建成功")
