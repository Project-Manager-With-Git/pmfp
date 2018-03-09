"""项目初始化使用的mixin汇总."""
import traceback
from .init_readme import InitReadmeMixin
from .init_env import InitEnvMixin
from .init_template import InitTemplateMixin
from .init_dev_requirements import InitDevRequirementMixin


class InitProjectMixin(InitReadmeMixin, InitEnvMixin, InitTemplateMixin, InitDevRequirementMixin):
    """项目初始化使用的mixin汇总.

    需要CleanMixin.会执行步骤:`初始化env->初始化模板->初始化readme`
    """

    def init_project(self):
        """创建项目."""
        try:
            self._init_template()
            if self.form.compiler in ("python", 'node'):
                self._init_env()
            self._init_readme()

        except Exception as e:
            traceback.print_exc()
            print(str(e))
            self.clean(total=True)
            raise e
        else:
            return True


__all__ = ["InitProjectMixin"]
