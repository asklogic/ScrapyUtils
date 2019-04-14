from unittest import TestCase
from typing import *
from types import *
import unittest
import copy
from base import core, common, command

from base.log import act, status
from base.lib import Config, ComponentMeta, Component, Setting
from base.task import Task
from base.Prepare import Prepare, DefaultRequestPrepare
from base.Model import Model, TaskModel, ProxyModel, ModelManager, ModelMeta, Field
from base.scheme import Action, Parse
from base.Process import Processor, Pipeline
from base.common import Proxy_Processor, DefaultAction, DefaultXpathParse
from base.hub import Hub
from base.Scraper import Scraper
from base.scheme import Scheme

import faker
import time

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


class TestHub(unittest.TestCase):
    def setUp(self) -> None:
        global f
        self.empty = Hub()
        self.normal = Hub(models=[MockModel])

        components = core.load_components('TestMock')
        setting = core.load_setting(components[0])

        self.empty_dump = Hub(models=[MockModel])

        # dump
        dump_setting = copy.deepcopy(setting)
        dump_setting.DumpLimit = 100

        self.dump = Hub(models=[MockModel], setting=dump_setting)

        pipeline = Pipeline([MockEmptyProcessor], setting=dump_setting)
        self.dump.add_dump_pipeline('MockModel', pipeline)

        # feed setting
        feed_setting = copy.deepcopy(setting)
        feed_setting.DumpLimit = 100
        feed_setting.FeedLimit = 20

        self.feed = Hub(models=[MockCompanyModel], setting=feed_setting)

        self.feed.add_feed_pipeline('MockCompanyModel', Pipeline([MockFeedProcessor], setting=feed_setting))

        # mock models
        models = [MockModel() for x in range(100)]
        for model in models:
            model.name = f.name()
            model.age = f.random_int(max=60)
        self.mock_models = models

        companies = [MockCompanyModel() for x in range(100)]
        for company in companies:
            company.name = f.bs()
            company.address = f.address()
        self.mock_companies = companies

        from base.log import act

        act.disabled = True

        super().setUp()

    def tearDown(self) -> None:
        super().tearDown()

    def test_init_hub(self):
        empty_hub = Hub()

    def test_save(self):
        [self.normal.save(x) for x in self.mock_models]

    def test_save_failed(self):
        with self.assertRaises(KeyError):
            [self.empty.save(x) for x in self.mock_models]

    def test_pop(self):
        [self.normal.save(x) for x in self.mock_models]

        for i in range(100):
            model = self.normal.pop('MockModel')
            self.assertIsInstance(model, MockModel)

    def test_get_number(self):
        self.assertEqual(self.normal.get_number('MockModel'), 0)
        [self.normal.save(x) for x in self.mock_models[:20]]
        self.assertEqual(self.normal.get_number('MockModel'), 20)

        with self.assertRaises(KeyError):
            model = self.empty.get_number('MockModel')

    def test_pop_empty_hub(self):
        with self.assertRaises(KeyError):
            model = self.empty.pop('MockModel')

    def test_dump_hub(self):
        self.assertEqual(self.dump.get_number('MockModel'), 0)

        [self.dump.save(x) for x in self.mock_models[:50]]

        self.assertEqual(self.dump.get_number('MockModel'), 50)

        [self.dump.save(x) for x in self.mock_models]
        self.assertEqual(self.dump.get_number('MockModel'), 150)

        self.dump.activate()

        time.sleep(1)

        self.assertEqual(self.dump.get_number('MockModel'), 50)
        self.dump.stop()
        self.assertEqual(self.dump.get_number('MockModel'), 0)

    def test_feed_hub(self):

        self.assertEqual(self.feed.get_number('MockCompanyModel'), 0)

        self.feed.activate()
        time.sleep(1)
        self.assertEqual(self.feed.get_number('MockCompanyModel'), 20)

        [self.feed.save(x) for x in self.mock_companies]

        self.assertEqual(self.feed.get_number('MockCompanyModel'), 120)
        time.sleep(1)
        self.assertEqual(self.feed.get_number('MockCompanyModel'), 120)

        self.feed.stop()
        self.assertEqual(self.feed.get_number('MockCompanyModel'), 0)

    def test_build_hub(self):
        setting = Setting()

        sys_hub = Hub([ProxyModel, TaskModel], setting=setting)
        dump_hub = Hub(setting=setting)

        dump_pipeline = Pipeline([], setting=setting)
        dump_hub.add_dump_pipeline('Model', dump_pipeline)

        # TODO proxy pipeline



