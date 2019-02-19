"""package's install entrypoint."""
import json
from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent

with open(HERE.joinpath("pmfprc.json")) as project_info_json:
    project_info = json.load(project_info_json)
classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    f'License :: OSI Approved :: {project_info.get("license")} License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Documentation :: Sphinx',
]
packages = find_packages(exclude=['contrib', 'docs', 'test'])
with open(str(HERE.joinpath('README.rst')), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=project_info["project-name"],
    version=project_info["version"],
    description=project_info["description"],
    long_description=long_description,
    url=project_info["url"],
    author=project_info["author"],
    author_email=project_info["author-email"],
    license=project_info["license"],
    classifiers=classifiers,
    keywords=project_info["keywords"],
    packages=packages,
    include_package_data=True,
    install_requires=project_info["requirement"],
    extras_require={
        'dev': project_info["requirement-dev"]
    },
    zip_safe=False
)