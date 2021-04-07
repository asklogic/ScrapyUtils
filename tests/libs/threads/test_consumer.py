import unittest
import time

from queue import Queue
from threading import Event, Lock
from time import sleep
from typing import Union

from ScrapyUtils.libs.threads.consumer import Consumer
from ScrapyUtils.libs import BaseThread


class Custom(Consumer):
    def consuming(self, obj):
        pass


class Count(Custom):

    def __init__(self, source: Queue, delay: Union[int, float] = 0.1, lock: Lock = None, **kwargs):
        self.mock_count = 0

        super().__init__(source, delay, lock, **kwargs)

    def consuming(self, obj):
        self.mock_count += 1


class ComsumerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.queue = Queue()
        for i in range(5):
            self.queue.put(i)

    def test_class_base_thread(self):
        """The subclass of BaseThread
        """

        assert issubclass(Consumer, BaseThread)
        assert issubclass(Custom, BaseThread)

    def test_sample_consume(self):
        """Consume items without delay.

        Consume all item within 0.1 second.
        """

        custom = Custom(self.queue, 0)
        custom.resume()
        sleep(0.1)

        print(custom.source.qsize())
        assert custom.source.qsize() == 0

    def test_sample_delay(self):
        """Consume item with delay.

        Delay before consuming!
        """
        custom = Custom(self.queue, 0.1)
        custom.resume()
        assert self.queue.qsize() == 5
        sleep(0.15)
        assert self.queue.qsize() == 4

    def test_sample_multi_consume(self):
        """Share queue.
        """
        event = Event()

        count0 = Count(self.queue, 0.1, event=event)
        count1 = Count(self.queue, 0.1, event=event)

        count0.resume()
        count1.resume()
        sleep(0.15)

        # print(count0.mock_count, count1.mock_count)

        assert count0.mock_count == 1
        assert count1.mock_count == 1

        assert self.queue.qsize() == 3

    def test_sample_multi_delay(self):
        """Share lock to limit multi consuming
        """
        lock = Lock()
        event = Event()

        count0 = Count(self.queue, 0.1, lock, event=event)
        count1 = Count(self.queue, 0.1, lock, event=event)

        assert count0.event == count1.event

        count0.resume()
        sleep(0.25)
        assert self.queue.qsize() == 3

    def test_arguments_queue(self):
        """The argument queue. Consumer item from queue.
        """
        queue = Queue()

        custom = Custom(queue)
        assert custom.queue is queue

    def test_arguments_lock(self):
        """The argument lock. Shared lock to limit the speed of consuming.
        """

        lock = Lock()

        custom = Custom(self.queue, lock=lock)
        assert custom.lock is lock

    def test_arguments_daly(self):
        """The argument queue. Consumer item from queue.
        """
        delay = 1.1
        custom = Custom(self.queue, delay=delay)
        assert custom.delay == delay

    # def test_property_queue(self):
    #     """Consumer property : queue type: queue.Queue"""
    #
    #     consuemr = Consumer(Queue())
    #
    #     assert isinstance(consuemr.queue, Queue)
    #
    #     # set
    #     the_queue = Queue()
    #     consuemr._queue = the_queue
    #     assert the_queue is consuemr.queue
    #
    # def test_property_delay(self):
    #     """Consumer property : delay type : number(int or float"""
    #
    #     consuemr = Consumer(Queue())
    #
    #     assert isinstance(consuemr.delay, int)
    #     # default 1
    #     assert consuemr.delay == 1
    #
    #     # set
    #     consuemr._delay = 1.5
    #     assert consuemr._delay == 1.5
    #
    # def test_property_lock(self):
    #     """Consuemr property : lock type : theading.Lock"""
    #     import threading
    #
    #     consuemr = Consumer(Queue())
    #
    #     # not a type
    #     # assert isinstance(consuemr.lock, threading.Lock)
    #     assert consuemr.lock.locked() is False
    #
    #     the_lock = threading.Lock()
    #     consuemr._lock = the_lock
    #     assert consuemr.lock is the_lock
    #
    # def test_property_stopped(self):
    #     consuemr = Consumer(Queue())
    #
    #     assert consuemr.stopped is True
    #
    # def test_method_start_and_stop(self):
    #     """method in BaseThread : start & stop"""
    #     custom = Custom(self.queue)
    #
    #     # BaseThread
    #     assert custom.is_alive() is True
    #     assert custom.event.is_set() is False
    #     assert custom.stopped is True
    #
    #     custom.start()
    #
    #     assert custom.is_alive() is True
    #     assert custom.event.is_set() is True
    #     assert custom.stopped is False
    #
    #     custom.stop()
    #     assert custom.event.is_set() is False
    #     assert custom.stopped is True
    #
    # def test_method_lock_in_run(self):
    #     custom = Custom(self.queue)
    #     custom.delay = 0.3
    #     assert custom.delay == 0.3
    #
    #     assert custom.queue.qsize() == 10
    #     custom.start()
    #     assert custom.queue.qsize() == 10
    #
    #     time.sleep(0.1)
    #     assert custom.queue.qsize() == 10
    #
    #     # after 0.3(0.1 + 0.2 + 0.01) second delay
    #     time.sleep(0.2 + 0.01)
    #     assert custom.queue.qsize() == 9
    #
    # def test_method_lock_in_group(self):
    #     class Custom(Consumer):
    #         def consuming(self, obj):
    #             time.sleep(0.3)
    #             print(self.name, 'done', obj)
    #
    #     lock = Lock()
    #     custom1 = Custom(self.queue, delay=0.3, lock=lock, name='custom1')
    #     custom2 = Custom(self.queue, delay=0.3, lock=lock, name='custom2')
    #     assert custom2.queue is custom1.queue
    #
    #     custom1.start()
    #     custom2.start()
    #
    #     assert custom1.queue.qsize() == 10
    #     time.sleep(0.3 * 3)
    #     assert custom1.queue.qsize() == 7
    #
    #     custom1.queue.join()
    #
    # def test_method_exit(self):
    #     """block till queue empty and stopped."""
    #     start = time.time()
    #     queue = Queue()
    #     [queue.put(x) for x in range(3)]
    #
    #     custom = Custom(queue, delay=0.1)
    #     print(time.time() - start)
    #
    #     custom.start(True)
    #     print(time.time() - start)
    #
    #     # TODO : exit cost 1.2 second.
    #     custom.wait_exit()
    #     print(time.time() - start)
    #
    #     assert custom.queue.qsize() == 0
    #     assert custom.stopped is True
    #     assert custom.event.is_set() is False
    #     print(time.time() - start)
    #


if __name__ == '__main__':
    unittest.main()
