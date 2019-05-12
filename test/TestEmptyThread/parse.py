from typing import Generator

from base.components.model import ModelManager
from base.components import Parse, active
from .model import *

from base.common import HiddenInputParse
from base.tool import xpathParse, xpathParseList


@active
class TestemptythreadParse(Parse):

    def parsing(self, content: str) -> Model or Generator[Model]:
        m = ModelManager.model('TestemptythreadModel')
        m.filed = "filed content"
        yield m
