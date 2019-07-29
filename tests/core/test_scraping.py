import unittest

from unittest import TestCase

from base import core

from base.libs.task import Task
from base.components import Scheme, Action
from base.libs import Scraper
from base.libs.scraper import RequestScraper


class TestScraping(TestCase):

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def test_core_scraping(self):
        t = Task()
        t.url = 'http://127.0.0.1:/mock/get'

        core.do_action()

        pass

    def test_init_scraper(self):
        self.fail()


if __name__ == '__main__':
    print(__name__)
