from typing import Generator, List

from ScrapyUtils.components import ParseStep, active, set_active
from .model import *

from ScrapyUtils.common import HiddenInputParse
from ScrapyUtils.tool import xpathParse, xpathParseList, XpathParser


@active
class AtomParse(ParseStep):

    def parsing(self) -> Model or Generator[Model]:
        parser = XpathParser(self.content)
        
        m = AtomModel()
        m.filed = "filed content"
        yield m

    def check(self, models: List[Model]):
        pass
