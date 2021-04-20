import os
import shutil
from pathlib import Path
from typing import Any
from pmfp.utils.run_command_utils import run
from pmfp.utils.template_utils import template_2_content


def sphinx_build(source_dir: Path, doc_dir: Path, *, cwd: Path = Path(".")) -> None:
    """编译更新文档.

    Args:
        source_dir (Path): 文档源码位置
        doc_dir (Path): 文档输出目标位置
        cwd (Path): 执行位置

    """
    command = f"sphinx-build {str(source_dir)} {str(doc_dir)}"
    run(command, cwd=cwd, visible=True)


def sphinx_new(source_dir: Path, project_name: str, author: str, version: str, *,
               cwd: Path = Path(".")) -> None:
    """为python/c++项目构造api文档.

    Args:
        source_dir (str): 文档源码位置
        project_name (str): 项目名
        author (str): 项目作者
        version (str): 项目版本

    """
    command = f"sphinx-quickstart --no-sep -v {version} -r {version} -p {project_name} -a {author} -l zh_CN --ext-todo --ext-mathjax --ext-viewcode {str(source_dir)}"
    run(command, cwd=cwd, visible=True, fail_exit=True)


def sphinx_config(source_dir: Path, append_content: str) -> None:
    """为sphinx的配置增加配置项.

    Args:
        source_dir (Path): 文档源文件地址
        append_content (str): 要添加的配置文本.

    """
    print("更新配置文件")
    with open(source_dir.joinpath("conf.py"), "r", encoding="utf-8") as fr:
        content = fr.read()
    with open(source_dir.joinpath("conf.py"), "w", newline="", encoding="utf-8") as fw:
        new_content = content + append_content
        fw.write(new_content)


def sphinx_config_update_version(source_dir: Path, version: str) -> None:
    """为sphinx的配置增加配置项.

    Args:
        version (str): 要更新的版本好.

    """
    print("更新项目配置中的版本号")
    content = []
    with open(source_dir.joinpath("conf.py"), "r", encoding="utf-8") as fr:
        for line in fr.readlines():
            if line.startswith("version"):
                line = f"version = '{version}'\n"
            if line.startswith("release"):
                line = f"release= '{version}'\n"
            content.append(line)

    with open(source_dir.joinpath("conf.py"), "w", newline="", encoding="utf-8") as fw:
        fw.write("".join(content))


def no_jekyll(output: Path) -> None:
    """为目录添加一个空文件`.nojekyll`.

    Args:
        output (Path): 放置的目录位置

    """
    nojekyll = output.joinpath(".nojekyll")
    if not nojekyll.exists():
        print("添加`.nojekyll文件`")
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
    print("复制README.md")
    _move_to_source(source_dir=source_dir, root=root, file_name="README.md")
    print("复制CHANGELOG.md")
    _move_to_source(source_dir=source_dir, root=root, file_name="CHANGELOG.md")


def makeindex(source_dir: Path, template: str, **kwargs: Any) -> None:
    """创建index.md.

    Args:
        source_dir (Path): [description]
        root (Path): [description]
    """
    content = template_2_content(template, **kwargs)
    if source_dir.joinpath("index.rst").exists():
        os.remove(source_dir.joinpath("index.rst"))
    with open(source_dir.joinpath("index.md"), "w", newline="", encoding="utf-8") as f:
        f.write(content)
