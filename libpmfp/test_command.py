import subprocess

import copy

from .utils import find_package_name, get_command,project_form
_, COMMAND, _, _ = get_command()


def runtest():
    print("unittest start")
    package_name = find_package_name()
    command1 = copy.copy(COMMAND)
    command1 += "-m coverage run --source {package_name} unittest discover -v -s test".format(
        package_name=package_name).split(" ")
    subprocess.check_call(command1)
    print("unittest done!")


def runcoverage(com):
    print("coverage start")
    package_name = find_package_name()
    command1 = copy.copy(COMMAND)
    command1 += "-m coverage {com}".format(com=com).split(" ")
    subprocess.check_call(command1)
    print("coverage done!")


def runtypecheck():
    print("type check start")
    form = project_form()
    if form in ["command","script","model"]:
        package_name = find_package_name()
        if form == "command":
            package_name = "lib"+package_name
        elif form == "script":
            package_name = package_name+".py"
        command1 = copy.copy(COMMAND)
        command1 += "-m mypy "+package_name
        subprocess.check_call(command1)

    else:
        package_name = find_package_name()
        if form == "command":
            package_name = "lib"+package_name
        elif form == "script":
            package_name = package_name+".py"
        command1 = copy.copy(COMMAND)
        command1 += "-m mypy "+package_name
        subprocess.check_call(command1)
    print("type check done!")

def test(args):
    if args.typecheck:
        runtypecheck()
    else:
        if not args.coverage:
            runtest()
        else:
            runcoverage(args.coverage)
