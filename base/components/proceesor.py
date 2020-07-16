from abc import abstractmethod
from typing import Any

from base.components.base import ComponentMeta, Component
from base.libs import Model


class ProcessorMeta(ComponentMeta):

    def __new__(cls, name, bases, attrs: dict):
        # default target : Model
        """
        Args:
            name:
            bases:
            attrs (dict):
        """
        if not attrs.get("target"):
            attrs["target"] = Model
        return super().__new__(cls, name, bases, attrs)


class Processor(Component, metaclass=ProcessorMeta):
    target: type(Model) = Model
    data: [] = None
    count: int = 0

    config: dict = None

    def __init__(self, config: dict = None):
        """
        Args:
            config (dict):
        """
        self.count: int = 0
        self.data = []

        self.config = config

    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_exit(self):
        pass

    @abstractmethod
    def process_item(self, model: Model) -> Any:
        """
        Args:
            model (Model):
        """
        pass
