"""用于获取不同平台下项目使用的python的mixin"""
import platform
from pathlib import Path


class PythonPathMixin:
    """获取不同平台下项目使用的python."""

    def _get_sphinx_path(self):
        """获取Sphinx的地址."""
        if platform.system() == 'Windows':
            if self.form.env == "env":
                python_path = Path("env/Scripts/python")
            elif self.form.env == "conda":
                python_path = Path("env/python")
            else:
                python_path = Path("python")
        else:
            if self.form.env == "env":
                python_path = Path("env/bin/python")
            elif self.form.env == "conda":
                python_path = Path("env/bin/python")
            else:
                python_path = Path("python")
        return str(python_path)

    def _get_python_path(self):
        """获取python解释器的地址."""
        if platform.system() == 'Windows':
            if self.form.env == "env":
                python_path = Path("env/Scripts/python")
            elif self.form.env == "conda":
                python_path = Path("env/python")
            else:
                python_path = Path("python")
        else:
            if self.form.env == "env":
                python_path = Path("env/bin/python")
            elif self.form.env == "conda":
                python_path = Path("env/bin/python")
            else:
                python_path = Path("python")
        return str(python_path)


__all__ = ["PythonPathMixin"]
