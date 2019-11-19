"""模块的公开方法.

避免让外部直接访问定义的对象,以此来进行解耦.
"""
import asyncio
from typing import Type
import peewee_async
import peewee_asyncext
from playhouse.db_url import connect
from .user import User
from ._base import (
    db,
    BaseModel,
    Tables
)


def bind_db(dburl: str, loop: asyncio.BaseEventLoop =None):
    """指定数据库的url初始化代理对象并创建表.

    Args:
        dburl (str): 支持peewee所支持的数据库url写法
        loop (asyncio.BaseEventLoop, optional): Defaults to None. 指定事件循环
    """

    database = connect(dburl)
    db.initialize(database)
    loop = loop or asyncio.get_event_loop()
    db.create_tables(list(Tables.values()), safe=True)
    db_manager = peewee_async.Manager(db)
    return db_manager


def drop_tables():
    """清理数据库.

    注意通常用于测试环境或清理脚本
    """
    db.drop_tables(list(Tables.values()), safe=True)
    db.close()


def get_table(name: str)->Type[BaseModel]:
    """避免暴露类而使用一个方法来作为工厂.

    Args:
        name (str): 表名

    Returns:
        Type[BaseModel]: [description]
    """
    return Tables.get(name)


def moke_data():
    """创建假数据.

    通常用于测试环境.
    """

    data_source = [
        {
            "age": 11,
            "name": "Liu"
        },
        {
            "age": 10,
            "name": "Li"
        },
        {
            "age": 11,
            "name": "Lu"
        },
        {
            "age": 9,
            "name": "Xu"
        },
    ]
    iq = User.insert_many(data_source)
    iq.execute()


__all__ = ["drop_tables", "bind_db", "get_table", "moke_data"]
