import unittest

from base.command.thread_ import ScrapyConsumer
from base.core import collect_scheme
from base.core import *

from base.libs import ThreadWrapper, Task

from typing import Callable
from tests.telescreen import tests_path
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool
from multiprocessing import TimeoutError
import random
import time

import threadpool
import threading
from threading import Thread
from base.components import StepSuit


class ScrapyConsumerTestCase(unittest.TestCase):

    def setUp(cls) -> None:
        collect_scheme('atom')

        suit = StepSuit(get_steps(), get_scraper_generate()())
        suit.suit_activate()

        cls.params = {
            'queue': get_tasks(),
            'delay': 0.3,

            'suit': suit,
            'proxy': collect.proxy,
            'pipeline': collect.models_pipeline,

        }

        cls.scraper = collect.scrapers()

    # def test_test(self):
    #     class Wrapper(threading.Thread):
    #
    #         def __init__(self, callback: threading.Thread):
    #             super().__init__()
    #             self.callback = callback
    #
    #             # self.setDaemon(True)
    #
    #         def run(self) -> None:
    #             print('run wrapper', self.callback)
    #             self.callback.start()
    #
    #             time.sleep(1)
    #             print('wrapper done.')
    #
    #     class Instable(threading.Thread):
    #         def __init__(self):
    #             super(Instable, self).__init__()
    #             self.setDaemon(False)
    #
    #         def run(self) -> None:
    #             delay = random.uniform(1, 5)
    #             print('inner start. ', delay)
    #
    #             time.sleep(delay)
    #
    #             print('inner done.')
    #
    #     ins = Instable()
    #     wrapper = Wrapper(ins)
    #
    #     wrapper.run()
    #
    #     # time.sleep(4)
    #     print('main done')
    #     pass

    # wrapper.join()

    #
    # @unittest.skip
    # def test_demo(self):
    #
    #     def instable(*args):
    #         delay = random.uniform(1, 5)
    #         print('start. ', delay)
    #
    #         time.sleep(delay)
    #
    #         print('done.')
    #
    #     def callback(req, value, ):
    #         print('callback', req, value)
    #
    #     def error_callback(*args):
    #         print('error_callback', args)
    #
    #     # res = the_pool.apply_async(instable, callback=callback, error_callback=error_callback)
    #
    #     _thread_pool = threadpool.ThreadPool(5)
    #     res = threadpool.makeRequests(instable, [], callback=callback, exc_callback=error_callback)
    #     res = threadpool.makeRequests(instable, [None], callback=callback)
    #
    #     _thread_pool.putRequest(res[0], block=True, timeout=2.5)
    #     try:
    #         res
    #     except TimeoutError as e:
    #         print('timeout')
    #         time.sleep(3)
    #         pass
    #
    #     _thread_pool.wait()
    #     # _thread_pool.poll(block=True)

    def test_init(self):
        self.params['delay'] = 1
        self.params['lock'] = threading.Lock()
        # self.params['event'] = threading.Event()

        consumer = ScrapyConsumer(**self.params)
        consumer.start()
        consumer.wait_exit()

    def test_case_lock(self):
        pass


    # # @unittest.skip
    # def test_method_consuming_prototype(self):
    #     # prepare
    #     queue = self.params.get('queue')
    #     [queue.get() for i in range(9)]
    #     consumer = ScrapyConsumer(**self.params)
    #     task = queue.get()
    #
    #     consumer.start()
    #     consumer.exit()
    #
    #     consumer.suit.suit_activate()
    #
    #     func = consumer.suit.closure_scrapy()
    #
    #     t = ThreadWrapper(func, (task,), 2)
    #     t.start()
    #     t.join()
    #     assert t.result[0] is True
    #     assert isinstance(t.result[1], Task)
    #
    # def test_method_start(self):
    #     consumer = ScrapyConsumer(**self.params)
    #     consumer.start()
    #
    #     assert consumer.scraper.activated is True
    #
    #     assert consumer.suit.steps
    #     assert consumer.suit.scraper
    #
    # def test_method_stop(self):
    #     consumer = ScrapyConsumer(**self.params)
    #     consumer.start()
    #
    #     consumer.stop()
    #
    #     assert consumer.scraper.activated is False
    #
    # def test_method_consuming(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
