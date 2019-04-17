from typing import Generator

from base.components.model import ModelManager
from base.components.scheme import Parse
from .model import *


class TestMockCustomParse(Parse):
    _active = True

    def parsing(self, content: str) -> Model or Generator[Model]:
        m = ModelManager.model('TestMockCustomModel')
        m.filed = "filed content"
        yield m
