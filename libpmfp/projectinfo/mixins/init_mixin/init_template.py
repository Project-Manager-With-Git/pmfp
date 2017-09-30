class InitTemplateMixin:
    def _init_template(self):
        """初始化模板
        """
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
            else:
                print("unknown template")
                return False
            subprocess.call(command, shell=True)
        elif self.form.compiler == "node":
            if self.form.project_type == "vue":

                with open("package.json") as f:
                    package = json.load(f)
                package.update({"name": self.meta.project_name,
                                "version": self.meta.version,
                                "description": self.desc.description,
                                "author": self.author.author + " <" + self.author.author_email + ">"
                                })
                with open("package.json", "w") as f:
                    json.dump(package, f)
            elif self.form.project_type == "frontend":
                pass
            else:
                print("unknown node project type")
                return False

        elif self.form.compiler in ["python","cython"]:
            pass
        else:
            print("unknown compiler to init the template")
            return False
