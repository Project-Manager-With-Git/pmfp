"""用于验证pmfp.json的schema."""
import getpass
from typing import Dict
from typing import Any as typeAny
from voluptuous import (All, Any, Email, Equal, In, Invalid, NotIn,
                        Required, Schema, Url)

NOT_NAME_RANGE = ["app", "application", "module", "project"]
STATUS_RANGE = ["prod", "release", "dev", "test"]
LANGUAGE_RANGE = ["Python", "Javascript", "Golang"]
ENV_RANGE = ["env", "conda", "node", "frontend", "webpack", "vue", "vue-electron", "vue-native", "vue-nativescript", "gomod"]
TYPE_RANGE = ["application", "module"]
LICENSE_RANGE = ["MIT", "Apache", "BSD", "Mozilla", "LGPL", "GPL", "GNU"]
DEFAULT_AUTHOR = getpass.getuser()


def env_match(language: str, env: str) -> bool:
    """检测language和env是否匹配.

    Args:
        language (str): language
        env (str): env

    Returns:
        bool: 是否匹配

    """
    if language == "Python":
        if env not in ("env", "conda"):
            return False
        else:
            return True
    elif language in ("Javascript", ):
        if env not in ("node", "frontend", "webpack", "vue", "vue-electron", "vue-native", "vue-nativescript"):
            return False
        else:
            return True
    elif language in ("Golang",):
        if env not in ("gomod", ):
            return False
        else:
            return True
    else:
        raise AttributeError(f"unknown language {language}")


def config_must_match(config: Dict[str, typeAny]) -> Dict[str, typeAny]:
    """检测配置是否符合要求的函数.

    Args:
        config (Dict[str, Any]): 项目当前配置.

    Raises:
        Invalid: 项目非法.

    Returns:
        Dict[str, Any]: 如果项目配置没问题,返回项目配置

    """
    env = config['env']
    language = config['project-language']
    if not env_match(language, env):
        raise Invalid(f'{env}不是{language}允许的环境')
    return config


config_schema = Schema(
    All(
        {
            Required("project-name"): All(
                str,
                NotIn(
                    NOT_NAME_RANGE,
                    msg=f"项目名不可以在{NOT_NAME_RANGE}中"
                )
            ),
            Required('license', default="MIT"): All(
                str,
                In(LICENSE_RANGE,
                   msg=f"license 只能在{LICENSE_RANGE}范围内")
            ),
            Required('version', default="0.0.0"): str,
            Required('status', default="dev"): All(
                str,
                In(
                    STATUS_RANGE,
                    msg=f"status只能在{STATUS_RANGE}范围内"
                )
            ),
            Required('url', default=""): Any(Equal(""), Url(None)),
            Required('author', default=DEFAULT_AUTHOR): str,
            Required('author-email', default=""): Any(Equal(""), Email(None)),
            Required('keywords', default=["tools"]): list,
            Required('description', default="simple tools"): str,
            Required('project-language'): All(
                str,
                In(
                    LANGUAGE_RANGE,
                    msg=f"项目语言只能在{LANGUAGE_RANGE}范围内"
                )
            ),
            Required('gcc', default="gcc"): str,
            Required('env'): All(str, In(ENV_RANGE, msg=f"项目环境只能在{ENV_RANGE}范围内")),
            Required('global-python', default="python"): str,
            Required('project-type'): All(str, In(TYPE_RANGE, msg=f"项目类型只能在{TYPE_RANGE}范围内")),
            Required('template'): str,
            Required('remote_registry', default=""): str,
            Required("requirement", default=[]): list,
            Required("requirement-dev", default=[]): list,
            Required("entry", default=""): str
        },
        config_must_match
    )
)
