from typing import Any

from base.components import Processor, active
from base.libs import Model


@active
class Count(Processor):
    count = 0

    def process_item(self, model: Model) -> Any:
        """
        Args:
            model (Model):
        """
        self.count += 1


@active
class Duplication(Processor):
    priority = 900
    pass


@active
class MysqlSave(Processor):
    priority = 400
    pass
