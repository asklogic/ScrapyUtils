import unittest
import time

from base.libs import Producer, FireFoxScraper, MultiProducer, PoolProducer
from queue import Queue
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool
from multiprocessing import TimeoutError
import time

from threading import Event


class Custom(Producer):

    def producing(self):
        return '1'


class ProxyMock(MultiProducer):

    def producing(self, increment):
        """
        Args:
            increment:
        """
        print('start get proxy')
        time.sleep(0.3)
        print('proxy done.')
        for i in range(increment):
            yield i


def wrapper():
    f = FireFoxScraper(headless=False)
    f.scraper_activate()
    return f


class ScraperProducer(Producer):

    def producing(self):
        return wrapper()


class ProducerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        queue = Queue(10)
        self.producer = Producer(queue)

        self.half = Queue(10)
        [self.half.put(x) for x in range(5)]

        self.queue = Queue(10)
        self.event = Event()

    def test_init(self):
        producer = Producer(Queue(10))

    # @unittest.skip
    def test_method_start_producing(self):
        custom = Custom(Queue(10))
        custom.start()

        time.sleep(1.1)

        assert custom.queue.qsize() == 10

    def test_case_slow_producing(self):
        """slow producing. by concurrent.ThreadPoolExecutor"""

        class Slow(Producer):
            def producing(self):
                time.sleep(0.4)
                return '1'

        slows = [Slow(self.half) for x in range(5)]

        [x.start() for x in slows]

        time.sleep(0.5)

        assert self.half.qsize() == 10

    def test_case_stop_at_once(self):
        customs = [Custom(self.queue, event=self.event) for x in range(6)]

        assert self.queue.qsize() == 0

        customs[0].start(False)
        customs[0].stop()

        time.sleep(1)

        assert self.queue.qsize() == 6

    @unittest.skip
    def test_case_stop_at_once_delay(self):
        queue = Queue(1)

        # FIXME: wtf!
        class FoxCustom(Producer):
            def producing(self):
                f = FireFoxScraper(headless=False)
                f.scraper_activate()
                return f

        customs = [FoxCustom(queue, event=self.event, delay=0.01) for x in range(12)]

        customs[0].start()
        # [x.start() for x in customs]

        [x.stop() for x in customs]

        # assert self.queue.qsize() == 1

        scrapers = [queue.get()] + [custom.current for custom in customs if custom.current]

        # assert len(scrapers) == 7

        [scraper.scraper_quit() for scraper in scrapers]

        print(len(scrapers))
        # assert len(scrapers) == 12

    def test_multi_producing(self):
        proxy_mock = ProxyMock(limit=1, increment=15, queue=self.queue, delay=0.5)
        proxy_mock.start()

        time.sleep(0.5 + 0.5 + 0.3 + 0.3 + 0.1)
        print(proxy_mock.queue.qsize())
        assert proxy_mock.queue.qsize() == 10

    def test_function_wrapper(self):
        def wrapper(func, timeout: int = 3):
            with Pool(1) as pool:
                res = pool.apply_async(func)
                try:
                    res.get(timeout)
                except TimeoutError as te:
                    pass
                # pool.terminate()

        def inner():
            time.sleep(2)
            print('done')

        wrapper(inner, 3)

        time.sleep(4)

    # @unittest.skip
    def test_case_firefox_pool(self):
        class FoxCustom(PoolProducer):
            def producing(self):
                f = FireFoxScraper(headless=False)
                f.scraper_activate()
                return f

        fox = FoxCustom(Queue(5), concurrent=2)
        fox.start()

        time.sleep(1)
        fox.stop()


    def test_case_pool(self):
        class Custom(PoolProducer):
            def producing(self):
                return '1'

        custom = Custom(Queue(50), concurrent=10, delay=0.1)
        custom.start()

        time.sleep(1)
        print(custom.future_queue.qsize())

        custom.stop()

if __name__ == '__main__':
    unittest.main()
