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

## 使用

pmfp现在被设计为两个部分:

1. `项目管理部分`用于快速根据托管在github上的模板项目构造项目
2. `调用功能部分`用于为不同的项目提供特定功能

### 项目管理



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

## 设计

ppm实际上可以认为是一个客户端-服务端架构的工具,客户端就是这个python包,服务端实际上并不是真的有个服务器,而是参考golang的设计,使用`git`项目仓库,也就是说只要是git仓库的实现就可以作为客户端要连接的服务器使用.

服务端用于保存模板,客户端用于下载模板,解析为组件并使用组件构造项目.

模板必须在根目录包含文件`.pmfp_template.json`,其格式为:

```json
{
    "language":{

    }
}
```
 