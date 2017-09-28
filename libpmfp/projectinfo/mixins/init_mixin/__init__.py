from .init_docker import InitDockerMixin
from .init_readme import InitReadmeMixin
from .init_docs import InitDocsMixin
from .init_env import InitEnvMixin
from .init_setup import InitSetupMixin


class InitProjectMixin(InitDockerMixin, InitReadmeMixin, InitDocsMixin,
                       InitEnvMixin, InitSetupMixin):

    def _init_test(self, parameter_list):
        raise NotImplementedError

    def _init_template(self, parameter_list):
        raise NotImplementedError

    def _init_requirement(self):
        pass

    def _init_packagejson(self):
        pass

    def _init_makefile(self):
        pass

    def init_project(self):
        pass
