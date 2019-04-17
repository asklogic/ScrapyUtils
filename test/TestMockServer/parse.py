from typing import Generator

from base.components.model import ModelManager
from base.components.scheme import Parse
from .model import *


class TestMockServerParse(Parse):
    _active = True

    def parsing(self, content: str) -> Model or Generator[Model]:
        m = ModelManager.model('TestMockServerModel')
        m.filed = "filed content"
        yield m
