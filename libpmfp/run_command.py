import subprocess
from .utils import get_command
def run(args):
    _, COMMAND, _, _ = get_command()
    command = COMMAND + args.args
    subprocess.check_call(command)
