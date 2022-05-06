import unittest
from typing import Iterator, Optional

from ScrapyUtils.components.action import ActionSuit, Action, ActionContent
from ScrapyUtils.libs import Task, Scraper, Model


# mocks
class AlphaAction(Action):
    pass


class BetaAction(Action):
    pass


class CountAction(Action):
    def __init__(self):
        self.count = 0

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        self.count += 1


available = []


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.suit = ActionSuit()

    def test_suit_initial(self):
        """ActionSuit Sample"""
        assert self.suit
        assert isinstance(self.suit, ActionSuit)

    def test_argument_init_with_class(self):
        """Initial with action classes"""
        suit = ActionSuit(AlphaAction, BetaAction)

        assert len(suit.components) == 2
        assert isinstance(suit.components[0], AlphaAction)
        assert isinstance(suit.components[1], BetaAction)

    def test_arguments_init_with_ins(self):
        """Initial with action instance"""
        origin = BetaAction()

        suit = ActionSuit(AlphaAction, origin)
        assert len(suit.components) == 2

        assert isinstance(suit.components[0], AlphaAction)
        assert suit.components[1] == origin

    def test_do_scrape(self):
        """Do scrape callback"""
        suit = ActionSuit(CountAction)

        suit.generate_callback(Task())()

        assert suit.components[0].count == 1

    def test_property_scraper(self):
        """property scraper. Default is RequestsScraper"""
        assert isinstance(self.suit.scraper, Scraper)

    def test_property_set_scraper(self):
        """method set_scraper"""
        from ScrapyUtils.libs.scraper.request_scraper import RequestScraper
        scraper = RequestScraper()

        self.suit.set_scraper(scraper)
        assert self.suit.scraper == scraper


if __name__ == '__main__':
    unittest.main()
