"""restfulapi蓝图模组.

## 使用方法

core 模块中import进默认的实例`restapi`
使用rergister(url)来将view注册至对象中
```python
@restapi.register("/")
class IndexAPI(HTTPMethodView):
    pass
```
同时注意在`__init__.py`import 进写好的class

## 注册到app的方法

```python
from api import restapi
restapi.init_app(app)
```

注意:json需要在后面加上`ensure_ascii=False`来将unicode转换
"""
from .core import restapi
from .index import *
from .user import *
