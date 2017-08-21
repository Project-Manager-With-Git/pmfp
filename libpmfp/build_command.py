from .utils import find_package_form, get_command, find_package_name,project_compiler
import subprocess
import copy
import shutil
from pathlib import Path

from argparse import Namespace


def build(args: Namespace)->int:
    print(type(args))
    _, COMMAND, _, _ = get_command()
    form = find_package_form()
    name = find_package_name()
    if form in ["gui"]:
        print('build app to pyz file')
        command0 = copy.copy(COMMAND)
        command0 += ["-m", "zipapp", name, '-m',
                     "main:main", "-p", "/usr/bin/env python3"]
        subprocess.check_call(command0)
        print('build app to pyz file done!')
        return 1
    elif form in ["web"]:
        print('move template and static files')
        here = Path(".").absolute()
        static = here.joinpath(name).joinpath("static")
        templates = here.joinpath(name).joinpath("templates")
        dir_static = here.joinpath("static")
        dir_templates = here.joinpath("templates")
        if static.exists():
            shutil.copytree(str(static),
                            str(dir_static))
            print("move static files done!")
            shutil.rmtree(str(static))
            print("remove original static files done!")
        if templates.exists():
            shutil.copytree(str(templates),
                            str(dir_templates))
            print("move template files done!")
            shutil.rmtree(str(templates))
            print("remove original templates files done!")

        print('move template and static files done!')
        print('build app to pyz file')
        command0 = copy.copy(COMMAND)
        command0 += ["-m", "zipapp", name, '-m',
                     "main:main", "-p", "/usr/bin/env python3"]
        subprocess.check_call(command0)
        print('build app to pyz file done!')

        if args.docker:
            print('build app to docker img')
            command = ["docker", "build","-t",name, "." ]
            try:
                subprocess.check_call(command)
            except Exception as e:
                print("error:",str(e))
            else:
                print('build app to docker img done!')
            
        if dir_static.exists():
            shutil.copytree(str(dir_static),
                            str(static))
            print("move static files done!")

        if dir_templates.exists():
            shutil.copytree(str(dir_templates),
                            str(templates))
            print("move template files done!")
        return 1

    elif form in ["command"]:
        if args.egg:
            print('build model to egg file')
            command0 = copy.copy(COMMAND)
            command0 += ["setup.py", 'bdist_egg']
            subprocess.check_call(command0)
            print('build model to egg file done!')

        if args.wheel:
            print('build model to wheel file')
            command0 = copy.copy(COMMAND)
            command0 += ["setup.py", "bdist_wheel"]
            subprocess.check_call(command0)
            print('build model to wheel file done!')

        if not any([args.egg, args.wheel]):
            print('build app to pyz file')
            command0 = copy.copy(COMMAND)
            command0 += ["-m", "zipapp", "lib" + name, '-m', "main:main",
                         "-p", "/usr/bin/env python3", "-o", name + ".pyz"]
            subprocess.check_call(command0)
            print('build app to pyz file done!')
        return 1
    elif form in ["model"]:
        if project_compiler() == "python":
            print('build model to wheel file')
            command0 = copy.copy(COMMAND)
            command0 += ["setup.py", "bdist_wheel"]
            subprocess.check_call(command0)
            print('build model to wheel file done!')
            if args.egg:
                print('build model to egg file')
                command0 = copy.copy(COMMAND)
                command0 += ["setup.py", 'bdist_egg']
                subprocess.check_call(command0)
                print('build model to egg file done!')
        elif project_compiler() == "cython":
            print('build cython model')
            command0 = copy.copy(COMMAND)
            command0 += ["setup.py",'build_ext','--inplace']
            subprocess.check_call(command0)
            print('build cython model done!')

        return 1

    elif form in ["script"]:
        print("script do not need to build")
        return 0

    else:
        print("unkown form")
        return 0
