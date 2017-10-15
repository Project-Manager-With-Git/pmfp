# 模板说明

这个模板用于定义带一定限制的简单的api服务,返回的默认是json. 如果写好文档,会在主页显示api文档. api服务器可能会接收来自许多不同源的频繁调用,因此使用线程模型的flask可能并不是最好的选择,即便结合gevent,恐怕也不能与使用uvloop的sanic相比.但如果服务并不是特别需要高并发,其实也是可以用的.毕竟python3.5后的协程配套工具还不成熟.

这个模板有管理员工具,适合开放读取权限,而其他权限受限的服务.可以使用管理员权限登录`/admin`,之后再在界面上管理资源

## 特性

+ 设置`SQLALCHEMY_BINDS`的`admin_users`的数据库来作为存储管理员账户的数据库数据库使用
+ 自动映射`SQLALCHEMY_DATABASE_URI`指定的数据库中的表格
+ 可以通过设置`MANAGE_TABLES`指定管理的的表
+ 可以通过设置`MANAGE_PROJECT`指定管理项目名,默认名为`Target`

## 结构和用法描述

+ app_creater 用于生成flask的app对象

+ model 定义数据库orm

    其中的
    + `sql_model.admin`定义管理员用户和相关权限
    + `sql_model.targetdb`则是要管理的目标数据库的映射
    + `peewee_model`定义peewee的orm映射,推荐使用peewee主要是因为轻量
    + `DB_URL`需要定义一个字典来指定数据库的名字和对应的dburi

+ admin 定义视图admin中的视图

    其中
    + `admin.modelview.sql_view`用于定义model对应的view
    + `admin.modelview.my_model_view`可以直接用,也可以作为基类结合`admin.modelview.mixins`中的mixin构建指定view
    + `admin.__init__`中有方法`add_db_views`,可以对其进行修改来应用自己定义的view

+ apivx 用blueprint来注册namespace从而描述source.
    
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

+ 目标数据库外键并没有设置显示,初版只能显示python对象的字符串输出
+ 如果`SQLALCHEMY_BINDS`的`admin_users`和`SQLALCHEMY_DATABASE_URI`指定的数据库一致,那么很可能会出现冲突,因此建议`admin_users`独立使用一个数据库.本身管理员一般不会有大量用户的数据,因此完全可以用sqlite来做,这样迁移还方便些

