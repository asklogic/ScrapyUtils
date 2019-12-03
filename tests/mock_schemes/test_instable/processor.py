from typing import Any

from base.components import Processor, active
from base.common import DumpInPeeweeProcessor, DuplicateProcessor, JsonFileProcessor

from .model import *


@active
class Test_instableProcess(Processor):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
        return model


@active
class Count(Processor):
    priority = 1000
    count = 0

    def process_item(self, model: Model) -> Any:
        self.count += 1
