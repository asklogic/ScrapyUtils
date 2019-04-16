from unittest import TestCase
from typing import *
from types import *
import unittest

from base.hub import Hub
from base.Model import TaskModel, Model, Field, ModelManager, ProxyModel
from base.lib import Setting
from base.task import Task
from base.Process import Processor, Pipeline


import requests
import faker
import time
import queue
from urllib.parse import *

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
    query_param: Dict = {}

    query_parsed: ParseResult
    query_number_key = ''

    _headers = {
        'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        "Content-Type": "application/x-www-form-urlencoded",
        'Connection': 'close',
        'Cache-Control': 'max-age=0',
    }

    def start_task(self, setting: Setting):
        if not setting.ProxyFunc and setting.ProxyURL is '':
            raise Exception("didn't set proxy info. check setting")

        if setting.ProxyURL:
            self.query_parsed = urlparse(setting.ProxyURL)

            for item in parse_qsl(self.query_parsed.query):
                self.query_param[item[0]] = item[1]

        if setting.ProxyNumberParam:
            self.query_number_key = setting.ProxyNumberParam
        else:
            self.query_number_key = 'qty'

        if setting.ProxyFunc:
            self.proxy_get = setting.ProxyFunc

    def proxy_get(self, number: int):

        self.query_param[self.query_number_key] = number
        result = list(tuple(self.query_parsed))
        result[4] = urlencode(self.query_param)

        url = urlunparse(tuple(result))

        res = requests.get(url, headers=self._headers)

        assert res.status_code >= 200 and res.status_code < 300

        proxy_list = res.content.decode("utf-8").split("\r\n")

        for proxy in proxy_list:
            assert ':' in proxy

        self.proxy_list = proxy_list

    def start_process(self, number: int, model: str = "Model"):

        self.proxy_get(number)

        print('proxy success')

    def process_item(self, model: Model) -> Any:
        proxy = self.proxy_list.pop().split(":")
        model.ip = proxy[0]
        model.port = proxy[1]
        return model


import redis

class ProxyProcessor(Processor):
    query_param: Dict = {}

    query_parsed: ParseResult
    query_number_key = ''

    _headers = {
        'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        "Content-Type": "application/x-www-form-urlencoded",
        'Connection': 'close',
        'Cache-Control': 'max-age=0',
    }

    def start_task(self, setting: Setting):
        if not setting.ProxyFunc and setting.ProxyURL is '':
            raise Exception("didn't set proxy info. check setting")

        if setting.ProxyURL:
            self.query_parsed = urlparse(setting.ProxyURL)

            for item in parse_qsl(self.query_parsed.query):
                self.query_param[item[0]] = item[1]

        if setting.ProxyNumberParam:
            self.query_number_key = setting.ProxyNumberParam
        else:
            self.query_number_key = 'qty'

        if setting.ProxyFunc:
            self.proxy_get = setting.ProxyFunc

    def proxy_get(self, number: int):

        self.query_param[self.query_number_key] = number
        result = list(tuple(self.query_parsed))
        result[4] = urlencode(self.query_param)

        url = urlunparse(tuple(result))

        res = requests.get(url, headers=self._headers)

        assert res.status_code >= 200 and res.status_code < 300

        proxy_list = res.content.decode("utf-8").split("\r\n")

        for proxy in proxy_list:
            assert ':' in proxy

        self.proxy_list = proxy_list

    def start_process(self, number: int, model: str = "Model"):

        self.proxy_get(number)

        print('proxy success')

    def process_item(self, model: Model) -> Any:
        proxy = self.proxy_list.pop().split(":")
        model.ip = proxy[0]
        model.port = proxy[1]
        return model


class DuplicateProcessor(Processor):
    # property
    host: int = '127.0.0.1'
    port: int = '6379'
    db: int = 0
    password: str = ''

    redis_connect: redis.Redis = None

    # Duplicate property
    baseList: List[str] = []
    modelKey: str = ''

    def start_task(self, setting: Setting):
        assert bool(self.modelKey)

        duplication_setting = setting.Duplication

        for key, value in duplication_setting.items():
            setattr(self, key, value)

        if self.baseList:
            self._set_base(self.baseList)
        else:
            self._set_base(baseList=[setting.Target, self.modelKey])

        self.connect()

    def connect(self):
        self.redis_connect = redis.Redis(host=self.host, port=self.port, db=self.db,
                                         password=self.password, decode_responses=True,
                                         socket_connect_timeout=3)
        try:
            self.redis_connect.keys('1')
        except redis.ConnectionError as e:
            print(e.args)
            raise TypeError('redis connect failed')

    def _set_base(self, baseList: List):
        self.base = ":".join(baseList)

    def _key(self, key: str) -> str:
        return ":".join([self.base, key])

    def process_item(self, model: Model) -> Any:
        key = getattr(model, self.modelKey)
        if key and self.check_identification(key):
            return model
        else:
            return False

    def exist_identification(self, key_name) -> bool:
        """
        存在key 返回True
        不存在key 返回False
        :param key_name:
        :return:
        """
        return self.redis_connect.exists(self._key(key_name))

    def save_identification(self, key_name):
        """
        保存
        :param key_name:
        :return:
        """
        self.redis_connect.set(self._key(key_name), 1)

    def check_identification(self, key):
        """
        查询并且保存
        存在 返回False
        不存在 返回True
        :param key:
        :return:
        """
        if self.exist_identification(key):
            return False
        else:
            self.save_identification(key)
            return True


class FailedDuplication(DuplicateProcessor):
    pass


class CannotConnectDuplication(DuplicateProcessor):
    modelKey = MockCompanyModel


class CustomMockDuplication(DuplicateProcessor):
    modelKey = 'name'
    baseList = ['testcustom', 'company', 'name']


class TestCommonHub(TestCase):

    def setUp(self) -> None:
        setting = Setting()
        # cut down timeout
        setting.Timeout = 1.5
        self.sys_hub = Hub([TaskModel, ProxyModel], setting=setting)
        self.normal_dump_hub = Hub(setting=setting)

        self.custom_dump_hub = Hub(setting=setting)

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

    @unittest.skip
    def test_proxy_feed_default(self):
        feed_default_setting = Setting()
        feed_default_setting.ProxyURL = r'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson='

        feed_default_setting.FeedLimit = 20
        pipeline = Pipeline([ProxyProcessor], setting=feed_default_setting)

        test_feed_hub = Hub([ProxyModel], setting=feed_default_setting)
        test_feed_hub.add_feed_pipeline('ProxyModel', pipeline=pipeline)

        test_feed_hub.activate()
        time.sleep(5)
        self.assertEqual(test_feed_hub.get_number('ProxyModel'), 20)

        test_feed_hub.stop()

    @unittest.skip
    def test_duplication_failed(self):
        failed_setting = Setting()

        failed_setting.Duplication = {
            'host': '1.1.1.1',
        }
        with self.assertRaises(Exception):
            pipeline = Pipeline([FailedDuplication], setting=failed_setting)

        with self.assertRaises(TypeError):
            pipeline = Pipeline([CannotConnectDuplication], setting=failed_setting)

        failed = Hub(setting=failed_setting)

        failed.add_feed_pipeline('Model', pipeline=pipeline)

    @unittest.skip
    def test_duplication(self):
        setting = Setting()

        pipeline = Pipeline([CustomMockDuplication], setting=setting)
        r = redis.Redis()

        for k in r.keys('testcustom:*'):
            r.delete(k)

        hub = Hub(setting=setting)
        hub.add_dump_pipeline('Model', pipeline=pipeline)
        hub.activate()
        time.sleep(1)
        hub.stop(dump_all=True)

        self.assertEqual(len(r.keys('testcustom:*')), 100)
