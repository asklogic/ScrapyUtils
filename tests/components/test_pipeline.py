import unittest

from base.components import *
from base.libs import *


class MockModel(Model):
    name = Field('K')


class TestPipeline(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)

    def test_init(self):
        pipeline = Pipeline([])
        pipeline.exit()

        m = MockModel()
        pass


if __name__ == '__main__':
    unittest.main()
