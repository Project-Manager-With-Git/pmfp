from .utils import read_ppmrc, is_inited
import re
from pathlib import Path
import configparser
from argparse import Namespace


def status(args: Namespace)->int:
    if is_inited():
        conf = read_ppmrc()
        info = conf.items("project")
        info = sorted(info, reverse=True)
        for i in info:
            print(i[0] + ":" + i[1])
        return 0
    else:
        parser = configparser.ConfigParser(allow_no_value=True)
        p = Path(__file__).absolute().parent.parent
        parser.read(str(p.joinpath('.ppmrc')))
        print("pmfp version:" + parser["project"]["version"])
    return 1
