from typing import List

import time
import os
from queue import Queue

from base.command import Command
from base.components import *
from base.libs import *

from base.core import collect_profile, collect_steps, collect_processors


class Thread(Command):
    pipeline: Pipeline = None
    steps: List[Step] = None

    task_queue: Queue = None

    config: dict = None

    def syntax(self) -> str:
        return '[TEST_COMMAND]'

    def options(self, **kwargs):
        path = kwargs.get('path')
        assert path

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

        scraper = RequestScraper

        # init ScrapyThread
        scrapy_threads = []

        # TODO
        for scraper in self.config.get('scrapers'):
            scrapy_threads.append(ScrapyThread(self.task_queue, self.steps, scraper, self.pipeline))

        for thread in scrapy_threads:
            thread.start()

        # main thread block
        # TODO: refact
        done = False
        while not done:
            done = True
            for thread in scrapy_threads:
                if thread.queue.qsize() > 0:
                    done = False
            time.sleep(1)

    def exit(self):
        # print(self.task_queue.qsize())
        print('thread exit!')


class ScrapyThread(Consumer):
    def __init__(self, task_queue: Queue, steps: List[Step], scraper: Scraper, pipeline: Pipeline):
        super(ScrapyThread, self).__init__(task_queue)

        self.suit = StepSuit(steps, scraper)
        self.pipeline = pipeline

    def consuming(self, current: Task):
        # log in scrapy method
        self.suit.scrapy(current)
        # TODO refact models deque
        for model in self.suit.models:
            self.pipeline.push(model)
        self.suit.models.clear()
