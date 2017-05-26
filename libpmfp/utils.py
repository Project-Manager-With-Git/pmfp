import platform
import re
from pathlib import Path
import configparser
import shutil
import os

def get_git_url():
    pointgit = Path(".git")
    gitconfig = pointgit.joinpath('config')
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read(str(gitconfig))
    return parser['remote "origin"']['url']


def has_pypirc():
    home = Path.home()
    if home.joinpath(".pypirc").exists():
        return True
    else:
        return False
def has_pointgit():
    here = Path(".").absolute()
    if here.joinpath(".git").exists():
        return True
    else:
        return False



def clean_init():
    print("clean init")
    path = Path(".").absolute()
    for i in path.iterdir():
        if i.is_dir():
            shutil.rmtree(str(i))
        else:
            os.remove(str(i))
    print("clean init done!")


def is_inited():
    path = Path(".ppmrc")
    return path.exists()


def project_form():
    return read_ppmrc()["form"]['form']


def read_ppmrc():
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read('.ppmrc')
    return parser


def write_ppmrc(pyrc_dict):
    print(pyrc_dict)
    print("write .ppmrc")
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read_dict(pyrc_dict)
    with open(".ppmrc", "w") as f:
        parser.write(f)
    print("write .ppmrc done!")
    return True


def find_package_name():
    parser = read_ppmrc()
    name = parser["project"]['project_name']
    return name


def find_package_form():
    parser = read_ppmrc()
    name = parser["form"]['form']
    return name


def get_command():
    if platform.system() == 'Windows':
        PYTHON = 'python'
        p = Path(".\env")
        if p.exists():
            COMMAND = ['env\Scripts\python']
            sphinx_apidoc = ['env\Scripts\sphinx-apidoc']
            make = ['env\Scripts\sphinx-build']
        else:
            COMMAND = [PYTHON]
            sphinx_apidoc = ['sphinx-apidoc']
            make = ['sphinx-build']
    else:
        PYTHON = 'python3'
        p = Path("./env")
        if p.exists():
            COMMAND = ['env/bin/python']
            sphinx_apidoc = ['env/bin/sphinx-apidoc']
            make = ['env/bin/sphinx-build']
        else:
            COMMAND = [PYTHON]
            sphinx_apidoc = ['sphinx-apidoc']
            make = ['sphinx-build']
    return PYTHON, COMMAND, sphinx_apidoc, make
