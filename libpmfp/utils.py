import platform
import re
from pathlib import Path
import configparser
import shutil
import os

from typing import Dict, Tuple, List, Any


def get_git_url()->str:
    pointgit = Path(".git")
    gitconfig = pointgit.joinpath('config')
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read(str(gitconfig))
    return parser['remote "origin"']['url']


def has_pypirc()->bool:
    home = Path.home()
    if home.joinpath(".pypirc").exists():
        return True
    else:
        return False


def has_pointgit()->bool:
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


def is_inited()->bool:
    path = Path(".ppmrc")
    return path.exists()


def project_form()->str:
    return read_ppmrc()["form"]['form']


def read_ppmrc()->configparser.ConfigParser:
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read('.ppmrc')
    return parser


def write_ppmrc(pyrc_dict: Dict[str, Dict[str, Any]])->bool:
    print(pyrc_dict)
    print("write .ppmrc")
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read_dict(pyrc_dict)
    with open(".ppmrc", "w") as f:
        parser.write(f)
    print("write .ppmrc done!")
    return True


def is_conda()->bool:
    parser = read_ppmrc()
    return parser["env"]['env'] == "conda"


def find_package_name()->str:
    parser = read_ppmrc()
    name = parser["project"]['project_name']
    return name


def find_package_form()->str:
    parser = read_ppmrc()
    name = parser["form"]['form']
    return name


def get_command()->Tuple[str, List[str], List[str], List[str]]:
    if platform.system() == 'Windows':
        PYTHON = 'python'
        p = Path(".\env")
        if p.exists():
            if is_conda():
                COMMAND = ['env\python']
            else:
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
