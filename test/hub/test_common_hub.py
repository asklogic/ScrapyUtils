from unittest import TestCase
from typing import *
from types import *
import unittest

from base.hub import Hub
from base.Model import TaskModel, Model, Field, ModelManager, ProxyModel
from base.lib import Setting
from base.task import Task
from base.Process import Processor, Pipeline

from base.common import Proxy_Processor

import faker
import time
import queue

f = faker.Faker(locale='zh_CN')


class MockModel(Model):
    name = Field()
    age = Field()


class MockCompanyModel(Model):
    name = Field()
    address = Field()


class MockEmptyProcessor(Processor):

    def process_item(self, model: Model) -> Any:
        pass


class MockFeedProcessor(Processor):
    target = MockCompanyModel

    def process_item(self, model: Model) -> Any:
        model.name = f.bs()
        model.address = f.address()
        return model


class MockCommonProceesor(Processor):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data())


class ProxyProcessor(Processor):

    def start_task(self, setting: Setting):
        if not setting.ProxyFunc and setting.ProxyURL is '':
            raise Exception("didn't set proxy info. check setting")

    def proxy_get(self):
        pass

    def start_process(self, number: int, model: str = "Model"):
        pass

    def process_item(self, model: Model) -> Any:
        pass


class TestCommonHub(TestCase):

    def setUp(self) -> None:
        setting = Setting()
        # cut down timeout
        setting.Timeout = 1.5
        self.sys_hub = Hub([TaskModel, ProxyModel], setting=setting)
        self.normal_dump_hub = Hub(setting=setting)

        self.custom_dump_hub = Hub(setting=setting)

        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_init(self):
        print('out')
        pass

    def test_demo(self):
        pass

    def test_task(self):
        # init
        sys = self.sys_hub
        sys.activate()

        # save tasks in sys_model
        for i in range(3000):
            task = Task()
            sys.save(task)
        self.assertEqual(sys.get_number('TaskModel'), 3000)

        # pop some task
        [self.assertIsInstance(sys.pop('TaskModel'), TaskModel) for i in range(1000)]
        self.assertEqual(sys.get_number('TaskModel'), 2000)

        # pop out of task
        with self.assertRaises(queue.Empty):
            [self.assertIsInstance(sys.pop('TaskModel'), TaskModel) for i in range(3000)]
        self.assertEqual(sys.get_number('TaskModel'), 0)

    def test_proxy_feed_failed(self):
        failed_setting = Setting()

        failed_setting.ProxyFunc = None
        failed_setting.ProxyURL = ''
        failed_setting.ProxyAble = True

        failed = Hub([TaskModel, ProxyModel], setting=failed_setting)

        with self.assertRaises(Exception):
            failed.add_feed_pipeline('ProxyModel', Pipeline([ProxyProcessor], setting=failed_setting))

        failed.activate()

        failed.stop()

    def test_proxy_feed_default(self):
        print('asd')
        feed_default_setting = Setting()
        feed_default_setting.ProxyURL = r'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson='

        from urllib.parse import urlparse, ParseResult,parse_qs,parse_qsl

        parsed: ParseResult = urlparse(feed_default_setting.ProxyURL)

        print(parsed)
        print(parse_qs(parsed.query))
        print(parse_qsl(parsed.query))
