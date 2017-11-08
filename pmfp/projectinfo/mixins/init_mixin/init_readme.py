from string import Template
from pathlib import Path

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

README_MARKDOWN = Template("""
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

```


````

## Install

`python -m pip install $project_name`


## Documentation

Documentation on github page <$url>



## TODO

+ todo

## Limitations

+ limit

""")


class InitReadmeMixin:

    def _init_readme(self):
        """初始化readme文件
        只有md文件和rst文件都被初始化了才返回True
        """
        print("writing readme.")
        local_path = Path(".")
        result = [True, True]
        if local_path.joinpath("README.rst").exists():
            print("already have README.rst")
            result[0] = False
        else:
            with open(str(local_path.joinpath("README.rst")), "w") as f:
                f.write(README_RST.substitute(project_name=self.meta.project_name,
                                              author=self.author.author,
                                              author_email=self.author.author_email,
                                              version=self.meta.version,
                                              status=self.meta.status,
                                              url=self.meta.url,
                                              description=self.desc.description,
                                              keywords=",".join(self.desc.keywords)))
            result[0] = True

        if local_path.joinpath("README.md").exists():
            with open(str(local_path.joinpath("README.md"))) as f:
                n = len(f.readlines())
            if n > 50:
                print("already have README.md")
                result[1] = False
                return all(result)
            else:
                print("README.md changed")
        with open("README.md", "w") as f:
            f.write(README_MARKDOWN.substitute(project_name=self.meta.project_name,
                                               author=self.author.author,
                                               author_email=self.author.author_email,
                                               version=self.meta.version,
                                               status=self.meta.status,
                                               url=self.meta.url,
                                               description=self.desc.description,
                                               keywords=",".join(self.desc.keywords)))
        return all(result)


__all__ = ["InitReadmeMixin"]
