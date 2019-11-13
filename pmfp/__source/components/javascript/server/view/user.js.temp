import connection from "../model/model"


const User = {
  get: async (ctx, name) => {
    try {
      let result = await connection.get_table("User").findAll({
        where: {
          name: name
        }
      })
      if (result.length > 1) {
        ctx.body = JSON.stringify({
          "data": result[0]
        })
      } else {
        ctx.response.status = 404
        ctx.body = JSON.stringify({
          "msg": "404 user not found"
        })
      }

    } catch (error) {
      ctx.response.status = 500
      ctx.body = JSON.stringify({
        "msg": "500 db error"
      })
    }
  },

  put: async (ctx, name) => {
    let change = ctx.request.body
    try {
      let result = await connection.get_table("User").update(
        change, {
          where: {
            name: name
          }
        })
      ctx.body = JSON.stringify({
        "data": result
      })
    } catch (error) {
      ctx.response.status = 500
      ctx.body = JSON.stringify({
        "msg": "500 db error"
      })
    }
  },
  delete: async (ctx, name) => {
    try {
      let result = await connection.get_table("User").destroy({
        where: {
          name: name
        }
      })
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

export default User