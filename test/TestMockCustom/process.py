from typing import Any

from base.components import Processor, active
from base.common import DuplicateProcessor

from .model import *


@active
class TestMockCustomProcess(Processor):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
        return model


@active
class TestDuplication(DuplicateProcessor):
    target = OtherTestModel
    modelKey = 'name'
