# celery模板

## 默认使用的依赖

默认使用redis存结果,用rabitmq作为queue.

## 使用方法

项目可以使用zipapp打包,运行的话默认是使用default配置运行worker和flower,使用`worker`和`flower`命令可以单独运行,并可以用`-e`指定配置`-c`指定其他参数.`all`命令可以同时运行worker和flower,也可以用-e指定配置

## 扩展方式

基本上扩展任务只要在`App.tasks`中定义任务即可,而修改配置就是在`config`模块中修改即可,而模块名则在`App.celery_app`中修改
