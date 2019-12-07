from typing import List, Tuple

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
            'suit_param': (collect.steps, collect.scraper_generate, collect.proxy, self.log),

            'pipeline': collect.models_pipeline,
        }

        suit = ThreadSuit(ScrapyConsumer, collect.config['thread'], kw=kwargs, copy_attr=['suit'])
        suit.start_all()

        while not collect.tasks.empty():
            time.sleep(0.3)

        suit.stop()

    def exit(self):
        print('invoke command exit!')

    def signal_callback(self, signum, frame):
        print('invoke command signal callback exit!')

    def failed(self):
        print('invoke command failed!')


class ScrapyConsumer(Consumer):
    _suit: StepSuit
    _pipeline: Pipeline

    def __init__(self, suit_param: Tuple, pipeline: Pipeline, **kwargs):
        Consumer.__init__(self, kwargs.pop('queue'), kwargs.pop('delay', 1), kwargs.pop('lock', None), **kwargs)

        # TODO: suit
        scraper = suit_param[1]()
        suit = StepSuit(suit_param[0], scraper, suit_param[2], suit_param[3])

        assert isinstance(suit, StepSuit), 'ScrapyConsumer need StepSuit.'
        assert isinstance(pipeline, Pipeline), 'ScrapyConsumer need Pipeline.'

        self._suit = suit
        self._pipeline = pipeline

    @property
    def suit(self):
        return self._suit

    @property
    def pipeline(self):
        return self._pipeline

    def run(self):
        # TODO : scraper exit
        self.suit.scraper.scraper_activate()

        self.suit.scraper.proxy = self.suit.pool.get()

        super(ScrapyConsumer, self).run()

    def stop(self):
        self.suit.scraper.scraper_quit()
        super(ScrapyConsumer, self).stop()

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

    def __del__(self):
        self.suit.scraper.scraper_quit()
