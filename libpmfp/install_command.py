import subprocess
import copy
from .utils import get_command, is_conda
from typing import List
PYTHON, COMMAND, sphinx_apidoc, make = get_command()

from argparse import Namespace


def pip_install_requirement(env: str="")->int:
    if env:
        env = "_" + env
    command = copy.copy(COMMAND)
    command += ["-m", "pip", "install", "-r",
                "requirements/requirements" + env + ".txt"]
    subprocess.check_call(command)
    print("pip install requirements" + env + ".txt")
    return 1


def pip_install(packages: List[str])->int:
    if is_conda():
        subprocess.check_call(
            ["conda", "install", "-y", "-p", "env"] + packages)
        print("conda installed " + " ".join(packages))
    else:
        command = copy.copy(COMMAND)
        command += ["-m", "pip", "install"]
        command += packages
        subprocess.check_call(command)
        print("pip installed " + " ".join(packages))
    return 1


def write_requirement(package: List[str], env: str="")->int:
    if env:
        env = "_" + env
    exit_ = True
    with open("requirements/requirements" + env + ".txt", "r") as f:
        for i in f:
            if i.split(" ")[0] == package[-1]:
                break
        else:
            exit_ = False
    if exit_:
        print("package exist")
        return 0

    with open("requirements/requirements" + env + ".txt", "a") as f:
        i = package[0]  # " ".join(package)
        if i.split(".")[-1] == "whl":
            i = i.split("-")[0]
        f.write(i + "\n")
    print("updated requirements" + env + ".txt")
    return 1


def install(args: Namespace)->int:
    if args.self:
        print("install self to local")
        python = COMMAND[0]
        subprocess.check_call(
            "{PYTHON} setup.py install".format(PYTHON=python).split(" "))
        #subprocess.check_call("{PYTHON} setup.py install".split(" "))
        return 0
    else:
        if args.dev or args.dev == []:
            print("args.dev")
            if args.dev == []:
                pip_install_requirement("dev")
            else:
                pip_install(args.dev)
                write_requirement(args.dev, "dev")
        elif args.test or args.test == []:
            print('args.test')
            if args.test == []:
                pip_install_requirement("test")
            else:
                pip_install(args.test)
                write_requirement(args.test, "test")
        elif args.requirements or args.requirements == []:
            print('args.requirements')
            if args.test == []:
                pip_install_requirement()
            else:
                print(args.requirements)
                pip_install(args.requirements)
                write_requirement(args.requirements, "")
        return 1
