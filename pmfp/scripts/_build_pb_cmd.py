from pmfp.build_pb import build_pb
from pmfp.config import load_rc


def build_pb_cmd(args):
    config = load_rc()
    if config:
        kwargs = _parser_args(args)
        build_pb(config, kwargs)
    else:
        print("命令需要在pmfp项目中执行")


def _parser_args(args):
    kwargs = {
        "name": "data.proto",
        "dir": "pbschema",
        "language": "",
        "grpc": False,
        "to": "",
    }
    if args.name:
        kwargs.update({
            "name": args.name
        })
    if args.dir:
        kwargs.update({
            "dir": args.dir
        })

    if args.language:
        kwargs.update({
            "language": args.language
        })

    if args.grpc:
        kwargs.update({
            "grpc": args.grpc
        })

    if args.to:
        kwargs.update({
            "to": args.to
        })

    return kwargs
