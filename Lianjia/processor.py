from typing import Any

from ScrapyUtils.components import Processor, active, set_active
from ScrapyUtils.common import DuplicateProcessor, JsonFileProcessor, CSVFileProcessor, ExeclFileProcessor

from .model import *


@active
class LianjiaProcess(Processor):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data)
        return model        
