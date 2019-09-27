import unittest
from unittest import TestCase, skip

from typing import *
from types import *

from base import core

from base.components.prepare import Prepare
from base.components.model import Model, Field, ModelManager
from base.components.scheme import Scheme, Action, Parse
from base.components.proceesor import Processor
from base.libs.scraper import Scraper, RequestScraper

from base.command import Command

from base.hub.hub import Hub
from base.libs.scraper import RequestScraper
from base.libs.task import Task


class TestCommand(Command):

    def syntax(self):
        return '[Test]'


class ErrorAction(Action):

    def scraping(self, task: Task, scraper: Scraper) -> str:
        raise Exception('custom error action')


class HTTPErrorAction(Action):
    def scraping(self, task: Task, scraper: Scraper) -> str:
        return scraper.get("http://wocao.wocao")


class MockModel(Model):
    name = Field()


ModelManager.add_model(MockModel)


class SingleModelParse(Parse):

    def parsing(self, content: str) -> Model or Generator[Model]:
        model = ModelManager.model('MockModel')
        return model


def scrapy(scheme_list: List[Action or Parse], scraper: Scraper, task: Task, dump_hub: Hub, sys_hub: Hub,
           log: callable):
    for scheme in scheme_list:
        pass


class TestScrapy(TestCase):

    def setUp(self) -> None:
        r = RequestScraper()
        r.scraper_activate()
        self.scraper = r

        task = Task()
        task.url = 'test url'
        task.param = {'key': 'key value'}
        self.task = task

        self.sys = Hub()
        self.dump = Hub()

        self.log = TestCommand().log

    def tearDown(self) -> None:
        super().tearDown()

    def scraping(self, scheme_list):
        schemes = core.build_schemes(scheme_list)

        return core.scrapy(schemes, self.scraper, self.task, self.dump, self.sys)

    def refact_scrapy(self, scheme_list):
        schemes = core.build_schemes(scheme_list)

        scrapy(schemes, self.scraper, self.task, self.dump, self.sys, self.log)

        # scheme_suit scraper task
        # suit.scrapy(task)
        # suit.save(dump)
        # suit.append(sys)

        # scrapy in suit

        # suit.scrapy(task)

    def test_refact_scrapy(self):
        self.assertEqual(self.sys.get_number('MockModel'), 0)

        self.refact_scrapy([SingleModelParse])

        self.assertEqual(self.sys.get_number('MockModel'), 1)

    @skip
    def test_demo(self):
        self.scraping([ErrorAction])

    @unittest.skip
    def test_http_error(self):
        self.scraping([HTTPErrorAction])
