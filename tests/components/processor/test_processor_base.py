import unittest
from typing import Any

from base.components import Processor, Pipeline
from base.components.pipeline import ProcessorSuit
from base.libs import Model, Field


class MockProcessor(Processor):

    def process_item(self, model: Model) -> Any:
        """
        Args:
            model (Model):
        """
        pass


class CustomTarget(Model):
    age = Field()


class TestProcessorBase(unittest.TestCase):
    def setUp(self) -> None:
        self.processor = MockProcessor()

    def test_demo(self):
        processor = MockProcessor()

        processor.on_start()
        processor.on_exit()

    def test_property_target_default(self):
        assert self.processor.target == Model
        assert self.processor.target is Model

    def test_property_target(self):
        class CustomProcessor(Processor):
            target = CustomTarget

    def test_property_data(self):
        p1 = MockProcessor()
        p2 = MockProcessor()

        assert p1.data == [] == p2.data
        assert p1.data is not p2.data

    def test_property_count(self):
        assert self.processor.count == 0


if __name__ == '__main__':
    unittest.main()
