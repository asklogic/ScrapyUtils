from base.Conserve import Conserve, allow
from base.Model import Model
import scrapy_config
import os
import json
import peewee


# db = peewee.MySQLDatabase('mysql', user='root', password='87886700', host='logic-ol.me', port=3306,
#                           charset='utf8mb4')
#
#
# class PorxyInfo(peewee.Model):
#     UID = peewee.PrimaryKeyField()
#     ip = peewee.CharField()
#     port = peewee.CharField()
#
#
# PorxyInfo.bind(db)
# PorxyInfo.drop_table()
# PorxyInfo.create_table()


class DefaultConserve(Conserve):
    name = "default"

    @allow(Model)
    def feed_func(self, model: Model):
        PorxyInfo.insert_many(model.pure_data()).execute()

        print(model)
        print(model.pure_data())


class ProxyTestConserve(Conserve):
    name = "test_conserve"

    def start_conserve(self):
        self.data = []

    def end_conserve(self):
        pass
        with open(os.path.join(scrapy_config.Assets_Path, "ProxyModel.json"), "w") as f:
            json.dump(self.data, f)

    def feed_function(self, model: Model):
        print(model.pure_data())
        self.data.append(model.ip + ":" + model.port)
        pass
