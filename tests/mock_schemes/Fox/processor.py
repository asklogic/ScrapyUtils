from typing import Any

from base.components import Processor, active
from base.common import DumpInPeeweeProcessor, DuplicateProcessor, JsonFileProcessor

from .model import *


@active
class FoxProcess(Processor):

    def process_item(self, model: Model) -> Any:
        """
        Args:
            model (Model):
        """
        print(model.pure_data())
        return model        
