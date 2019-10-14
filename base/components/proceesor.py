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
        self.data = []

        self.setting = setting

        self.on_start()



    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass

    @abstractmethod
    def process_item(self, model: Model) -> Any:
        pass
