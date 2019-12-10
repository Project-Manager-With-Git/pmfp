import argparse
from pmfp.status import status
from pmfp.config import load_rc


def status_cmd():
    config = load_rc()
    if config:
        status(config)
    else:
        print("命令需要在pmfp项目中执行")
