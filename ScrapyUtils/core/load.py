# -*- coding: utf-8 -*-
"""Step Load - Load the components and the scrapers for scraping.

爬虫流程的第一步：加载 - Load。

与预加载不同，此步骤需要爬虫核心根据输入的命令来执行若干个不同操作，包含连接数据库、读取爬取任务等等较为耗时且不幂等的操作。

次步骤中的所有默认操作将会汇总成为一个单独的load函数。

函数:

    1. _load_scraper::

        根据setting中的设置启动若干个Scraper实例，通常由Selenium构成。

    2. _load_tasks::

        根据setting中的设置生成本次爬取需要执行的Task任务。

    3. _load_suit::

        根据Scheme包中的组件Component开启情况，加载各组件并且组合成为对应的Suit

    4. load::

        整合命令，启动加载流程


Todo:
    * 异常处理:

"""
from collections.abc import Iterable
from concurrent.futures.thread import ThreadPoolExecutor
from typing import NoReturn

from ScrapyUtils.components import ActionSuit
from ScrapyUtils.components.processor import ProcessorSuit
from ScrapyUtils.libs.scraper.request_scraper import RequestScraper, Scraper
from ScrapyUtils import configure


def _load_scraper():
    """initial scrapers"""
    scrapers = []

    # TODO: Limit
    with ThreadPoolExecutor(configure.THREAD) as pool:
        # futures and done callback
        futures = [pool.submit(configure.scraper_callable) for _ in range(configure.THREAD)]
        [future.add_done_callback(lambda f: scrapers.append(f.result())) for future in futures]

    pool.shutdown(wait=True)

    # filter scraper
    scrapers = [scraper for scraper in scrapers if isinstance(scraper, Scraper)]

    # TODO: scraper build failed
    if not scrapers:
        scrapers = [RequestScraper() for _ in range(configure.THREAD)]
        [scraper.scraper_attach() for scraper in scrapers]

    configure.scrapers = scrapers


def _load_tasks():
    """generate tasks"""

    iterator = configure.tasks_callable()
    if iterator and isinstance(iterator, Iterable):
        for task in iterator:
            configure.tasks.put(task)


def _load_suit():
    configure.action_suits = [
        ActionSuit(*configure.action_classes)
        for index in range(configure.THREAD)
    ]

    configure.processor_suit = ProcessorSuit(*configure.processor_classes)

    # on_start
    [suit.suit_start() for suit in configure.action_suits]
    configure.processor_suit.suit_start()


def load() -> NoReturn:
    """
    构建Scraper
    按顺序分配Scraper至Suit

    构建Task
    """
    _load_suit()
    _load_scraper()

    for index in range(configure.THREAD):
        scraper = configure.scrapers[index]
        suit = configure.action_suits[index]
        suit.set_scraper(scraper)

    _load_tasks()


if __name__ == '__main__':
    pass
