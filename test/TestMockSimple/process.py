from typing import Any

from base.Model import Model
from base.Process import Processor
from base.common import JsonFileProcessor, DuplicateProcessor, DumpProcessor

from .model import *
from base.common import DumpProcessor


class TestMockSimpleProcess(Processor):
    _active = True

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
        return model        
