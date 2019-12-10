import argparse
from pmfp.init import init
from pmfp.config.utils import load_rc, write_rc
from pmfp.config.new_config import new_config


def init_cmd(args: argparse.Namespace):
    kwargs = _parser_args(args)
    config = load_rc()
    if config is False:
        config = new_config(kwargs["project_name"], kwargs["template"], kwargs["language"])
        print("创建项目配置文件")
        write_rc(config)
    init(config, test=kwargs["test"], doc=kwargs["doc"], noinstall=kwargs["noinstall"])


def _parser_args(args: argparse.Namespace):
    result = {
        "template": None,
        "language": None,
        'project_name': None,
        "test": False,
        "doc": False,
        "noinstall": False
    }
    if args.project_name:
        result["project_name"] = args.project_name
    if args.template:
        result['template'] = args.template
    if args.language:
        result['language'] = args.language.capitalize()
    if args.test:
        result['test'] = args.test
    if args.doc:
        result['doc'] = args.doc
    if args.noinstall:
        result['noinstall'] = args.noinstall
    return result
