import unittest
from typing import Any
from unittest import TestCase

import sys

sys.path.append(r"E:\cloudWF\python\ScrapyUtils")

from base.hub.pipeline import Pipeline
from base.Process import Pipeline, target
from base.components.proceesor import Processor
from base.common import JsonFileProcessor, ProxyModel
from base.components.model import Field, Model, ModelManager


class TestFeedModel(Model):
    name = Field()
    age = Field()


class Feed_Proxy_TestProcessor(Processor):
    target = ProxyModel

    def start_process(self, model: type(Model), number: int):
        pass
        # self.proxy_data: [] = jinglin(5)

    def process_item(self, model: ProxyModel) -> Any:
        # proxy = self.proxy_data.pop().split(":")
        # model.ip = proxy[0]
        # model.port = proxy[1]

        model.ip = "4321"
        model.port = "1234"
        return model


class Feed_TestFeedModel_Processor(Processor):
    target = TestFeedModel

    def process_item(self, model: TestFeedModel) -> Any:
        model.name = "tn"
        model.age = "ta"
        print(model.pure_data())

        return model


class Dump_test_processor(Processor):

    def start_process(self, model: type(Model), number: int):
        print(model)
        print(number)

    @target(ProxyModel)
    def process_item(self, model: Model) -> Any:
        # print(model.pure_data())
        pass


class File_test_process(JsonFileProcessor):

    def start_task(self):
        self.dir_path = r"E:\cloudWF\python"
        self.mark = str(6324)


class re_Pipeline_Test(TestCase):
    def test_init(self):
        pipeline = Pipeline([Feed_Proxy_TestProcessor])

    def test_feed(self):
        return
        ModelManager.add_model(ProxyModel, TestFeedModel)

        m = ModelManager.model("ProxyModel")
        isinstance(m, Model)

        pipeline = Pipeline([Feed_Proxy_TestProcessor, Feed_TestFeedModel_Processor])

        models = pipeline.feed_model("ProxyModel", 5)
        print([x.pure_data() for x in models])

        self.assertEqual(len(models), 5)
        self.assertIsInstance(models[0], Model)

        models = pipeline.feed_model("TestFeedModel", 10)
        print([x.pure_data() for x in models])


if __name__ == '__main__':
    unittest.main()
