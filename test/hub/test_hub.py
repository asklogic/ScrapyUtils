import unittest
from typing import Any
from unittest import TestCase
import sys
import multiprocessing.dummy as dummy
import time

sys.path.append(r"E:\cloudWF\python\ScrapyUtils")

from base.Model import Model
from base.lib import Config

from base._core import load_default_models
from base.Process import Pipeline, Processor, target
from base.common import JsonFileProcessor, DuplicateProcessor
from base.Model import ProxyModel, ModelManager, FailedTaskModel, TaskModel, Field

from base.hub import Hub
from base.tool import get_proxy_model, jinglin

import faker
import redis

f = faker.Faker(locale='zh_CN')


class Feed_Proxy_TestProcessor(Processor):
    target = ProxyModel

    def start_process(self, model: type(Model), number: int):
        pass
        # self.proxy_data: [] = jinglin(number)

    def process_item(self, model: ProxyModel) -> Any:
        # proxy = self.proxy_data.pop().split(":")
        # model.ip = proxy[0]
        # model.port = proxy[1]

        model.ip = "4321"
        model.port = "1234"
        return model


class Proxy_Processor(Processor):
    target = ProxyModel

    def start_process(self, number: int, model: str = "Model"):
        self.proxy_data: [] = jinglin(number)

    def process_item(self, model: ProxyModel) -> Any:
        proxy = self.proxy_data.pop().split(":")
        model.ip = proxy[0]
        model.port = proxy[1]
        return model


class TestStudentModel(Model):
    name = Field()
    age = Field()


class FakeName_Feed_Test_Processor(Processor):
    target = TestStudentModel

    def process_item(self, model: TestStudentModel) -> Any:
        model.name = f.name()
        model.age = f.random_digit()
        return model


class RandomDump_Processor(Processor):
    # target = TestStudentModel
    def process_item(self, model: Model) -> Any:
        if f.random_digit() > 5:
            return model


class FakeName_Dump_Test_Processor(Processor):
    # target = TestStudentModel

    def start_process(self, number: int, model: str = "Model"):
        print("start dump")
        self.count = 0

    def process_item(self, model: TestStudentModel) -> Any:
        self.count = self.count + 1
        return model
        pass

    def end_process(self):
        print("process number", self.count)
        pass


class Duplication(DuplicateProcessor):
    target = TestStudentModel

    # def start_task(self, settings: dict):
    #     self.set_base("Test", "StudentModel", "FakeName")

    def process_item(self, model: TestStudentModel) -> Any:
        if self.check_identification(model.name):
            self.count = self.count + 1
            return model

    def end_process(self):
        print("save key:", self.count)


class TestHub(TestCase):
    def setUp(self):
        ModelManager.add_model(TestStudentModel)

        # self.mock_pipeline = Pipeline([FakeName_Feed_Test_Processor])

        pass

    def tearDown(self):
        r = redis.Redis(decode_responses=True)
        for k in r.keys("Test*"):
            pass
            r.delete(k)

    def test_init_hub(self):
        ModelManager.add_model(ProxyModel)
        return

        # hub = Hub([ProxyModel], self.mock_pipeline)

        # m: ProxyModel = hub.pop("ProxyModel")
        # print(m.pure_data())
        # time.sleep(0.5)

    def test_dump_hub(self):

        return
        # [ModelManager.model("TestStudentModel") for i in range(20)]

        # class TestClass(object):
        #
        #     def __init__(self):
        #         self.data = {}
        #
        # testList = [TestStudentModel() for x in range(20)]
        #
        # [print("test list id ", id(x.data)) for x in testList]

        temp_p = Pipeline([FakeName_Feed_Test_Processor])
        mockModel = temp_p.feed_model("TestStudentModel", 2000)

        for model in mockModel:
            self.assertEqual(len(mockModel), 2000)
            self.assertIsInstance(model, TestStudentModel)

        hub = Hub([TestStudentModel], Pipeline([FakeName_Dump_Test_Processor]), feed=False,
                  limit=500)

        for model in mockModel:
            hub.save(model)
        time.sleep(5)
        hub.stop()
        time.sleep(1)

    def test_feed_hub(self):
        return

        ModelManager.add_model(ProxyModel, TaskModel, TestStudentModel)
        hub = Hub([ProxyModel, TaskModel, TestStudentModel],
                  Pipeline([Feed_Proxy_TestProcessor, FakeName_Feed_Test_Processor]), 5)

        tm: TaskModel = ModelManager.model("TaskModel")
        tm.url = "https://ip.cn/"

        hub.remove_pipeline("TaskModel")
        hub.save(tm)
        hub.save(tm)
        hub.save(tm)
        hub.save(tm)
        hub.save(tm)
        hub.save(tm)

        # try:
        #     for i in range(10):
        #         print(i)
        #         pm: TaskModel = hub.pop("TaskModel")
        #         self.assertIsInstance(pm, TaskModel)
        #         self.assertEqual(pm.url, "https://ip.cn/")
        # except Exception as e:
        #     print("end!")

        # for i in range(20):
        #     m = hub.pop("TestStudentModel")
        #     print(m.pure_data())
        #
        # time.sleep(30)
        # hub.stop()

        # hub.pop("ProxyModel")

    def test_sys_feed_hub(self):
        return

        ModelManager.add_model(ProxyModel, TaskModel)

        # ModelManager.add_model(TestStudentModel)
        #
        # temp_p = Pipeline([FakeName_Feed_Test_Processor])
        # mock_models = temp_p.feed_model("TestStudentModel", 5000)

        # 建立sys hub
        sys_hub = Hub([ProxyModel, TaskModel], Pipeline([Proxy_Processor]), 5, 20, feed=True)

        # 重要
        # 移除TaskModel的pipeline
        sys_hub.remove_pipeline("TaskModel")
        sys_hub.remove_pipeline("ProxyModel")

        sys_hub.activate()
        # time.sleep(5)

        # 获取Proxy

        # for i in range(50):
        #     time.sleep(0.2)
        #     m = sys_hub.pop("ProxyModel")
        #     self.assertIsInstance(m, ProxyModel)
        #     print(m.pure_data())

        # 保存Task 并且取用Task对象
        print(" - test - task storage")
        for i in range(2000):
            tm: TaskModel = ModelManager.model("TaskModel")
            tm.url = f.url()
            sys_hub.save(tm)

        while True:
            import queue
            try:
                tm = sys_hub.pop("TaskModel")
                self.assertIsInstance(tm, TaskModel)
            except Exception as qe:
                print(" no task model in hub")
                self.assertIsInstance(qe, queue.Empty)
                break

        try:
            print("first")
            tm = sys_hub.pop("TaskModel")
            self.assertIsInstance(tm, TaskModel)
        except Exception as qe:
            self.assertIsInstance(qe, queue.Empty)

        try:
            print("second")
            tm = sys_hub.pop("TaskModel")
            self.assertIsInstance(tm, TaskModel)
        except Exception as qe:
            self.assertIsInstance(qe, queue.Empty)

        pass
        # 添加TaskModel

        pass

    def test_sys_dump_hub(self):
        return


        ModelManager.add_model(TestStudentModel)

        temp_p = Pipeline([FakeName_Feed_Test_Processor])
        mock_models = temp_p.feed_model("TestStudentModel", 50000)

        print("test start")
        # [print(x.pure_data()) for x in mock_models]

        setting = {
            "job": "TestJob",
        }

        #
        p = Pipeline([Duplication, FakeName_Dump_Test_Processor], setting)

        setting2 = {
            "JsonFile": {
                "mark": 1001,
            }
        }
        p2 = Pipeline([Duplication, FakeName_Dump_Test_Processor, JsonFileProcessor], setting2)
        dump_hub = Hub([TestStudentModel], p2, limit=5000, feed=False, )
        dump_hub.activate()

        [dump_hub.save(x) for x in mock_models]
        time.sleep(10)


if __name__ == '__main__':
    unittest.main()
