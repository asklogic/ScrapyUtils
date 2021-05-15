import unittest
import os
import time
import json
from typing import Any

from base.components import Processor, Pipeline
from base.components.pipeline import ProcessorSuit
from base.libs import Model, Field

from collections import deque




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
