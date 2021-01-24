import unittest

from ScrapyUtils.components.step import BaseStepSuit, BaseActionStep, BaseParseStep

from ScrapyUtils.components.step import StepSuit, ActionStep, ParseStep


class CountAction(ActionStep):

    def scraping(self, task, scraper):
        return 'The mock content.'


class SimpleParser(ParseStep):

    def parsing(self, content):
        for i in range(2):
            yield {'data': content[-5:]}


class StepSuitTestCase(unittest.TestCase):

    def test_normal_inital(self):
        suit = StepSuit([], {})

        # log out.
        suit.suit_start()

        # configure
        # check the scraper and start it.
        # suit.set_scraper()

        # callback = suit.closure_scrapy()

        # callback(object)

        # log out
        suit.suit_exit()

        pass

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

        suit.simple_task('url')
        suit.simple_task('url')

        assert suit.models and len(suit.models) == 6


if __name__ == '__main__':
    unittest.main()
