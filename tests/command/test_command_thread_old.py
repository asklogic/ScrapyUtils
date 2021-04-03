import unittest
import time

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as ConcurrentTimeout

from base.command import Command, ComponentMixin, trigger
from base.libs import *
from base.components import *

from threading import Lock, Event





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
        """
        Args:
            suit (StepSuit):
            pipeline (Pipeline):
            proxy (Producer):
            timeout:
            **kwargs:
        """
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

        """
        Args:
            current (Task):
        """
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
                current.mock_count += 1

                # TODO: custom retry count.
                if current.mock_count <= 3:
                    self.queue.put(current)

                if self.proxy:
                    self.scraper.proxy = self.proxy.queue.get()


if __name__ == '__main__':
    unittest.main()
