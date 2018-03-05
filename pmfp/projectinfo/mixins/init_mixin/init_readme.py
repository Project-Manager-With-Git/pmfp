"""初始化readme的部件."""
from string import Template
from pathlib import Path


class InitReadmeMixin:
    """初始化readme混入."""

    README_RST = Template("""
$project_name
===============================

* version: $version

* status: $status

* author: $author

* email: $author_email

Desc
--------------------------------

$description


keywords:$keywords


Feature
----------------------
* Feature1
* Feature2

Example
-------------------------------

.. code:: python



Install
--------------------------------

- ``python -m pip install $project_name``


Documentation
--------------------------------

`Documentation on Readthedocs <$url>`_.



TODO
-----------------------------------
* todo

Limitations
-----------
* limit

""")

    README_MD = Template("""
# $project_name

+ version: $version
+ status: $status
+ author: $author
+ email: $author_email

## Description

$description


keywords:$keywords

## Feature

+ Feature1
+ Feature2

## Example

```python
```

## Install

`python -m pip install $project_name`


## Documentation

Documentation on github page <$url>

## TODO

+ todo1
+ todo2

## Limitations

+ limit1
+ limit2
""")

    def _init_universal_readme(self, suffix):
        up_suffix = suffix.upper()
        local_path = Path(".")
        if local_path.joinpath("README.{}".format(suffix)).exists():
            print("already have README.{}".format(suffix))

        else:
            with open(str(local_path.joinpath("README.{}".format(suffix))), "w") as f:
                readme = getattr(self.__class__, "README_" + up_suffix)
                f.write(
                    readme.substitute(
                        project_name=self.meta.project_name,
                        author=self.author.author,
                        author_email=self.author.author_email,
                        version=self.meta.version,
                        status=self.meta.status,
                        url=self.meta.url,
                        description=self.desc.description,
                        keywords=",".join(self.desc.keywords)
                    )
                )

    def _init_readme(self):
        """初始化readme文件."""
        print("writing readme.")
        for i in ("md", "rst"):
            self._init_universal_readme(i)
        print("write readme done!")


__all__ = ["InitReadmeMixin"]
