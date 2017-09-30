"""
用于保存创建project对象的类方法的mixin
"""
import json
import getpass
from pathlib import Path
from ..core import MetaInfo, AuthorInfo, DescriptionInfo, FormInfo

IGNOR_PROJECT_NAME = ["app"]


class CreateMixin:
    @classmethod
    def from_dict(cls, info: dict):
        meta = MetaInfo(**info["meta"])
        author = AuthorInfo(**info["author"])
        desc = DescriptionInfo(**info["desc"])
        form = FormInfo(**info["form"])
        obj = cls(meta, author, desc, form,
                  info['with_test'], info['with_docs'], info['with_dockerfile'])
        return obj

    @classmethod
    def from_json(cls, path: str):
        with open(path) as f:
            info = json.load(f)
        obj = cls.from_dict(info)
        return obj

    @classmethod
    def input_info(cls, with_test,
                   with_docs,
                   with_dockerfile,
                   template: str,
                   env: str='env',
                   compiler: str='python',
                   project_type: str='script'
                   ):
        local_path = Path(".").absolute()

        while True:
            project_name = input("project name:")
            if project_name in IGNOR_PROJECT_NAME:
                print("{project_name} can not use as a project name".format(
                    project_name=project_name))
            else:
                break
        project_name = project_name or local_path.name
        license_path = local_path.joinpath("LICENSE")
        if license_path.exists():
            with license_path.open("r") as f:
                i = next(f)
            license_def = i.split(" ")[0]
        else:
            license_ = input("license:")
            license_def = "MIT"
            license_ = license_ or license_def

        url = input("url:")
        url = url or ""
        version = input("project version:")
        version = version or "0.0.1"
        meta = MetaInfo(project_name=project_name,
                        license=license_, url=url, version=version)

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
        keywords = keywords or "'tools'"
        description = input("description:")
        description = description or "simple tools"
        desc = DescriptionInfo(keywords=keywords, description=description)

        install_remote = input(
            "use a special remote repository to install packages:")
        if not install_remote:
            if compiler == "cpp":
                install_remote = "conan-transit"
            else:
                install_remote = None

        upload_remote = input("use a special remote repository to upload:")
        if not upload_remote:
            if compiler == "cpp":
                upload_remote = "conan-transit"
            else:
                upload_remote = None
        form = FormInfo(env, compiler, project_type, template,
                        install_remote, upload_remote)
        obj = cls(meta, author, desc, form,
                  with_test, with_docs, with_dockerfile)
        return obj


__all__ = ["CreateMixin"]
