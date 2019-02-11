from pmfp.doc import doc
from pmfp.config import load_rc


def doc_cmd(args):
    config = load_rc()
    if config:
        kwargs = _parser_args(args)
        doc(config, kwargs)
    else:
        print("命令需要在pmfp项目中执行")


def _parser_args(args):
    kwargs = {
        "serve": False
    }
    if args.serve:
        kwargs.update({
            "serve": args.serve
        })

    return kwargs
