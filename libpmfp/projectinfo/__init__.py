"""描述project类的模块
"""
from .mixins import ToDictMixin, CreateMixin
from .core import MetaInfo, AuthorInfo, DescriptionInfo, FormInfo


class ProjectInfo(ToDictMixin):
    """项目对象,记录针对项目的特征和方法
    """

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        content = """project:{self.meta.name}
        version:{self.meta.name}
        license:{self.meta.license}
        """.format(self=self)
        return content

    def __init__(self, meta: MetaInfo, author: AuthorInfo, desc: DescriptionInfo, form: FormInfo,
                 with_test: bool=True,
                 with_docs: bool=True,
                 with_dockerfile: bool=True):
        self.meta = meta
        self.author = author
        self.desc = desc
        self.form = form
        self.with_test = with_test
        if self.with_test != with_test:
            print(self.form.compiler, " do not support test now")
        self.with_docs = with_docs
        if self.with_docs != with_docs:
            print(self.form.compiler, " do not support docs now")
        self.with_dockerfile = with_dockerfile and self.form.compiler in [
            'python', "node"] and self.form.project_type in ["web", "celery", 'frontend']
        if self.with_dockerfile != with_dockerfile:
            print(self.form.compiler, self.form.project_type,
                  " do not support test now")
