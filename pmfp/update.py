import re
from pmfp.const import PROJECT_HOME


def update_readme(config):
    readme_rst = PROJECT_HOME.joinpath('README.rst')
    readme_md = PROJECT_HOME.joinpath('README.md')
    if readme_rst.exists():
        print("update readme.rst")
        with open(str(readme_rst), "r", encoding="utf-8") as f:
            lines = []
            for i in f:
                if re.match(r"\* version:", i):
                    i = "* version: " + config["version"] + "\n"  # os.linesep
                if re.match(r"\* status:", i):
                    i = "* status: " + config["status"] + "\n"  # os.linesep
                lines.append(i)
        with open(str(readme_rst), "w", encoding="utf-8") as f:
            for i in lines:
                f.write(i)
    if readme_md.exists():
        print("update readme.md")
        with open(str(readme_md), "r", encoding="utf-8") as f:
            lines = []
            for i in f:
                if re.match(r"\+ version:", i):
                    i = "+ version: " + config["version"] + "\n"  # os.linesep
                if re.match(r"\+ status:", i):
                    i = "+ status: " + config["status"] + "\n"  # os.linesep
                lines.append(i)
        with open(str(readme_md), "w", encoding="utf-8") as f:
            for i in lines:
                f.write(i)


def update_doc(config):
    doc = PROJECT_HOME.joinpath('document')
    if doc.exists():
        print("update document/conf.py")
        with open("document/conf.py", "r", encoding="utf-8") as f:
            lines = []
            for i in f:
                if re.match(r"version =", i):
                    i = "version = '" + config["version"] + "'\n"
                lines.append(i)
        with open("document/conf.py", "w", encoding="utf-8") as f:
            for i in lines:
                f.write(i)

        with open("document/index.rst", "r", encoding="utf-8") as f:
            lines = []
            for i in f:
                if re.match(r"\* version:", i):
                    i = "* version: " + config["version"] + "\n"  # os.linesep
                if re.match(r"\* status:", i):
                    i = "* status: " + config["status"] + "\n"  # os.linesep
                lines.append(i)
        with open("document/index.rst", "w", encoding="utf-8") as f:
            for i in lines:
                f.write(i)


def update_package_json(config):
    package = PROJECT_HOME.joinpath("package.json")
    if package.exists():
        print("update package.json")
        with open(str(package), "r") as f:
            pak = json.load(f)
        pak.update({"version": config["version"]})
        with open(str(package), "w") as f:
            json.dump(pak, f)


def update_setup_py(config):
    setup = PROJECT_HOME.joinpath("setup.py")
    if setup.exists():
        print("update setup.py")
        with open("setup.py", "r", encoding="utf-8") as f:
            lines = []
            for i in f:
                if re.match(r"VERSION =", i):
                    i = "VERSION = '" + config["version"] + "'\n"
                lines.append(i)
        with open("setup.py", "w", encoding="utf-8") as f:
            for i in lines:
                f.write(i)


def update(config):
    update_doc(config)
    update_readme(config)
    update_package_json(config)
    update_setup_py(config)