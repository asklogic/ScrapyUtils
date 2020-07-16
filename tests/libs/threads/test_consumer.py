import unittest
import time

from threading import Lock
from base.libs import Consumer
from base.libs import FireFoxScraper
from queue import Queue


class Custom(Consumer):
    def consuming(self, obj):
        """
        Args:
            obj:
        """
        time.sleep(0.3)


class ComsumerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.queue = Queue()
        for i in range(10):
            self.queue.put(i)

    def test_property_queue(self):
        """Consumer property : queue type: queue.Queue"""

        consuemr = Consumer(Queue())

        assert isinstance(consuemr.queue, Queue)

        # set
        the_queue = Queue()
        consuemr._queue = the_queue
        assert the_queue is consuemr.queue

    def test_property_delay(self):
        """Consumer property : delay type : number(int or float"""

        consuemr = Consumer(Queue())

        assert isinstance(consuemr.delay, int)
        # default 1
        assert consuemr.delay == 1

        # set
        consuemr._delay = 1.5
        assert consuemr._delay == 1.5

    def test_property_lock(self):
        """Consuemr property : lock type : theading.Lock"""
        import threading

        consuemr = Consumer(Queue())

        # not a type
        # assert isinstance(consuemr.lock, threading.Lock)
        assert consuemr.lock.locked() is False

        the_lock = threading.Lock()
        consuemr._lock = the_lock
        assert consuemr.lock is the_lock

    def test_property_stopped(self):
        consuemr = Consumer(Queue())

        assert consuemr.stopped is True

    def test_method_start_and_stop(self):
        """method in BaseThread : start & stop"""
        custom = Custom(self.queue)

        # BaseThread
        assert custom.is_alive() is True
        assert custom.event.is_set() is False
        assert custom.stopped is True

        custom.start()

        assert custom.is_alive() is True
        assert custom.event.is_set() is True
        assert custom.stopped is False

        custom.stop()
        assert custom.event.is_set() is False
        assert custom.stopped is True

    def test_method_lock_in_run(self):
        custom = Custom(self.queue)
        custom.delay = 0.3
        assert custom.delay == 0.3

        assert custom.queue.qsize() == 10
        custom.start()
        assert custom.queue.qsize() == 10

        time.sleep(0.1)
        assert custom.queue.qsize() == 10

        # after 0.3(0.1 + 0.2 + 0.01) second delay
        time.sleep(0.2 + 0.01)
        assert custom.queue.qsize() == 9

    def test_method_lock_in_group(self):
        class Custom(Consumer):
            def consuming(self, obj):
                time.sleep(0.3)
                print(self.name, 'done', obj)

        lock = Lock()
        custom1 = Custom(self.queue, delay=0.3, lock=lock, name='custom1')
        custom2 = Custom(self.queue, delay=0.3, lock=lock, name='custom2')
        assert custom2.queue is custom1.queue

        custom1.start()
        custom2.start()

        assert custom1.queue.qsize() == 10
        time.sleep(0.3 * 3)
        assert custom1.queue.qsize() == 7

        custom1.queue.join()

    def test_method_exit(self):
        """block till queue empty and stopped."""
        start = time.time()
        queue = Queue()
        [queue.put(x) for x in range(3)]

        custom = Custom(queue, delay=0.1)
        print(time.time() - start)

        custom.start(True)
        print(time.time() - start)

        # TODO : exit cost 1.2 second.
        custom.wait_exit()
        print(time.time() - start)

        assert custom.queue.qsize() == 0
        assert custom.stopped is True
        assert custom.event.is_set() is False
        print(time.time() - start)


if __name__ == '__main__':
    unittest.main()
