"""初始化cython的执行环境."""
import pkgutil
import warnings
from pathlib import Path
from configparser import ConfigParser
from typing import Optional, List, Dict, Any
import toml
from pmfp.utils.run_command_utils import run
from pmfp.utils.tools_info_utils import get_global_python, get_config_info
from pmfp.utils.template_utils import template_2_content
from pmfp.const import GOLBAL_CC
from .utils import new_env_py_pypiconf, new_env_py_venv, new_env_py_conda, new_env_py_manifest

cython_setup_py_template = ""
template_io = pkgutil.get_data('pmfp.entrypoint.env_.new.source_temp', 'cython_setup.py.jinja')
if template_io:
    cython_setup_py_template = template_io.decode('utf-8')
else:
    raise AttributeError("cython_setup.py模板失败")


def new_env_cython_setup(cwd: Path,
                         project_name: str,
                         version: str,
                         author: str,
                         author_email: str,
                         description: str,
                         keywords: str,
                         requires: Optional[List[str]] = None,
                         test_requires: Optional[List[str]] = None,
                         setup_requires: Optional[List[str]] = None,
                         extras_requires: Optional[List[str]] = None) -> None:
    """初始化cython项目的setup.py和setup.cfg文件.

    Args:
        cwd (Path): [description]
    """
    # setup.py
    setup_py_path = cwd.joinpath("setup.py")
    if setup_py_path.exists():
        warnings.warn("setup.py已存在!")
        print("""根据模板构造setup.cfg文件成功,修改setup.cfg可以
    后续可以查看<https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html#declarative-config>实现
    """)
    else:

        content = template_2_content(template=cython_setup_py_template)
        if setup_requires:
            for req in setup_requires:
                if "cython" in req:
                    break
            else:
                setup_requires.append("cython")
        else:
            setup_requires = ["cython"]

        with open(setup_py_path, "w", newline="", encoding="utf-8") as f:
            f.write(content)
        print("根据模板构造setup.py文件成功")

    # pyproject.toml(PEP-518)
    pyproject_toml_path = cwd.joinpath("pyproject.toml")
    if pyproject_toml_path.exists():
        warnings.warn("pyproject.toml已存在!")
    else:
        with open(pyproject_toml_path, "w", encoding="utf-8") as f:
            toml.dump(
                {
                    "build-system": {
                        "requires": ["setuptools >= 40.9.0", "wheel", "cython"],
                        "build-backend": "setuptools.build_meta"
                    }

                }, f
            )

    # setup.cfg
    setup_cfg_path = cwd.joinpath("setup.cfg")
    if setup_cfg_path.exists():
        warnings.warn("setup.cfg已存在!")
    else:
        config = ConfigParser()
        metadata = {
            "name": project_name,
            "version": version,
            "author": author,
            "author_email": author_email,
            "description": description,
            "long_description": "file: README.md, CHANGELOG.md, LICENSE",
            "long_description_content_type": "text/markdown",
            "keywords": keywords,
            "license": "MIT License",
            "classifiers": """
    License :: OSI Approved :: MIT License
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    """
        }
        options: Dict[str, Any] = {
            "zip_safe": False,
            "include_package_data": True,
            "packages": "find:"}
        if requires:
            options.update({
                "install_requires": """
    """ + """
    """.join(requires)})

        if test_requires:
            options.update({
                "tests_require": """
    """ + """
    """.join(test_requires)})
        else:
            options.update({
                "tests_require": """
    coverage >= 5.5
    mypy >= 0.800
    autopep8 >= 1.5.6
    pylint >= 2.8.0
    pydocstyle>=6.0.0
    """})

        if setup_requires:
            options.update({
                "setup_requires": """
    """ + """
    """.join(setup_requires)})
        else:
            options.update({
                "setup_requires": """
    wheel >= 0.36.2
    setuptools >= 47.1.0
    """})
        setup: Dict[str, Any] = {
            "metadata": metadata,
            "options": options,
            "options.packages.find": {
                "include": project_name,
                "exclude": "tests",
            }
        }
        if extras_requires:
            options_extras_requires: Dict[str, List[str]] = {}
            for line in extras_requires:
                key, package = line.split(":")
                if key in options_extras_requires:
                    options_extras_requires[key].append(package)
                else:
                    options_extras_requires[key] = [package]
            options_extras_requires_str: Dict[str, str] = {}
            for key, packages in options_extras_requires.items():
                options_extras_requires_str[key] = """
    """ + """
    """.join(packages)
            setup.update({
                "options.extras_require": options_extras_requires_str
            })
        setup.update({
            "build_ext": {
                "inplace": "1"
            },
            "build": {
                "compiler": GOLBAL_CC
            }
        })

        config.read_dict(setup)
        config.write(open(setup_cfg_path, "w", newline="", encoding="utf-8"))
        print("""根据模板构造setup.cfg文件成功,修改setup.cfg可以
        后续可以查看<https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html#declarative-config>实现
        """)


def init_cython_env(env: str,
                    cwd: Path,
                    project_name: str,
                    version: str,
                    author: str,
                    author_email: str,
                    description: str,
                    keywords: str,
                    requires: Optional[List[str]] = None,
                    test_requires: Optional[List[str]] = None,
                    setup_requires: Optional[List[str]] = None,
                    extras_requires: Optional[List[str]] = None) -> None:

    if env == "conda":
        new_env_py_conda(cwd=cwd)
    else:
        new_env_py_venv(cwd=cwd)
    new_env_py_manifest(cwd=cwd, project_name=project_name)
    new_env_py_pypiconf(cwd=cwd)
    new_env_cython_setup(cwd=cwd,
                         project_name=project_name,
                         version=version,
                         author=author,
                         author_email=author_email,
                         description=description,
                         keywords=keywords,
                         requires=requires,
                         test_requires=test_requires,
                         setup_requires=setup_requires,
                         extras_requires=extras_requires)
    print("构造cython环境完成")
