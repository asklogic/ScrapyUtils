from typing import Any

from base.Model import Model
from base.Process import Process
from base.Conserve import allow

from .model import ProjectBaseModel
from .peewee_connect import ProjectBase

import redis


class TestProcess(Process):

    def start_task(self):
        self.count = 0
        self.insert = 0
        self.url = []
        print("start task!")

    def start_process(self):
        print("start process ", self.count)

    @allow(ProjectBaseModel)
    def process_item(self, model: ProjectBaseModel) -> Any:
        self.count += 1
        if not model.url in self.url:
            self.url.append(model.url)
            self.insert += 1
        return model

    def end_task(self):
        print("url len: ", len(self.url))
        print("insert: ", self.insert)


class DuplicateProcess(Process):

    def start_task(self):
        self.db = redis.Redis(decode_responses=True)
        self.name = "base:url:"

    def load_identification(self):
        pass

    def check_identification(self, key):
        """
        存在key 返回True
        不存在key 返回False
        :param key:
        :return:
        """
        return bool(self.db.keys(self.name + key))

    def save_identification(self, key):
        self.db.set(self.name + key, 1)

    @allow(ProjectBaseModel)
    def process_item(self, model: ProjectBaseModel) -> Any:
        key = model.url
        if self.check_identification(key):
            return False
        else:
            self.save_identification(key)
            return model

class MysqlProcess(Process):

    def start_process(self):
        self.data = []

    @allow(ProjectBaseModel)
    def process_item(self, model: ProjectBaseModel) -> Any:
        self.data.append(model.pure_data())

    def end_process(self):
        if self.data:
            ProjectBase.insert_many(self.data).execute()