import unittest
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from typing import NoReturn, Optional, Iterator

from ScrapyUtils.components.action import ActionSuit, Action, ActionContent
from ScrapyUtils.libs import Task, Scraper, Model


class CountAction(Action):

    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Optional[Iterator[Model]]:
        self.count += 1


class DelayErrorAction(Action):
    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Optional[Iterator[Model]]:
        self.count += 1
        if self.count == 3:
            raise Exception('delay error')


class MockModel(Model):
    pass


class ParseAction(Action):

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Optional[Iterator[Model]]:
        for i in range(5):
            yield MockModel()


single_pool = ThreadPoolExecutor(1)


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.suit = ActionSuit()

        self.tasks = [Task() for i in range(10)]

    def test_scrape_count(self):
        split_limit = 6

        count = CountAction()

        suit = ActionSuit(count)

        callbacks = [suit.generate_callback(task) for task in self.tasks[:split_limit]]

        futures = [single_pool.submit(callback) for callback in callbacks]

        [future.result() for future in futures]

        assert count.count == split_limit

    def test_scrape_with_error(self):
        """raise exception if some action failed."""
        delay_error = DelayErrorAction()
        suit = ActionSuit(delay_error)

        callbacks = [suit.generate_callback(task) for task in self.tasks]

        with self.assertRaises(Exception) as e:
            futures = [single_pool.submit(callback) for callback in callbacks]
            [future.result() for future in futures]

            assert str(e.exception) == 'delay error'

    def test_yield_model(self):
        """callback will yield model"""
        parse = ParseAction()
        suit = ActionSuit(parse)

        assert len(list(chain.from_iterable([suit.generate_callback(task)() for task in self.tasks]))) == 5 * 10


if __name__ == '__main__':
    unittest.main()
