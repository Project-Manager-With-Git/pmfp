import traceback
from .init_docker import InitDockerMixin
from .init_readme import InitReadmeMixin
from .init_docs import InitDocsMixin
from .init_env import InitEnvMixin
from .init_setup import InitSetupMixin
from .init_test import InitTestMixin
from .init_requirements import InitRequirementMixin
from .init_template import InitTemplateMixin


class InitProjectMixin(InitDockerMixin, InitReadmeMixin, InitDocsMixin,
                       InitEnvMixin, InitSetupMixin, InitTestMixin,
                       InitRequirementMixin, InitTemplateMixin):
    """需要InstallMixin,CleanMixin
    """

    def _init_sup(self, install):
        """初始化周边配套
        """
        if self.with_docs:
            self._init_docs()
        if self.with_test:
            self._init_test(install)
        if self.with_dockerfile:
            self._init_docker()
        return True

    def init_project(self, install=False):
        """创建项目
        """
        try:
            self._init_env()
            self._init_setup()
            self._init_readme()
            self._init_template()
            self._init_requirements(install=install)
            if install:
                self._install_python_requirements(record="dev")
                print("#################################################")
                print("dev installed")
                print("#################################################")
            self._init_sup(install=install)
            
        except Exception as e:
            traceback.print_exc()
            print(str(e))
            self.clean(all=True)
            raise e
        else:
            return True


__all__ = ["InitProjectMixin"]
