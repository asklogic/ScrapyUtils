# -*- coding: utf-8 -*-
"""Prepare - Load the components and the scrapers for scraping.

preload自动导入的组件后，开始逐个加载需要的组件


函数:

    1. _load_scraper::

        根据setting中的设置启动若干个Scraper实例，通常由Selenium构成。

    2. _load_tasks::

        根据setting中的设置生成本次爬取需要执行的Task任务。

    3. _load_suit::

        根据project包中的组件Component开启情况，加载各组件并且组合成为对应的Suit

    4. load::

        整合命令，启动加载流程


Todo:
    * 异常处理:

"""
from collections.abc import Iterable
from concurrent.futures.thread import ThreadPoolExecutor
from logging import getLogger
from queue import Queue
from threading import Lock, Event
from typing import NoReturn, List, Callable, Any, Union

from ScrapyUtils.components import Component, Action, Process
from ScrapyUtils.libs import Consumer, Task, Model
from ScrapyUtils.libs.scraper.request_scraper import RequestScraper, Scraper
from ScrapyUtils import configure

logger = getLogger(__name__)


class ScraperComponent(Component):
    scraper: Scraper = None
    scraper_callback: Callable = None

    def __init__(self, scraper_callback: Callable[[], Scraper]) -> None:
        self.scraper = None
        self.scraper_callback = scraper_callback

    def on_start(self) -> NoReturn:
        """Initial and attach"""
        callback_result = self.scraper_callback()

        if not isinstance(callback_result, Scraper):
            callback_result = RequestScraper()

        self.scraper = callback_result
        callback_result.scraper_attach()

    def on_exit(self) -> NoReturn:
        """detach"""
        self.scraper.scraper_detach()


lock = Lock()


class TaskChainConsumer(Consumer):
    head_action: Action
    scraper: Scraper
    model_queue: Queue

    def __init__(self, action: Action, scraper: Scraper, **kwargs):
        super().__init__(configure.tasks, configure.DELAY, lock=lock, **kwargs)
        self.head_action = action
        self.scraper = scraper

        self.pool = ThreadPoolExecutor(1)
        self.resume()

    def consuming(self, obj: Task) -> NoReturn:
        try:
            future = self.pool.submit(self.head_action.generate_callback(obj, self.scraper))
            result = future.result(timeout=configure.TIMEOUT)
        # TODO: timeout and other exception
        except Exception as e:
            configure.failed_tasks.put(obj)
            logger.info(f'Task failed {obj}')
        else:
            configure.models.extend(result)
            logger.info(f'Task success {obj}')


class ModelChainConsumer(Consumer):
    head_process = Process

    def __init__(self, process: Process, **kwargs):
        super().__init__(configure.models, 0, **kwargs)
        self.head_process = process
        self.pool = ThreadPoolExecutor(1)

        self.resume()

    def consuming(self, obj: Model) -> NoReturn:
        try:
            future = self.pool.submit(self.head_process.generate_callback(obj))
            future.result(timeout=configure.TIMEOUT)
        # TODO: timeout and other exception
        except Exception as e:
            configure.failed_models.put(obj)


def _load_tasks():
    """generate tasks"""

    iterator = configure.tasks_callable()
    if iterator and isinstance(iterator, Iterable):
        for task in iterator:
            configure.tasks.put(task)


def build_chain(*linked_component):
    for node_index in range(len(linked_component) - 1):
        linked_component[node_index].next = linked_component[node_index + 1]

    return linked_component[0]


# module variable

TASK_CHAIN_CONSUMERS: List[TaskChainConsumer] = []
MODEL_CHAIN_CONSUMER: ModelChainConsumer


def start_engine() -> NoReturn:
    """
    构建Scraper
    按顺序分配Scraper至Suit

    构建Task
    """

    __import__(configure.project_package_path)

    # action sequence
    for thread_index in range(configure.THREAD):
        [configure.components.append(action()) for action in configure.action_classes]

    # processor sequence
    [configure.components.append(process()) for process in configure.process_classes]

    # scraper sequence
    [configure.components.append(ScraperComponent(configure.scraper_callable)) for _ in range(configure.THREAD)]

    action_number = len(configure.action_classes)
    process_number = len(configure.process_classes)

    # build chain: actions
    head_actions = []
    for chain_index in range(configure.THREAD):
        action_components = configure.components[chain_index * action_number: (chain_index + 1) * action_number]
        head_action = build_chain(*action_components)
        head_actions.append(head_action)

    # build chain: process
    process_components = configure.components[
                         action_number * configure.THREAD: action_number * configure.THREAD + process_number]
    head_process = build_chain(*process_components)

    # components on_start
    futures = []
    with ThreadPoolExecutor(max((int(configure.THREAD / 2), 1))) as pool:
        for index, component in enumerate(configure.components):
            future = pool.submit(component.on_start)
            futures.append(future)

    [_.result() for _ in futures]

    scraper_components = configure.components[(action_number * configure.THREAD) + process_number:]
    scrapers = [scraper_component.scraper for scraper_component in scraper_components]

    global TASK_CHAIN_CONSUMERS, MODEL_CHAIN_CONSUMER

    TASK_CHAIN_CONSUMERS = [TaskChainConsumer(head_actions[index], scrapers[index])
                            for index in range(configure.THREAD)]

    MODEL_CHAIN_CONSUMER = ModelChainConsumer(head_process)


def stop_engine() -> NoReturn:
    for task_chain_consumer in TASK_CHAIN_CONSUMERS:
        task_chain_consumer.pause(block=True)

    MODEL_CHAIN_CONSUMER.pause(block=True)


def exit_engine() -> NoReturn:
    # components on_start
    with ThreadPoolExecutor(max((int(configure.THREAD / 2), 1))) as pool:
        for component in configure.components:
            pool.submit(component.on_exit)


if __name__ == '__main__':
    pass
