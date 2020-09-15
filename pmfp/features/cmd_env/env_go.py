"""使用go mod初始化golang的执行环境."""
import warnings
from pmfp.utils.run_command_utils import get_golang_version
from pmfp.utils.fs_utils import get_abs_path
from pmfp.const import GO_ENV_PATH
from pmfp.utils.template_utils import template_2_content

PMFP_GOLANG_ENV_TEMP = """module ${project_name}

require (
    
)
go ${language_version}
"""


def new_env_go(root: str, project_name: str) -> None:
    """初始化golang默认的虚拟环境.

    Args:
        root (str): 虚拟环境所在的根目录
        project_name (str): 项目名

    """
    root_path = get_abs_path(root)
    go_env_path = root_path.joinpath(GO_ENV_PATH)
    if go_env_path.exists():
        warnings.warn("go的虚拟环境已存在!")
    else:
        language_version = get_golang_version()
        if language_version:
            content = template_2_content(template=PMFP_GOLANG_ENV_TEMP, project_name=project_name, language_version=language_version)
            with open(str(go_env_path), "w", encoding="utf-8") as f:
                f.write(content)
        else:
            warnings.warn("""需要先安装go语言编译器.""")
