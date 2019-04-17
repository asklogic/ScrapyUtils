from typing import *
import unittest
import copy
from base import core

from base.libs.setting import Setting
from base.common import ProxyModel
from base.libs.task import TaskModel
from base.components.model import Field, Model
from base.hub.pipeline import Pipeline
from base.components.proceesor import Processor
from base.hub.hub import Hub

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

        setting = core.build_setting('TestMock')

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
            [self.normal.save(x) for x in self.mock_companies]

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
            model = self.normal.get_number('MockCompanyModel')

    def test_pop_empty_hub(self):
        with self.assertRaises(KeyError):
            model = self.normal.pop('MockCompanyModel')

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

        setting.DumpLimit = 5

        sys_hub = Hub([ProxyModel, TaskModel], setting=setting)
        dump_hub = Hub(setting=setting)

        dump_pipeline = Pipeline([MockCommonProceesor], setting=setting)
        dump_hub.add_dump_pipeline('Model', dump_pipeline)

        [dump_hub.save(x) for x in self.mock_companies[:20]]
        [dump_hub.save(x) for x in self.mock_models[:20]]


        sys_hub.activate()
        dump_hub.activate()

        time.sleep(2)

        dump_hub.stop(dump_all=True)

        # TODO proxy pipeline
