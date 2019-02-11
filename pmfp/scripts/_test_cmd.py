from pmfp.test_ import test
from pmfp.config import load_rc


def test_cmd(args):
    config = load_rc()
    if config:
        kwargs = _parser_args(args)
        test(config, kwargs)
    else:
        print("命令需要在pmfp项目中执行")


def _parser_args(args):
    kwargs = {
        'html': False,
        "typecheck": False,
        "source":[]
    }
    if args.html:
        kwargs.update({
            "html": args.html
        })
    if args.typecheck:
        kwargs.update({
            "typecheck": args.typecheck
        })
    if args.source:
        kwargs.update({
            "source":  args.source
        })
    return kwargs
