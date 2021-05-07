# v4.0.4

## bug修复

1. 修复依赖错误

# v4.0.3

## bug修复

1. 修复了python项目创建时的bug
2. 修复依赖不全安装报错的bug

# v4.0.2

## bug修复

1. 修复了python新建环境时报错的bug

## 改进

1. 修改了模板的类型枚举
2. `project as_template`子命令现在也会生成测试依赖了
3. 修改了`env new`的参数,改为必须有language而非env
4. 修改`project new`,现在env不是必填的参数,如果指定了template则可以不再指定language,如果没有则必须指定language

# v4.0.1

## bug修复

1. 修正了cache clean命令无法执行的bug

## 改进

1. 修改protocol,支持不声明language的组件
2. 修改cc和cxx为全局项目配置
3. 修改golang_version,python_version,node_version为全局项目配置

# v4.0.0

4.0.0版本在整体架构和使用方式上都做出了大规模修改,现在多数功能都可以脱离`pmfprc.json`单独执行.`pmfprc.json`的作用现在只是一个存储默认参数的特殊文件,没有也可以执行.同时改用git仓库作为模板保存工具,从而增强扩展性同时减小pmfp的大小

## 新特性

1. 功能性操作全部不再依赖`pmfprc.json`
2. 使用git仓库作为模板保存位置.

## 移除的特性(后续版本会回来)

1. 移除对python 3.6以下的支持,本工具必须使用python3.6以上的版本