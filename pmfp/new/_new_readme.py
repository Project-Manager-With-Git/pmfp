"""新建README文件."""
from string import Template
from typing import Dict, Any
from pmfp.const import (
    PMFP_README_TEMP,
    PROJECT_HOME,
)


def new_readme(config: Dict[str, Any]):
    """新建README文件.

    Args:
        config (Dict[str, Any]): 项目配置字典
    """
    rst_path = PROJECT_HOME.joinpath("README.rst")
    md_path = PROJECT_HOME.joinpath("README.md")
    rst_temp_path = PMFP_README_TEMP.joinpath("README.rst.temp")
    md_temp_path = PMFP_README_TEMP.joinpath("README.md.temp")
    # rst
    print("创建rst格式的文档")
    template_content = Template(rst_temp_path.open(encoding="utf-8").read())
    content = template_content.safe_substitute(
        project_name=config["project-name"],
        status=config["status"],
        version=config["version"],
        description=config["description"],
        url=config["url"],
        author=config["author"],
        author_email=config["author-email"],
        keywords=str(config["keywords"])
    )
    rst_path.open("w", encoding="utf-8").write(content)
    # md
    print("创建md格式的文档")
    template_content = Template(md_temp_path.open(encoding="utf-8").read())
    content = template_content.safe_substitute(
        project_name=config["project-name"],
        status=config["status"],
        version=config["version"],
        description=config["description"],
        url=config["url"],
        author=config["author"],
        author_email=config["author-email"],
        keywords=str(config["keywords"])
    )
    md_path.open("w", encoding="utf-8").write(content)
