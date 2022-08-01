from typing import Any

from ScrapyUtils.components import Process, active, set_active
from ScrapyUtils.common import JsonFileProcess, CSVFileProcess, ExeclFileProcess

from .model import *


@active
class ErrorProcess(Process):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data)
        return model

