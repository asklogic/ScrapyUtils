from typing import Any

from base.Model import Model
from base.Process import Process


class PrintProcess(Process):
    def process_item(self, model: Model) -> Any:
        print(model.pure_data())

        import json
        with open("temp.json", "w") as f:
            json.dump(model.pure_data(), f)
