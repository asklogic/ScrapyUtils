from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from typing import Callable

from .scheme import Scheme

from ScrapyUtils import configure
from ScrapyUtils.libs import RequestScraper, Scraper

logger = getLogger('Scraper')


def thread_build(func: Callable, number: int):
    with ThreadPoolExecutor(number) as pool:
        result_list = []

        def inner():
            res = func()
            result_list.append(res)

        futures = [pool.submit(inner) for x in range(number)]
        [future.result() for future in futures]
    return result_list


def default_scraper():
    r = RequestScraper()
    r.scraper_attach()

    return r


class ScraperScheme(Scheme):
    @classmethod
    def start(cls):
        scraper_callable = configure.scraper_callable

        logger.info(f'Start build {configure.THREAD} scrapers... ')

        scrapers = thread_build(scraper_callable, configure.THREAD)

        for scraper in scrapers:
            if scraper is None:
                logger.info('Build default RequestScraper.')
                scrapers = thread_build(default_scraper, configure.THREAD)
                break
        configure.scrapers = scrapers

    @classmethod
    def verify(cls) -> bool:
        assert configure.scrapers
        return True

    @classmethod
    def stop(cls):
        scrapers = configure.scrapers

        for scraper in scrapers:
            scraper.scraper_detach()
