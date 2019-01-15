from typing import Any

from base.Model import Model
from base.Process import *
from .model import *


class CustomProcess(Process):

    def start_task(self, args=None):
        self.count = 0
        pass

    @target(Model)
    def process_item(self, model: Model) -> Any:
        self.count = self.count + 1
        return model
        # return False


class TestJson(JsonFileProcess):
    # name = "TestJsonName"

    @target(Model)
    def process_item(self, model: Model) -> Model:
        return super().process_item(model)


class Duplication(DuplicateProcess):
    name = "name"
    @target(Model)
    def process_item(self, model: Model) -> Any:
        return self.check_identification(str(model.name))
