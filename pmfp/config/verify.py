import getpass
from voluptuous import (
    Schema,
    All,
    Range,
    Required,
    Any,
    Invalid,
    In,
    Url,
    NotIn,
    Email,
    Equal
)

NOT_NAME_RANGE = ["app", "application", "module", "project"]
STATUS_RANGE = ["production", "release", "dev", "test"]
LANGUAGE_RANGE = ["Python", "Javascript"]
ENV_RANGE = ["env", "conda", "node", "ts-node"]
TYPE_RANGE = ["application", "module"]
DEFAULT_AUTHOR = getpass.getuser()


def config_must_match(config):
    env = config['env']
    language = config['project-language']
    if language == "Python":
        if env not in ("env", "conda"):
            raise Invalid(f'{env}不是{language}允许的环境')
    elif language in ("Javascript", "Typescript"):
        if env not in ("node", "ts-node"):
            raise Invalid(f'{env}不是{language}允许的环境')
    return config


config_schema = Schema(
    All(
        {
            Required("project-name"): All(str, NotIn(NOT_NAME_RANGE, msg=f"项目名不可以在{NOT_NAME_RANGE}中")),
            Required('license', default="MIT"): str,
            Required('version', default="0.0.0"): str,
            Required('status', default="dev"): All(str, In(STATUS_RANGE, msg=f"status只能在{STATUS_RANGE}范围内")),
            Required('url', default=""): Any(Equal(""), Url()),
            Required('author', default=DEFAULT_AUTHOR): str,
            Required('author-email', default=""): Any(Equal(""), Email()),
            Required('keywords', default=["tools"]): list,
            Required('description', default="simple tools"): str,
            Required('project-language'): All(str, In(LANGUAGE_RANGE, msg=f"项目语言只能在{LANGUAGE_RANGE}范围内")),
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
