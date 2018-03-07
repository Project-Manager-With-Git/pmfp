"""创建混入."""
from string import Template
from pathlib import Path


class InitDockerMixin:
    """创建dockerfile的混入."""

    PYTHON_WEB_DOCKER_TEMPLATE = Template("""FROM python:last
ADD ./$project_name.pyz /code/$project_name.pyz
ADD ./requirements/requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
""")
    PYTHON_SCRIPT_DOCKER_TEMPLATE = Template("""FROM python:last
ADD ./$project_name.py /code/$project_name.py
ADD ./requirements/requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
""")

    CELERY_DOCKER_TEMPLATE = Template("""FROM python:last
ADD ./* /code
WORKDIR /code
RUN python setup.py install
""")

    FRONTEND_DOCKER_TEMPLATE = Template("""""")

    PYTHON_DOCKER_TEMPLATES = {
        "sanic": PYTHON_WEB_DOCKER_TEMPLATE,
        "flask": PYTHON_WEB_DOCKER_TEMPLATE,
        "celery": CELERY_DOCKER_TEMPLATE,
        'script': PYTHON_SCRIPT_DOCKER_TEMPLATE
    }

    NODE_DOCKER_TEMPLATES = {
        "vue": FRONTEND_DOCKER_TEMPLATE,
        "script": FRONTEND_DOCKER_TEMPLATE
    }

    def init_docker(self)->None:
        """初始化一个dockerfile.

        Raise:
            AttributeError: - 项目类型未被支持

        """
        print("copy dockerfile template")

        local_path = Path(".").absolute()
        if local_path.joinpath("Dockerfile").exists():
            print(str(local_path.joinpath("Dockerfile")) + " exists")
        else:
            try:
                temp = getattr(self, "{}_DOCKER_TEMPLATES".format(self.form.compiler.upper()))
                content = temp.get(
                    self.form.project_form
                ).substitute(
                    project_name=self.meta.project_name
                )
            except:
                print("unknown project type")
                return
            else:
                with open(str(local_path.joinpath("Dockerfile")), "w") as f:
                    f.write(content)
                print("create a dockerfile for this project!")


__all__ = ["InitDockerMixin"]
