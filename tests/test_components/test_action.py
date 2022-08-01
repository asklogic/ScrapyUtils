import unittest
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from typing import NoReturn, Optional, Iterator

from ScrapyUtils.components.action import Action, ActionContent
from ScrapyUtils.libs import Task, Scraper, Model


class CountAction(Action):

    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        self.count += 1


class ErrorAction(Action):

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        raise Exception('error action.')


class DelayErrorAction(Action):
    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        self.count += 1
        if self.count == 3:
            raise Exception('delay error')


class MockModel(Model):
    pass


class ParseAction(Action):

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        for i in range(5):
            yield MockModel()


def build_action_chain(*actions: Action):
    for index in range(len(actions) - 1):
        actions[index].next = actions[index + 1]

    return actions[0]


class DoActionTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.tasks = [Task() for i in range(10)]

    def test_single_action_cases(self):
        """execute single count task."""

        with self.subTest('single count'):
            action = CountAction()
            task = self.tasks[0]

            # execute
            res = action.generate_callback(task, None)()
            assert action.count == 1
            assert res == []

        with self.subTest('single parse'):
            action = ParseAction()
            task = self.tasks[0]

            res = action.generate_callback(task, None)()
            assert len(res) == 5

        with self.subTest('single error'):
            action = ErrorAction()
            task = self.tasks[0]

            with self.assertRaises(Exception) as e:
                res = action.generate_callback(task, None)()

            assert 'error action.' in str(e.exception)

    def test_error_after_some_task(self):
        """raise exception after some task"""

        action = build_action_chain(CountAction(), ParseAction(), DelayErrorAction(), )

        with self.assertRaises(Exception) as e:
            [action.generate_callback(task, None)() for task in self.tasks]

            assert str(e.exception) == 'delay error'

    def test_yield_model_cases(self):
        """Yield models from action"""

        with self.subTest('multi parse yield'):
            action = build_action_chain(ParseAction(), ParseAction())

            result = chain(*[action.generate_callback(task, None)() for task in self.tasks])

            assert len(list(result)) == 5 * 10 * 2


if __name__ == '__main__':
    unittest.main()
