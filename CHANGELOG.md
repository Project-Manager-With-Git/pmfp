# v4.1.3

## bug修复

+ 修正`proto build`和`grpc build`因为`source_relative`字段改动造成无法使用的问题

# v4.1.2

## 变动

+ `proto build`命令针对js语言增加了参数`js_import_style`
+ `proto build`命令针对go语言增参数`source_relative`改为`go_source_relative`
+ `grpc build`命令针对js语言增加了参数`js_import_style`,`web`,`web_import_style`和`web_mode`来细化js模块的使用环境
+ `grpc build`命令针对go语言增参数`source_relative`改为`go_source_relative`
+ `grpc build`命令现在加回了对c++的支持

# v4.1.1

## 变动

1. `grpc build`接口变动,新增字段`serv_file`用于指定定义rpc接口的文件.针对python的编译会将两个文件放在`{serv_file}_pb`模块下
2. 删除`grpc build`使用的jinja2模板
3. 暂时取消了`grpc build`对c++的支持

## bug修复

1. 修复`grpc build`对python时会一直往`__init__.py`中写东西的bug

# v4.1.0

## 新增特性

1. 现在模板配置的`template_keys`字段支持新字段`ask(boolean)`,用于让pmfp提示用户输入key的取值
2. go语言的`env new`可以指定依赖了

## 变动

1. grpc现在不再用于构造基于模板的项目,grpc项目现在也将使用project命名构造.grpc的build命令将只用于编译grpc的proto到目标语言的模块
2. go语言的`require install`命令当不指定`-n`时使用`go mod tidy`更新依赖

## bug修复

1. 修复`docker image build --push`报错的问题
2. 修复`docker image build`逻辑错误

# v4.0.10

## bug修复

1. 修正`project new`时参数覆盖顺序的问题,现在越浅层会覆盖深层

# v4.0.9

## 改进

1. 改进了grpc query和grpc stress的使用,`-d/--payload`现在指向一个写着请求json的地址,默认为`query.json`,新增`-s/--service`,用户不再需要记怎么将service和method组合了

# v4.0.8

## bug修复

1. 修正了`env new`无法给已经初始化过的项目创建执行环境的bug
2. 修正了`project as_temp`无法转换dockerfile和docker-compose的问题
3. 修正了`project as_temp`转换文件后source字段不加`.jinja`的问题
4. 修正了`project new`和`project add`不会将项目信息作为参数的问题

## 改进

1. 新增快捷命令`install`相当于`requires install`
2. 新增快捷命令`uninstall`相当于`requires uninstall`
3. 命令`build`和`pack`合并,重新整理,这条命令现在用于打包项目到可分发状态
4. 命令`env new`针对python,当对应参数没有填时会添加默认的`tests_require`和`setup_requires`
5. 命令`env new`针对cython,当对应参数没有填时会添加默认的`tests_require`和`setup_requires`
6. `project new`现在当组件不存在时会提示是什么组件

# v4.0.7

## 改进

1. 修改了project new的执行顺序,现在先拉取模板再创建执行环境
2. 现在project new执行报错后会删除这步操作时创建文件和文件夹
3. 现在project new执行过程中使用Ctrl+Break或者Ctrl+C(KeyboardInterrupt, SystemExit)终端执行时也会删除这步操作时创建的文件和文件夹

# v4.0.6

## bug修复

1. 修正了version命令展示过期版本问题
2. 修正了project add和project new时无法使用自定义key作为路径参数的bug
3. 修正了project new时外部组件不能使用模板定义的参数的问题

# v4.0.5

## bug修复

1. 修正了gomod中加载项目依赖信息的错误
2. 修正了project as_temp在没有依赖时也会添加null的错误

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
