"""用于设定和验证数据格式的组件.

用法:

先需要在目录下自己定义格式

>>> user_schema = register_schema(
...     "user",
...     {
...         'name': str,
...         'age': int
...     }
... )

注意需要在`_methods.py`中将自己写的模块import进来

之后外部引用该模块后可以使用`get_schema`方法获取注册好的格式.

>>> get_schema("user")({"name":"qweq","age":123})
{'name': 'qweq', 'age': 123}

"""
from .methods import get_schema
