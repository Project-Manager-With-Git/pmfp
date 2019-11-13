/**
 * # 使用
 * 
 * + 定义纯异步方法对象
 * + 将异步方法注册到api
 */
import route from "koa-route"
import compose from "koa-compose"
import Main from "./main"
import User from "./user"
import ListUser from "./list_user"

const router = compose(
    [
        route.get('/api/', Main.get),
        route.get('/api/user', ListUser.get),
        route.post('/api/user', ListUser.post),
        route.get('/api/user/:name', User.get),
        route.put('/api/user/:name', User.put),
        route.delete('/api/user/:name', User.delete)
    ]
)
export default router