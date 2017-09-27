"""用于组合projectinfo的对象
"""
from typing import List
from .mixins import ToDictMixin


class MetaInfo(ToDictMixin):
    """用于描述项目元数据的类
    """

    def __init__(self, project_name: str, url: str,license: str="MIT", version: str="0.0.1"):
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

    def __init__(self, env: str, language: str, project_type: str,template:str):
        self.env = env
        self.language = language
        self.project_type = project_type
        self.template = template



__all__=["MetaInfo","AuthorInfo","DescriptionInfo","FormInfo"]