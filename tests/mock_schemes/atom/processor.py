from typing import Any

from base.components import Processor, active
from base.libs import Model


@active
class Count(Processor):
    count = 0
    def process_item(self, model: Model) -> Any:
        self.count += 1
        print(model.name, model.pure_data)


@active
class Duplication(Processor):
    priority = 800
    pass


class Mysql(Processor):
    pass