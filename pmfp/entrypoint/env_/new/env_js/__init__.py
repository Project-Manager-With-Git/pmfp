from pathlib import Path
from typing import Optional, List
from .env_node import new_env_node
from .env_webpack import new_env_webpack


def init_js_env(cwd: Path, env: str, project_name: str, version: str, description: str, author: str,
                author_email: Optional[str] = None,
                keywords: Optional[List[str]] = None,
                requires: Optional[List[str]] = None,
                test_requires: Optional[List[str]] = None) -> None:
    if env == "webpack":
        new_env_webpack(cwd=cwd, project_name=project_name, version=version, description=description, author=author,
                        author_email=author_email, keywords=keywords, requires=requires, test_requires=test_requires)
    else:
        new_env_node(cwd=cwd, project_name=project_name, version=version, description=description, author=author,
                     author_email=author_email, keywords=keywords, requires=requires, test_requires=test_requires)
    print("构造js环境完成")
