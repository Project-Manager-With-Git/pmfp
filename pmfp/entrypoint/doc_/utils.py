import shutil
from pathlib import Path
from pmfp.utils.run_command_utils import run_command
from pmfp.utils.template_utils import template_2_content
from promise import Promise


def sphinx_build(source_dir: Path, doc_dir: Path, *, cwd: Path = Path(".")) -> Promise:
    """编译更新文档.

    Args:
        source_dir (Path): 文档源码位置
        doc_dir (Path): 文档输出目标位置
        cwd (Path): 执行位置

    """
    command = f"sphinx-build {str(source_dir)} {str(doc_dir)}"
    return run_command(command, cwd=cwd)


def sphinx_new(source_dir: Path, project_name: str, author: str, version: str, *,
               cwd: Path = Path(".")) -> Promise:
    """为python/c++项目构造api文档.

    Args:
        source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本

    """
    command = f"sphinx-quickstart --no-sep -v {version} -r {version} -p {project_name} -a {author} -l en --ext-todo --ext-mathjax --ext-viewcode {str(source_dir)}"
    return run_command(command, cwd=cwd)


def sphinx_config(source_dir: Path, append_content: str) -> None:
    """为sphinx的配置增加配置项.

    Args:
        source_dir (Path): 文档源文件地址
        append_content (str): 要添加的配置文本.

    """
    with open(source_dir.joinpath("conf.py"), "r", encoding="utf-8") as fr:
        content = fr.read()
    with open(source_dir.joinpath("conf.py"), "w", encoding="utf-8") as fw:
        new_content = content + append_content
        fw.write(new_content)


def no_jekyll(output: Path) -> None:
    """为目录添加一个空文件`.nojekyll`.

    Args:
        output (Path): 放置的目录位置

    """
    nojekyll = output.joinpath(".nojekyll")
    if not nojekyll.exists():
        nojekyll.touch()


def _move_to_source(source_dir: Path, file_name: str, *, root: Path) -> None:
    rootp = root.joinpath(file_name)
    sourcep = source_dir.joinpath(file_name)
    if rootp.is_file():
        shutil.copy(
            str(rootp),
            str(sourcep)
        )
        print(f"复制{file_name}成功")


def move_to_source(source_dir: Path, *, root: Path) -> None:
    """将项目根目录下的描述文件复制同步到项目下.

    Args:
        source_dir (Path): 文档源文件所在文件夹位置
        root (Path): 要移动文档的项目根目录.

    """
    _move_to_source(source_dir=source_dir, root=root, file_name="README.md")
    _move_to_source(source_dir=source_dir, root=root, file_name="CHANGELOG.md")