from typing import Any

from base.components.proceesor import Processor
from base.common import DuplicateProcessor

from .model import *


class TestMockCustomProcess(Processor):
    _active = True

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
        return model


class TestDuplication(DuplicateProcessor):
    target = OtherTestModel
    modelKey = 'name'
