from typing import List

import time
import os
from queue import Queue

from base.command import Command
from base.components import *
from base.libs import *

from base.core import collect, PROJECT_PATH
from base import log


class Thread(Command):
    do_collect = True

    def syntax(self) -> str:
        return '[THREAD]'

    def options(self, **kwargs):
        # path = kwargs.get('path', PROJECT_PATH)
        # scheme = kwargs.get('scheme')
        # assert scheme, 'no scheme'
        #
        # path = os.path.join(path, scheme)
        # assert os.path.exists(path), path + ' not exist'

        # TODO: exception info
        line = int(kwargs.get('line', 3))
        log.line = line

        # TODO:  task's count

    def run(self):
        kwargs = {
            'queue': collect.tasks,
            'delay': collect.config['timeout'],
            # TODO. stepsuit
            'suit': StepSuit(collect.steps, collect.scraper()),

            'pipeline': collect.models_pipeline,
        }

        suit = ThreadSuit(ScrapyConsumer, collect.config['thread'], kw=kwargs, copy_attr=['suit'])
        suit.start_all()

        while not collect.tasks.empty():
            time.sleep(0.3)

    def exit(self):
        print('invoke command exit!')

    def signal_callback(self, signum, frame):
        print('invoke command signal callback exit!')

    def failed(self):
        print('invoke command failed!')


class ScrapyThread(Consumer):
    def __init__(self, steps: List[Step], scraper: type(Scraper), pipeline: Pipeline, log, **kwargs):
        # super(ScrapyThread, self).__init__(task_queue, kwargs.get('delay'), **{})
        Consumer.__init__(self, queue=kwargs.get('queue'), delay=kwargs.pop('delay', 1), lock=kwargs.get('lock'),
                          **kwargs)

        #
        scraper = scraper()
        scraper.scraper_activate()

        self.suit = StepSuit(steps, scraper, log)
        self.pipeline = pipeline

    def consuming(self, current: Task):
        # log in scrapy method
        if self.suit.scrapy(current):
            # TODO refact models deque
            for model in self.suit.models:
                self.pipeline.push(model)
        else:

            current.count += 1
            if current.count <= 3:
                self.queue.put(current)

        self.suit.models.clear()


class ScrapyConsumer(Consumer):
    _suit: StepSuit
    _pipeline: Pipeline

    def __init__(self, suit: StepSuit, pipeline: Pipeline, **kwargs):
        Consumer.__init__(self, kwargs.pop('queue'), kwargs.pop('delay', 1), kwargs.pop('lock', None), **kwargs)

        assert isinstance(suit, StepSuit), 'ScrapyConsumer need StepSuit.'
        assert isinstance(pipeline, Pipeline), 'ScrapyConsumer need Pipeline.'

        self._suit = suit
        self._pipeline = pipeline

        # TODO
        suit.scraper.scraper_activate()

    @property
    def suit(self):
        return self._suit

    @property
    def pipeline(self):
        return self._pipeline

    def consuming(self, current: Task):
        # log in scrapy method
        if self.suit.scrapy(current):
            # TODO refact models deque
            for model in self.suit.models:
                self.pipeline.push(model)
        else:

            current.count += 1
            if current.count <= 3:
                self.queue.put(current)

        self.suit.models.clear()
