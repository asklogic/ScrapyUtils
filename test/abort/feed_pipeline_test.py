import unittest
from typing import Any
from unittest import TestCase
import concurrent.futures

import sys

sys.path.append(r"E:\cloudWF\python\ScrapyUtils")

from base.Model import Model, ModelManager
from base.Process import Pipeline, Processor, target
from base.Model import ProxyModel
from base.Container import _Container
from multiprocessing import dummy


# from

class Feed_Proxy_TestProcessor(Processor):

    def start_process(self):
        pass

    @target(ProxyModel)
    def process_item(self, model: ProxyModel) -> Any:
        model.ip = "123"
        model.port = "1234"
        return model


class Feed_Pipeline_Test(TestCase):

    def setUp(self) -> None:
        self.manager = ModelManager([ProxyModel])
        self.pipeline = Pipeline(self.manager, [Feed_Proxy_TestProcessor])
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def tearDown(self):
        self.pool.shutdown(wait=True)

    def test_feed(self):
        pass
        # manager = ModelManager([ProxyModel])
        # f = FeedPipeline(manager, [Feed_Proxy_TestProcess])

        # for model in res:
        #     self.assertIsInstance(model, ProxyModel)
        #     print(model.pure_data())

    def test_feed_in_poo1(self):
        # pool = dummy.Pool(processes=1)

        print("conccurrent!")

        def feed_callback(fu: concurrent.futures.Future):
            print(fu.result())
            pass

        # pool.submit(self.pipeline.feed_process, "ProxyModel", 10).add_done_callback(feed_callback)

        self.pool.shutdown(wait=True)

    def test_dump(self):
        def feed_callback(fu: concurrent.futures.Future):
            print(fu.result())

        res = self.pipeline.feed_model("ProxyModel", 10)
        self.pool.submit(self.pipeline.dump_model, res).add_done_callback(feed_callback)

        self.pool.shutdown(wait=True)

    # def test_concurrent(self):
    #     import concurrent.futures
    #
    #
    #     def callback(obj: concurrent.futures.Future):
    #         print(obj)
    #         print(obj.result())
    #         pass
    #
    #     def sel(p):
    #         return "1"
    #
    #     print("conccurrent!")
    #     pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    #
    #     pool.submit(sel, ("ToT")).add_done_callback(callback)


if __name__ == '__main__':
    unittest.main()
