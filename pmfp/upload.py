import time
import subprocess
import configparser
from pmfp.const import PROJECT_HOME


def _git_check()->bool:
    """检测项目有没有.git可以用于上传和打标签等操作."""
    if not PROJECT_HOME.joinpath(".git").exists():
        return False
    else:
        return True


def _git_check_and_find_remote()->str:
    """从项目的.git中找到远端仓库url."""
    if not _git_check():
        raise AttributeError("upload to git should have a .git dir in root path")
    else:
        pointgit = PROJECT_HOME.joinpath(".git")
        gitconfig = pointgit.joinpath('config')
        parser = configparser.ConfigParser(allow_no_value=True)
        parser.read(str(gitconfig))
        path = parser['remote "origin"']['url']
        return path


def git_tag(config):
    """为项目打标签."""
    remote = _git_check_and_find_remote()
    version = config["version"]
    status = config["status"]
    tag = "{status}-{version}".format(version=version, status=status)
    command = f"git tag -a {tag} -m 'version: {tag}'"
    subprocess.check_call(command, shell=True)
    command = f"git push --tag"
    subprocess.check_call(command, shell=True)
    print(f"push tag {tag} for package to {remote} done")


def git_push(config, msg: str=None):
    """对项目推代码."""
    remote = _git_check_and_find_remote()
    version = config["version"]
    status = config["status"]
    timestemp = int(time.time())
    command = "git add ."
    subprocess.check_call(command, shell=True)
    now_timestamp = time.time()
    time_ = time.ctime(now_timestamp)
    command = f'git commit -m "{msg}@{time}"'
    subprocess.check_call(command, shell=True)

    command = "git pull"
    subprocess.check_call(command, shell=True)
    command = "git push"
    subprocess.check_call(command, shell=True)
    print(f"push code to {remote} done")


def upload(config, kwargs):
    """将代码上传至远端git仓库."""
    msg = kwargs.get("msg")
    tag = kwargs.get("tag")
    git_push(config, msg)
    if tag:
        git_tag(config)
