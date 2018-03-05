"""将项目上传至github或者pypi"""
import time
import subprocess
import configparser
from pathlib import Path


class UploadMixin:

    def upload(self, git=None):
        if git or git == [] or git == "":
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
                status = self.meta.status
                timestemp = int(time.time())
                print("push package to {path}".format(path=path))
                subprocess.check_call(["git", "add", "."])
                now_timestamp = time.time()
                time_ = time.ctime(now_timestamp)
                if git == []:
                    msg = ""
                else:
                    msg = "".join(git) + ":"
                subprocess.check_call(
                    ["git", "commit", "-m", "{msg}{time}".format(msg=msg,
                                                                 time=time_)])
                subprocess.check_call("git pull".split(" "))
                subprocess.check_call(["git",
                                       'tag',
                                       '-a',
                                       "{version}-{timestemp}-{status}".format(
                                           version=version,
                                           status=status,
                                           timestemp=timestemp),
                                       '-m',
                                       "'version: {version}-{timestemp}-{status}'".format(
                                           version=version,
                                           status=status,
                                           timestemp=timestemp)])
                subprocess.check_call("git push --tag".split(" "))
                subprocess.check_call("git push".split(" "))
                print("push done")
                return True
        else:
            if self.form.compiler == "python":
                home = Path.home()
                if home.joinpath(".pypirc").exists():
                    path = "pypi"
                    command = "python setup.py sdist upload"
                    subprocess.call(command, shell=True)

                    command = "python setup.py bdist_wheel upload"
                    subprocess.call(command, shell=True)
                    print(
                        "upload package to {path} done!".format(path=path))
                    return True
                else:
                    print("pypi upload should have a .pypirc file in home path")
                    return False

            elif self.form.compiler == "node":
                command = "npm publish"
                subprocess.call(command, shell=True)

            else:
                print("unknown compiler!")
                return False
            subprocess.call(command, shell=True)


__all__ = ["UploadMixin"]
