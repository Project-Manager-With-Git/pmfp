"""将项目上传至github或者pypi."""
import time
import subprocess
import configparser
from pathlib import Path


class UploadMixin:
    """上传项目至git或者pypi服务器上."""

    def git_upload(self, git):
        """将项目上传至git仓库."""
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
                ["git",
                 "commit",
                 "-m",
                 "{msg}{time}".format(msg=msg, time=time_)]
            )
            subprocess.check_call("git pull".split(" "))
            subprocess.check_call(
                ["git",
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
                     timestemp=timestemp
                 )]
            )
            subprocess.check_call("git push --tag".split(" "))
            subprocess.check_call("git push".split(" "))
            print("push done")

    def _python_upload(self):
        home = Path.home()
        if home.joinpath(".pypirc").exists():
            command = "python setup.py sdist upload"
            subprocess.call(command, shell=True)
            command = "python setup.py bdist_wheel upload"
            subprocess.call(command, shell=True)
            print("upload package to done!")
        else:
            raise AttributeError("pypi upload should have a .pypirc file in home path")

    def _node_upload(self):
        command = "npm publish"
        subprocess.call(command, shell=True)

    def upload(self):
        """上传数据至各语言的官方包管理服务器,支持python和node."""
        if self.form.compiler == "python":
            self._python_upload()
        elif self.form.compiler == "node":
            self._node_upload()
        else:
            raise AttributeError("unknown compiler!")


__all__ = ["UploadMixin"]
