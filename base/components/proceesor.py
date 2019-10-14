from abc import abstractmethod
from typing import Any

from base.components.base import ComponentMeta, Component
from base.libs.setting import Setting
from base.libs import Model


class ProcessorMeta(ComponentMeta):

    def __new__(cls, name, bases, attrs: dict):
        # default target : Model
        if not attrs.get("target"):
            attrs["target"] = Model
        return super().__new__(cls, name, bases, attrs)


class Processor(Component, metaclass=ProcessorMeta):
    target: type(Model)
    data: []

    setting: Setting

    def __init__(self, setting: Setting = Setting()):
        self.count: int = 0
        self.next: Processor = None
        self.data = []

        self.setting = setting

    @abstractmethod
    def start_task(self, setting: Setting):
        pass

    @abstractmethod
    def start_process(self, number: int, model: str = "Model"):
        pass

    @abstractmethod
    def end_process(self):
        pass

    @abstractmethod
    def end_task(self):
        pass

    @abstractmethod
    def process_item(self, model: Model) -> Any:
        pass
