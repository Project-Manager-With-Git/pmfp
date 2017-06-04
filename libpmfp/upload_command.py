from .utils import has_pypirc, has_pointgit, get_git_url, get_command, read_ppmrc
import subprocess
import copy
import time
from argparse import Namespace


def upload(args: Namespace)->int:
    if args.regist:
        if not has_pypirc():
            print("pypi upload should have a .pypirc file in home path")
            return 0
        else:
            path = args.regist
            _, COMMAND, _, _ = get_command()
            print("regist package to {path}".format(path=path))
            command = copy.copy(COMMAND)
            command += ["setup.py", "register"]
            if args.regist != "pypi":
                command += ["-r", args.regist]
            subprocess.check_call(command)
            print("regist package to {path} done!".format(path=path))
            return 1
    if args.pypi or args.localpypi:
        if not has_pypirc():
            print("pypi upload should have a .pypirc file in home path")
            return 0
        else:
            path = args.localpypi or "pypi"
            _, COMMAND, _, _ = get_command()

            print("upload package to {path}".format(path=path))
            command = copy.copy(COMMAND)
            command += ["setup.py", "sdist", "upload"]
            if args.localpypi:
                command += ["-r", args.localpypi]
            subprocess.check_call(command)
            command = copy.copy(COMMAND)
            command += ["setup.py", "bdist_wheel", "upload"]
            if args.localpypi:
                command += ["-r", args.localpypi]
            subprocess.check_call(command)
            print("upload package to {path} done!".format(path=path))
            return 1
    elif args.git or args.git == []:
        if not has_pointgit():
            print("upload should have a .git dir in root path")
            return 0
        else:
            path = get_git_url()
            version = read_ppmrc()["project"]["version"]
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
            return 1
