# pmfp

+ version: 4.0.0
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

## 使用

pmfp现在被设计为两个部分:

1. `项目管理部分`用于快速根据托管在git仓库上的模板仓库项目构造项目
2. `调用功能部分`用于为不同的项目提供特定功能

### 项目管理

项目管理的整体设计思路是这样:

1. 借助git仓库来保存组件模板.
2. 每个组件模板使用jinja2作为模板引擎,允许使用其模板语法
3. 用于保存组件模板的git仓库称为资源包(source pack)
4. 资源包需要使用一个文件来声明其中注册的组件和默认行为,默认这个文件为资源包根目录下的`.pmfp_template.json`文件.其具体schema可以查看项目的`protocol.py`文件中的`TEMPLATE_INFO_SCHEMA`对象定义
5. 如果资源包声明文件中`template_type`不为`components`则说明这是一个模板资源包,我们就可以根据其作为模板构造项目.
6. 资源包中每个组件都有一个`source`字段,这个字段用于声明组件的位置,如果其中有`//`则说明它是引用的另一个资源项目的组件
7. 根据模板包构造项目只要指定一个资源包路径即可,其形式为`[[{host}::]{repo_namespace}::]{repo_name}[@{tag}]`
8. 如果是已有项目要添加组件,则可以使用`[[{host}::]{repo_namespace}::]{repo_name}[@{tag}]//{component_path_str}`
9. 默认的host为`github.com`,默认的repo_namespace为`Project-Manager-With-Git`,默认的tag为`latest`,如果tag为latest它会拉取master分支的head

### 直接调用功能

支持直接调用功能的子命令包括:

+ `build`快速编译支持的静态语言项目
+ `doc`快速构造项目的文档
+ `docker image`快速构造docker镜像
+ `docker compose`快速构造docker部署配置
+ `env`快速构建项目的独立执行环境
+ `grpc`快速构造了grpc的客户端和服务端
+ `http`用于构造静态http服务和构造http请求和压测
+ `pack`打包动态语言构造的项目
+ `proto`用于快速构建和编译protobuf文件
+ `schema`用于校验`jsonschema`
+ `test`用于对项目进行测试
+ `release`用于发布项目
+ `requires`用于管理依赖
