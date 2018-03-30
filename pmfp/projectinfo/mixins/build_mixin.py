import os
import stat
import shutil
import compileall
import platform
import tempfile
import subprocess
import zipapp
from pathlib import Path
import shutil


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def delete_py_source(p):
    if p.is_file():
        if p.suffix == ".py":
            os.remove(str(p))
    else:
        if p.name == "__pycache__":
            try:
                shutil.rmtree(str(p), onerror=remove_readonly)
            except Exception as e:
                print(e)
        else:
            for i in p.iterdir():
                delete_py_source(i)


class BuildMixin:
    """编译项目的混入"""

    def _build_egg(self):
        if Path("setup.py").exists():
            print('build model to egg file')
            command = "python setup.py bdist_egg"
            subprocess.check_call(command)
            print('build model to egg file done!')
        else:
            print("build model to egg need file setup.py")

    def _build_wheel(self):
        print('build model to wheel file')
        command = "python setup.py bdist_wheel"
        subprocess.check_call(command)
        print('build model to wheel file done!')

    def _build_app(self):
        """将gui项目打包为app,windows下也就是exe."""
        python_path = self._get_python_path()
        logo_path = str(Path("./logo.ico"))
        if self.form.project_form == "script" and self.form.template in ("tk",):
            if logo_path.is_file():
                command = f"{python_path} -OO -m PyInstaller -F {self.meta.project_name} --noconsole --icon {logo_path}"
            else:
                command = f"{python_path} -OO -m PyInstaller -F {self.meta.project_name} --noconsole"
            subprocess.check_call(command)
            return
        elif self.form.project_form == "gui":
            if logo_path.is_file():
                command = f"{python_path} -OO -m PyInstaller -F  -n {self.meta.project_name} main.py --noconsole --icon {logo_path}"
            else:
                command = f"{python_path} -OO -m PyInstaller -F  -n {self.meta.project_name} main.py --noconsole"
            
            subprocess.check_call(command)
            return
        else:
            print("only gui can build to a app")
            return


    def _build_pyz(self):
        print('build {self.meta.project_name} to pyz file'.format(self=self))
        t = tempfile.mkdtemp(dir=".")
        tp = Path(t)
        # tp.mkdir()
        if self.form.project_form == "script":
            project_path = Path(self.meta.project_name + ".py")
            shutil.copy(
                str(project_path),
                str(tp.joinpath(self.meta.project_name + ".py"))
            )
            main = self.meta.project_name + ":main"
        else:
            project_path = Path(self.meta.project_name)
            shutil.copytree(
                str(project_path),
                str(tp.joinpath(self.meta.project_name))
            )
            shutil.copy(
                "main.py",
                str(tp.joinpath('main.py'))
            )
            main = "main:main"
        compileall.compile_dir(str(tp), force=True, legacy=True, optimize=2)
        delete_py_source(tp)
        source = t
        zipapp.create_archive(source, target=self.meta.project_name + ".pyz", interpreter='/usr/bin/python3', main=main)
        print("1234")
        if tp.exists():
            shutil.rmtree(str(tp))

        # if self.form.project_form == "script":
        #     print("script can not build to pyz")
        # else:
        #     source = self.meta.project_name
        #     main = "main:main"
        #     zipapp.create_archive(source, interpreter='/usr/bin/python3', main=main)
        # print('build self.meta.peoject_name to pyz file done!'.format(self=self))

    def _build_cython(self):
        print('build cython model')
        command = 'python setup.py build_ext --inplace'
        if platform.system() == 'Windows':
            command = 'python setup.py build_ext --inplace -c msvc'
        subprocess.check_call(command)
        print('build cython model done!')

    # def _build_c(self):
    #     command = "conan build"
    #     subprocess.call(command, shell=True)
    #     return True

    def _build_node(self):
        print("build node project")
        command = "npm run build"
        subprocess.call(command, shell=True)
        print("build node project done!")

    def build_docker(self):
        """将项目编译为docker的image."""
        if Path("Dockfile").exists() or Path("dockerfile").exists():
            print("build docker image")
            command = "sudo docker build -t {project_name}:v{version}-{status} .".format(
                project_name=self.meta.project_name,
                version=self.meta.version,
                status=self.meta.status
            )
            subprocess.call(command, shell=True)
            print("build docker image done!")
        else:
            print("need a dockerfile")

    def build(self,
              egg: bool=False,
              wheel: bool=False,
              pyz: bool=False,
              app: bool=False,
              cython: bool=False)->None:
        """编译项目.

        Args:
            app (bool,optional): 是否打包成可执行文件(Defaults to False).
            egg (bool, optional): 是否将python项目编译为egg(Defaults to False).
            wheel (bool, optional): 是否将python项目编译为wheel(Defaults to False).
            pyz (bool, optional): 是否将python项目编译为pyz文件(Defaults to False).
            cython (bool, optional): 是否编译将cython项目(Defaults to False).

        Raises:
            AttributeError: 不支持的项目语言不编译

        """
        if self.form.compiler == "python":
            if Path("setup.py").exists():
                if cython:
                    self._build_cython()
                if egg:
                    self._build_egg()
                if wheel:
                    self._build_wheel()
            else:
                print("build model to egg,wheel,cython need file setup.py")
            if pyz:
                self._build_pyz()
            if app:
                self._build_app()

        # elif self.form.compiler == "cpp":
        #     self._build_c()

        elif self.form.compiler == "node":
            self._build_node()

        else:
            raise AttributeError("unknown compiler!")


__all__ = ["BuildMixin"]
