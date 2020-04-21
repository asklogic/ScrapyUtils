import unittest
import os
import time
import json
from typing import Any

from base.components import Processor, Pipeline
from base.components.pipeline import ProcessorSuit
from base.libs import Model, Field

from collections import deque


class JsonFileProcessor(Processor):
    file_folder: str
    file_name: str

    file_path: str

    file = None

    def __init__(self, config: dict = None):
        super().__init__(config)

        self.file_folder = config.get('file_folder', os.getcwd())
        self.file_name = config.get('file_name', str(int(time.time())))

        self.file_path = os.path.join(self.file_folder, self.file_name + '.json')

        self.data = deque()

    def on_start(self):
        temp_path = os.path.join(self.file_folder, 'touch')
        with open(temp_path, 'w') as f:
            pass
        os.remove(temp_path)

    def on_exit(self):
        with open(self.file_path, 'w') as f:
            json.dump(list(self.data), f)

    def process_item(self, model: Model) -> Any:
        self.data.append(model.pure_data)



class TestCommonProcessor(unittest.TestCase):
    def test_file_processor_demo(self):
        config = {
            # 'file_folder': r'D:\RTW\ScrapyUtils\assets',
            'file_name': r'test_file_processor_data'
        }
        suit = ProcessorSuit([JsonFileProcessor], config=config)
        suit.suit_start()
        suit.suit_exit()

        assert os.path.exists(os.path.join(os.getcwd(), 'test_file_processor_data' + '.json'))
        os.remove(os.path.join(os.getcwd(), 'test_file_processor_data' + '.json'))

    def test_duplication(self):
        pass

    def test_mysql(self):
        pass


if __name__ == '__main__':
    unittest.main()
