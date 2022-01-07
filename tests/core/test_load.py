import unittest

from ScrapyUtils.core.load import _load_scraper, _load_tasks
from ScrapyUtils import configure

from ScrapyUtils.libs import Scraper, Task


def mock_tasks_callable():
    for i in range(10):
        yield Task()


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        configure.scrapers = []
        configure.scraper_callable = None

        configure.tasks_callable = mock_tasks_callable

    def test_load_scraper_sample(self):
        assert configure.scrapers == []

        _load_scraper()

        assert configure.scrapers

        [self.assertIsInstance(x, Scraper) for x in configure.scrapers]

    def test_load_task_sample(self):
        assert configure.tasks.qsize() == 0

        _load_tasks()

        assert configure.tasks.qsize() == 10

        assert isinstance(configure.tasks.get(), Task)


if __name__ == '__main__':
    unittest.main()
