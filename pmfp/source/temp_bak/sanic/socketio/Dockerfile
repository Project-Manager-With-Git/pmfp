FROM python:last
ADD ./$project_name.pyz /code/$project_name.pyz
ADD ./static /code/static
ADD ./templates /code/templates
ADD ./requirements/requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt