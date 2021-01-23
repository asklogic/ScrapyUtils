import unittest

from ScrapyUtils.components.step import BaseStepSuit, BaseActionStep, BaseParseStep


class CountAction(BaseActionStep):

    def scraping(self, task):
        return 'The mock content.'


class SimpleParser(BaseParseStep):

    def parsing(self):
        for i in range(2):
            yield {'data': self.content[-5:]}


class StepSuitTestCase(unittest.TestCase):
    def test_initial(self):
        suit = BaseStepSuit()

        suit = BaseStepSuit(BaseActionStep)

        suit = BaseStepSuit([BaseActionStep, BaseActionStep])

    def test_error_initial(self):
        with self.assertRaises(AssertionError) as ae:
            suit = BaseStepSuit(1)

    def test_simple_run(self):
        suit = BaseStepSuit(CountAction, SimpleParser)

        suit.simple_task('url')

        assert suit.models and len(suit.models) == 2
        assert suit.content == 'The mock content.'

        suit.simple_task('url')
        suit.simple_task('url')

        assert suit.models and len(suit.models) == 6


if __name__ == '__main__':
    unittest.main()
