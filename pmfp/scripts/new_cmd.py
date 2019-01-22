from pmfp.new import new,new_component
from pmfp.config import load_rc


def new_cmd(args):
    config = load_rc()
    if config is False:
        #print("new命令需要目录下有.pmfprc.json配置文件.")
        kwargs_o = _parser_args(args)
        c_language = kwargs_o.get("language").capitalize()
        spl_name = kwargs_o.get("component_name").split("-")
        c_category = spl_name[0]
        c_name = "".join(spl_name[1:])
        path = f"{c_language}/{c_category}/{c_name}"
        config = {
            "project-language":c_language,
            "project-name":"tempname"
        }
        to = "." if kwargs_o.get("to") == "-" else kwargs_o.get("to")
        new_component(
            config, 
            path, 
            to,
            kwargs_o.get("rename"), 
            kwargs_o.get("test")
        )
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
