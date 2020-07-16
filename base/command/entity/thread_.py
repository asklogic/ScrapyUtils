import time
from concurrent.futures._base import TimeoutError as ConcurrentTimeout
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock, Event
from typing import List

from base.components import *
from base.exception import CommandExit
from . import Command, ComponentMixin

from base.components import *
from base.libs import Task, Consumer, Producer
from base.core import get_scraper


class Thread(Command, ComponentMixin):
    do_collect = True

    consumers: List[Consumer] = []

    @classmethod
    def syntax(cls):
        return '[Thread]'

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

        # TODO: refactor this

        # empty_flag = False
        #
        # while not empty_flag:
        #     [x.start() for x in cls.consumers]
        #     while cls.tasks.qsize() != 0:
        #         time.sleep(0.1)
        #
        #     [x.stop() for x in cls.consumers]
        #
        #     empty_flag = cls.tasks.empty()
        #
        # [x.stop() for x in cls.consumers]

    @classmethod
    def exit(cls):
        """
        正常退出
        """
        # scrapers = get_scraper()
        # [scraper.scraper_quit() for scraper in scrapers]

        [x.stop() for x in cls.consumers]

        log.info('exit command {}'.format(cls.__name__), 'System')

        # suit exit
        [suit.suit_exit() for suit in cls.suits]

        if cls.pipeline:
            cls.pipeline.suit.suit_exit()
            # TODO: wait to pipeline.
            cls.pipeline.exit()

        log.info('tasks remain: {}'.format(cls.tasks.qsize()), 'Exit')
        log.info('models remain: {}'.format(len(cls.pipeline.failed)), 'Exit')

        log.info('command finished.')

    @classmethod
    def signal_callback(cls, signum, frame):
        # [x.stop() for x in cls.consumers]

        log.warning('thread signal callback exit!.', 'Interrupt')

        # while not cls.tasks.empty():
        #     cls.tasks.get()

        raise CommandExit()

    @classmethod
    def failed(cls):
        # TODO: failed in command thread
        # [x.stop() for x in cls.consumers]

        # [x.scraper.scraper_quit() for x in cls.suits]

        log.info('command Thread failed!.')

    @classmethod
    def finished(cls):
        case_empty = cls.tasks.qsize() == 0
        case_block = [None for consumer in cls.consumers if not consumer.block] == []
        return case_empty and case_block
        # return case_empty and not [None for consumer in cls.consumers if not consumer.block]
        # return not (cls.tasks.qsize() > 0 or [None for consumer in cls.consumers if not consumer.block])


class ScrapyConsumer(Consumer):
    _suit: StepSuit = None
    _pipeline: Pipeline = None
    _proxy: Producer = None

    def __init__(self, suit: StepSuit, pipeline: Pipeline, proxy: Producer = None,
                 timeout=20,
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
        Consumer.__init__(self, kwargs.pop('queue'), kwargs.pop('delay', 1), kwargs.pop('lock', None), True, **kwargs)

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

            current.count += 1
            if current.count <= 5:
                self.queue.put(current)
            if self.proxy:
                self.scraper.proxy = self.proxy.queue.get()

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
