import unittest
from typing import Iterator, Optional, Union

from ScrapyUtils.components.processor import Processor
from ScrapyUtils.libs import Model, Proxy


class MockProcessor(Processor):

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        return True


class ProcessorTestCase(unittest.TestCase):
    def test_import(self):
        from ScrapyUtils.components import Processor

    def test_method_process_item(self):
        processor = Processor()
        processor.process_item(Proxy())


if __name__ == '__main__':
    unittest.main()
