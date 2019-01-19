from typing import Any

from base.Model import Model
from base.Process import Process


class Generator_testDefaultProcess(Process):
    def process_item(self, model: Model) -> Any:
        print(model.pure_data())
