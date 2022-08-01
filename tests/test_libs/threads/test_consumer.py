import unittest
import time

from queue import Queue
from threading import Event, Lock
from time import sleep
from typing import Union, Any

from ScrapyUtils.libs import Consumer
from ScrapyUtils.libs.threads.consumer import BaseConsumer
from ScrapyUtils.libs import BaseThread


class Custom(Consumer):
    def consuming(self, obj):
        pass


class Count(Consumer):

    def __init__(self, source: Any, delay: Union[int, float] = 0.1, lock: Lock = None, event: Event = None,
                 start_thread: bool = True, **kwargs):
        self.mock_count = 0

        super().__init__(source, delay, lock, event, start_thread, **kwargs)

    def consuming(self, obj):
        self.mock_count += 1


class ConsumerTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.queue = Queue()
        for i in range(5):
            self.queue.put(i)

    def test_arguments(self):
        """arguments in Consumer"""
        base = Custom(source=Queue())

        with self.subTest('source'):
            queue = Queue()
            base = Custom(source=queue)
            assert base.source == queue

        with self.subTest('lock'):
            lock = Lock()
            base = Custom(queue, lock=lock)
            assert base.lock is lock

        with self.subTest('delay'):
            assert base.delay == 0.1

    def test_class_and_subclass(self):
        """The subclass of BaseThread
        """

        assert issubclass(Consumer, BaseThread)
        assert issubclass(Custom, BaseThread)

        with self.assertRaises(TypeError) as te:
            base = Consumer(source=Queue())

    def test_sample_consume(self):
        """Consume items without delay.

        Consume all items in 0.1 second.
        """

        custom = Custom(source=self.queue, delay=0)
        custom.resume()
        sleep(0.1)

        assert custom.source.qsize() == 0

    def test_sample_delay(self):
        """Consume item with delay.

        Delay before consuming!
        """
        custom = Custom(source=self.queue, delay=0.1)
        assert self.queue.qsize() == 5
        custom.resume()
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

        custom = Custom(source=queue)
        assert custom.source is queue

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


if __name__ == '__main__':
    unittest.main()
