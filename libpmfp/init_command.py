from pathlib import Path
from string import Template
import shutil
from .utils import get_command, write_ppmrc, is_inited, clean_init
from .Data import SETUPPY, COMMAND_MAIN, CONF, READMERST, PACKAGEJSON, SCRIPT
from .install_command import pip_install, write_requirement
import subprocess
import sys
import copy
import platform
import getpass

file_path = Path(__file__).absolute()
dir_path = file_path.parent
local_path = Path(".").absolute()


# def init_git(giturl):
#     print('cloning git')
#     PYTHON, _, _, _ = get_command()
#     command = ['git', 'clone', giturl]
#     subprocess.check_call(command)
#     print('cloning git done!')
#     return 0


def create_env():
    print('creating env')
    PYTHON, _, _, _ = get_command()
    command = [PYTHON, '-m', 'venv', 'env']
    subprocess.check_call(command)
    print('creating env done!')
    return 0


def install_math():
    print("install math libs")
    pip_install(["numpy"])
    write_requirement(["numpy"])
    pip_install(["mkl"])
    write_requirement(["mkl"])
    if platform.system() == 'Windows':
        print("""windoescan not install scipy and sklearn through pip,
              please go to http://www.lfd.uci.edu/~gohlke/pythonlibs
              and download the packages you need,then install""")
        return 0
    else:
        pip_install(["scipy"])
        write_requirement(["scipy"])
        pip_install(["scikit_learn"])
        write_requirement(["scikit_learn"])
    print("install math libs done!")


def input_info():
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
        keywords = ["'" + i + "'"for i in keywords.split(',')]
    project_name = project_name or local_path.name
    author = author or getpass.getuser()
    author_email = author_email or "author_email"
    license_ = license_ or "MIT"
    keywords = keywords or "'tools'"
    version = version or "0.0.1"
    description = description or "simple tools"
    url = url or ""
    return project_name, author, author_email, license_, keywords, version, description, url


def init_test():
    print("copy test template")
    if local_path.joinpath("test").exists():
        print(str(local_path.joinpath("test")) + " exists")
    else:
        shutil.copytree(str(dir_path.joinpath("test")),
                        str(local_path.joinpath("test")))
    print("copy test template done!")
    return 0


def init_doc(args, project_name, author, version, ky):
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
    return 0


def init_install():
    _, command, _, _ = get_command()
    print('update pip')
    command0 = copy.copy(command)
    command0 += ["-m", "pip", "install", "--upgrade", "pip"]
    subprocess.check_call(command0)
    print('update pip done')
    print('update setuptools')
    command0 = copy.copy(command)
    command0 += ["-m", "pip", "install", "setuptools", "--upgrade"]
    subprocess.check_call(command0)
    print('update setuptools done!')
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
    return 0


def init_ppmrc(rc, ky):
    if local_path.joinpath(".ppmrc").exists():
        print("already inited")
    else:
        rccontent = copy.copy(rc)
        rccontent.update(form={'form': ky})
        write_ppmrc(rccontent)
    return 0


def init_readme(project_name, author, author_email, version, url):
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
    return 0


def init_setuppy(project_name, author, author_email, license_, keywords, version, description, url, entry_points=""):
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
    return 0


def init_requirements(ky=""):
    print("copy requirements template")
    if local_path.joinpath("requirements").exists():
        print(str(local_path.joinpath("requirements")) + " exists")
    else:
        shutil.copytree(str(dir_path.joinpath("requirements" + ky)),
                        str(local_path.joinpath("requirements")))
    print("copy requirements template done!")
    return 0


def init_app(project_name, ky="model"):
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

    return 0


def init_packagejson(project_name, version, description, author, license_):

    print("writing package.json")
    if local_path.joinpath("package.json").exists():
        print("already have package.json")
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
    return 0


def init(args):
    if is_inited():
        print("already inited")
        sys.exit(0)
    try:
        # if args.git:
        #     giturl = args.git
        #     init_git(giturl)
        create_env()
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
            init_ppmrc(rc, "script")
            init_app(project_name, ky="script")
            init_requirements("script")
            cmd = "script"
        elif args.gui:
            init_ppmrc(rc, "gui")
            init_app(project_name, ky="gui")
            init_requirements("")
            cmd = "gui"
        elif args.command:
            init_ppmrc(rc, "command")
            entry_points_T = Template(
                "entry_points={'console_scripts': ['$project_name = lib$project_name.main:main']},")
            entry_points = entry_points_T.substitute(project_name=project_name)
            init_setuppy(project_name, author, author_email, license_, keywords, version, description, url,
                         entry_points=entry_points
                         )
            init_app(project_name, ky="command")
            init_requirements("")
            cmd = "command"
        elif args.model:
            init_ppmrc(rc, "model")
            init_setuppy(project_name, author, author_email,
                         license_, keywords, version, description, url)
            init_app(project_name)
            init_requirements("")
            cmd = "model"
        elif args.web:
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
        init_test()
        init_install()
        init_doc(args, project_name, author, version, ky=cmd)
        if args.math:
            install_math()

    except:
        clean_init()
        raise