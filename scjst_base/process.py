from typing import Any

from base.Model import Model
from base.Process import *
from base.Conserve import allow
from base.lib import Config

from .model import ProjectBaseModel
from .peewee_connect import ProjectBase

import redis


class PrintProcess(Process):

    def start_task(self, config: Config = None):
        self.count = 0
        pass

    @target(Model)
    def process_item(self, model: Model) -> Any:
        self.count = self.count + 1
        print(model.pure_data())

    def end_task(self):
        print(self.count)


class Duplication(DuplicateProcess):



    def config(self):
        self.base = "base:url"

    @target(ProjectBaseModel)
    def process_item(self, model: ProjectBaseModel) -> Any:
        return self.check_identification(model.url)


class BaseInfo(JsonFileProcess):

    def config(self):
        self.limit = 10000

    @target(ProjectBaseModel)
    def process_item(self, model: Model) -> Any:
        self.save_model(model)
