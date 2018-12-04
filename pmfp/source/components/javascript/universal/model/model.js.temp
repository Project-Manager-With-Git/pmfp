/**
 * # 使用方法
 * 
 * + 定义数据库模型对象,包含字段: 
 *   + name 表名
 *   + schema 存储格式
 *   + meta 元数据,定义一些如db名这类的东西
 * 
 * + 使用`connection.register(Model)`将表注册到连接对象
 * + `connection.init_app(app)`将koa模板的app注册并连接数据库,或者`connection.init_url(url)`直接连接到url指定的数据库
 * + `connection.create_tables(table,safe)`可以去数据库中创建表格
 * + `connection.drop_table(table)`可以删除表
 * + `connection.get_table(table)`可以获取到指定表名的表格对象
 */
import connection from "./core"
import UserModel from "./user"
connection.register(UserModel)
export default connection