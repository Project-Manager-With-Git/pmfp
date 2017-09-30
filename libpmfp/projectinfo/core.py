"""用于组合projectinfo的对象
"""
from typing import List, Optional
from .mixins import ToDictMixin


class MetaInfo(ToDictMixin):
    """用于描述项目元数据的类
    """

    def __init__(self, project_name: str, url: str, license: str="MIT", version: str="0.0.1"):
        self.project_name = project_name
        self.license = license
        self.version = version
        self.url = url


class AuthorInfo(ToDictMixin):
    """用于描述项目作者信息的类
    """

    def __init__(self, author: str, author_email: str):
        self.author = author
        self.author_email = author_email


class DescriptionInfo(ToDictMixin):
    """用于记录项目描述的类
    """

    def __init__(self, keywords: List[str], description: str):
        self.keywords = list(keywords)
        self.description = description


class FormInfo(ToDictMixin):
    """用于记录项目类型的类
    """

    def __init__(self, env: str, compiler: str, project_type: str,
                 template: str, install_remote: Optional[str]=None, 
                 upload_remote: Optional[str]=None):
        self.env = env
        self.compiler = compiler
        self.project_type = project_type
        self.template = template
        self.install_remote = install_remote
        self.upload_remote = upload_remote


__all__ = ["MetaInfo", "AuthorInfo", "DescriptionInfo", "FormInfo"]
