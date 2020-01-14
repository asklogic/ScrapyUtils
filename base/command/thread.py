from typing import List, Tuple, Callable

import time
import os
from queue import Queue
from threading import Lock, Event

from base.command import Command
from base.components import *
from base.libs import *

from base.core import *
from base.log import set_syntax, set_line

from multiprocessing.dummy import Pool as ThreadPool
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as ConcurrentTimeout

from multiprocessing import TimeoutError


class Thread(Command):
    do_collect = True

    config: dict = None
    suits: List[StepSuit] = None

    def syntax(self) -> str:
        return '[THREAD]'

    def options(self, **kwargs):
        # path = kwargs.get('path', PROJECT_PATH)
        # scheme = kwargs.get('scheme')
        # assert scheme, 'no scheme'
        #
        # path = os.path.join(path, scheme)
        # assert os.path.exists(path), path + ' not exist'

        set_syntax('[Thread]')
        set_line(kwargs.get('line', 3))

        # TODO:  task's count

        # TODO: log out config info.

        steps = get_steps()
        gen = get_scraper_generate()

        self.config = get_config()
        self.queue = get_tasks()

        def inner_suit():
            suit = StepSuit(steps, gen())
            suit.suit_activate()
            return suit

        self.suits = list_builder(inner_suit, self.config.get('thread'), 10)

    def run(self):
        # def inner_suit():
        #     suit = StepSuit(steps, gen())
        #     suit.suit_activate()
        #     return suit

        # TODO: to suit builder
        # scrapers = list_builder(get_scraper_generate(), config.get('thread'), 10)
        # suits = list_builder(inner_suit, config.get('thread'), 10)

        # suits = []
        # for x in scrapers:
        #     suit = StepSuit(steps, x)
        #     suit.suit_activate()
        #     suits.append(suit)

        current_pipeline = get_pipeline()

        # consumer's
        event = Event()
        lock = Lock()

        kws = [
            {
                'queue': self.queue,
                'delay': self.config.get('timeout'),
                'suit': x,
                'pipeline': current_pipeline,

                'event': event,
                'lock': lock,
            }

            for x in self.suits
        ]

        consumers = [ScrapyConsumer(**kw) for kw in kws]

        [x.start() for x in consumers]

        time.sleep(1)

        # TODO: log out

        # [x.stop() for x in consumers]
        #
        consumers[0].exit()

        [x.stop() for x in consumers]

        [suit.suit_exit() for suit in self.suits]

    def exit(self):
        log.info('trying to exit suits and scrapers.')

        [suit.suit_exit() for suit in self.suits]

        log.info('done.')

        time.sleep(1)

        # TODO: wait to pipeline.

        log.info('command Thread done.')

    def signal_callback(self, signum, frame):
        [suit.suit_exit() for suit in self.suits]

        log.info('command Thread signal callback exit!.')

    def failed(self):
        [suit.suit_exit() for suit in self.suits]

        log.info('command Thread failed!.')


class ScrapyConsumer(Consumer):
    _suit: StepSuit = None
    _pipeline: Pipeline = None
    _proxy: Consumer = None

    def __init__(self, suit: StepSuit, pipeline: Pipeline, proxy: Consumer = None,
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
        # if self.proxy:
        #     self.scraper.proxy = self.proxy.get()
        pass

        # if self.suit.scrapy(current):
        #     # res is True. gather model.
        #     for model in self.suit.models:
        #         self.pipeline.push(model)
        # else:
        #     # res is False, retry.
        #     current.count += 1
        #
        #     # TODO: custom retry count.
        #     if current.count <= 3:
        #         self.queue.put(current)

        func = self.suit.closure_scrapy()

        # kw = {'task': current}

        # async_res = thread_pool.apply_async(func, kwds=kw, callback=self.callback())
        # TODO: timeout

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

    # abort
    # def error_callback(self):
    #     def error_callback_inline():
    #         pass
    #
    #     return error_callback_inline


def list_builder(invoker, number, timeout=10):
    res_list = []

    def inner():
        res = invoker()
        res_list.append(res)

    with ThreadPoolExecutor(number) as executor:
        futures = [executor.submit(inner) for x in range(number)]

    [x.result(timeout) for x in futures]

    return res_list
