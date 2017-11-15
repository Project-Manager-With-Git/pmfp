# celery模板

## 默认使用的依赖

默认使用redis存结果,用rabitmq作为queue.

## 配置

修改`config`文件夹下各个不同环境的py文件以写死配置,之后再打包安装到docker

## 启动方法

项目可以使用zipapp打包,运行的话默认是使用default配置运行worker和flower,使用`worker`和`flower`命令可以单独运行,并可以用`-e`指定配置`-c`指定其他参数.使用worker的话最好使用`-c "-n xxxxx"`指定worker名以避免冲突.`all`命令可以同时运行worker和flower,也可以用-e指定配置

## 扩展方式

### 横向扩展

+ `flower`指令用于启动监控和调用服务,可以起多个然后结合nginx做负载均衡以应对高并发
+ `worker`则是用于横向扩展,多起几个worker在不同的主机上以应付大规模计算的需求

### 纵向扩展

基本上扩展任务只要在`App.tasks`中定义任务即可,而修改配置就是在`config`模块中修改即可,而模块名则在`App.celery_app`中修改

## 监控方法

可以访问用`all`或者`flower`启动的服务,有web界面可以监控

## 任务调用

任务调度同样是访问用`all`或者`flower`启动的服务可以使用api下的指令进行操作