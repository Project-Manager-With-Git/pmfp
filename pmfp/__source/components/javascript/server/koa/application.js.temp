import Application from "./core"
import router from "./view/view"
import connection from "./model/model"
import io from "./sio/sio"

function init_app(config) {
  let app = new Application(config)
  connection.init_app(app)
  connection.create_tables()
  connection.moke_dataSync()
  io.attach(app.server, {
    pingInterval: 10000,
    pingTimeout: 5000,
    cookie: false
  })
  app.use(router)
  return app
}
export default init_app