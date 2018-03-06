import os
import http.server
import socketserver
import subprocess
from pathlib import Path


class DocMixin:
    """用于处理项目文档的混入"""
    def _build_doc(self):

        if self.form.compiler == "python":
            if self.form.project_form == "script":
                print("building apidoc")
                command = "sphinx-apidoc -o document {self.meta.project_name}".format(
                    self=self)
                subprocess.call(command, shell=True)
                print("build document done!")
            else:
                print("building apidoc")
                command = "sphinx-apidoc -o document {self.meta.project_name}".format(
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

    def doc(self, command="build")->None:
        """操作文档生成或者预览的方法.

        Args:
            command (str, optional): - build,serve二选一(Defaults to "build"). 

        """
        if Path("document").is_dir():
            if command == "serve":
                self._serve_doc()
                return True
            else:
                self._build_doc()
        else:
            print("need to new a document first")


__all__ = ["DocMixin"]
