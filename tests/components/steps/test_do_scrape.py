import random
import unittest
from typing import List, Optional, Union, Iterable, Sequence

from ScrapyUtils.components import Action, Parse, StepSuit
from ScrapyUtils.libs import Scraper, Task, Model


class CountAction(Action):
    count = 0

    def scraping(self, task: Task, scraper: Scraper) -> Optional[str]:
        self.count += 1


class CountParse(Parse):
    count = 0

    def parsing(self, content: str) -> Union[Iterable[Model], Sequence[Model]]:
        self.count += 1


class ErrorAction(Action):
    priority = 550

    def scraping(self, task: Task, scraper: Scraper) -> Optional[str]:
        assert False


class DoScrapeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.count_action = CountAction()
        self.count_parse = CountParse()
        self.error_action = ErrorAction()
        self.task = Task()

        self.suit = StepSuit()

    def test_do_scrape(self):
        """Method do scrape will execute all the step."""
        suit = StepSuit(self.count_action, self.count_parse)

        execute_number = random.randint(5, 10)

        [suit.do_scrape(self.task) for x in range(execute_number)]

        self.assertEqual(self.count_action.count, execute_number)
        self.assertEqual(self.count_parse.count, execute_number)

    def test_do_scrape_error_step(self):
        """Raise the exception if steps raise."""

        suit = StepSuit(self.count_action, self.error_action, self.count_parse)

        with self.assertRaises(AssertionError) as ae:
            suit.do_scrape(self.task)


if __name__ == '__main__':
    unittest.main()
