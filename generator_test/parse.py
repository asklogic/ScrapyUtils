from typing import Generator

from base.Model import ModelManager, Model
from base.Parse import Parse
from .model import *

from base.tool import xpathParse, xpathParseList


class Generator_testParse(Parse):
    def parsing(cls, content: str, manager: ModelManager) -> Model or Generator[Model]:
        pass
