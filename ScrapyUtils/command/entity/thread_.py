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
from ScrapyUtils.core import *

from ScrapyUtils.core import configure

from . import log


class Thread(Command, ComponentMixin):
    do_collect = True

    consumers: List[Consumer] = []

    @classmethod
    def syntax(cls):
        return '[Thread]'

    @classmethod
    def logout(cls):
        # output
        time.sleep(1)
        log.info('Scheme basic info:')

        log.info('Task number: {}.'.format(get_tasks().qsize()))
        # log.info(f'Task number: <{tasks.qsize()}> - ')
        log.info('Threads number : {}'.format(configure.THREAD))

        log.info(' ---------- Activated Steps List ----------')
        for i in range(len(get_steps())):
            # log.info(f'<{i + 1}> - {steps_class[i].name} - {steps_class[i].step_type}')
            log.info(
                f'({get_steps()[i].priority}) - <{get_steps()[i].name}> - '
                f'{"Action" if isinstance(get_steps()[i], ActionStep) else "Parser"}')

        # log.info('Processor Components:')
        log.info(' ---------- Activated Processors List ----------')
        for i in range(len(get_processors())):
            log.info(f'({get_processors()[i].priority}) - <{get_processors()[i].name}>')

    @classmethod
    def run(cls, options):

        cls.logout()

        event = Event()
        lock = Lock()

        kws = [
            {
                'queue': get_tasks(),
                'delay': configure.TIMEOUT,
                'suit': x,
                'pipeline': get_pipeline(),
                'proxy': get_proxy(),

                'event': event,
                'lock': lock,
            }
            for x in get_suits()
        ]
        cls.consumers = [ScrapyConsumer(**kw) for kw in kws]

        event.set()

    @classmethod
    def exit(cls):
        cls.consumers[0].stop(block=True)

        log.info('exit command {}'.format(cls.__name__), 'System')

        if cls.pipeline:
            cls.pipeline.suit.suit_exit()
            # TODO: wait to pipeline.
            cls.pipeline.exit()

        log.info('tasks remain: {}'.format(get_tasks().qsize()), 'Exit')
        log.info('models remain: {}'.format(len(get_pipeline().failed)), 'Exit')

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
        case_empty = get_tasks().qsize() == 0
        case_block = [None for consumer in cls.consumers if not consumer.block] == []
        return case_empty and case_block

        # return case_empty and not [None for consumer in cls.consumers if not consumer.block]
        # return not (cls.tasks.qsize() > 0 or [None for consumer in cls.consumers if not consumer.block])


class ScrapyConsumer(Consumer):
    _suit: StepSuit = None
    _pipeline: Pipeline = None
    _proxy: Producer = None

    def __init__(self, suit: StepSuit, pipeline: Pipeline, proxy: Producer = None,
                 timeout=100,
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
        # except ConcurrentTimeout as CT:
        #     # TODO: rebuild
        #     pass
        #
        #     current.count += 1
        #     if current.count <= 5:
        #         self.queue.put(current)
        #     if self.proxy:
        #         self.scraper.proxy = self.proxy.queue.get()
        except Exception as e:
            # failed.
            current.count += 1

            # TODO: custom retry count.
            if current.count <= 3:
                self.queue.put(current)

            if self.proxy:
                self.scraper.proxy = self.proxy.queue.get()

            log.error(f'failed in {current.url}')
            log.exception(e, line=2)

        else:
            # success
            for model in self.suit.models:
                self.pipeline.push(model)

            log.info(f'success in {current.url}')
