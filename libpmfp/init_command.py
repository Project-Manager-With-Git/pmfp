from pathlib import Path
from string import Template
import shutil
from .utils import get_command, write_ppmrc, is_inited, clean_init, is_conda
from .Data import SETUPPY, COMMAND_MAIN, CONF, READMERST, PACKAGEJSON, SCRIPT, MANIFEST
from .install_command import pip_install, write_requirement
import subprocess
import sys
import copy
import platform
import getpass
from argparse import Namespace
from typing import Dict,Tuple

file_path = Path(__file__).absolute()
dir_path = file_path.parent
local_path = Path(".").absolute()


def init_manifest(project_name: str)->int:
    print('create MANIFEST.in')
    with open("MANIFEST.in", "w") as f:
        f.write(MANIFEST.substitute(
            project_name=project_name))
    print('create MANIFEST.in done!')
    return 1


def create_env()->int:
    print('creating env')
    PYTHON, _, _, _ = get_command()
    command = [PYTHON, '-m', 'venv', 'env']
    subprocess.check_call(command)
    print('creating env done!')
    return 1


def create_conda_env()->int:
    print('creating conda env')
    command = ["conda", 'create', "-p", 'env', "python=" +
               str(sys.version_info[0]) + "." + str(sys.version_info[1])]
    subprocess.check_call(command)
    print('creating conda env done!')
    return 1


def install_math()->int:
    print("install math libs")
    pip_install(["mkl"])
    write_requirement(["mkl"])
    pip_install(["numpy"])
    write_requirement(["numpy"])

    if platform.system() == 'Windows' and (not is_conda()):
        print("""windoescan not install scipy and sklearn through pip,
              please go to http://www.lfd.uci.edu/~gohlke/pythonlibs
              and download the packages you need,then install""")
        return 0
    else:
        pip_install(["scipy"])
        write_requirement(["scipy"])
        pip_install(["scikit-learn"])
        write_requirement(["scikit-learn"])
    print("install math libs done!")
    return 1

def input_info()->Tuple[str, str, str, str, str, str, str, str]:
    while True:
        project_name = input("project name:")
        if project_name in ["app"]:
            print("{project_name} can not use as a project name".format(
                project_name=project_name))
        else:
            break
    author = input("author:")
    author_email = input("author_email:")
    license_ = input("license:")
    keywords = input("keywords,split by ',':")
    version = input("project version:")
    description = input("description:")
    url = input("url:")
    if keywords:
        keywords = [i for i in keywords.split(',')]
    else:
        keywords = []
    project_name = project_name or local_path.name
    author = author or getpass.getuser()
    author_email = author_email or "author_email"
    here = Path(".").absolute()
    license_path = here.joinpath("LICENSE")
    if license_path.exists():
        with license_path.open("r") as f:
            i = next(f)
        license_def = i.split(" ")[0]
    else:
        license_def = "MIT"
    license_ = license_ or license_def
    keywords = keywords or "'tools'"
    version = version or "0.0.1"
    description = description or "simple tools"
    url = url or ""
    return project_name, author, author_email, license_, keywords, version, description, url


def init_test()->int:
    print("copy test template")
    if local_path.joinpath("test").exists():
        print(str(local_path.joinpath("test")) + " exists")
    else:
        shutil.copytree(str(dir_path.joinpath("test")),
                        str(local_path.joinpath("test")))
    print("copy test template done!")
    return 1


def init_doc(args, project_name: str, author: str, version: str, ky: str)->int:
    if args.script:
        return 0
    _, _, auto_api, _ = get_command()
    KY = {
        "commamd": ("sys.path.insert(0, str(p.parent.parent))",
                    "'sphinx.ext.autodoc'"),
        "gui": ("sys.path.insert(0, str(p.parent.parent.joinpath('{project_name}')))".format(
            project_name=project_name),
            "'sphinx.ext.autodoc'"),
        "web": ("", "'sphinxcontrib.httpdomain'"),
        "zerorpc": ("sys.path.insert(0, str(p.parent.parent.joinpath('{project_name}')))".format(
            project_name=project_name),
            "'sphinx.ext.autodoc'"),
        "flask": ("", "'sphinxcontrib.httpdomain','sphinxcontrib.autohttp.flask','sphinxcontrib.autohttp.flaskqref'")
    }
    print('building apidoc')
    path = Path("apidoc")
    if path.exists():
        print("apidoc exists")
    else:
        command3 = copy.copy(auto_api)
        if args.command:
            project_name1 = "lib" + project_name
        else:
            project_name1 = project_name

        command3 += ["-F", "-H", project_name1, '-A', author,
                     '-V', version, "-a", '-o', 'apidoc', project_name1]
        subprocess.check_call(command3)
        with open("apidoc/conf.py", "w") as f:
            print(project_name1)
            f.write(CONF.substitute(
                project_name=project_name,
                author=author,
                version=version,
                ky0=KY.get(
                    ky, ("sys.path.insert(0, str(p.parent.parent))", "'sphinx.ext.autodoc'"))[0],
                ky1=KY.get(
                    ky, ("sys.path.insert(0, str(p.parent.parent))", "'sphinx.ext.autodoc'"))[1]
            ))
    print('building apidoc done')
    return 1


def init_install()->int:
    _, command, _, _ = get_command()
    # print('update pip')
    # command0 = copy.copy(command)
    # command0 += ["-m", "pip", "install", "--upgrade", "pip"]
    # subprocess.check_call(command0)
    # print('update pip done')
    # print('update setuptools')
    # command0 = copy.copy(command)
    # command0 += ["-m", "pip", "install", "setuptools", "--upgrade"]
    # subprocess.check_call(command0)
    # print('update setuptools done!')
    print('install wheel')
    command0 = copy.copy(command)
    command0 += ["-m", "pip", "install", "wheel"]
    subprocess.check_call(command0)
    print('install wheel done!')

    print("install requirements")
    command1 = copy.copy(command)
    command1 += ["-m", "pip", "install", "-r",
                 "requirements/requirements_dev.txt"]
    command2 = copy.copy(command)
    command2 += ["-m", "pip", "install", "-r",
                 "requirements/requirements_test.txt"]

    command3 = copy.copy(command)
    command3 += ["-m", "pip", "install", "-r", "requirements/requirements.txt"]
    subprocess.check_call(command1)
    subprocess.check_call(command2)
    subprocess.check_call(command3)
    print("install requirements done!")
    return 1


def init_ppmrc(rc: Dict[str, str], ky: str, conda: bool=False)->int:
    if local_path.joinpath(".ppmrc").exists():
        print("already inited")
    else:
        rccontent = copy.copy(rc)
        rccontent.update(form={'form': ky})
        if conda:
            rccontent.update(env={'env': "conda"})
        else:
            rccontent.update(env={'env': "venv"})
        write_ppmrc(rccontent)

    return 1


def init_readme(project_name: str, author: str, author_email: str, version: str, url: str)->int:
    print("writing readme.")
    if local_path.joinpath("README.rst").exists():
        print("already have README.rst")
    else:
        with open("README.rst", "w") as f:
            f.write(READMERST.substitute(project_name=project_name,
                                         author=author,
                                         author_email=author_email,
                                         version=version,
                                         url=url))
    print("writing readme done")
    return 1


def init_setuppy(project_name: str,
                 author: str,
                 author_email: str,
                 license_: str,
                 keywords: str,
                 version: str,
                 description: str,
                 url: str,
                 entry_points: str="")->int:
    setup = SETUPPY.substitute(project_name=project_name,
                               author=author,
                               author_email=author_email,
                               license_=license_,
                               keywords=keywords,
                               version=version,
                               description=description,
                               url=url,
                               entry_points=entry_points
                               )
    print("writing setup.py")
    if local_path.joinpath("setup.py").exists():
        print("already have setup.py")
    else:
        with open("setup.py", "w") as f:
            f.write(setup)
    print("writing setup.py done!")
    return 1


def init_requirements(ky: str="")->int:
    print("copy requirements template")
    if local_path.joinpath("requirements").exists():
        print(str(local_path.joinpath("requirements")) + " exists")
    else:
        shutil.copytree(str(dir_path.joinpath("requirements" + ky)),
                        str(local_path.joinpath("requirements")))
    print("copy requirements template done!")
    return 1


def init_app(project_name: str, ky: str="model")->int:
    if ky == 'model':
        print("copy model template")
        if local_path.joinpath(project_name).exists():
            print(str(local_path.joinpath(project_name)) + " exists")
        else:
            shutil.copytree(str(dir_path.joinpath("model")),
                            str(local_path.joinpath(project_name)))
        print("copy model template done!")

    elif ky == "script":
        print("copy model template")
        if local_path.joinpath(project_name + ".py").exists():
            print(str(local_path.joinpath(project_name + ".py")) + " exists")
        else:
            with open(project_name + ".py", "w") as f:
                f.write(SCRIPT)

        print("copy model template done!")

    elif ky == "command":
        print("copy command template")
        if local_path.joinpath(project_name + ".py").exists():
            print(str(local_path.joinpath(project_name + ".py")) + " exists")
        else:
            print(str(local_path.joinpath(project_name + ".py")) + " init")
            with open(project_name + ".py", "w") as f:
                f.write(COMMAND_MAIN.format(project_name='lib' + project_name))
            print(str(local_path.joinpath(project_name + ".py")) + " init done!")
        if local_path.joinpath("lib" + project_name).exists():
            print(str(local_path.joinpath("lib" + project_name)) + " exists")
        else:
            shutil.copytree(str(dir_path.joinpath("commandapp")), str(
                local_path.joinpath("lib" + project_name)))
        print("copy command template")

    else:
        print("copy {ky} template".format(ky=ky))
        if local_path.joinpath(project_name).exists():
            print(str(local_path.joinpath(project_name)) + " exists")
        else:
            shutil.copytree(str(dir_path.joinpath("{ky}app".format(ky=ky))), str(
                local_path.joinpath(project_name)))
        print("copy {ky} template done!".format(ky=ky))

    return 1


def init_packagejson(project_name: str, version: str, description: str, author: str, license_: str)->int:

    print("writing package.json")
    if local_path.joinpath("package.json").exists():
        print("already have package.json")
        return 0
    else:
        package = PACKAGEJSON.substitute(
            project_name=project_name,
            version=version,
            description=description,
            author=author,
            license_=license_)
        with open("package.json", "w") as f:
            f.write(package)
    print("writing  package.json done!")
    return 1


def init(args: Namespace)->int:
    if is_inited():
        print("already inited")
        python, command, _, _ = get_command()
        comd = input("use virtual env?enter y to install\n")
        if comd in ["y", "Y"]:
            if is_conda():
                create_conda_env()
            else:
                create_env()
        comd = input("install the requirements?enter y to install\n")
        if comd in ["y", "Y"]:
            command1 = copy.copy(command)
            command1 += ["-m", "pip", "install",
                         "-r", "requirements/requirements.txt"]
            subprocess.check_call(command1)
        comd = input("install the test requirements?enter y to install\n")
        if comd in ["y", "Y"]:
            command1 = copy.copy(command)
            command1 += ["-m", "pip", "install", "-r",
                         "requirements/requirements_test.txt"]
            subprocess.check_call(command1)
        comd = input("install the dev requirements?enter y to install\n")
        if comd in ["y", "Y"]:
            command1 = copy.copy(command)
            command1 += ["-m", "pip", "install", "-r",
                         "requirements/requirements_dev.txt"]
            subprocess.check_call(command1)
        sys.exit(0)
        return 0

    try:
        # if args.git:
        #     giturl = args.git
        #     init_git(giturl)

        project_name, author, author_email, license_, keywords, version, description, url = input_info()
        rc = {
            "project": {
                'project_name': project_name,
                'license': license_,
                'keywords': keywords,
                'version': version,
                'description': description,
                'url': url
            },
            "author": {
                'author': author,
                'author_email': author_email
            }
        }
        init_readme(project_name, author, author_email, version, url)

        cmd = None
        if args.script:
            if args.conda:
                create_conda_env()
                init_ppmrc(rc, "script", conda=True)
            else:
                create_env()
                init_ppmrc(rc, "script")
            init_app(project_name, ky="script")
            init_requirements("script")
            cmd = "script"
        elif args.gui:
            if args.conda:
                create_conda_env()
                init_ppmrc(rc, "gui", conda=True)
            else:
                create_env()
                init_ppmrc(rc, "gui")
            init_app(project_name, ky="gui")
            init_requirements("")
            cmd = "gui"
        elif args.command:
            if args.conda:
                create_conda_env()
                init_ppmrc(rc, "command", conda=True)
            else:
                create_env()
                init_ppmrc(rc, "command")
            entry_points_T = Template(
                "entry_points={'console_scripts': ['$project_name = lib$project_name.main:main']},")
            entry_points = entry_points_T.substitute(project_name=project_name)
            init_setuppy(project_name, author, author_email, license_, keywords, version, description, url,
                         entry_points=entry_points
                         )
            init_manifest("lib" + project_name)
            init_app(project_name, ky="command")
            init_requirements("")
            cmd = "command"
        elif args.model:
            if args.conda:
                create_conda_env()
                init_ppmrc(rc, "model", conda=True)
            else:
                create_env()
                init_ppmrc(rc, "model")
            init_setuppy(project_name, author, author_email,
                         license_, keywords, version, description, url)
            init_manifest(project_name)
            init_app(project_name)
            init_requirements("")
            cmd = "model"
        elif args.web:
            if args.conda:
                create_conda_env()
                init_ppmrc(rc, "web", conda=True)
            else:
                create_env()
                init_ppmrc(rc, "web")
            if args.web == "sanic":
                init_app(project_name, ky="sanic")
                init_requirements("sanic")
                init_packagejson(project_name, version,
                                 description, author, license_)
                cmd = "web"
            elif args.web == "zerorpc":
                init_app(project_name, ky='zerorpc')
                init_requirements("zerorpc")
                cmd = 'zerorpc'
            elif args.web == "flask":
                init_app(project_name, ky='flask')
                init_requirements("flask")
                init_packagejson(project_name, version,
                                 description, author, license_)
                cmd = 'flask'
            else:
                init_app(project_name, ky='flask')
                init_requirements("flask")
                init_packagejson(project_name, version,
                                 description, author, license_)
                cmd = 'flask'

        else:
            if args.conda:
                create_conda_env()
                init_ppmrc(rc, "model", conda=True)
            else:
                create_env()
                init_ppmrc(rc, "model")
            init_setuppy(project_name, author, author_email,
                         license_, keywords, version, description, url)
            init_manifest(project_name)
            init_app(project_name)
            init_requirements("")
            cmd = "model"
        init_test()
        init_install()
        init_doc(args, project_name, author, version, ky=cmd)
        if args.math:
            install_math()
        return 1

    except:
        clean_init()
        raise
