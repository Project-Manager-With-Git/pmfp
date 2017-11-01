from .cat import Cat, testdb_proxy


database_proxys = {"test": testdb_proxy}


def init_db(db):
    """create tables and insert default data for database
    """
    try:
        db.create_tables((Cat,))
        print("table created")
        with db.atomic():
            Cat.insert_many([
                {"name": "hello"},
                {"name": "kitty"}
            ]).execute()
        print("default data inserted")
    except Exception as e:
        print(e)
        print("db already exist")
        return False
    else:
        return True
