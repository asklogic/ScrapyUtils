# -*- coding: utf-8 -*-
"""爬取核心模块

爬虫流程的第二步：爬取 - Scrape。

根据Setting中的设置，开启若干个爬虫线程。


Todo:
    * For module TODOs
    
"""
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from queue import Queue
from threading import Event, Lock
from typing import NoReturn, Any, Union

from ScrapyUtils.components import ActionSuit
from ScrapyUtils.core.pipeline import Pipeline
from ScrapyUtils.libs import Consumer, Task

from ScrapyUtils import configure

logger = getLogger('scrape')

event = Event()
"""ScrapyConsumer common event"""


class ScrapyConsumer(Consumer):
    suit: ActionSuit = None
    pool: ThreadPoolExecutor = None

    def __init__(self, suit: ActionSuit, source: Union[Queue, deque], delay: Union[int, float] = 0.1, lock: Lock = None,
                 event: Event = Event(), start_thread: bool = None, **kwargs):
        super().__init__(source, delay, lock, event, start_thread, **kwargs)

        self.suit = suit
        self.build_pool()

    def consuming(self, task: Task) -> NoReturn:
        # case: task in scraping
        if task.count < configure.RETRY:
            task_callback = self.suit.generate_callback(task=task)

            try:
                future = self.pool.submit(task_callback)
                future.result(configure.TIMEOUT)
            # case failed: retry
            except Exception as e:
                self.build_pool()
                task.count += 1

                configure.tasks.put(task)
                logger.error(f'Task scraping error. <{task.count}>. {task}', exc_info=e)
            # case success
            else:
                configure.models.extend(future.result())
                logger.info(f'Task success! {task}')

        # case: too many failed
        else:
            logger.info(f'Task failed. {task}')
            configure.failed.put(task)

    def build_pool(self):
        if self.pool:
            self.pool.shutdown()
        self.pool = ThreadPoolExecutor(max_workers=1)


def stop_scraping() -> NoReturn:
    event.clear()


def start_scraping() -> NoReturn:
    event.set()


def scrape():
    consumers = [
        ScrapyConsumer(
            suit=configure.action_suits[index],
            source=configure.tasks,
            delay=configure.DELAY,
            event=event,
            start_thread=True,
        ) for index in range(configure.THREAD)
    ]

    [consumer.resume() for consumer in consumers]

    configure.scrape_consumers = consumers

    configure.models_pipeline = Pipeline(source=configure.models, suit=configure.processor_suit)
