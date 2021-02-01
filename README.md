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


