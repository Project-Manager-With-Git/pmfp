# 模板说明

这个模板用于映射和管理特定已存在的数据库

模板build后运行会自动生成一个`admin:admin`的默认管理员和`user:user`的默认用户保存在本地的sqlite数据库中.默认指定管理的数据库则是一个保存了`iris`的数据库

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
    + `sql_model.targetdb`则是目标数据库的映射

+ admin 定义视图admin中的视图

    其中
    + `admin.modelview.sql_view`用于定义model对应的view
    + `admin.modelview.my_model_view`可以直接用,也可以作为基类结合`admin.modelview.mixins`中的mixin构建指定view
    + `admin.__init__`中有方法`add_db_views`,可以对其进行修改来应用自己定义的view

+ config 定义环境设置.

    设置了默认的环境有`default`,`dev/development`,`test/testing`,`production`4种,服务启动的时候只能使用指定的环境之一,其他的默认会使用`default`环境

    + `default` 环境用于开发调试和单元测试
    + `dev/development` 环境用于性能优化和试运行,使用的测试用的`werkzeug.contrib.profiler import ProfilerMiddleware`用以分析调用情况
    + `test/testing` 环境用于压力测试和线上运行测试
    + `production` 环境用于线上正式运行

+ server 定义使用的服务器

    设置了默认的环境有`default`,`dev/development`,`test/testing`,`production`4种,服务启动的时候只能使用指定的环境之一,其他的默认会使用`default`环境.

    + `test/testing`和`production`设置的是默认使用gevent来跑服务,而其他两个都是使用自带的服务器,
    + `default`使用debug模式
    + `dev`则使用`werkzeug`的`ProfilerMiddleware`进行调用的cpu资源使用检测


+ static 静态文件地址

+ templates jinja2模板文件

    + `admin`文件夹下是`admin`uri下使用的模板
    + `security`文件夹下是登录,注册等账户管理工具模板的存放地址

+ main.py 启动文件

## 限制

+ 目标数据库外键并没有设置显示,初版只能显示python对象的字符串输出
+ 如果`SQLALCHEMY_BINDS`的`admin_users`和`SQLALCHEMY_DATABASE_URI`指定的数据库一致,那么很可能会出现冲突,因此建议`admin_users`独立使用一个数据库.本身管理员一般不会有大量用户的数据,因此完全可以用sqlite来做,这样迁移还方便些
