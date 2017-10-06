import os
import http.server
import socketserver
import subprocess
from pathlib import Path


class DocMixin:

    def _build_doc(self):

        if self.form.compiler in ["python", "cython"]:
            if self.form.template in ["tk", "sanic", "flask"]:
                print("this template do not need to build apidoc")

            if self.form.project_type == "script":
                print("building apidoc")
                command = "sphinx-apidoc -o apidoc {self.meta.project_name}".format(
                    self=self)
                subprocess.call(command, shell=True)
                print("build apidoc done!")
            else:
                print("building apidoc")
                command = "sphinx-apidoc -o apidoc {self.meta.project_name}".format(
                    self=self)
                subprocess.call(command, shell=True)
                print("build apidoc done!")

        command = "sphinx-build -b html document docs"
        print("building document")
        subprocess.call(command, shell=True)
        print("build Document done!")
        here = Path(".").absolute()
        docs = here.joinpath("docs")
        nojekyll = docs.joinpath(".nojekyll")
        if not nojekyll.exists():
            with nojekyll.open("w") as f:
                pass
        return True

    def _serve_doc(self):
        self._build_doc()
        os.chdir("./docs")
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
        return True

    def doc(self, command="build"):
        if self.with_docs:
            if command == "serve":
                self._serve_doc()
                return True
            else:
                self._build_doc()
        else:
            print('this project do not have document')


__all__ = ["DocMixin"]
