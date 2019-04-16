from unittest import TestCase
from typing import *
from types import *
import unittest
import time

from base import core, common, command

from base.log import act, status
from base.lib import Config, ComponentMeta, Component, Setting
from base.task import Task
from base.Prepare import Prepare, DefaultRequestPrepare
from base.Model import Model, TaskModel, ProxyModel, ModelManager, ModelMeta, Field
from base.scheme import Action, Parse
from base.Process import Processor, Pipeline
from base.common import DefaultAction, DefaultXpathParse
from base.hub import Hub, Resource
from base.Scraper import Scraper
from base.scheme import Scheme

import faker

f: faker.Generator = faker.Faker(locale='zh_CN')


class MockModel(Model):
    name = Field()
    age = Field()


class MockCompanyModel(Model):
    name = Field()
    address = Field()


class MockEmptyProcessor(Processor):

    def process_item(self, model: Model) -> Any:
        # time.sleep(1)
        # print(model.pure_data())
        pass


class MockFeedProcessor(Processor):
    target = MockCompanyModel

    def process_item(self, model: Model) -> Any:
        model.name = f.bs()
        model.address = f.address()
        return model


class MockCommonProceesor(Processor):

    def process_item(self, model: Model) -> Any:
        pass


class TestResource(TestCase):

    def setUp(self) -> None:

        self.empty = Resource()

        self.normal = Resource(MockModel, 5, dump_limit=300)
        self.common = Resource(Model, 5, dump_limit=300)

        self.quick = Resource(timeout=0.5)

        self.dump = Resource(MockModel, 5,
                             dump_limit=40,
                             dump_pipeline=Pipeline([MockEmptyProcessor]))
        self.feed = Resource(MockCompanyModel, 5,
                             dump_limit=50, feed_limit=30,
                             feed_pipeline=Pipeline([MockFeedProcessor]))

        self.feed_dump = Resource(MockCompanyModel, 3,
                                  feed_limit=100, dump_limit=400,
                                  feed_pipeline=Pipeline([MockFeedProcessor]),
                                  dump_pipeline=Pipeline([MockCommonProceesor]))

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


    def test_size(self):
        self.assertEqual(self.normal.size(), 0)

    def test_save(self):
        import time

        start = time.time()

        index = 10
        self.assertEqual(self.normal.size(), 0)
        # not MockModel but MockCompanies

        for i in range(index):
            [self.normal.add(x) for x in self.mock_models]
        self.assertEqual(self.normal.size(), index * 100)

        end = time.time()

        print('save {0} in {1}'.format(index * 100, end - start))

    def test_save_failed(self):
        self.assertEqual(self.normal.size(), 0)
        with self.assertWarns(Warning):
            [self.normal.add(x) for x in self.mock_companies[:20]]
        self.assertEqual(self.normal.size(), 20)

    def test_pop(self):
        self.assertEqual(self.normal.size(), 0)
        [self.normal.add(x) for x in self.mock_models[:20]]
        self.assertEqual(self.normal.size(), 20)

        [self.assertIsInstance(model, MockModel) for model in [self.normal.pop() for x in range(20)]]

    def test_pop_failed(self):
        # timeout
        self.assertEqual(self.quick.size(), 0)
        [self.quick.add(x) for x in self.mock_models[:20]]
        self.assertEqual(self.quick.size(), 20)

        import queue
        with self.assertRaises(queue.Empty):
            [self.quick.pop() for x in range(30)]

    def test_dump(self):
        # dump Resource
        # limit 50 . add 100 MockModel
        self.dump.start()

        [self.dump.add(x) for x in self.mock_models]

        time.sleep(1)
        self.assertTrue(self.dump.size() < 50)
        self.dump.stop()

    def test_feed(self):

        self.assertEqual(self.feed.size(), 0)

        self.feed.start()
        time.sleep(1)

        self.assertEqual(self.feed.size(), 30)

    def test_empty_hub(self):
        # simple queue
        empty = self.empty

        self.assertEqual(empty.size(), 0)
        [empty.add(x) for x in self.mock_models[:50]]
        self.assertEqual(empty.size(), 50)

        [empty.add(x) for x in self.mock_companies[:30]]
        self.assertEqual(empty.size(), 80)

        # first 50 MockModel
        [self.assertIsInstance(model, MockModel) for model in [empty.pop() for x in range(50)]]

        # then 30 MockCompanyModel
        [self.assertIsInstance(model, MockCompanyModel) for model in [empty.pop() for x in range(30)]]

    def test_normal_hub(self):
        normal = self.normal

        self.assertEqual(normal.size(), 0)
        [normal.add(x) for x in self.mock_models[:50]]
        self.assertEqual(normal.size(), 50)

        # force ( default
        with self.assertWarns(Warning):
            [normal.add(x) for x in self.mock_companies[:10]]
        self.assertEqual(normal.size(), 60)

        # not force
        with self.assertWarns(Warning):
            [normal.add(x, force=False) for x in self.mock_companies[:10]]
        self.assertEqual(normal.size(), 60)

    def test_dump_resource(self):

        dump = self.dump
        [dump.add(x) for x in self.mock_models]
        self.assertEqual(dump.size(), 100)
        dump.start()

        time.sleep(1)
        self.assertEqual(dump.size(), 20)

        remain = dump.stop(False)
        self.assertEqual(len(remain), 20)

    def test_feed_resource(self):
        feed = self.feed
        [feed.add(x) for x in self.mock_companies[:10]]
        self.assertEqual(feed.size(), 10)
        feed.start()

        time.sleep(1)
        self.assertEqual(feed.size(), 40)

        [feed.pop() for x in range(35)]
        time.sleep(1)
        self.assertEqual(feed.size(), 35)

        remain = feed.stop()
        self.assertEqual(len(remain), 35)

    # @unittest.skip
    def test_feed_dump_resource(self):
        final = self.feed_dump

        self.assertEqual(final.size(), 0)

        # add 300 size: 300
        [final.add(x) for x in self.mock_companies]
        [final.add(x) for x in self.mock_companies]
        [final.add(x) for x in self.mock_companies]
        self.assertEqual(final.size(), 300)

        final.start()

        # add 300 size: 600 dump 400
        [final.add(x) for x in self.mock_companies]
        [final.add(x) for x in self.mock_companies]
        [final.add(x) for x in self.mock_companies]

        # remain 200
        time.sleep(1)
        self.assertEqual(final.size(), 200)

        [final.pop() for x in range(180)]
        # pop 180 size: 20
        self.assertEqual(final.size(), 20)

        time.sleep(2)
        # feed 100 size : 120
        self.assertEqual(final.size(), 120)

        remain = final.stop()
        self.assertEqual(len(remain), 120)


