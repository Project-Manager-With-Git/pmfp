"""模块的公开方法.

避免让外部直接访问定义的对象,以此来进行解耦.
"""
import contextlib
from typing import Type
from playhouse.db_url import connect
from .user import User
from ._base import (
    db,
    BaseModel,
    Tables
)


def bind_db(dburl: str):
    """指定数据库的url初始化代理对象并创建表.

    Args:
        dburl (str): 支持peewee所支持的数据库url写法
    """
    database = connect(dburl)
    db.initialize(database)
    db.create_tables(list(Tables.values()), safe=True)


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
    User.insert_many(data_source).execute()


@contextlib.contextmanager
def query():
    """确保对数据库的请求有连接可用,并且在使用完后关闭连接的上下文管理器."""
    try:
        db.connect()
    except:
        pass
    yield db
    db.close()


__all__ = ["drop_tables", "bind_db", "get_table", "query"]