import subprocess
from .init_docker import InitDockerMixin
from .init_readme import InitReadmeMixin
from .init_docs import InitDocsMixin
from .init_env import InitEnvMixin
from .init_setup import InitSetupMixin
from .init_test import InitTestMixin
from .init_requirements import InitRequirementMixin


class InitProjectMixin(InitDockerMixin, InitReadmeMixin, InitDocsMixin,
                       InitEnvMixin, InitSetupMixin, InitTestMixin,
                       InitRequirementMixin):

    def _init_template(self, parameter_list):
        raise NotImplementedError

    def _init_packagejson(self):
        raise NotImplementedError

    def init_project(self):
        if self.form.compiler == "cpp":
            if self.form.template == "source":
                if self.with_test:
                    command = "conan new -s -t {self.meta.project_name}/{self.meta.version}@{self.author.author/testing}".format(
                        self=self)
                else:
                    command = "conan new -s {self.meta.project_name}/{self.meta.version}@{self.author.author/testing}".format(
                        self=self)

            elif self.form.template == "header":
                if self.with_test:
                    command = "conan new -i -t {self.meta.project_name}/{self.meta.version}@{self.author.author/testing}".format(
                        self=self)
                else:
                    command = "conan new -i {self.meta.project_name}/{self.meta.version}@{self.author.author/testing}".format(
                        self=self)

            subprocess.call(command, shell=True)
            if self.with_docs:
                self._init_docs()

            self._init_requirements()
        elif self.form.compiler == "node":
            if self.form.project_type == "vue":
                pass
            elif self.form.project_type == "frontend":
                pass

            else:
                print("unknown project type")

        elif self.form.compiler in ["python", "cython"]:
            pass

        else:
            print("unknown compiler")




__all__ = ["InitProjectMixin"]
