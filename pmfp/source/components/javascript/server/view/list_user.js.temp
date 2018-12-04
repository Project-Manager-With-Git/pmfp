import connection from "../model/model"
const ListUser = {
  get: async (ctx) => {
    try {
      let result = await connection.get_table("User").findAll()
      ctx.body = JSON.stringify({
        "data": result
      })
    } catch (error) {
      console.log(error)
      ctx.response.status = 500
      ctx.body = JSON.stringify({
        "msg": "500 db error",
      })
    }
  },
  post: async (ctx) => {
    try {
      let pre_ins = ctx.request.body
      let result = await connection.get_table("User").create(pre_ins)
      ctx.body = JSON.stringify({
        "data": result
      })
    } catch (error) {
      ctx.response.status = 500
      ctx.body = JSON.stringify({
        "msg": "500 db error"
      })
    }
  }
}
export default ListUser