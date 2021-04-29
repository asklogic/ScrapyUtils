import unittest
import time
import random
from typing import Any

from base.components import *
from base.libs import *


class MockModel(Model):
    name = Field(default='K')
    age = Field()


class Adult(Processor):

    def process_item(self, model: Model) -> Any:
        """
        Args:
            model (Model):
        """
        if model.age >= 20:
            self.count += 1


class Block(Processor):

    def process_item(self, model: Model) -> Any:
        """
        Args:
            model (Model):
        """
        self.count += 1
        time.sleep(0.001)


class TestPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.models = [MockModel(age=random.randint(0, 40)) for x in range(10000)]

    def test_demo(self):
        suit = ProcessorSuit([Adult])
        pipeline = Pipeline(suit)

        pipeline.consumer.stop()

        [pipeline.push(x) for x in self.models]

        assert pipeline.queue.qsize() == 10000
        assert len(pipeline.failed) == 0

        pipeline.consumer.start()
        time.sleep(0.1)
        assert pipeline.queue.qsize() == 0
        assert pipeline.suit.schemes[0].mock_count > 4700
        assert pipeline.suit.schemes[0].mock_count < 5300

    @unittest.skip
    def test_process_block(self):
        """block"""
        pipeline = Pipeline(ProcessorSuit([Block]))
        [pipeline.push(x) for x in self.models[:2000]]

        # FIXME: 1s process 500 models. ?
        for i in range(3):
            print(pipeline.queue.qsize())
            time.sleep(1)

    def test_process_exit(self):
        pipeline = Pipeline(ProcessorSuit([Block]))
        [pipeline.push(x) for x in self.models[:2000]]

        pipeline.stop(1)

        # print(len(pipeline.failed))
        # print(pipeline.suit.components[0].count)

        assert pipeline.suit.schemes[0].mock_count + len(pipeline.failed) == 2000

    def test_property_suit(self):
        pass

    def test_property_queue(self):
        pass

    def test_perperty_failed(self):
        pass


if __name__ == '__main__':
    unittest.main()
