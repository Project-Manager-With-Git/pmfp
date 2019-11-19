from model import bind_db, drop_tables, moke_data
from .method import hooks


@hooks.register('after_server_start')
async def setup_db(app, loop):
    db_manager = bind_db(app.config["DB_URL"], loop=loop)
    app.db_manager = db_manager
    await app.db_manager.connect()
    if app.config.DEBUG:
        print("debug model, moke data")
        moke_data()


@hooks.register('after_server_stop')
async def setup_db(app, loop):
    if app.config.DEBUG:
        print("debug model,delete moke data")
        drop_tables()


__all__ = ["setup_db"]
