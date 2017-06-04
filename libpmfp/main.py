import sys
if sys.version_info[0] != 3:
    raise OSError("only for python 3.5+")
if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    raise OSError("only for python 3.5+")
import argparse
from . import init, doc, test, install, clean, update, build, upload, rename, run, status, docker
from pathlib import Path

from typing import Sequence


def main(argv: Sequence[str]=sys.argv[1:]):

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    init_parsers = subparsers.add_parser("init")
    init_parsers.add_argument("-M", "--math", action="store_true")
    init_parsers.add_argument("-C", "--conda", action="store_true")
    init_group = init_parsers.add_mutually_exclusive_group(required=False)
    init_group.add_argument('-w', '--web', type=str,
                            choices=["sanic", "flask", "zerorpc"])
    init_group.add_argument('-g', '--gui', action="store_true")
    init_group.add_argument('-c', '--command', action="store_true")
    init_group.add_argument('-m', '--model', action="store_true")
    init_group.add_argument('-s', '--script', action="store_true")
    init_parsers.set_defaults(func=init)

    doc_parsers = subparsers.add_parser("doc")
    doc_group = doc_parsers.add_mutually_exclusive_group(required=False)
    doc_group.add_argument('-s', '--serve', action="store_true")
    doc_group.add_argument('-b', '--build', action="store_true")
    doc_parsers.set_defaults(func=doc)

    install_parsers = subparsers.add_parser("install")
    install_group = install_parsers.add_mutually_exclusive_group(required=True)
    install_group.add_argument('-d', '--dev', nargs='*', required=False)
    install_group.add_argument('-t', '--test', nargs='*', required=False)
    install_group.add_argument(
        '-r', '--requirements', nargs='*', required=False)
    install_group.add_argument('--self', action="store_true")
    install_parsers.set_defaults(func=install)

    clean_parsers = subparsers.add_parser("clean")
    clean_group = clean_parsers.add_mutually_exclusive_group(required=False)
    clean_group.add_argument('-s', '--leave_source', action="store_true")
    clean_group.add_argument('-a', '--all', action="store_true")
    clean_parsers.set_defaults(func=clean)

    update_parsers = subparsers.add_parser("update")
    update_parsers.add_argument('vers', type=str)
    update_parsers.set_defaults(func=update)

    rename_parsers = subparsers.add_parser("rename")
    rename_parsers.add_argument('name', type=str)
    rename_parsers.set_defaults(func=rename)

    build_parsers = subparsers.add_parser("build")
    build_parsers.add_argument(
        '-e', '--egg', action="store_true")
    build_parsers.add_argument(
        '-w', '--wheel', action="store_true")
    build_parsers.set_defaults(func=build)

    run_parsers = subparsers.add_parser("run")
    run_parsers.add_argument('args', type=str, nargs='+')
    run_parsers.set_defaults(func=run)

    test_parsers = subparsers.add_parser("test")
    test_parsers.add_argument('-t', '--typecheck', action="store_true")
    test_parsers.add_argument(
        '-c', '--coverage', type=str, choices=["report", "html"])
    test_parsers.set_defaults(func=test)

    upload_parsers = subparsers.add_parser("upload")
    upload_group = upload_parsers.add_mutually_exclusive_group(required=False)
    upload_group.add_argument('-r', '--regist', type=str,
                              choices=["pypi", "local"])
    upload_group.add_argument('-p', '--pypi', action="store_true")
    upload_group.add_argument('-l', '--localpypi', type=str)
    upload_group.add_argument('-g', '--git', type=str,
                              nargs='*', required=False)
    upload_parsers.set_defaults(func=upload)

    test_parsers = subparsers.add_parser("status")
    test_parsers.set_defaults(func=status)

    upload_parsers = subparsers.add_parser("docker")
    upload_group = upload_parsers.add_mutually_exclusive_group(required=False)
    upload_group.add_argument('-i', '--init', action="store_true")
    upload_group.add_argument('-b', '--build', action="store_true")
    upload_group.add_argument('-p', '--push', type=str,
                              nargs='*', required=False)

    upload_parsers.set_defaults(func=docker)

    args = parser.parse_args()
    args.func(args)
