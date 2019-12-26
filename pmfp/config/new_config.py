"""在没有pmfp.json时根据命令行的输入构造一个."""

import json
import warnings
from typing import Optional, Dict, Any
from pmfp.const import PROJECT_HOME
from pmfp.show import show
from pmfp.utils import (
    find_template_path,
    _find_template_path,
    get_node_version,
    get_golang_version
)
from .verify import (
    DEFAULT_AUTHOR,
    LANGUAGE_RANGE,
    NOT_NAME_RANGE,
    LICENSE_RANGE,
    STATUS_RANGE,
    env_match
)


def _init_config(
        project_name: str,
        template: Optional[str] = None,
        language: Optional[str] = None) -> Dict[str, Any]:
    """初始化配置.

    构造一个默认的初始化配置.

    Args:
        project_name (str): 项目名
        template (Optional[str], optional): Defaults to None. 项目模板
        language (Optional[str], optional): Defaults to None. 项目编程语言

    Returns:
        Dict[str, Any]: 默认的初始化配置

    """
    config = {
        "project-name": project_name,
        'project-language': language,
        'env': None,
        'project-type': None,
        'template': template,
        'license': None,
        'version': None,
        'status': None,
        'url': None,
        'author': None,
        'author-email': None,
        'keywords': None,
        'description': None,
        'gcc': "",
        'global-python': "python",
        'remote_registry': "",
        "requirement": [],
        "requirement-dev": [],
        "entry": None,
    }
    if template and language:
        language = language.capitalize()
        t_p = template.split("-")
        template_path = _find_template_path(language, t_p)
        with open(str(template_path), encoding="utf-8") as f:
            template_info = json.load(f)
            if template_info.get("env"):
                config.update({"env": template_info.get("env")})
            if template_info.get("gcc"):
                config.update({"gcc": template_info.get("gcc")})
            if template_info.get("env"):
                config.update({"entry": template_info.get("entry")})
    return config


def _init_project_name(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目名.

    Args:
        config ([type]): 默认

    Returns:
        Dict[str, Any]: 更新了项目名的配置

    """
    config = dict(config)
    if not config.get("project-name"):
        project_name = input("项目名:")
        project_name = project_name or PROJECT_HOME.name
    else:
        project_name = config.get("project-name")
    if project_name in NOT_NAME_RANGE:
        print(f"名字{project_name}不可以是如下{NOT_NAME_RANGE},请重新输入")
        while True:
            project_name = input("项目名:")
            if project_name in NOT_NAME_RANGE:
                print(f"名字{project_name}不可以是如下{NOT_NAME_RANGE},请重新输入")
            else:
                break
    if "-" in project_name:
        project_name = project_name.replace("-", "_")
        print(f"已将项目名中的-改为了_,项目名为{project_name}")

    config.update({
        "project-name": project_name
    })
    return config


def _init_language(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目language.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过language后的配置.

    """
    config = dict(config)
    if not config.get("project-language"):
        project_language = input("项目语言:")
    else:
        project_language = config.get("project-language")
    project_language = project_language.capitalize()
    if project_language not in LANGUAGE_RANGE:
        print(f"不支持的语言{project_language},目前只支持{LANGUAGE_RANGE},请重新输入")
        while True:
            project_language = input("项目语言:")
            project_language = project_language.capitalize()
            if project_language not in LANGUAGE_RANGE:
                print(f"不支持的语言{project_language},目前只支持{LANGUAGE_RANGE},请重新输入")
            else:
                break

    if project_language == "Golang":
        if get_golang_version() is None:
            warnings.warn("本机没有go语言环境")
    elif project_language == "Javascript":
        if get_node_version() is None:
            warnings.warn("本机没有node环境")

    config.update({
        "project-language": project_language
    })
    return config


def _init_env(config: Dict[str, Any]) -> Dict[str, Any]:
    """创建env环境.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过env后的配置.

    """
    config = dict(config)
    language = config.get("project-language")
    if language == "Python":
        default_env = config.get("env") or "env"
    elif language == "Javascript":
        default_env = config.get("env") or "node"
    elif language == "Golang":
        default_env = config.get("env") or "gomod"
    else:
        print("不支持的项目语言")
        return
    env = input("环境:")
    env = env or default_env
    if not env_match(language, env):
        print(f"语言{language}不支持的环境 {env},请重新输入")
        while True:
            env = input("环境:")
            if env_match(language, env):
                break
    config.update({
        "env": env
    })
    return config


def _init_template(config: Dict[str, Any]) -> Dict[str, Any]:
    """通过template构造项目配置.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过template和project-type后的配置.

    """
    config = dict(config)
    if config.get("template") is None:
        while True:
            print("可选的模板有:")
            all_templates = show({
                "name": None,
                'category': None,
                "type": "template",
                "language": config["project-language"]
            })
            template = input("请输入模板:")
            if template not in all_templates:
                print("未知的模板,请重新输入")
            else:
                config.update({
                    "template": template
                })
                break
    template_path = find_template_path(config)
    with open(str(template_path), encoding="utf-8") as f:
        template_info = json.load(f)
    config.update({
        "project-type": template_info["project-type"]
    })
    return config


def _init_license(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目license.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过license后的配置.

    """
    config = dict(config)
    license_ = input("license:")
    if not license_:
        license_ = "MIT"
    if license_ not in LICENSE_RANGE:
        print("未知的授权协议,请重新输入")
        while True:
            license_ = input("license:")
            if license_ not in LICENSE_RANGE:
                print("未知的授权协议,请重新输入")
            else:
                break

    config.update({
        "license": license_
    })
    return config


def _init_version(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目版本.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过version后的配置.

    """
    config = dict(config)
    version = input("project version:")
    if not version:
        version = "0.0.1"
    config.update({
        "version": version
    })
    return config


def _init_status(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目状态.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过version后的配置.

    """
    config = dict(config)
    status = input("project status:")
    if not status:
        status = "dev"
    if status not in STATUS_RANGE:
        print("未知的授权协议,请重新输入")
        while True:
            status = input("project status:")
            if status not in STATUS_RANGE:
                print("未知的项目状态,请重新输入")
            else:
                break
    config.update({
        "status": status
    })
    return config


def _init_url(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目的主页.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过version后的配置.

    """
    config = dict(config)
    url = input("project's url:")
    if not url:
        url = ""
    config.update({
        "url": url
    })
    return config


def _init_author(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目的作者.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过version后的配置.

    """
    config = dict(config)
    author_ = input("project's author:")
    if not author_:
        author_ = DEFAULT_AUTHOR
    config.update({
        "author": author_
    })
    return config


def _init_author_email(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目的作者邮箱.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过version后的配置.

    """
    config = dict(config)
    author_email = input("project author's email:")
    if not author_email:
        author_email = ""
    config.update({
        "author-email": author_email
    })
    return config


def _init_keywords(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目的关键字.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过version后的配置.

    """
    config = dict(config)
    keywords = input("keywords,split by ',':")
    if not keywords:
        keywords = ["tools"]
    else:
        keywords = [i for i in keywords.split(',')]
    config.update({
        "keywords": keywords
    })
    return config


def _init_desc(config: Dict[str, Any]) -> Dict[str, Any]:
    """初始化项目的作者邮箱.

    Args:
        config (Dict[str, Any]): 项目当前的配置.

    Returns:
        Dict[str, Any]: 项目更新过version后的配置.

    """
    config = dict(config)
    description = input("description:")
    if not description:
        description = "simple tools"
    config.update({
        "description": description
    })
    return config


def _init_entry(config: Dict[str, Any]) -> Dict[str, Any]:
    config = dict(config)
    if not config.get("entry"):
        if config["project-language"] == "Python":
            if config["project-type"] == "application":
                entry = config["project-name"]
                config.update({
                    "entry": entry
                })
            else:
                config.update({
                    "entry": ""
                })
        if config["project-language"] == "Javascript":
            config.update({
                "entry": "es/index.js"
            })
        else:
            config.update({
                "entry": ""
            })
    else:
        config.update({
            "entry": ""
        })
    return config


def new_config(
        project_name: str,
        template: Optional[str] = None,
        language: Optional[str] = None) -> Dict[str, Any]:
    """创建一个项目配置.

    Args:
        project_name (str): 项目名
        template (Optional[str], optional): Defaults to None. 项目模板
        language (Optional[str], optional): Defaults to None. 项目编程语言

    Returns:
        Dict[str, Any]: 默认的初始化配置

    """
    config = _init_config(project_name, template, language)
    config = _init_project_name(config)
    config = _init_language(config)
    config = _init_env(config)
    config = _init_template(config)
    config = _init_license(config)
    config = _init_version(config)
    config = _init_status(config)
    config = _init_url(config)
    config = _init_author(config)
    config = _init_author_email(config)
    config = _init_keywords(config)
    config = _init_desc(config)
    config = _init_entry(config)
    return config
