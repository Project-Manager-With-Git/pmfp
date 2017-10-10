from peewee import Model, CharField, PrimaryKeyField, Proxy

testdb_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = testdb_proxy


class Cat(BaseModel):
    id = PrimaryKeyField()
    name = CharField()

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name

        }


__all__ = ['testdb_proxy', "Cat"]
