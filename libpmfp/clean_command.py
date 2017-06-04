
from pathlib import Path
from .utils import get_command

from argparse import Namespace

PYTHON, _, _, _ = get_command()


def clean(args: Namespace)->int:
    path = Path(".").absolute()
    apidoc = Path('apidoc')
    docs = Path('docs')
    env = Path('env')
    test = Path('test')
    ppmrc = Path(".ppmrc")
    requirements = Path("requirements")
    setup = Path("setup.py")
    rms = []
    if args.all:
        rms = [apidoc, docs, env, test, ppmrc, requirements, setup]
    elif args.leave_source:
        rms = [docs, env, ppmrc]

    for i in rms:
        try:
            os.remove(str(path.joinpath(i)))
        except Exception as e:
            print(e)
            print("skip " + str(path.joinpath(i)))
            continue
    return 0
