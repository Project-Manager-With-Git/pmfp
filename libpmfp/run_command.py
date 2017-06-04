import subprocess
from .utils import get_command
from argparse import Namespace


def run(args: Namespace)->int:
    _, COMMAND, _, _ = get_command()
    command = COMMAND + args.args
    subprocess.check_call(command)
    return 1
