import unittest
import time
from typing import Callable

from base.libs import RequestScraper, Scraper, FireFoxScraper, Producer
from base.components import StepSuit

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as ConcurrentTimeout
from multiprocessing.dummy import Pool as ThreadPool

from base.components import Step
from queue import Queue

from base.command import *
from base.libs import *
from base.components import *
from base.log import set_syntax

from threading import Lock, Event

from tests import telescreen


class Thread(Command, ComponentMixin):

    @classmethod
    def run(self):
        event = Event()
        lock = Lock()

        kws = [
            {
                'queue': self.tasks,
                'delay': self.config.get('timeout'),
                'suit': x,
                'pipeline': self.pipeline,
                'proxy': self.proxy,

                'event': event,
                'lock': lock,
            }
            for x in self.suits
        ]
        consumers = [ScrapyConsumer(**kw) for kw in kws]

        event.set()

        while self.tasks.qsize() != 0:
            time.sleep(0.1)

        [x.stop() for x in consumers]


class CommandThread(unittest.TestCase):

    def test_demo(self):
        trigger('thread', **{'scheme': 'atom'})


class ScrapyConsumer(Consumer):
    _suit: StepSuit = None
    _pipeline: Pipeline = None
    _proxy: Producer = None

    def __init__(self, suit: StepSuit, pipeline: Pipeline, proxy: Producer = None,
                 timeout=10,
                 **kwargs):

        # assert
        assert isinstance(pipeline, Pipeline), 'ScrapyConsumer need Pipeline.'
        assert isinstance(suit, StepSuit), 'ScrapyConsumer need StepSuit instance.'

        assert suit.scraper.activated, 'scraper must be activated.'

        self._pipeline = pipeline
        self._proxy = proxy
        self._suit = suit

        self.timeout = timeout

        # super
        Consumer.__init__(self, kwargs.pop('queue'), kwargs.pop('delay', 1), kwargs.pop('lock', None), **kwargs)

    @property
    def suit(self):
        return self._suit

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def proxy(self):
        return self._proxy

    @property
    def scraper(self):
        return self.suit.scraper

    def consuming(self, current: Task):

        # TODO: proxy.
        # if self.proxy and not self.scraper.proxy:
        #     self.scraper.proxy = self.proxy.queue.get()

        func = self.suit.closure_scrapy()

        try:
            with ThreadPoolExecutor(1) as pool:
                future = pool.submit(func, current)
                result = future.result(self.timeout)
        except ConcurrentTimeout as CT:
            # TODO: rebuild
            pass
        else:
            if result[0]:
                for data_model in self.suit.models:
                    self.pipeline.push(data_model)
            else:
                # res is False, retry.
                current.count += 1

                # TODO: custom retry count.
                if current.count <= 3:
                    self.queue.put(current)

                if self.proxy:
                    self.scraper.proxy = self.proxy.queue.get()


if __name__ == '__main__':
    unittest.main()
