# pmfp

+ version: 3.1.0
+ status: dev
+ author: hsz
+ email: hsz1273327@gmail.com

## Description

一个用于管理python及相关开发的工具

keywords:tool,project_manager

## 特点

+ 根据模板快速构建pytho项目,支持flask,sanic,celery等
+ 简单的编译和打包指令,支持wheel,egg,cython,和docker编译
+ 快速测试
+ 文档维护,支持github page

## 注意

+ 要支持grpc或者protobuf需要安装相关依赖
  
    + 通用的编译工具:protoc
    + python: `grpcio`,`grpcio-tools`
    + node: `@grpc/proto-loader`,`async`,`google-protobuf`,`grpc`,`lodash`,`minimist`
  
## Install

`python -m pip install pmfp`


## Documentation

Documentation on github page <https://github.com/Python-Tools/pmfp>

## TODO

+ 增加对github release的支持
+ 添加更多模板
+ 完善node支持
+ 添加C语言支持
+ 添加go语言支持

## Limitations

+ 只支持python3.6+

## 版本更新

3.x版本是对之前版本的重构,相较于之前的版本使用了更加简练的写法,同时配置文件前面不加`.`号以方便自己编辑.

计划3.0.x版本的目标是将现有的模板整理重新发布,3.1.x版本的目标是支持上go语言和c语言.

3.0.3版本之前的版本具体改了多少东西已经不可考以下是更新的记录

### 3.1.1

1. 更新grpc相关的模板,使之更加好用
   1. 修改了python的grpc相关模板,使之可以更灵活的使用json格式的log
   2. 为js,python,go增加了grpc的复杂模板,这个模板可以做流输入和流输出.
   3. build_pb和new pb/grpc/grpc-streaming命令现在可以在没有pmfprc.json的情况下使用了
   4. 新增grpc-web支持,为其添加了对应的反向代理docker-compose模板
2. 替换subprocess使用run的方法
3. 为go语言新增http模板,使用的是gin框架
4. go语言的build方法可以选择编译为动态库还是静态库,使用flag`--asdll`
5. 新增模板`frontend-vue_default`用于初始化vue的web端项目

### 3.1.0

1. 为freeze命令增加解析,现在默认只固定`requirement`字段中的依赖,但可以通过`--dev`来固定开发依赖,用`--all`来固定全部依赖,`--noversion`不固定依赖的版本.
2. python模板中的log使用结构化log模块
3. python模板中的config部分和dataschema改用json schema
4. init命令新增字段`--noinstall`,标明创建时不安装依赖
5. sanic,flask,rpc项目的dockerfile中不再强制使用`pyz`
6. sanic,flask,rpc项目新增docker-compose模板
7. 新增了对golang的支持,目前支持的主要是grpc和gin
8. build方法新增对golang交叉编译的支持
9. run方法新增对golang指定入口文件的支持
10. 所有提示改为中文
11. 为项目增加类型注解

### 3.0.15

1. doc初始化增加了对国际化的支持,默认`zh`和`en`
2. 可以使用doc命令`locale`新增小语种支持.
3. doc命令新增了`update`


### 3.0.14

1. 修正了upload命令不加-m内容就显示None的bug.
2. 修正了js中koa模板的一些bug

### 3.0.13

1. 修改模板的`setup.py.temp`,`cmd_setup.py.temp`以及`cython_setup.py.temp`和`cython_numpy_setup.py.temp`使其依赖于文件`pmfprc.json`,并修改 `new setup`命令的实现.
2. 修改doc的config部分文件,使版本更新依赖于项目配置文件.,并修改`new doc`命令的实现.
3. 修改update命令的实现,因为已经不再需要更新`setup.py`和`document`的`config.py`了,并且现在需要修改python项目源码中的`info.py`
4. 现在可以在python项目的源码文件夹根目录加一个`info.py`文件,以如下形式描述项目的自身情况

    ```python
    """描述项目自身状态."""
    VERSION = "3.0.12"
    STATUS = "dev"
    ```

5. pmfp本身运行不再支持python 3.5

### 3.0.12

1. 修正创建python的module项目时因为entry字段引起的错误.
2. 新增python通用的test组件,现在可以在new中使用
3. TODO新增node.js对grpc的支持.
4. TODO新增node.js对zerorpc的支持.

### 3.0.11

1. 新增js前端环境`frontend`
2. 为js项目新增`eslint`作为dev依赖
3. 为pmfp增加类型注解
4. 部分代码微调

### 3.0.10

1. 新增js的前端环境`webpack`
2. 新增js模板`frontend-webpack`
3. 修改js下`run`子命令,执行package.json中的`start`,即行为与`npm start`一致
4. 新增`version`子命令用于展示当前pmfp工具的版本
5. 新增`help`子命令用于展示pmfp工具的用法

### 3.0.9

1. 修正了模板`task-schedule`的bug,现在可以正常生成
2. 模板现在可以添加`env`,`gcc`和`entry`字段作为默认
3. 修正了windows下python模板编码问题
4. python模板 rpc-grpc现在可以在实现接口时使用self.app获取到它注册的app信息
5. python模板 rpc-zerorpc现在可以在实现接口时使用self.app获取到它注册的app信息
6. 修复python组件 database-model的bug
7. 现在new操作可以在没有配置文件的地方执行

### 3.0.8

1. 修改了install命令不会将包名写入配置的bug
2. `server-static_server`模板代码结构进行了优化
3. 新增了koa模板,包括
    1. `server-koa`带socketio和restful接口的koa模板
    2. `server-koa_rest`使用rest风格接口的koa模板
    3. `server-koa_socketio`使用socketio的koa模板

### 3.0.7

1. 修改了cython模板,使之可以和纯python配合使用,如果要让application类型的项目支持,
    1. 先修改`pmfp.json`中的`template`字段,只要里面有cython字样就可以编译
    2. 使用new命令`new -t "-" -r <name without suffix> cython-simple.pyx.temp`
    3. 使用new命令`new -r setup.py cython_numpy_setup`或者`new -r setup.py cython_setup`创建`setup.py`文件配置编译行为
    4. 之后虽然是是application,但不会打包为.pyz
2. build命令现在有参数`--inplace`,专为cython模块编译项目到本地使用
3. 重构grpc的客户端组件,使之可以嵌入到项目中
4. 重构zerorpc的客户端组件,使之可以嵌入到项目中
5. 重构xmlrpc的客户端组件,使之可以嵌入到项目中
6. 重构jsonrpc的客户端组件,使之可以嵌入到项目中
7. 新增node支持(babel),不再打算支持typescript,新增了相关模板:
    1. `server-static_server`一个简易静态http服务器
    2. `module-classmodel`一个简易的单文件node模块

### 3.0.6

1. 增加了对cython的支持.现在支持两种模板:
    1. module-cython_simple
    2. module-cython_numpy
    cython模板使用c语言编译器而非c++,需要的话可以自己改setup.py
    
2. build命令现在可以对module类型的python项目生效了

### 3.0.5

1. 修正了python的task-celery模板的依赖问题
2. 修正了模板中几处命名错误
3. 新增了python的task-schedule模板用于创建定时执行的任务
4. 修正了build 命令对python的application类型项目打包后.pyz文件无法执行的bug
5. 新增python组件类型`partten`,包括:
    + `aio_actor.py.temp` 异步接口的简单actor模型实现
    + `aio_pubsub.py.temp`异步接口的简单发布订阅模式实现
    + `callback.py.temp` 面向切面编程中的回调函数装饰器
    + `timer.py.temp`面向切面编程中的简单计时器装饰器
    + `mediator.py.temp`中介模式的简单实现
    + `pool.py.temp`池模式的简单实现
    + `proxy.py.temp`代理模式的简单实现
    + `singleton.py.temp`单例模式的简单实现
    + `import_url.py.temp`用于通过url导入远程文件服务器中模块的`import hook`

### 3.0.4

1. 修正了config中导入json配置文件的一处bug

### 3.0.3

1. 新增对celery的支持
2. 为sanic新增了exception组件,用于定义全局的异常