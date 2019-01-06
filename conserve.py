from base.Conserve import Conserve, allow
from base.Model import Model

import peewee

db = peewee.MySQLDatabase('mysql', user='root', password='87886700', host='logic-ol.me', port=3306,
                          charset='utf8mb4')


class PorxyInfo(peewee.Model):
    UID = peewee.PrimaryKeyField()
    ip = peewee.CharField()
    port = peewee.CharField()


PorxyInfo.bind(db)
PorxyInfo.drop_table()
PorxyInfo.create_table()


class DefaultConserve(Conserve):
    name = "default"

    @allow(Model)
    def feed_func(self, model: Model):
        PorxyInfo.insert_many(model.pure_data()).execute()

        print(model)
        print(model.pure_data())
