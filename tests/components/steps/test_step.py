import unittest

from ScrapyUtils.components import Step


class StepTestCase(unittest.TestCase):

    def test_property_context(self):
        step = Step()

        self.assertIsNone(step.context)


if __name__ == '__main__':
    unittest.main()
