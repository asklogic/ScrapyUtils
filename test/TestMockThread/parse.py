from typing import Generator

from base.Model import ModelManager, Model
from base.scheme import Parse
from .model import *

from base.tool import xpathParse, xpathParseList
from base.common import DefaultXpathParse, HiddenInputParse


class TestMockThreadParse(Parse):
    _active = True

    def parsing(self, content: str) -> Model or Generator[Model]:
        m = ModelManager.model('TestMockThreadModel')
        m.filed = "filed content"
        yield m


class Mapping(DefaultXpathParse):
    mapper_model = TestMockThreadModel
    auto_yield = True
