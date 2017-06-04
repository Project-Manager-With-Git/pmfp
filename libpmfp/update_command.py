from .utils import read_ppmrc, write_ppmrc
import re
from pathlib import Path
from argparse import Namespace


def update(args: Namespace)->int:
    path = Path(".").absolute()
    apidoc = Path('apidoc')
    readme = Path('README.rst')
    test = Path('test')
    setup = Path("setup.py")

    conf = read_ppmrc()
    conf["project"]["version"] = args.vers
    conf = dict(conf)
    write_ppmrc(conf)
    if path.joinpath(readme).exists():
        with open("README.rst", "r") as f:
            lines = []
            for i in f:
                if re.match(r"version:", i):
                    i = "version: " + args.vers + "\n"
                lines.append(i)
        with open("README.rst", "w") as f:
            for i in lines:
                f.write(i)
    if path.joinpath(apidoc).exists():
        with open("apidoc/conf.py", "r") as f:
            lines = []
            for i in f:
                if re.match(r"version =", i):
                    i = "version = '" + args.vers + "'\n"
                lines.append(i)
        with open("apidoc/conf.py", "w") as f:
            for i in lines:
                f.write(i)
    if path.joinpath(setup).exists():
        with open("setup.py", "r") as f:
            lines = []
            for i in f:
                if re.match(r"VERSION =", i):
                    i = "VERSION = '" + args.vers + "'\n"
                lines.append(i)
        with open("setup.py", "w") as f:
            for i in lines:
                f.write(i)
    return 1
