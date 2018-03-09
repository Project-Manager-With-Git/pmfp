"""执行项目下的脚本."""
import subprocess
from pathlib import Path


class RunMixin:
    """执行项目的混入类.

    需要PythonPathMixin混入
    """

    def _python_run(self, cmd: str)->None:
        """执行python项目或脚本.

        python项目会在cmd非空时,使用env定义的python解释器执行相应的指令,
        但cmd为空时,语义改为执行项目,执行项目的优先级顺序为

        <project_name>.py > <project_name>.pyz > <project_name>/main.py

        Args:
            cmd (str, optional): - 要执行的命令(Defaults to "")

        Raises:
            AttributeError: - python下当指令为空且执行项目优先级顺序中的文件都不存在或者找不到python_path时时抛出

        """
        if cmd == "":
            if Path(self.meta.project_name + ".py").exists():
                cmd = self.meta.project_name + ".py"
            if Path(self.meta.project_name).exists() and Path(self.meta.project_name).is_dir():
                cmd = Path("main.py")
            if Path(self.meta.project_name + ".pyz").exists():
                cmd = self.meta.project_name + ".pyz"
            print("run:")
            print(cmd)
        if cmd == "":
            print("need a cmd")
            raise AttributeError("need a cmd")
        python_path = self._get_python_path()
        if python_path:
            command = "{python_path} {cmd}".format(
                python_path=python_path, cmd=cmd)
            subprocess.call(command, shell=True)
        else:
            raise AttributeError("no python path")

    def _node_run(self, cmd: str)->None:
        """执行node项目或者脚本.

        node项目在cmd非空时执行`npm run`;而在cmd为空值时使用`node --use_strict <cmd>`执行
        注意要先将es6或者typescript 编译为node可运行的代码

        Args:
            cmd (str, optional): - 要执行的命令(Defaults to "")
        """
        if cmd == "":
            command = "npm run"
        else:
            command = "node --use_strict {cmd}".formmat(cmd=cmd)
        subprocess.call(command, shell=True)

    def run(self, cmd: str="")->None:
        """执行项目或指令.

        python项目会在cmd非空时,使用env定义的python解释器执行相应的指令,
        但cmd为空时,语义改为执行项目,执行项目的优先级顺序为

        ```
        <project_name>.py > <project_name>.pyz > <project_name>/main.py
        ```

        node项目在cmd非空时执行`npm run`;而在cmd为空值时使用`node --use_strict <cmd>`执行

        Args:
            cmd (str, optional): - 要执行的命令(Defaults to "")

        Raises:
            AttributeError: - python下当指令为空且执行项目优先级顺序中的文件都不存在或者找不到python_path时时抛出

        """
        SUP_COM = {
            "python": self._python_run,
            "node": self._node_run
        }
        SUP_COM.get(
            self.form.compiler,
            lambda x: print("unknown compiler!")
        )(cmd)


__all__ = ["RunMixin"]
