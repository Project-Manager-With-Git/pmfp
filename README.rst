pmfp
===============================
* version: 3.1.1
* status: prod
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
* 增加对github release的支持
* 添加更多模板
* 完善node支持
* 添加C语言支持


Limitations
-----------
* 只支持python3.5+
* mac osx下会有bug,venv的虚拟环境无法自动安装


Version Update
------------------

3.x版本是对之前版本的重构,相较于之前的版本使用了更加简练的写法,同时配置文件前面不加`.`号以方便自己编辑.

计划3.0.x版本的目标是将现有的模板整理重新发布,3.1.x版本的目标是支持上go语言和c语言.

3.0.3版本之前的版本具体改了多少东西已经不可考以下是更新的记录

New in 3.1.0
^^^^^^^^^^^^^^^^^^^^^^
* 为freeze命令增加解析,现在默认只固定`requirement`字段中的依赖,但可以通过`--dev`来固定开发依赖,用`--all`来固定全部依赖,`--noversion`不固定依赖的版本.
* python模板中的log使用结构化log模块
* python模板中的config部分和dataschema改用json schema
* init命令新增字段`--noinstall`,标明创建时不安装依赖
* sanic,flask,rpc项目的dockerfile中不再强制使用`pyz`
* sanic,flask,rpc项目新增docker-compose模板
* 新增了对golang的支持,目前支持的主要是grpc和gin
* build方法新增对golang交叉编译的支持
* run方法新增对golang指定入口文件的支持
* 所有提示改为中文
* 为项目增加类型注解

New in 3.0.15
^^^^^^^^^^^^^^^^^

* doc初始化增加了对国际化的支持,默认`zh`和`en`
* 可以使用doc命令`locale`新增小语种支持.
* doc命令新增了`update`


New in 3.0.14
^^^^^^^^^^^^^^^^^

* 修正了upload命令不加-m内容就显示None的bug.
* 修正了js中koa模板的一些bug


New in 3.0.13
^^^^^^^^^^^^^^^^^

* 修改模板的``setup.py.temp``,``cmd_setup.py.temp``以及``cython_setup.py.temp``和``cython_numpy_setup.py.temp``使其依赖于文件``pmfprc.json``,并修改``new setup``命令的实现.
* 修改doc的config部分文件,使版本更新依赖于项目配置文件.,并修改``new doc``命令的实现.
* 修改update命令的实现,因为已经不再需要更新``setup.py``和``document``的``config.py``了,并且现在需要修改python项目源码中的``info.py``
* 现在可以在python项目的源码文件夹根目录加一个``info.py``文件,以如下形式描述项目的自身情况

.. code:: python

    """描述项目自身状态."""
    VERSION = "3.0.12"
    STATUS = "dev"

* pmfp本身运行不再支持python 3.5

New in 3.0.12
^^^^^^^^^^^^^^^^^

* 修正创建python的module项目时因为entry字段引起的错误.
* 新增python通用的test组件,现在可以在new中使用
* TODO新增node.js对grpc的支持.
* TODO新增node.js对zerorpc的支持.

New in 3.0.11
^^^^^^^^^^^^^^^^^

* 新增js前端环境``frontend``
* 为js项目新增``eslint``作为dev依赖
* 为pmfp增加类型注解
* 部分代码微调

New in 3.0.10
^^^^^^^^^^^^^^^^^

* 新增js的前端环境``webpack``
* 新增js模板``frontend-webpack``
* 修改js下`run``子命令,执行package.json中的``start``,即行为与``npm start``一致
* 新增``version``子命令用于展示当前pmfp工具的版本
* 新增``help``子命令用于展示pmfp工具的用法

New in 3.0.9
^^^^^^^^^^^^^^^^^

* 修正了模板``task-schedule``的bug,现在可以正常生成
* 模板现在可以添加``env``,``gcc``和``entry``字段作为默认
* 修正了windows下python模板编码问题
* python模板 rpc-grpc现在可以在实现接口时使用self.app获取到它注册的app信息
* python模板 rpc-zerorpc现在可以在实现接口时使用self.app获取到它注册的app信息
* 修复python组件 database-model的bug
* 现在new操作可以在没有配置文件的地方执行

New in 3.0.8
^^^^^^^^^^^^^^^^^

* 修改了install命令不会将包名写入配置的bug
* 对``server-static_server``模板代码结构进行了优化
* 新增了koa模板,包括
    + 带socketio和restful接口的koa模板``server-koa``
    + 使用rest风格接口的koa模板``server-koa_rest``
    + 使用socketio的koa模板``server-koa_socketio``

New in 3.0.7
^^^^^^^^^^^^^^^^^

* 修改了cython模板,使之可以和纯python配合使用,如果要让application类型的项目支持,
    + 先修改``pmfp.json``中的``template``字段,只要里面有cython字样就可以编译
    + 使用new命令``new -t "-" -r <name without suffix> cython-simple.pyx.temp``
    + 使用new命令``new -r setup.py cython_numpy_setup``或者``new -r setup.py cython_setup``创建``setup.py``文件配置编译行为
    + 之后虽然是是application,但不会打包为.pyz
* build命令现在有参数``--inplace``,专为cython模块编译项目到本地使用
* 重构grpc的客户端组件,使之可以嵌入到项目中
* 重构zerorpc的客户端组件,使之可以嵌入到项目中
* 重构xmlrpc的客户端组件,使之可以嵌入到项目中
* 重构jsonrpc的客户端组件,使之可以嵌入到项目中
* 新增node支持(babel),不再打算支持typescript,新增了相关模板:
    + 一个简易静态http服务器``server-static_server``
    + 一个简易的单文件node模块``module-classmodel``

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
* 新增python组件类型``partten``,包括:
    + 异步接口的简单actor模型实现``aio_actor.py.temp``
    + 异步接口的简单发布订阅模式实现``aio_pubsub.py.temp``
    + 面向切面编程中的回调函数装饰器``callback.py.temp``
    + 面向切面编程中的简单计时器装饰器``timer.py.temp``
    + 中介模式的简单实现``mediator.py.temp``
    + 池模式的简单实现``pool.py.temp``
    + 代理模式的简单实现``proxy.py.temp``
    + 单例模式的简单实现``singleton.py.temp``
    + 用于通过url导入远程文件服务器中模块的``import hook``的``import_url.py.temp``

New in 3.0.4
^^^^^^^^^^^^^^^^
* 修正了config中导入json配置文件的一处bug

New in 3.0.3
^^^^^^^^^^^^^^^^

* 新增对celery的支持
* 为sanic新增了exception组件,用于定义全局的异常
