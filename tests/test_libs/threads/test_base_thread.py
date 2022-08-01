import unittest
import sys
import threading
import time

from threading import Event
from time import sleep

from ScrapyUtils.libs.threads.base_thread import BaseThread


class Count(BaseThread):
    mock_count = 0

    def __init__(self, event: Event = Event(), start_thread: bool = True, **kwargs):
        self.mock_count = 0

        super().__init__(event, start_thread, **kwargs)

    def run(self) -> None:
        while self.thread_wait():
            self.mock_count += 1
            time.sleep(0.2)


class Max(BaseThread):
    max_count = 0

    def run(self):
        while self.thread_wait():
            self.max_count += 1


class BaseThreadTestCase(unittest.TestCase):

    def test_samples_count(self):
        """The sample thread for count.

        Count类每次工作时间花费0.2秒。

        只要开启线程，并且event没有阻塞，就会进入一次工作。

        此时调用非阻塞调用stop方法，线程暂停，当前工作结束后将会被event阻塞。
        """
        count = Count(start_thread=True)
        assert count.mock_count == 0
        count.resume()
        sleep(0.1)
        count.pause(True)
        assert count.mock_count == 1

    def test_sample_multi_count(self):
        """Shared event in multi thread.

        多个线程共用event。

        多个count可以共用一个event，通过控制event来控制多个count的启停。
        """
        event = threading.Event()
        counter0 = Count(event=event)
        counter1 = Count(event=event)
        counter2 = Count(event=event)
        counter3 = Count()

        counter0.resume()
        counter1.resume()
        counter2.resume()
        counter3.resume()

        # 三次计数
        time.sleep(0.21)

        # 暂停
        event.clear()

        time.sleep(0.21)

        assert counter0.event is counter1.event is counter2.event

        assert counter0.mock_count >= 1
        assert counter1.mock_count >= 1
        assert counter2.mock_count >= 1
        assert counter3.mock_count >= 2

    def test_arguments(self):
        """Arguments for BaseThread"""

        assert issubclass(BaseThread, threading.Thread)
        assert issubclass(Count, threading.Thread)

        with self.subTest('start_thread: Default is True. 自动启动'):
            base = BaseThread()
            assert base.is_alive() is True

        with self.subTest('start_thread is False. 不自动启动'):
            base = BaseThread(start_thread=False)
            assert base.is_alive() is False

        with self.subTest('event. Event property'):
            event = Event()
            base = BaseThread(event=event)
            assert base.event is event

    def test_properties(self):
        """property in BaseThread"""
        base = BaseThread()

        with self.subTest('daemon is Fixed:True'):
            base = BaseThread()
            assert base.daemon is True

        with self.subTest('paused_flag'):
            base = BaseThread()
            assert base.paused_flag is True
            base.resume()
            assert base.paused_flag is False

        with self.subTest('event'):
            base = BaseThread()
            assert base.event.is_set() is True

    def test_method_pause(self):
        """Pause by barrier.wait() in method thread_wait.
        """
        count = Count()
        count.resume()
        assert count.mock_count == 0
        sleep(0.1)
        assert count.mock_count == 1
        count.pause()
        assert count.mock_count == 1
        sleep(0.1)
        assert count.mock_count == 1

    def test_method_idempotent(self):
        """pause and resume is idempotent."""
        count = Count()

        with self.subTest('resume'):
            count.resume()
            count.resume()

        with self.subTest('pause but block'):
            count.pause(block=True)
            count.pause(block=True)

        with self.subTest('pause'):
            count.pause()
            count.pause()

    # @unittest.skip
    def test_sample_max_count(self):
        max_counter = Max()
        max_counter.resume()
        time.sleep(0.001)
        print(max_counter.max_count)


if __name__ == '__main__':
    unittest.main()
