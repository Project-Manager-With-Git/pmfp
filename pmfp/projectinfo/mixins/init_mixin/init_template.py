"""初始化模板."""
import shutil
from pathlib import Path
from string import Template


class InitTemplateMixin:
    """初始化模板的混入.

    需要Temp2pyMixin.
    """

    def _change_file_name(self, path):
        if path.is_file():
            with open(str(path), "r", encoding="utf-8") as f:
                content = f.read()
            content = Template(content)
            with open(str(path), "w", encoding="utf-8") as f:
                f.write(
                    content.substitute(
                        project_name=self.meta.project_name
                    )
                )

    def _temp_test(self, path):
        if path.is_dir():
            for child in path.iterdir():
                self._temp_test(child)
        else:
            self._change_file_name(path)
        # if path.is_file():
        #     with open(str(path), "r", encoding="utf-8") as f:
        #         content = f.read()
        #     content = Template(content)
        #     with open(str(path), "w", encoding="utf-8") as f:
        #         f.write(content.substitute(project_name=self.meta.project_name))

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
                        suffix = "." + p.name.split(".")[-2]
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
        test_path = Path("test")
        if test_path.is_dir():
            self._temp_test(test_path)
        self._change_file_name(Path("main.py"))
        print("1234")
        self._change_file_name(Path("Dockerfile"))
