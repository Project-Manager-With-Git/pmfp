from pmfp.new import new
from pmfp.config import load_rc


def new_cmd(args):
    config = load_rc()
    if config is False:
        print("install命令需要目录下有.pmfprc.json配置文件.")
    else:
        kwargs_o = _parser_args(args)
        language = config["project-language"]
        
        new(config, kwargs_o)


def _parser_args(args):
    result = {
        "component_name": None,
        'to': "-",
        'rename': "-",
        "language": "-",
        "test": False
    }
    if args.component_name:
        result["component_name"] = args.component_name
    if args.to:
        result['to'] = args.to
    if args.rename:
        result['rename'] = args.rename
    if args.language:
        result['language'] = args.language
    if args.test:
        result['test'] = args.test
    return result
