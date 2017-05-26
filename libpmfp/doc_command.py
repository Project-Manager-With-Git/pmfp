import os
import http.server
import socketserver
import subprocess
from .utils import get_command, find_package_form
import copy
PYTHON, COMMAND, sphinx_apidoc, make = get_command()


def build():
    make1 = copy.copy(make)
    command = make1 + ["-b", "html", "apidoc", "docs"]
    print(command)
    print("building")
    subprocess.check_call(command)
    print("build Document done!")

    # subprocess.check_call(command)


def serve():
    build()
    os.chdir("./docs")
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


def doc(args):
    if find_package_form() == "script":
        print("script have no apidoc")
        return 0

    if args.serve:
        print("serve")
        serve()

    elif args.build:
        print("build")
        build()

    else:
        print("build")
        build()
