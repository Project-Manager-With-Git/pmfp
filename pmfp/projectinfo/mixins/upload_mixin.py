"""将项目上传至github或者pypi."""
import time
import subprocess
import configparser
from pathlib import Path
from typing import Dict,List


class UploadMixin:
    """上传项目至git或者pypi服务器上."""

    def _git_check(self)->bool:
        """检测项目有没有.git可以用于上传和打标签等操作."""
        here = Path(".").absolute()
        if not here.joinpath(".git").exists():
            return False
        else:
            return True

    def _git_check_and_find_remote(self)->str:
        """从项目的.git中找到远端仓库url."""
        if not self._git_check():
            raise AttributeError("upload to git should have a .git dir in root path")
        else:
            pointgit = Path(".git")
            gitconfig = pointgit.joinpath('config')
            parser = configparser.ConfigParser(allow_no_value=True)
            parser.read(str(gitconfig))
            path = parser['remote "origin"']['url']
            return path

    def git_tag(self):
        """为项目打标签."""
        remote = self._git_check_and_find_remote()
        version = self.meta.version
        status = self.meta.status
        tag = "{status}-{version}".format(version=version, status=status)
        subprocess.check_call(
            ["git",
             'tag',
             '-a',
             tag,
             '-m',
             "'version: " + tag]
        )
        subprocess.check_call("git push --tag".split(" "))
        print("push tag {tag} for package to {remote} done".format(remote=remote, tag=tag))

    def git_push(self, git: List[str]):
        """对项目推代码."""
        remote = self._git_check_and_find_remote()
        version = self.meta.version
        status = self.meta.status
        timestemp = int(time.time())
        subprocess.check_call(["git", "add", "."])
        now_timestamp = time.time()
        time_ = time.ctime(now_timestamp)
        if git == []:
            msg = ""
        else:
            msg = "".join(git)
        subprocess.check_call(
            ["git",
             "commit",
             "-m",
             "{msg}@{time}".format(msg=msg, time=time_)]
        )
        subprocess.check_call("git pull".split(" "))
        subprocess.check_call("git push".split(" "))
        print("push code to {remote} done".format(remote=remote))

    def git_upload(self, git: List[str], tag: bool):
        """将代码上传至远端git仓库."""
        self.git_push(git)
        if tag:
            self.git_tag()

    def git_upload_bak(self, git):
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
