pmfp
===============================
* version: 3.0.8
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

New in 3.0.8
^^^^^^^^^^^^^^^^^

* 修改了install命令不会将包名写入配置的bug
* `server-static_server`模板代码结构进行了优化
* 新增了koa模板,包括
    + `server-koa`带socketio和restful接口的koa模板
    + `server-koa_rest`使用rest风格接口的koa模板
    + `server-koa_socketio`使用socketio的koa模板

New in 3.0.7
^^^^^^^^^^^^^^^^^

* 修改了cython模板,使之可以和纯python配合使用,如果要让application类型的项目支持,
    + 先修改`pmfp.json`中的`template`字段,只要里面有cython字样就可以编译
    + 使用new命令`new -t "-" -r <name without suffix> cython-simple.pyx.temp`
    + 使用new命令`new -r setup.py cython_numpy_setup`或者`new -r setup.py cython_setup`创建`setup.py`文件配置编译行为
    + 之后虽然是是application,但不会打包为.pyz
* build命令现在有参数`--inplace`,专为cython模块编译项目到本地使用
* 重构grpc的客户端组件,使之可以嵌入到项目中
* 重构zerorpc的客户端组件,使之可以嵌入到项目中
* 重构xmlrpc的客户端组件,使之可以嵌入到项目中
* 重构jsonrpc的客户端组件,使之可以嵌入到项目中
* 新增node支持(babel),不再打算支持typescript,新增了相关模板:
    + `server-static_server`一个简易静态http服务器
    + `module-classmodel`一个简易的单文件node模块

New in 3.0.6
^^^^^^^^^^^^^^^^

* 增加了对cython的支持.现在支持两种模板:
    + module-cython_simple
    + module-cython_numpy
    cython模板使用c语言编译器而非c++,需要的话可以自己改setup.py
    
* build命令现在可以对module类型的python项目生效了

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