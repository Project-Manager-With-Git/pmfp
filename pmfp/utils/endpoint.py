import re
import json
from pathlib import Path
from configparser import ConfigParser
from typing import Dict, Any, List, Union
from schema_entry import EntryPoint
from pmfp.const import PMFP_CONFIG_HOME, PMFP_CONFIG_DEFAULT_NAME


def setup_cfg_handdler(p: Path) -> Dict[str, Any]:
    config = ConfigParser()
    result: Dict[str, Union[str, List[str]]] = {"language": "py"}
    with open(p, encoding="utf-8") as f:
        config.read_file(f)
    config_dict = dict(config.items())
    metadata = config_dict.get("metadata")
    if metadata:
        project_name = metadata.get("name")
        if project_name:
            result.update(project_name=project_name)
        version = metadata.get("version")
        if version:
            result.update(version=version)
        author = metadata.get("author")
        if project_name:
            result.update(author=author)
        author_email = metadata.get("author_email")
        if project_name:
            result.update(author_email=author_email)
        description = metadata.get("description")
        if project_name:
            result.update(description=description)
        keywords = metadata.get("keywords")
        if keywords:
            result.update({"keywords": [i.strip() for i in keywords.split(",")]})
    options = config_dict.get("options")
    if options:
        # 安装依赖
        requires = config["options"].get("install_requires")
        if requires:
            result.update(requires=[i.strip() for i in requires.splitlines() if i.strip() != ""])
        # 测试依赖
        test_requires = config["options"].get("tests_require")
        if test_requires:
            result.update(test_requires=[i.strip() for i in test_requires.splitlines() if i.strip() != ""])
        # setup依赖
        setup_requires = config["options"].get("setup_requires")
        if setup_requires:
            if "cython" in setup_requires or "Cython" in setup_requires:
                result.update({"language": "cython"})
            setup_requires_str = [i.strip() for i in setup_requires.splitlines() if i.strip() != ""]
            result.update(setup_requires=setup_requires_str)
        # 其他依赖
        extras_require = config_dict.get("options.extras_require")
        if extras_require:
            extras_requires = []
            for key, v in extras_require.items():
                extras_requires += [f"{key}:" + i.strip() for i in v.splitlines() if i.strip() != ""]
            if extras_requires:
                result.update(
                    extras_requires=extras_requires
                )

    return result


def go_mod_handdler(p: Path) -> Dict[str, Any]:
    result: Dict[str, Union[str, List[str]]] = {"language": "go"}
    with open(p, encoding="utf-8") as f:
        con = f.read()
    r = re.search(r"module [\w|.|\-|/]+\s", con)
    if r:
        s = r.group(0)
        result.update(project_name=s.replace("module ", "").strip())
    _, req1 = con.split("require (")
    infos = req1.split(")")
    requirements = infos[0].strip()
    result["requires"] = [i.strip().replace(" ", "@") for i in requirements.splitlines()]
    return result


def cmake_handdler(p: Path) -> Dict[str, Any]:
    result: Dict[str, Union[str, List[str]]] = {"language": "CXX"}
    with open(p, encoding="utf-8") as f:
        con = f.read()
    r = re.search(r"project\s*\(\w+", con)
    if r:
        s = r.group(0)
        project_name = s.replace("project", "").replace("(", "").strip()
        result.update(project_name=project_name)
        r = re.search(r"project\s*\(" + project_name + r"\s+ VERSION \S+", con)
        if r:
            s = r.group(0)
            version = s.replace("project", "").replace("(", "").replace(project_name, "").replace("VERSION", "").strip()
            result.update(version=version)

        r = re.search(r'DESCRIPTION\s+".*"', con)
        if r:
            s = r.group(0)
            description = s.replace("DESCRIPTION", "").replace('"', "").strip()
            result.update(description=description)

        r = re.search(r'LANGUAGES\s+\w+', con)
        if r:
            s = r.group(0)
            language = s.replace("LANGUAGES", "").strip()
            result.update(language=language)

    return result


def package_json_handdler(p: Path) -> Dict[str, Any]:
    result: Dict[str, Union[str, List[str]]] = {}
    with open(p, encoding="utf-8") as f:
        con = json.load(f)
    result["project_name"] = con.get("name")
    result["version"] = con.get("version")
    result["description"] = con.get("description")
    result["author"] = con.get("author")
    result["requires"] = [f"{p}@{v.replace('^', '')}" for p, v in con.get("dependencies", {}).items()]
    result["test_requires"] = [f"{p}@{v.replace('^', '')}" for p, v in con.get("devDependencies", {}).items()]
    if p.parent.joinpath("tsconfig.json").exists():
        result["language"] = "ts"
    else:
        result["language"] = "js"
    result["project_name"] = con.get("name")
    return result


class EndPoint(EntryPoint):
    load_all_config_file = True
    config_file_only_get_need = True
    default_config_file_paths = [
        str(PMFP_CONFIG_HOME.joinpath(PMFP_CONFIG_DEFAULT_NAME)),
        f"./{PMFP_CONFIG_DEFAULT_NAME}",
        "setup.cfg",
        # "package.json",
        "go.mod",
        "CMakeLists.txt",
        "package.json"
    ]
    _config_file_parser_map = {
        "setup.cfg": setup_cfg_handdler,
        "go.mod": go_mod_handdler,
        "CMakeLists.txt": cmake_handdler,
        "package.json": package_json_handdler
    }
