import unittest

from base.components import StepSuit, ActionStep, ParseStep
from base.libs import RequestScraper, Scraper, Model, Field, Task

from base.core import collect
from tests.telescreen import tests_path


def mock_wrapper():
    return RequestScraper()


class ItemTest(Model):
    name = Field()


class SingleAction(ActionStep):
    def scraping(self, task: Task):
        return self.scraper.get(task.url)


class SimpleAction(ActionStep):

    def scraping(self, task):
        return 'info'


class SimpleParse(ParseStep):
    def parsing(self):
        for i in range(5):
            import time
            item = ItemTest()
            item.name = str(int(time.time()))
            yield item


class StepSuitTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.r = RequestScraper()
        cls.r.scraper_activate()

    def test_init(self):
        suit = StepSuit([SingleAction], self.r, {})

        # suit = StepSuit(self.steps, self.scraper)

        assert suit.scraper and isinstance(suit.scraper, Scraper)
        assert len(suit.steps) == 1
        func = suit.closure_scrapy()

        func(Task(url='http://127.0.0.1:8090/mock/get'))

    def test_property_context(self):
        suit = StepSuit([SimpleAction, SimpleParse], self.r)

        assert suit.steps[0].context == suit.steps[1].context == {}
        assert suit.steps[0].context is suit.steps[1].context is suit.context

    def test_property_content(self):
        suit = StepSuit([SimpleAction, SimpleParse], self.r)

        assert suit.steps[0].content == suit.steps[1].content == ''
        assert suit.steps[0].content is suit.steps[1].content is suit.content

    def test_property_scraper(self):
        suit = StepSuit([SimpleAction, SimpleParse], self.r)

        assert suit.steps[0].scraper == suit.steps[1].scraper == self.r
        assert suit.steps[0].scraper is suit.steps[1].scraper is suit.scraper

    def test_property_models(self):
        suit = StepSuit([SimpleAction, SimpleParse], self.r)

        assert list(suit.models) == []

        # def test_init_step(self):
    #     suit = StepSuit([], self.scraper)
    #
    # def test_init_scraper(self):
    #     with self.assertRaises(AssertionError) as ae:
    #         suit = StepSuit(self.steps, collect.scrapers)
    #     assert 'StepSuit need a Scraper Instance.' in str(ae.exception)
    #
    # def test_method_suit_activate(self):
    #     """
    #     initialize steps and activate scraper instance.
    #     """
    #     # suit = StepSuit([], self.scraper)
    #     suit = StepSuit(self.steps, self.scraper)
    #
    #     assert suit.scraper.activated is False
    #     assert suit.steps is None
    #
    #     suit.suit_activate()
    #     assert suit.scraper.activated is True
    #     assert suit.steps is not None
    #
    #     assert len(suit.steps) == 4
    #
    # def test_method_suit_exit(self):
    #     """
    #     TODO: step instance exit.
    #     """
    #     suit = StepSuit(self.steps, self.scraper)
    #     suit.suit_activate()
    #
    #     assert suit.scraper.activated is True
    #     assert suit.steps is not None
    #
    #     suit.suit_exit()
    #     assert suit.scraper.activated is False
    #
    # # 太弱智就不写了
    # def test_property_scraper(self):
    #     pass
    #
    # def test_property_steps(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
