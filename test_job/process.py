from typing import Any

from base.Model import Model
from base.Process import Process


class CustomProcess(Process):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
        return model
