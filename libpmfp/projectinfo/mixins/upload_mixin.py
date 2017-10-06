import time
import subprocess
from pathlib import Path


class UploadMixin:

    def upload(self, remote=False):
        if argv.git or args.git == []:
            here = Path(".").absolute()
            if not here.joinpath(".git").exists():
                print("upload to git should have a .git dir in root path")
                return False
            else:
                pointgit = Path(".git")
                gitconfig = pointgit.joinpath('config')
                parser = configparser.ConfigParser(allow_no_value=True)
                parser.read(str(gitconfig))
                path = parser['remote "origin"']['url']
                version = self.meta.version
                print("push package to {path}".format(path=path))
                subprocess.check_call(["git", "add", "."])
                now_timestamp = time.time()
                time_ = time.ctime(now_timestamp)
                if args.git == []:
                    msg = ""
                else:
                    msg = "".join(args.git) + ":"
                subprocess.check_call(
                    ["git", "commit", "-m", "{msg}{time}".format(msg=msg, time=time_)])
                subprocess.check_call("git pull".split(" "))
                subprocess.check_call(["git", 'tag', '-a', "{version}".format(
                    version=version), '-m', "'version {version}'".format(
                    version=version)])
                subprocess.check_call("git push --tag".split(" "))
                subprocess.check_call("git push".split(" "))
                print("push done")
                return True
        else:
            if self.form.compiler in ["cython", "python"]:
                home = Path.home()
                if not home.joinpath(".pypirc").exists():
                    print("pypi upload should have a .pypirc file in home path")
                    return False
                else:
                    if remote:
                        path = self.form.upload_remote
                        command = "python setup.py sdist upload -r {self.form.upload_remote}".format(
                            self=self)
                        subprocess.call(command, shell=True)

                        command = "python setup.py bdist_wheel upload -r {self.form.upload_remote}".format(
                            self=self)
                        subprocess.call(command, shell=True)

                    else:
                        path = "pypi"
                        command = "python setup.py sdist upload"
                        subprocess.call(command, shell=True)

                        command = "python setup.py bdist_wheel upload"
                        subprocess.call(command, shell=True)

                    print("upload package to {path} done!".format(path=path))
                    return True

            elif self.form.compiler == "cpp":
                if remote:
                    command = "conan upload {self.meta.project_name}/{self.meta.version}@{self.author.author}/{self.meta.status} --all -r {self.form.upload_remote}".format(
                        self=self)
                else:
                    command = "conan upload {self.meta.project_name}/{self.meta.version}@{self.author.author}/{self.meta.status} --all -r conan-transit".format(
                        self=self)
                subprocess.call(command, shell=True)

            elif self.form.compiler == "js":
                if remote:
                    command = "npm publish --registry {self.form.upload_remote}".formmat(
                        self=self)
                else:
                    command = "npm publish"
                subprocess.call(command, shell=True)

            else:
                print("unknown compiler!")
                return False
            subprocess.call(command, shell=True)


__all__ = ["UploadMixin"]
