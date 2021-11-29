import unittest

from ScrapyUtils.core.load import _load_scraper
from ScrapyUtils import configure

from ScrapyUtils.libs import Scraper


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        configure.scrapers = []
        configure.scraper_callable = None

    def test_load_scraper_sample(self):
        assert configure.scrapers == []

        _load_scraper()

        assert configure.scrapers

        [self.assertIsInstance(x, Scraper) for x in configure.scrapers]


if __name__ == '__main__':
    unittest.main()
