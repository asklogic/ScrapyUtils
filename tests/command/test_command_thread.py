import unittest
import time
from threading import Thread
from typing import Callable

from base.libs import RequestScraper, Scraper, FireFoxScraper, Producer
from base.components import StepSuit

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as ConcurrentTE
from multiprocessing.dummy import Pool as ThreadPool

from base.libs import ThreadWrapper
from queue import Queue


def inner():
    suit = StepSuit([], FireFoxScraper(headless=False))
    suit.suit_activate()
    return suit


# def mock_firefox_generator():
#     f = FireFoxScraper(headless=False)
#     f.scraper_activate()
#     return f


def mock_firefox_generator():
    f = RequestScraper()
    f.scraper_activate()
    time.sleep(1)
    return f


# def scraper_builder(generator, number):
#     class InnerProducer(Producer):
#
#         def producing(self):
#             return generator()
#
#     queue = Queue(number)
#
#     producers = [InnerProducer(queue, delay=0.1) for x in range(number)]
#     [x.start(False) for x in producers]
#     time.sleep(0.1)
#     [x.stop() for x in producers]
#
#     scraper_list = list()
#     if not queue.empty():
#         scraper_list.append(queue.get())
#
#     [x.exit() for x in producers]
#     return scraper_list


# def scraper_builder(invoker, number):
#     scraper_list = []
#
#     executor = ThreadPoolExecutor(number)
#     with ThreadPoolExecutor(number) as executor:
#         futures = [executor.submit(inner) for x in range(number)]
#
#     [x.result(1) for x in futures]
#
#     return scraper_list


def scraper_builder(invoker, number, timeout=10):
    scraper_list = []

    def inner():
        res = invoker()
        scraper_list.append(res)

    pool = ThreadPool(number)
    # with ThreadPool(number) as pool:
    res = [pool.apply_async(inner) for x in range(number)]

    [x.get(timeout) for x in res]

    return scraper_list


class CommandThreadTestCase(unittest.TestCase):

    def test_init(self):
        pass

    def test_build_scraper(self):
        scrapers = scraper_builder(mock_firefox_generator, 2)

        for scraper in scrapers:
            assert scraper.scraper_quit
            assert isinstance(scraper, Scraper)
            assert scraper.activated is True

        [x.scraper_quit() for x in scrapers]

    def test_option(self):
        pass


if __name__ == '__main__':
    unittest.main()
