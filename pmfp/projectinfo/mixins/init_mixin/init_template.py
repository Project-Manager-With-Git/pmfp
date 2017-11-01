import shutil
import json
import subprocess
from pathlib import Path


class InitTemplateMixin:
    """需要Temp2pyMixin
    """

    def _init_template_python(self):
        dir_path = Path(__file__).parent.parent.parent.parent.joinpath("source/templates")
        local_path = Path(".")
        if self.form.project_type == "script":
            form_str = self.form.compiler + "_" + self.form.project_type + \
                "_" + self.form.template + ".py.temp"
            shutil.copy(str(dir_path.joinpath(form_str)), str(
                local_path.joinpath(self.meta.project_name + ".py")))

        elif self.form.project_type == "gui":
            if self.form.template in ["tk"]:
                form_str = self.form.compiler + "_" + self.form.project_type + \
                    "_" + self.form.template + ".py.temp"
                shutil.copy(str(dir_path.joinpath(form_str)), str(
                    local_path.joinpath(self.meta.project_name + ".py")))
            else:
                form_str = self.form.compiler + "_" + \
                    self.form.project_type + "_" + self.form.template
                shutil.copytree(str(dir_path.joinpath(form_str)), str(
                    local_path.joinpath(self.meta.project_name)))
                self.temp2py(local_path.joinpath(self.meta.project_name))

        elif self.form.project_type == "web":
            if self.form.template in ["flask", "sanic"]:
                form_str = self.form.compiler + "_" + self.form.project_type + \
                    "_" + self.form.template + ".py.temp"
                shutil.copy(str(dir_path.joinpath(form_str)), str(
                    local_path.joinpath(self.meta.project_name + ".py")))
            else:
                form_str = self.form.compiler + "_" + \
                    self.form.project_type + "_" + self.form.template
                shutil.copytree(str(dir_path.joinpath(form_str)), str(
                    local_path.joinpath(self.meta.project_name)))
                self.temp2py(local_path.joinpath(self.meta.project_name))
        else:
            form_str = self.form.compiler + "_" + \
                self.form.project_type + "_" + self.form.template
            shutil.copytree(str(dir_path.joinpath(form_str)), str(
                local_path.joinpath(self.meta.project_name)))
            self.temp2py(local_path.joinpath(self.meta.project_name))
            if self.form.project_type == "command":
                self._init_main()

    def _init_template_node(self):
        dir_path = Path(__file__).parent.parent.parent.parent.joinpath(
            "source/templates")
        local_path = Path(".")

        form_str = self.form.compiler + "_" + \
            self.form.project_type + "_" + self.form.template
        if dir_path.joinpath(form_str).exists():
            for p in dir_path.joinpath(form_str).iterdir():
                if p.is_dir():
                    shutil.copytree(str(p), str(local_path.joinpath(p.name)))
                else:
                    shutil.copy(str(p), str(local_path.joinpath(p.name)))
            with open("package.json") as f:
                package = json.load(f)
            package.update({"name": self.meta.project_name,
                            "version": self.meta.version,
                            "description": self.desc.description,
                            "author": self.author.author + " <" + self.author.author_email + ">"
                            })
            with open("package.json", "w") as f:
                json.dump(package, f)
            return True
        else:
            print("unknown template")
            return False

    # def _init_template_cpp(self):
    #     if self.form.template == "source":
    #         if self.with_test:
    #             command = "conan new -s -t {self.meta.project_name}/{self.meta.version}@{self.author.author}/{self.meta.status}".format(
    #                 self=self)
    #         else:
    #             command = "conan new -s {self.meta.project_name}/{self.meta.version}@{self.author.author}/{self.meta.status}".format(
    #                 self=self)

    #     elif self.form.template == "header":
    #         if self.with_test:
    #             command = "conan new -i -t {self.meta.project_name}/{self.meta.version}@{self.author.author}/{self.meta.status}".format(
    #                 self=self)
    #         else:
    #             command = "conan new -i {self.meta.project_name}/{self.meta.version}@{self.author.author}/{self.meta.status}".format(
    #                 self=self)
    #     else:
    #         print("unknown template")
    #         return False
    #     subprocess.call(command, shell=True)
    #     return True

    def _init_template(self):
        """初始化模板
        """
        dir_path = Path(__file__).parent.parent.parent.parent.joinpath(
            "source/templates")
        local_path = Path(".")

        # if self.form.compiler == "cpp":
        #     self._init_template_cpp()

        if self.form.compiler == "node":
            self._init_template_node()

        elif self.form.compiler in ["python", "cython"]:
            self._init_template_python()

        else:
            print("unknown compiler to init the template")
            return False
