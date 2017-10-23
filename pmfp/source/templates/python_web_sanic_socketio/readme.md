# 模板说明

这个模板用于设计socketio相关的服务,socketio支持长连接,适合及时性要求比较高并且需要有状态的服务,比如聊天室这种.

## 结构和用法描述

+ app_creater 用于生成flask的app对象

+ sockets 定义socketio的命名空间

    socketio通过命名空间区分不同用户所处的群组,它被定义在`sockets.namespaces`,在使用`sockets.on_namespace`方法注册到socket对象上.
    

+ config 定义环境设置.

    设置了默认的环境有`default`,`dev/development`,`test/testing`,`production`4种,服务启动的时候只能使用指定的环境之一,其他的默认会使用`default`环境

+ server 定义使用的服务器

    设置了默认的环境有`default`,`dev/development`,`test/testing`,`production`4种,服务启动的时候只能使用指定的环境之一,其他的默认会使用`default`环境.

    默认使用eventlet作为服务器

+ main.py 启动文件

## 说明

socketio一般是作为消息推送,或者是异步任务轮询结果的替代.因此socketio往往结合多线程或者消息队列(redis)来使用
