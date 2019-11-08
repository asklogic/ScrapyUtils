import unittest

import threading
import time

from queue import Queue
from typing import List
from base.libs.thread import BaseThreading, Consumer


class TestThread(unittest.TestCase):

    def setUp(self) -> None:
        self.queue = Queue()

        for i in range(1, 100):
            self.queue.put(i)

    def test_base(self):
        base = BaseThreading()

        base.start()

    def test_default_event(self):

        t1 = BaseThreading()
        t2 = BaseThreading()

        assert id(t1.event) == id(t2.event)

    def test_delay(self):
        class TestComsumer(Consumer):

            def consuming(self, obj):
                print(self.name, 'number:', obj)

        e = threading.Event()
        e.clear()

        lock = threading.Lock()

        # c1 = TestComsumer(self.queue, 0.4, event=e, lock=lock, name='custom-1')
        # c2 = TestComsumer(self.queue, 0.4, event=e, lock=lock, name='custom-3')
        # c3 = TestComsumer(self.queue, 0.4, event=e, lock=lock, name='custom-4')
        # c4 = TestComsumer(self.queue, 0.4, event=e, lock=lock, name='custom-5')

        # c1 = TestComsumer(self.queue, 0.4, lock=lock, name='custom-1')
        # c2 = TestComsumer(self.queue, 0.4, lock=lock, name='custom-2')
        # c3 = TestComsumer(self.queue, 0.4, lock=lock, name='custom-3')
        # c4 = TestComsumer(self.queue, 0.4, lock=lock, name='custom-4')

        # c1.start()
        # c2.start()
        # c3.start()
        # c4.start()

        thread_list = []
        for i in range(20):
            t = TestComsumer(self.queue, 0.03, lock=lock)
            thread_list.append(t)

        for t in thread_list:
            t.start()

        while self.queue.qsize() > 0:
            time.sleep(0.1)

    def test_mock_thread(self):
        import random
        class MockThread(Consumer):

            def __init__(self, **kw):
                super(MockThread, self).__init__(**kw)

            def consuming(self, obj):
                delay = random.randint(5, 20) / 100

                print(self.name, 'scraping!', 'delay', delay)
                time.sleep(delay)

        lock = threading.Lock()

        queue = Queue()
        [queue.put(i) for i in range(10)]

        c1 = MockThread(queue=queue, delay=0.2, lock=lock, name='scrapy-1')
        c2 = MockThread(queue=queue, delay=0.2, lock=lock, name='scrapy-2')
        c3 = MockThread(queue=queue, delay=0.2, lock=lock, name='scrapy-3')
        c4 = MockThread(queue=queue, delay=0.2, lock=lock, name='scrapy-4')

        c1.start()
        c2.start()
        c3.start()
        c4.start()

        queue.join()
        assert queue.qsize() == 0

    def test_consumer_suit(self):
        pass


class MyConsumer(Consumer):

    def consuming(self, obj):
        time.sleep(0.33)
        print(obj)


if __name__ == '__main__':
    # unittest.main()

    time.sleep(5)
