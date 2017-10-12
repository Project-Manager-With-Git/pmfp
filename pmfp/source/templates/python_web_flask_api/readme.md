# 模板说明

这个模板用于定义简单的api服务,返回的默认是json. 如果写好文档,会在主页显示api文档. api服务器可能会接收来自许多不同源的频繁调用,因此使用线程模型的flask可能并不是最好的选择,即便结合gevent,恐怕也不能与使用uvloop的sanic相比.但如果服务并不是特别需要高并发,其实也是可以用的.毕竟python3.5后的协程配套工具还不成熟.

## 结构和用法描述

+ app_creater 用于生成flask的app对象

+ model 定义数据库orm

    其中的
    + `peewee_model`定义peewee的orm映射,推荐使用peewee主要是因为轻量
    + `DB_URL`需要定义一个字典来指定数据库的名字和对应的dburi

+ apis 用namespace来定义source的描述.
    
    比如一般一个表的描述,会包括对表整体的描述和对表中某元素的描述,往往会使用不同的uri描述.一个类继承Source,只能绑定一个uri.namspace用来归类一组对同一source的描述更便于管理.


+ config 定义环境设置.

    设置了默认的环境有`default`,`dev/development`,`test/testing`,`production`4种,服务启动的时候只能使用指定的环境之一,其他的默认会使用`default`环境

    + `default` 环境用于开发调试和单元测试
    + `dev/development` 环境用于性能优化和试运行
    + `test/testing` 环境用于压力测试和线上运行测试
    + `production` 环境用于线上正式运行

+ server 定义使用的服务器

    设置了默认的环境有`default`,`dev/development`,`test/testing`,`production`4种,服务启动的时候只能使用指定的环境之一,其他的默认会使用`default`环境.

    + `test/testing`和`production`设置的是默认使用gevent来跑服务,而其他两个都是使用自带的服务器,
    + `default`使用debug模式
    + `dev`则使用`werkzeug`的`ProfilerMiddleware`进行调用的cpu资源使用检测

+ main.py 启动文件

## 限制

+ 没有权限管理和用户管理

    用户管理要看架构和用途,有的架构用户管理是有专门的服务器的,而有的架构则更倾向于自治,是单独维护的.像对外暴露的接口就适合统一的管理用户权限,而且颗粒度需要细些,而如果是为前端提供的则不需要很细的颗粒度,如果是内部处理数据代替rpc用的则可以不需要权限管理,毕竟这也要消耗资源的.