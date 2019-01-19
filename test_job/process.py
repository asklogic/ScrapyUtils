from typing import Any

from base.Model import Model
from base.Process import *
from .model import *


class CustomProcess(Process):

    def start_task(self, config: Config = None):
        self.count = 0

    @target(Model)
    def process_item(self, model: Model) -> Any:
        self.count = self.count + 1
        return model


class TestJson(JsonFileProcess):

    @target(Model)
    def process_item(self, model: Model) -> Model:
        return self.save_model(model)


class Duplication(DuplicateProcess):
    @target(Model)
    def process_item(self, model: Model) -> Any:
        return self.check_identification(str(model.name))
