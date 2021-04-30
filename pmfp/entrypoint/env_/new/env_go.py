"""使用go mod初始化golang的执行环境."""
import pkgutil
import warnings
from pathlib import Path
from pmfp.utils.tools_info_utils import get_golang_version
from pmfp.utils.template_utils import template_2_content

go_mod_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'go.mod.jinja')
if template_io:
    go_mod_template = template_io.decode('utf-8')
else:
    raise AttributeError("go.mod模板失败")


def init_go_env(cwd: Path, project_name: str) -> None:
    """初始化golang默认的虚拟环境.

    Args:
        cwd (Path): 虚拟环境所在的根目录
        project_name (str): 项目名

    """

    go_env_path = cwd.joinpath("go.mod")
    if go_env_path.exists():
        warnings.warn("go.mod已存在!")
    else:
        language_version = get_golang_version()
        if language_version:
            language_version = ".".join(language_version.split(".")[:2])
            content = template_2_content(template=go_mod_template, project_name=project_name, language_version=language_version)
            with open(go_env_path, "w", newline="", encoding="utf-8") as f:
                f.write(content)
        else:
            warnings.warn("""需要先安装go语言编译器.""")
    print("构造go环境完成")
