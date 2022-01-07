# -*- coding: utf-8 -*-
"""Step Load - Load the components and the scrapers for scraping.

1. 初始化Scraper

加载scheme中的各组件以及scraper和task。
执行 generate_tasks 和 generate_scraper 函数，加载至configure中。
根据开关加载各项组件，执行action、parsing和processor的on_start函数。
并且初始化pipeline以及各suit，等待爬取任务的开始。

另外提供scheme_load。

Todo:
    * 异常处理: Python加载异常（包含代码格式、缺少包）
"""
from collections.abc import Iterable, Iterator
from concurrent.futures.thread import ThreadPoolExecutor

from ScrapyUtils.libs.scraper.request_scraper import RequestScraper, Scraper
from ScrapyUtils import configure
from queue import PriorityQueue


def _load_scraper():
    """initial scrapers"""
    scrapers = []

    with ThreadPoolExecutor(configure.THREAD) as pool:
        future = pool.submit(configure.scraper_callable)
        future.add_done_callback(lambda f: scrapers.append(f.result()))
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


if __name__ == '__main__':
    pass
