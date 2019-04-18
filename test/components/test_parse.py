import unittest
from typing import *
from types import *

from base.components import Prepare
from base.components import Action, Parse, Scheme
from base.components import Processor
from base.components import Model
from base.components.model import Field
from base.components.base import Component

from base.libs.setting import Setting


class XpathMappingParse(Parse):
    models: List[Model]

    def check(self) -> bool:
        pass

    def parsing(self, content: str) -> Model or Generator[Model]:
        pass
