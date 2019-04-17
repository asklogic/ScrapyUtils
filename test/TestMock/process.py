from typing import Any

from base.components.proceesor import Processor

from .model import *


class TestMockProcess(Processor):
    _active = True

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
        return model        
