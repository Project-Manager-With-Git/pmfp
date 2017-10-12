# 模板说明

这个模板用于设计socketio相关的服务,socketio支持长连接,适合及时性要求比较高并且需要有状态的服务,比如聊天室这种.

## 结构和用法描述

+ app_creater 用于生成flask的app对象

+ namespace 定义socketio的命名空间

    socketio通过命名空间区分不同用户所处的群组
    + `admin.modelview.sql_view`用于定义model对应的view
    + `admin.modelview.my_model_view`可以直接用,也可以作为基类结合`admin.modelview.mixins`中的mixin构建指定view
    + `admin.__init__`中有方法`add_db_views`,可以对其进行修改来应用自己定义的view

+ config 定义环境设置.

    设置了默认的环境有`default`,`dev/development`,`test/testing`,`production`4种,服务启动的时候只能使用指定的环境之一,其他的默认会使用`default`环境

+ server 定义使用的服务器

    设置了默认的环境有`default`,`dev/development`,`test/testing`,`production`4种,服务启动的时候只能使用指定的环境之一,其他的默认会使用`default`环境.

    `test/testing`和`production`设置的是默认使用gevent来跑服务,而其他两个都是使用自带的服务器,并且是debug模式

+ static 静态文件地址

+ templates jinja2模板文件

    + `admin`文件夹下是`admin`uri下使用的模板
    + `security`文件夹下是登录,注册等账户管理工具模板的存放地址

+ main.py 启动文件

## 限制

+ 目标数据库外键并没有设置显示,初版只能显示python对象的字符串输出
+ 如果`SQLALCHEMY_BINDS`的`admin_users`和`SQLALCHEMY_DATABASE_URI`指定的数据库一致,那么很可能会出现冲突,因此建议`admin_users`独立使用一个数据库.本身管理员一般不会有大量用户的数据,因此完全可以用sqlite来做,这样迁移还方便些
