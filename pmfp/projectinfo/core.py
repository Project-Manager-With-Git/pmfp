"""用于组合projectinfo的对象."""
from typing import List
from .mixins import ToDictMixin


class MetaInfo(ToDictMixin):
    """用于描述项目元数据的类."""

    def __init__(self,
                 project_name: str,
                 url: str,
                 license: str="MIT",
                 version: str="0.0.1",
                 status="dev")->None:
        """描述项目元数据.

        Args:
            project_name (str): 项目名
            url (str): 项目地址
            license (str, optional): - 许可证声明(Defaults to "MIT")
            version (str, optional): - 项目版本(Defaults to "0.0.1")
            status (str, optional): -项目状态(Defaults to "dev")
        """
        self.project_name = project_name
        self.license = license
        self.version = version
        self.status = status
        self.url = url


class AuthorInfo(ToDictMixin):
    """用于描述项目作者信息的类."""

    def __init__(self,
                 author: str,
                 author_email: str)->None:
        """定义作者信息.

        Args:
            author (str): - 作者名
            author_email (str): - 作者邮箱
        """
        self.author = author
        self.author_email = author_email


class DescriptionInfo(ToDictMixin):
    """用于记录项目简介的类."""

    def __init__(self,
                 keywords: List[str],
                 description: str)->None:
        """项目简介.

        Args:
            keywords (List[str]): - 关键字
            description (str): - 简介
        """
        self.keywords = list(keywords)
        self.description = description


class FormInfo(ToDictMixin):
    """用于记录项目类型的类."""

    def __init__(self,
                 env: str,
                 compiler: str,
                 project_form: str,
                 template: str)->None:
        """记录项目设置

        python下可选的开发环境有`env`,`conda`,和`global`,
        对应于使用`venv`或者`conda`在项目下创建的虚拟环境和使用用户下的python环境

        Args:
            env (str): - 开发环境,
            compiler (str): - 使用的语言,可选的有python,node,和C
            project_form (str): - 项目类型
            template (str): - 项目模板
        """
        self.env = env
        self.compiler = compiler
        self.project_form = project_form
        self.template = template


__all__ = ["MetaInfo", "AuthorInfo", "DescriptionInfo", "FormInfo"]
