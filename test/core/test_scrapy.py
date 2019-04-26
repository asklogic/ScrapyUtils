import unittest
from unittest import TestCase

from base import core

from base.components.prepare import Prepare
from base.components.model import Model
from base.components.scheme import Scheme,Action,Parse
from base.components.proceesor import Processor
from base.libs.scraper import Scraper, RequestScraper

from base.hub.hub import Hub
from base.libs.scraper import RequestScraper
from base.libs.task import Task

class ErrorAction(Action):

    def scraping(self, task: Task, scraper: Scraper) -> str:
        raise Exception('custom error action')


class TestScrapy(TestCase):

    def setUp(self) -> None:
        r = RequestScraper()
        r.activate()
        self.scraper = r

        task = Task()
        task.url = 'test url'
        task.param = {'key': 'key value'}
        self.task = task

        self.sys = Hub()
        self.dump = Hub()

    def tearDown(self) -> None:
        super().tearDown()

    def scraping(self, scheme_list):
        schemes = core.build_schemes(scheme_list)

        core.scrapy(schemes, self.scraper, self.task, self.dump, self.sys)
        pass

    def test_demo(self):
        self.scraping([ErrorAction])


