"""描述project类的模块."""
from .mixins import (
    ToDictMixin,
    CreateMixin,
    InitProjectMixin,
    NewMixin,
    CleanMixin,
    InstallMixin,
    Temp2pyMixin,
    PythonPathMixin,
    UpdateMixin,
    UploadMixin,
    RunMixin,
    BuildMixin,
    TestMixin,
    DocMixin
)
from .core import (
    MetaInfo,
    AuthorInfo,
    DescriptionInfo,
    FormInfo
)


class ProjectInfo(
        ToDictMixin,
        CreateMixin,
        InitProjectMixin,
        NewMixin,
        CleanMixin,
        InstallMixin,
        Temp2pyMixin,
        PythonPathMixin,
        UpdateMixin,
        UploadMixin,
        RunMixin,
        BuildMixin,
        TestMixin,
        DocMixin):
    """项目对象,记录针对项目的特征和方法."""

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        content = """
project: {self.meta.project_name}
version: {self.meta.version}
status:  {self.meta.status}
license: {self.meta.license}
language: {self.form.compiler}
form: {self.form.project_form}
template: {self.form.template}
""".format(self=self)
        return content

    def __init__(self,
                 meta: MetaInfo,
                 author: AuthorInfo,
                 desc: DescriptionInfo,
                 form: FormInfo)->None:
        """初始化项目.

        Args:
            meta (MetaInfo): - 项目元信息
            author (AuthorInfo): - 作者信息
            desc (DescriptionInfo): - 项目简介
            form (FormInfo): - 项目设置
        """
        self.meta = meta
        self.author = author
        self.desc = desc
        self.form = form
