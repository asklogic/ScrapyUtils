import time
from concurrent.futures._base import TimeoutError as ConcurrentTimeout
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock, Event
from typing import List

from ScrapyUtils.components import *
from ScrapyUtils.exception import CommandExit
from . import Command, ComponentMixin

from ScrapyUtils.components import *
from ScrapyUtils.libs import Task, Consumer, Producer
from ScrapyUtils.core import get_scraper

from ScrapyUtils.core import configure

class Thread(Command, ComponentMixin):
    do_collect = True

    consumers: List[Consumer] = []

    @classmethod
    def syntax(cls):
        return '[Thread]'

    @classmethod
    def run(cls, options):
        """
        Args:
            options:
        """
        event = Event()
        lock = Lock()

        kws = [
            {
                'queue': cls.tasks,
                'delay': configure.TIMEOUT,
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

    @classmethod
    def exit(cls):
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

        # Tail open log file and 1 second delay to remove log file.
        time.sleep(1)

    @classmethod
    def paused(cls):
        [x.stop(False) for x in cls.consumers]

    @classmethod
    def restart(cls):
        [x.start() for x in cls.consumers]

    @classmethod
    def signal_callback(cls, signum, frame):
        # [x.stop() for x in cls.consumers]

        """
        Args:
            signum:
            frame:
        """
        log.warning('thread signal callback exit!.', 'Interrupt')

        # while not cls.tasks.empty():
        #     cls.tasks.get()

        raise CommandExit()

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

            current.count += 1
            if current.count <= 5:
                self.queue.put(current)
            if self.proxy:
                self.scraper.proxy = self.proxy.queue.get()

        else:
            if result:
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
