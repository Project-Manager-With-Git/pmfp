from string import Template
from pathlib import Path

WEB_DOCKER_TEMPLATE = Template("""FROM python:last
ADD ./$project_name.pyz /code/$project_name.pyz
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

DOCKER_TEMPLATES = {
    "web": WEB_DOCKER_TEMPLATE,
    "celery": CELERY_DOCKER_TEMPLATE,
    "frontend": FRONTEND_DOCKER_TEMPLATE
}


class InitDockerMixin:

    def init_docker(self)-> bool:
        '''
        初始化一个dockerfile
        Parameters:
            project_type (str): - 项目类型
            project_name (str): - 项目名
        Returns:
            bool: - 初始化是否成功
        Raise:
            AttributeError: - 项目类型未被支持
        '''
        print("copy dockerfile template")
        if self.with_dockerfile is False:
            return False
        else:
            local_path = Path(".").absolute()
            if local_path.joinpath("Dockerfile").exists():
                print(str(local_path.joinpath("Dockerfile")) + " exists")
                return False
            else:
                try:
                    content = DOCKER_TEMPLATES[self.form.project_type].substitute(
                        project_name=self.meta.project_name)
                except:
                    raise AttributeError("unknown project type")
                else:
                    with open(str(local_path.joinpath("Dockerfile")), "w") as f:
                        f.write(content)
                    print("copy dockerfile template done!")
                    return True


__all__ = ["InitDockerMixin"]
