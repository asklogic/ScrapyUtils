import unittest
import time

from queue import Queue
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool
from multiprocessing import TimeoutError
from time import sleep

from threading import Event, Lock
from typing import Union

from ScrapyUtils.libs.threads import BaseThread
from ScrapyUtils.libs.threads.producer import Producer


class Custom(Producer):

    def producing(self):
        return '1'


class Count(Producer):

    def __init__(self, source: Union[Queue, deque], delay: Union[int, float] = 0.1, lock: Lock = None,
                 expire: bool = True, event: Event = Event(), start_thread: bool = True, **kwargs):
        self.mock_count = 0
        super().__init__(source, delay, lock, expire, event, start_thread, **kwargs)

    def producing(self):
        self.mock_count += 1
        return time.time()


class ProducerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        queue = Queue(10)
        self.producer = Producer(queue)

        self.half = Queue(10)
        [self.half.put(x) for x in range(5)]

    def test_sample_produce(self):
        """Produce item without delay.
        """
        count = Count(Queue(), delay=0)
        count.resume()
        sleep(0.1)
        assert count.get_size() > 100

    def test_sample_produce_delay(self):
        """Produce item with delay.
        """

        count = Count(Queue(), delay=0.05)
        count.resume()

        sleep(0.1300)
        count.pause(block=True)
        assert count.get_size() == 2

    def test_class_base_thread(self):
        """The subclass of BaseThread
        """

        assert issubclass(Producer, BaseThread)
        assert issubclass(Custom, BaseThread)


if __name__ == '__main__':
    unittest.main()
