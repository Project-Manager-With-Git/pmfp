import platform
from pathlib import Path


class PythonPathMixin:
    def _get_sphinx_path(self):
        if platform.system() == 'Windows':
            if self.form.env == "env":
                python_path = Path("env/Scripts/python")
            elif self.form.env == "conda":
                python_path = Path("env/python")
            else:
                print("unknown env for python/cython!")
                return False
        else:
            if self.form.env == "env":
                python_path = Path("env/bin/python")
            elif self.form.env == "conda":
                python_path = Path("env/bin/python")
            else:
                print("unknown env for python/cython!")
                return False
        return str(python_path)
    def _get_python_path(self):
        if platform.system() == 'Windows':
            if self.form.env == "env":
                python_path = Path("env/Scripts/python")
            elif self.form.env == "conda":
                python_path = Path("env/python")
            else:
                print("unknown env for python/cython!")
                return False
        else:
            if self.form.env == "env":
                python_path = Path("env/bin/python")
            elif self.form.env == "conda":
                python_path = Path("env/bin/python")
            else:
                print("unknown env for python/cython!")
                return False
        return str(python_path)


__all__ = ["PythonPathMixin"]
