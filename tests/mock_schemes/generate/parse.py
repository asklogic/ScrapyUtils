from typing import Generator, List

from base.components import ParseStep, active
from .model import *

from base.common import HiddenInputParse
from base.tool import xpathParse, xpathParseList


@active
class GenerateParse(ParseStep):

    def parsing(self) -> Model or Generator[Model]:
        m = GenerateModel()
        m.filed = "filed content"
        yield m

    def check(self, models: List[Model]):
        pass
