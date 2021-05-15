import unittest

from ScrapyUtils.components import ProcessorSuit, Processor
from ScrapyUtils.libs import Proxy


class ProcecssorSuitTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.suit = ProcessorSuit()

    def test_sample(self):
        pass

    def test_attribute_target_component(self):
        """Attribute target_component: default fixed Processor type."""
        self.assertEqual(ProcessorSuit.target_components, Processor)

    def test_attribute_component_default(self):
        """Attribute target_component: default []."""
        self.assertEqual(ProcessorSuit.components, [])

    def test_method_process(self):
        """Method process: Success will return True"""
        res = self.suit.process(Proxy())

        self.assertTrue(res)

    def test_method_process_case(self):
        """To tests.processor.test_process module."""


if __name__ == '__main__':
    unittest.main()
