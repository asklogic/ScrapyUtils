from typing import List

import time
import os
from queue import Queue

from base.command import Command
from base.components import *
from base.libs import *

from base.core import collect_profile, collect_steps, collect_processors, PROJECT_PATH
from threading import Lock


class Thread(Command):
    pipeline: Pipeline = None
    steps: List[Step] = None

    task_queue: Queue = None

    config: dict = None

    def syntax(self) -> str:
        return '[THREAD]'

    def options(self, **kwargs):
        path = kwargs.get('path', PROJECT_PATH)
        scheme = kwargs.get('scheme')
        assert scheme, 'no scheme'

        path = os.path.join(path, scheme)
        assert os.path.exists(path), path + ' not exist'

        self.log.info('scheme path' + path, 'Option')

        config = collect_profile(path)
        self.config = config

        # TODO: default step
        steps = collect_steps(path)

        # TODO: default processor
        processors = collect_processors(path)

        # test parse
        # processors.append(GlobleCount)

        pipeline = Pipeline(processors)

        self.steps = steps
        self.pipeline = pipeline

        # TODO: resume tasks
        self.task_queue = Queue()

        self.task_queue = config['task_queue']

    def run(self):
        # profile

        # task and active scraper


        kwargs_list = [
            {
                'steps': self.steps,
                'scraper': scraper,
                'pipeline': self.pipeline,
                'log': self.log,
            }

            for scraper in self.config.get('scrapers')
        ]

        suit = ConsumerSuit(ScrapyThread, self.task_queue, len(self.config.get('scrapers')), self.config['timeout'],
                            'scrapy-thread',
                            kwargs_list)
        suit.start_all()

        # suit.block()
        #
        while not self.task_queue.empty():
            time.sleep(0.3)
        # TODO
        # for scraper in self.config.get('scrapers'):
        #     scrapy_threads.append(ScrapyThread(self.task_queue, self.steps, scraper, self.pipeline, self.log,
        #                                        delay=self.config['timeout'], lock=lock,
        #                                        name='scrapy-thread-{}'.format(i)), )
        #     i += 1
        # for thread in scrapy_threads:
        #     thread.start()
        #
        # # main thread block
        # # TODO: refact
        # done = False
        # while not done:
        #     done = True
        #     for thread in scrapy_threads:
        #         if thread.queue.qsize() > 0:
        #             done = False
        #     time.sleep(1)

    def exit(self):
        print('invoke command exit!')

    def signal_callback(self, signum, frame):
        print('invoke command signal callback exit!')

    def failed(self):
        print('invoke command failed!')


class ScrapyThread(Consumer):
    def __init__(self, queue: Queue, steps: List[Step], scraper: Scraper, pipeline: Pipeline, log, **kwargs):
        # super(ScrapyThread, self).__init__(task_queue, kwargs.get('delay'), **{})
        Consumer.__init__(self, queue, kwargs.pop('delay', 1), **kwargs)

        self.suit = StepSuit(steps, scraper, log)
        self.pipeline = pipeline

    def consuming(self, current: Task):
        # log in scrapy method
        self.suit.scrapy(current)
        # TODO refact models deque
        for model in self.suit.models:
            self.pipeline.push(model)
        self.suit.models.clear()
