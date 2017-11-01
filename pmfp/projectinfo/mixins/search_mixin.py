import subprocess


class SearchMixin:
    def search(self, package):
        if self.form.compiler in ["cython", "python"]:
            if self.form.env == "conda":
                command = "conda search {package}".format(package=package)
            else:
                command = "pip search {package}".format(package=package)
            subprocess.call(command, shell=True)
            return True
        elif self.form.compiler == "cpp":
            command = "conan search {package} -r conan-transit".format(
                package=package)
            subprocess.call(command, shell=True)
            return True
        elif self.form.compiler == "node":
            # 注意要先将es6或者typescript 编译为node可运行的代码

            command = "npm search {package}".format(package=package)
            subprocess.call(command, shell=True)
        else:
            print("unknown compiler!")
            return False


__all__ = ["SearchMixin"]
