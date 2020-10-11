from typing import Any

from ScrapyUtils.components import Processor, active, set_active
from ScrapyUtils.common import DumpInPeeweeProcessor, DuplicateProcessor, JsonFileProcessor, CSVFileProcessor

from .model import *


@active
class AtomProcess(Processor):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data)
        return model        
