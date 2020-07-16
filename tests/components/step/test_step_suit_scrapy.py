import unittest

from base.components import StepSuit, Step, ActionStep, ParseStep
from base.libs import RequestScraper, Task

from base.core import collect
from tests.telescreen import tests_path

from collections import deque
from multiprocessing.dummy import Pool as ThreadPool


class FailedAction(ActionStep):
    def scraping(self, task: Task):
        """
        Args:
            task (Task):
        """
        raise Exception('failed.')


class FailedParse(ParseStep):
    def parsing(self):
        raise Exception('failed.')


class Single(ActionStep):
    def scraping(self, task: Task):
        """
        Args:
            task (Task):
        """
        return self.scraper.get(task.url)


class Tasks(ParseStep):
    def parsing(self):
        for i in range(10):
            yield Task()


thread_pool = ThreadPool(5)


def callback(ojb):
    """
    Args:
        ojb:
    """
    assert ojb
    # raise Exception()
    pass


def error_callback(obj):
    """
    Args:
        obj:
    """
    assert obj


def assert_callback(args):
    """
    Args:
        args:
    """
    assert type(args[0]) is bool
    assert isinstance(args[1], Task)


class StepSuitScrapyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        collect.collect_scheme('atom')

        cls.steps = collect.steps_class
        cls.scraper = collect.scrapers()

    @classmethod
    def tearDown(self) -> None:
        thread_pool.close()
        thread_pool.join()

    def setUp(self) -> None:
        self.task = Task(url='http://127.0.0.1:8090/mock/random/dynamic')

    # @unittest.skip
    # def test_demo(self):
        # def inline():
        #     pass
        #
        # def failed(*args):
        #     raise Exception()
        #
        # res = thread_pool.apply_async(inline, callback=failed)
        #
        # try:
        #     res.get(1)
        # except:
        #     pass

    def test_closure_scrapy(self):
        suit = StepSuit(self.steps, self.scraper)
        suit.suit_activate()

        # res = suit.scrapy(self.task)
        #
        # assert res is True
        #
        # assert suit.models and isinstance(suit.models, deque)
        # assert len(suit.models) > 4
        # assert suit.content

        kw = {'task': self.task, }
        res = thread_pool.apply_async(suit.closure_scrapy(), kwds=kw, callback=assert_callback)
        res.get(1)

        suit.suit_exit()

    @unittest.skip
    def test_scrapy_content(self):
        """content and models."""
        suit = StepSuit([Single, Tasks], collect.scrapers)
        suit.suit_activate()

        suit.scrapy(self.task)

        assert '200 and success' in suit.content
        assert len(suit.models) is 10

    @unittest.skip
    def test_scrapy_failed(self):
        """interrupt."""
        suit = StepSuit([Single, FailedAction, Tasks], collect.scrapers)
        suit.suit_activate()

        suit.scrapy(self.task)
        assert '200 and success' in suit.content
        assert len(suit.models) is 0


if __name__ == '__main__':
    unittest.main()
