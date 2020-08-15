import argparse
import json
from pmfp.new import new, new_component, new_pb
from pmfp.config import load_rc


def new_cmd(args: argparse.Namespace):
    config = load_rc()
    if config is False:
        kwargs_o = _parser_args(args)
        c_language = kwargs_o.get("language").capitalize()
        spl_name = kwargs_o.get("component_name").split("-")
        if len(spl_name) == 1:
            print(spl_name)
            if spl_name[0] in ("pb", "grpc", "grpc-streaming"):
                if kwargs_o["rename"] == "-":
                    rename = "example"
                elif kwargs_o["rename"] == "":
                    rename = "example_pb"
                else:
                    rename = kwargs_o["rename"]
                print(spl_name)
                print(rename)
                print(kwargs_o.get("to", "pbschema"))
                new_pb(c_name=spl_name[0], rename=rename, to=kwargs_o.get("to", "pbschema"), project_name="example")
        else:
            c_category = spl_name[0]
            c_name = "".join(spl_name[1:])
            path = f"{c_language}/{c_category}/{c_name}"
            config = {
                "project-language": c_language,
                "project-name": "tempname"
            }
            to = "." if kwargs_o.get("to") == "-" else kwargs_o.get("to")
            new_component(
                config,
                path,
                to,
                kwargs_o.get("rename"),
                kwargs_o.get("test"),
                **kwargs_o.get("kwargs", {})
            )
    else:
        kwargs_o = _parser_args(args)
        new(config, kwargs_o)


def _parser_args(args: argparse.Namespace):
    result = {
        "component_name": None,
        'to': "-",
        'rename': "-",
        "language": "-",
        "test": False,
        "kwargs": {}
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
    if args.kwargs:
        print(args.kwargs)
        try:
            result['kwargs'] = json.loads(args.kwargs)
        except Exception as e:
            print("关键字kwargs无法解析为json形式")
    return result
