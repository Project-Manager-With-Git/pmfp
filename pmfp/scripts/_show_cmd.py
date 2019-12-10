import argparse
from pmfp.show import show


def show_template_cmd(args: argparse.Namespace):
    config = _parser_args(args)
    config.update({
        "type": "template"
    })
    print(config)
    show(config)


def show_component_cmd(args: argparse.Namespace):
    config = _parser_args(args)
    config.update({
        "type": "component"
    })
    show(config)


def _parser_args(args: argparse.Namespace):
    result = {
        "name": None,
        'language': None,
        'category': None
    }
    if args.name:
        result["name"] = args.name
    if args.language:
        result['language'] = args.language
    if args.category:
        result['category'] = args.category
    return result
