import unittest

from ScrapyUtils.components.step import BaseStepSuit, BaseActionStep, BaseParseStep

from ScrapyUtils.components.step import StepSuit, ActionStep, ParseStep, Task


class CountAction(ActionStep):

    def scraping(self, task, scraper):
        return 'The mock content.'


class SimpleParser(ParseStep):

    def parsing(self, content: str):
        for i in range(2):
            yield {'data': content[-5:]}


class StepSuitTestCase(unittest.TestCase):

    def test_suit_initial(self):
        suit = StepSuit([], {})

        # log out.
        suit.suit_start()

        # configure
        # check the scraper and start it.
        # suit.set_scraper(None)

        callback = suit.closure_scrapy()

        callback(Task())

        # log out
        suit.suit_exit()

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

    def test_suit_run(self):
        from ScrapyUtils.libs import RequestScraper

        r = RequestScraper()

        class SimpleAction(ActionStep):

            def scraping(self, task, scraper: RequestScraper):
                return scraper.get('https://ip.cn/')

        suit = StepSuit([SimpleAction, SimpleParser])
        suit.set_scraper(r)

        callback = suit.closure_scrapy()
        callback(Task())

        assert len(suit.models) == 2


if __name__ == '__main__':
    unittest.main()
