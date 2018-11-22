# pmfp

+ version: 3.0.4
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
  
## Install

`python -m pip install pmfp`


## Documentation

Documentation on github page <https://github.com/Python-Tools/pmfp>

## TODO

+ 添加更多模板
+ 添加node支持
+ 添加C语言支持
+ 添加go语言支持

## Limitations

+ 只支持python3.5+
+ mac osx下会有bug,venv的虚拟环境无法自动安装

## 版本更新:

### 3.0.4

1. 修正了config中导入json配置文件的一处bug

### 3.0.3

1. 新增对celery的支持
2. 为sanic新增了exception组件,用于定义全局的异常