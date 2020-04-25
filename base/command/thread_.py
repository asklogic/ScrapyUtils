from typing import List, Tuple, Callable

import time
import os
import click
from queue import Queue
from threading import Lock, Event

from base.components import *
from base.libs import *

from base.core import *
from base.log import set_syntax, set_line
from base.exception import CommandExit

from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as ConcurrentTimeout

from multiprocessing import TimeoutError

from ._base import Command, ComponentMixin


class Thread(Command, ComponentMixin):
    do_collect = True

    consumers = None

    @classmethod
    def run(cls, kw):
        event = Event()
        lock = Lock()

        kws = [
            {
                'queue': cls.tasks,
                'delay': cls.config.get('timeout'),
                'suit': x,
                'pipeline': cls.pipeline,
                'proxy': cls.proxy,

                'event': event,
                'lock': lock,
            }
            for x in cls.suits
        ]
        cls.consumers = [ScrapyConsumer(**kw) for kw in kws]

        event.set()

        while cls.tasks.qsize() != 0:
            time.sleep(0.1)

        [x.stop() for x in cls.consumers]

    @classmethod
    def exit(cls):
        """
        正常退出
        """
        log.debug('trying to exit suits and scrapers.')

        # suit exit
        [x.suit_exit() for x in cls.suits]
        cls.pipeline.suit.suit_exit()

        # TODO: wait to pipeline.

        cls.pipeline.exit()

        log.debug('command Thread exit.')

    @classmethod
    def signal_callback(cls, signum, frame):
        [x.stop() for x in cls.consumers]

        # [suit.suit_exit() for suit in self.suits]

        log.info('command Thread signal callback exit!.')
        raise CommandExit()

    @classmethod
    def failed(cls):
        [x.stop() for x in cls.consumers]

        # [x.scraper.scraper_quit() for x in cls.suits]

        log.info('command Thread failed!.')


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
                for model in self.suit.models:
                    self.pipeline.push(model)
            else:
                # res is False, retry.
                current.count += 1

                # TODO: custom retry count.
                if current.count <= 3:
                    self.queue.put(current)

                if self.proxy:
                    self.scraper.proxy = self.proxy.queue.get()


def list_builder(invoker, number, timeout=10):
    res_list = []

    def inner():
        res = invoker()
        res_list.append(res)

    executor = ThreadPoolExecutor(number)

    futures = [executor.submit(inner) for x in range(number)]

    # method result will raise exception when timeout.
    [x.result(timeout) for x in futures]

    # TODO: exit executor.
    executor.shutdown(False)

    return res_list
