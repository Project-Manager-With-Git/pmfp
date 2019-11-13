import Sequelize from 'sequelize'

export class Connection {
    constructor() {
        this.TABLES = new Map()
        this.db = null
        this.callbacks = []
    }

    run_callback() {
        if (this.callbacks.length > 0) {
            for (let callback of this.callbacks) {
                callback(this.db)
            }
            this.callbacks = []
        }
    }

    init_url(url, options = {}) {
        this.db = new Sequelize(url, options)
        this.run_callback()
        return this.db
    }

    init_app(app, options = {logging:false}) {
        let dburl = app.config.get("DB_URL")
        if (dburl) {
            app.db = this.init_url(dburl, options)
            return app
        } else {
            throw "DB_URL not exist"
        }
    }

    add_callback(func) {
        this.callbacks.push(func)
    }

    register(Model) {
        const name = Model.name
        const schema = Model.schema
        const meta = Model.meta
        if (this.db) {
            this.TABLES.set(name, this.db.define(name, schema, meta))
        } else {
            let TABLES = this.TABLES
            this.add_callback(
                function (db) {
                    TABLES.set(name, db.define(name, schema, meta))
                }
            )
            if (this.db) {
                run_callback()
            }
        }
    }

    get_table(db_name) {
        return this.TABLES.get(db_name)
    }

    create_tables(table_name = null, safe = true) {
        if (safe) {
            if (table_name) {
                this.TABLES.get(table_name).sync()
            } else {
                for (let [_, table] of this.TABLES.entries()) {
                    table.sync()
                }
            }
        } else {
            if (table_name) {
                this.TABLES.get(table_name).sync({
                    force: true
                })
            } else {
                for (let [_, table] of this.TABLES.entries()) {
                    table.sync({
                        force: true
                    })
                }
            }
        }
    }

    drop_table(table_name = null) {
        if (table_name) {
            this.TABLES.get(table_name).sync()
        } else {
            for (let [_, table] of this.TABLES.entries()) {
                table.sync()
            }
        }
    }

    async moke_data() {
        if (this.get_table("User")) {

            return await this.get_table("User").bulkCreate([{
                name: "John",
                age: 18
            }, {
                name: "Josta",
                age: 20
            }, {
                name: "Janne",
                age: 15
            }, {
                name: "Auther",
                age: 18
            }])
        } else {
            throw "table user not registed"
        }
    }
    moke_dataSync() {
        if (this.get_table("User")) {
            let Model = this.get_table("User")
            Model.findAll().then(users => {
                if (users.length == 0) {
                    Model.bulkCreate([{
                        name: "John",
                        age: 18
                    }, {
                        name: "Josta",
                        age: 20
                    }, {
                        name: "Janne",
                        age: 15
                    }, {
                        name: "Auther",
                        age: 18
                    }]).then(users => {
                        console.log('{"msg":"table have moke data"}')
                    })
                } else {
                    console.log('{"msg":"table already have data"}')
                }
            })
        } else {
            throw "table user not registed"
        }
    }
}
const connection = new Connection()
export default connection