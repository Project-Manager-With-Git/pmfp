from .init_docker import InitDockerMixin
from .init_readme import InitReadmeMixin
from .init_docs import InitDocsMixin
from .init_env import InitEnvMixin
from .init_setup import InitSetupMixin
from .init_test import InitTestMixin
from ._init_requirements import InitRequirementMixin


class InitProjectMixin(InitDockerMixin, InitReadmeMixin, InitDocsMixin,
                       InitEnvMixin, InitSetupMixin, InitTestMixin,
                       InitRequirementMixin):


    def _init_template(self, parameter_list):
        raise NotImplementedError



    def _init_packagejson(self):
        raise NotImplementedError


    def init_project(self):
        if self.form.com.compiler == "cpp":
            
