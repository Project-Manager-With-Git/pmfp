# pmfp

+ version: 4.0.0-per
+ status: dev
+ author: hsz
+ email: hsz1273327@gmail.com

## Description

一个用于管理项目及相关开发的工具

keywords: tool,project_manager

## 特点

+ 可以独立使用功能模块
+ 根据模板快速构建项目
+ 简单的编译和打包指令
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

## 设计

ppm实际上可以认为是一个客户端-服务端架构的工具,客户端就是这个python包,服务端实际上并不是真的有个服务器,而是参考golang的设计,使用`git`项目仓库,也就是说只要是git仓库的实现就可以作为客户端要连接的服务器使用.

服务端用于保存模板,客户端用于下载模板,解析为组件并使用组件构造项目.

### 项目

我们定义一个项目为一个使用单一代码仓库单独维护的代码集合.

现在把项目分成了如下几类:
+ `package`多语言的模块包,比如典型的tensorflow项目,uvloop项目.
+ `application`单语言的应用项目,可执行,比如一个grpc服务项目,一个vue前端项目.
+ `tool`单语言的命令行工具项目.
+ `module`单语言的模块项目.

C:\Users\hsz12\Documents\WORKSPACE\PythonTools\pmfp\main.py

/Users/huangsizhe/Workspace/Python-Tools/pmfp/main.py

一个项目的结构大致如下:

```bash
项目\
    |--\
    |  |-组件
    |  |-组件
    |
    |
    |--\
    |  |-组件
    |
    |-pmfprc.json
    ...
```

### 综合项目组

相比上一个大版本这版最重要的就是要解决多项目联动的问题,主要包括:

+ 多个项目构成的项目组维护.
+ 项目组联调配置维护

### 构造项目的数据流

```bash
命令行设定项目配置,确定用到的模块列表
    |
    V
客户端去模块对应的git仓库拉取模块配置模板
    |
    V
模板形式是否为模块组合配置
    |
    |--------------------|
    是                   否
    |                    |
    V                    V
去指定的模块拉取模块      在拉取的模板中查找模块
```

## TODO



## Limitations

+ 只支持python3.6+

## 版本更新

4.x版本是相对于之前版本的重构,之前的版本只能维护单语言单任务项目,4.x版本的目的就是为了支持多语言多任务的项目.

4.x版本将统一使用`jsonschema`来定义配置格式.

### v4.0.0

