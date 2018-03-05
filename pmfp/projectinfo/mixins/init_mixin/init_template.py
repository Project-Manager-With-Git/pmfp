"""初始化模板."""
import shutil
from pathlib import Path


class InitTemplateMixin:
    """初始化模板的混入.

    需要Temp2pyMixin.
    """

    def _init_template(self):
        """初始化模板."""
        dir_path = Path(__file__).parent.parent.parent.parent.joinpath(
            "source/templates")
        local_path = Path(".")
        template_path = dir_path.joinpath(self.form.compiler).joinpath(self.form.project_form).joinpath(self.form.template)
        if template_path.exists():
            for p in template_path.iterdir():
                if p.is_dir():
                    if p.name == "__project_name__":
                        shutil.copytree(
                            str(p),
                            str(local_path.joinpath(self.meta.project_name))
                        )
                    else:
                        shutil.copytree(
                            str(p),
                            str(local_path.joinpath(p.name))
                        )
                else:
                    if p.name.startswith("__project_name__"):
                        suffix = "."+p.name.split(".")[-2]
                        shutil.copy(
                            str(p),
                            str(local_path.joinpath(self.meta.project_name + suffix))
                        )

                    else:
                        shutil.copy(
                            str(p),
                            str(local_path.joinpath(p.name))
                        )
        else:
            raise AttributeError("Unsupport template!")
        for i in local_path.iterdir():
            self.temp2py(i.absolute())
