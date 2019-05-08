from typing import Generator

from base.components.model import ModelManager
from base.components.scheme import Parse
from .model import *

from base.common import XpathMappingParse


class TestMockThreadParse(Parse):
    _active = True

    def parsing(self, content: str) -> Model or Generator[Model]:
        m = ModelManager.model('TestMockThreadModel')
        m.filed = "filed content"
        yield m



