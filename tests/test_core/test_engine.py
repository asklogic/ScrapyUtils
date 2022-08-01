import os
import sys
import unittest
from os.path import dirname, abspath

from ScrapyUtils.core.engine import start_engine
from ScrapyUtils import configure

from ScrapyUtils.libs import Scraper, Task


def mock_tasks_callable():
    for i in range(10):
        yield Task()


class PrepareTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        mock_project_home = os.path.join(dirname(dirname(abspath(__file__))), 'mock_project')
        sys.path.insert(0, mock_project_home)

    def setUp(self) -> None:
        configure.scrapers = []
        configure.scraper_callable = None

        configure.tasks_callable = mock_tasks_callable

    def test_prepare(self):
        """entry of prepare"""

        configure.project_package_path = 'normal'
        start_engine()


if __name__ == '__main__':
    unittest.main()
