import unittest
import time

from base.libs import Consumer, ThreadSuit
from queue import Queue
from threading import Lock


class Custom(Consumer):
    def consuming(self, obj):
        time.sleep(0.3)
        print('done', obj, self.name)


class ThreadSuitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.queue = Queue()

        [self.queue.put(x) for x in range(50)]

    def test_demo(self):
        # TODO: thread suit test case
        kw = {
            'queue': self.queue,
            'delay': 0.1,
            'lock': Lock()
        }
        thread = ThreadSuit(Custom, 10, kw=kw)

        # thread.start_all()
        thread.start()

        while self.queue.qsize() != 0:
            time.sleep(0.02)
        start = time.time()

        print(time.time() - start)
        thread.stop_all()
        print(time.time() - start)


if __name__ == '__main__':
    unittest.main()
