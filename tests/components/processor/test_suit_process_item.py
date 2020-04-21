import unittest
from typing import Any

from base.components import Processor, Pipeline
from base.components.pipeline import ProcessorSuit
from base.libs import Model, Field


class Count(Processor):

    def process_item(self, model: Model) -> Any:
        self.count += 1


class ContinueProcessor(Processor):

    def process_item(self, model: Model) -> Any:
        pass


class Abort(Processor):
    def process_item(self, model: Model) -> Any:
        return False


class MockModel(Model):
    attr = Field('attr')


class TestProcessItemTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.model = MockModel()

    def test_demo(self):
        suit = ProcessorSuit([Count])
        suit.process(self.model)

    def test_normal(self):
        suit = ProcessorSuit([Count, Count])

        assert suit.components[0].count == 0
        assert suit.components[1].count == 0

        suit.process(self.model)

        assert suit.components[0].count == 1
        assert suit.components[1].count == 1

        suit.process(self.model)

        assert suit.components[0].count == 2
        assert suit.components[1].count == 2

    def test_continue(self):
        suit = ProcessorSuit([Count, ContinueProcessor, Count])

        assert suit.components[0].count == 0
        assert suit.components[2].count == 0

        suit.process(self.model)

        assert suit.components[0].count == 1
        assert suit.components[2].count == 1

    def test_abort(self):
        suit = ProcessorSuit([Count, Abort, Count])
        assert suit.components[0].count == 0
        assert suit.components[2].count == 0

        suit.process(self.model)

        assert suit.components[0].count == 1
        assert suit.components[2].count == 0


if __name__ == '__main__':
    unittest.main()
