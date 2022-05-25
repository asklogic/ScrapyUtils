import os
import sys
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Optional, Iterator, NoReturn

from ScrapyUtils import configure
from ScrapyUtils.components.action import ActionContent
from ScrapyUtils.core import collect_action
from ScrapyUtils.core.load import load
from ScrapyUtils.core.scrape import scrape, start_scraping
from ScrapyUtils.libs import Task, Scraper, Model, Proxy
from ScrapyUtils.libs.scraper.request_scraper import RequestScraper

from ScrapyUtils.components import Action, ActionSuit


class TestScrapeModel(Model):
    pass


class Normal(Action):
    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        yield TestScrapeModel()


class Parser(Action):

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        pass


class Failed(Action):

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        assert False


class HalfFailed(Action):

    def on_start(self) -> NoReturn:
        self.count = 0
        pass

    def action_step(self, task: Task, scraper: Scraper, content: ActionContent) -> Iterator[Model]:
        if self.count > 5:
            assert False
        else:
            self.count += 1


def callback_failed():
    assert False


def callback_timeout():
    import time
    time.sleep(1)


class ScrapeCase(unittest.TestCase):
    """
    设置Scraper 为 None.
    设置Task 为 10个ip.cn
    设置DELAY 为 0: 快速完成爬取流程

    suit默认为空
    """

    def setUp(self) -> None:
        self.pool = ThreadPoolExecutor(1)

        configure.scraper_callable = None
        configure.tasks_callable = lambda: [Task(url='https://ip.cn/') for i in range(10)]
        configure.DELAY = 0
        configure.THREAD = 1

    def tearDown(self) -> None:
        configure.tasks = Queue()
        configure.failed = Queue()

    def test_scrape_in_success(self):
        """回调成功"""
        self.pool.submit(lambda: True).result(0.1)

    def test_scrape_in_failed(self):
        """回调失败"""
        with self.assertRaises(Exception) as e:
            self.pool.submit(callback_failed).result(0.1)

    def test_scrape_in_timeout(self):
        """回调超时"""
        with self.assertRaises(Exception) as e:
            self.pool.submit(callback_timeout).result(0.1)

    def test_scrape_success(self):
        """成功 消费Task对象"""
        load()
        scrape()

        time.sleep(0.1)
        assert configure.tasks.qsize() == 0
        assert configure.failed.qsize() == 0

    def test_scrape_generate_models(self):
        """成功并且产生数据对象"""
        configure.action_classes = [Normal]
        load()
        scrape()
        configure.models_pipeline.pause()
        time.sleep(0.1)

        assert configure.tasks.qsize() == 0
        assert len(configure.models) == 10

    def test_scrape_failed(self):
        """失败 """
        configure.action_classes = [Failed]
        load()
        scrape()

        time.sleep(0.15)
        assert configure.tasks.qsize() == 0
        assert configure.failed.qsize() == 10


if __name__ == '__main__':
    unittest.main()
