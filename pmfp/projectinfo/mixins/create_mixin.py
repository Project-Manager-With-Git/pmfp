"""
用于保存创建project对象的类方法的mixin
"""
import json
import getpass
from pathlib import Path
import yaml
from ..core import MetaInfo, AuthorInfo, DescriptionInfo, FormInfo

IGNOR_PROJECT_NAME = ["app"]


class CreateMixin:
    @classmethod
    def from_dict(cls, info: dict):
        meta = MetaInfo(**info["meta"])
        author = AuthorInfo(**info["author"])
        desc = DescriptionInfo(**info["desc"])
        form = FormInfo(**info["form"])
        obj = cls(meta, author, desc, form)
        return obj

    @classmethod
    def from_json(cls, path: str):
        with open(path) as f:
            info = json.load(f)
        obj = cls.from_dict(info)
        return obj

    @classmethod
    def from_yaml(cls, path: str):
        with open(path) as f:
            info = yaml.load(f)
        obj = cls.from_dict(info)
        return obj

    @classmethod
    def input_info(
            cls,
            template: str,
            env: str,
            compiler: str,
            project_form: str):
        local_path = Path(".").absolute()
        while True:
            project_name = input("project name:")
            if project_name in IGNOR_PROJECT_NAME:
                print("{project_name} can not use as a project name".format(
                    project_name=project_name))
            else:
                break
        project_name = project_name or local_path.name
        if "-" in project_name:
            project_name.replace("-","_")
        license_path = local_path.joinpath("LICENSE")
        if license_path.exists():
            with license_path.open("r") as f:
                i = next(f)
            license_ = i.split(" ")[0]
        else:
            license_ = input("license:")
            license_def = "MIT"
            license_ = license_ or license_def

        url = input("url:")
        url = url or ""
        version = input("project version:")
        version = version or "0.0.1"
        status = input("project status:")
        status = status or "dev"
        meta = MetaInfo(project_name=project_name,
                        license=license_, url=url, version=version, status=status)

        author_ = input("author:")
        author_email = input("author_email:")
        author_ = author_ or getpass.getuser()
        author_email = author_email or ""
        author = AuthorInfo(author=author_, author_email=author_email)

        keywords = input("keywords,split by ',':")
        if keywords:
            keywords = [i for i in keywords.split(',')]
        else:
            keywords = []
        keywords = keywords or ['tools']
        description = input("description:")
        description = description or "simple tools"
        desc = DescriptionInfo(keywords=keywords, description=description)
        form = FormInfo(env, compiler, project_form, template)
        obj = cls(meta, author, desc, form)
        return obj


__all__ = ["CreateMixin"]
