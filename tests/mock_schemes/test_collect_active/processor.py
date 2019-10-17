from typing import Any

from base.components import Processor, active
from base.libs import Model


@active
class Count(Processor):
    count = 0

    def process_item(self, model: Model) -> Any:
        self.count += 1


class AbortProcessor(Processor):
    pass