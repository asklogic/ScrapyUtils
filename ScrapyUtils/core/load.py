# -*- coding: utf-8 -*-
"""Initial module to initial scheme's components and other settings.

加载scheme中的各组件以及scraper和task。
执行 generate_tasks 和 generate_scraper 函数，加载至configure中。
根据开关加载各项组件，执行action、parsing和processor的on_start函数。
并且初始化pipeline以及各suit，等待爬取任务的开始。

另外提供scheme_load。

Todo:
    * 异常处理: Python加载异常（包含代码格式、缺少包）
"""
from concurrent.futures.thread import ThreadPoolExecutor
from typing import *

from ScrapyUtils.components import StepSuit, ProcessorSuit
from ScrapyUtils.libs import Scraper, RequestScraper

from ScrapyUtils import configure


def _build_suits() -> Tuple[List[StepSuit], ProcessorSuit]:
    step_suits = [StepSuit(steps=configure.steps_class) for i in range(configure.THREAD)]
    processor_suit = ProcessorSuit(configure.processors_class)

    return step_suits, processor_suit


def _build_scraper() -> List[Scraper]:
    gen = _default_scraper(configure.scraper_callable)
    scrapers = list_builder(gen, configure.THREAD, timeout=configure.SCRAPER_TIMEOUT)


def scheme_initial(**command_kwargs):
    # build suits
    step_suits = [StepSuit(steps=configure.steps_class) for i in range(configure.THREAD)]
    processor_suit = ProcessorSuit(configure.processors_class)


default_flag = True


def _default_scraper(scraper_callable) -> Callable:
    def inner():
        current_scraper = None
        global default_flag
        try:
            current_scraper = scraper_callable()
            assert isinstance(current_scraper, Scraper)
        except Exception as e:
            current_scraper = RequestScraper()
            if default_flag:
                # TODO: wtf is that?
                # log.exception('Scraper', e)
                # log.warning('able default RequestScraper.', 'system')
                log.warning('able default RequestScraper.')
                default_flag = False
        finally:
            if not current_scraper.activated:
                current_scraper.scraper_activate()

        return current_scraper

    return inner


def list_builder(invoker: Callable, number: int, result: list = None, timeout=10):
    def inner():
        res = invoker()
        result.append(res)

    with ThreadPoolExecutor(number) as executor:
        futures = [executor.submit(inner) for x in range(number)]
        [x.result(timeout) for x in futures]

    return result


if __name__ == '__main__':
    def f():
        pass
    res = list_builder(f,5, [])

    print(res)