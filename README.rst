pmfp
===============================
* version: 3.0.5
* status: dev
* author: hsz
* email: hsz1273327@gmail.com


Desc
--------------------------------
一个用于管理python及相关开发的工具

keywords:tool,project_manager


Feature
----------------------
* 根据模板快速构建pytho项目,支持flask,sanic,celery等
* 简单的编译和打包指令,支持wheel,egg,cython,和docker编译
* 快速测试
* 文档维护,支持github page




Install
--------------------------------
- ``python -m pip install pmfp``


Documentation
--------------------------------
`Documentation on Readthedocs <https://github.com/Python-Tools/pmfp>`_.


TODO
-----------------------------------
* 添加更多模板
* 添加node支持
* 添加C语言支持
* 添加go语言支持


Limitations
-----------
* 只支持python3.5+
* mac osx下会有bug,venv的虚拟环境无法自动安装


Version Update
------------------

3.x版本是对之前版本的重构,相较于之前的版本使用了更加简练的写法,同时配置文件前面不加`.`号以方便自己编辑.

计划3.0.x版本的目标是将现有的模板整理重新发布,3.1.x版本的目标是支持上go语言和c语言.

3.0.3版本之前的版本具体改了多少东西已经不可考以下是更新的记录

New in 3.0.5
^^^^^^^^^^^^^^^^

* 修正了python的task-celery模板的依赖问题
* 修正了模板中几处命名错误
* 新增了python的task-schedule模板用于创建定时执行的任务
* 修正了build 命令对python的application类型项目打包后.pyz文件无法执行的bug
* 新增python组件类型`partten`,包括:
    + `aio_actor.py.temp` 异步接口的简单actor模型实现
    + `aio_pubsub.py.temp`异步接口的简单发布订阅模式实现
    + `callback.py.temp` 面向切面编程中的回调函数装饰器
    + `timer.py.temp`面向切面编程中的简单计时器装饰器
    + `mediator.py.temp`中介模式的简单实现
    + `pool.py.temp`池模式的简单实现
    + `proxy.py.temp`代理模式的简单实现
    + `singleton.py.temp`单例模式的简单实现
    + `import_url.py.temp`用于通过url导入远程文件服务器中模块的`import hook`

New in 3.0.4
^^^^^^^^^^^^^^^^
* 修正了config中导入json配置文件的一处bug

New in 3.0.3
^^^^^^^^^^^^^^^^

* 新增对celery的支持
* 为sanic新增了exception组件,用于定义全局的异常