from typing import Any

from base.components import Processor, active
from base.common import DumpInPeeweeProcessor, DuplicateProcessor, JsonFileProcessor

from .model import *


@active
class TestblockthreadProcess(Processor):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
        return model        
