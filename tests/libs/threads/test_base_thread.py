import unittest
import sys
import threading
import time

from threading import Event
from time import sleep

from ScrapyUtils.libs.threads.base_thread import BaseThread


class Count(BaseThread):
    mock_count = 0

    def __init__(self, **kwargs):
        self.mock_count = 0
        super(Count, self).__init__(**kwargs)

    def run(self) -> None:
        while True:
            self.event.wait()
            # self.count += 1
            self.mock_count = self.mock_count + 1
            time.sleep(0.2)


class BaseThreadTestCase(unittest.TestCase):

    def test_samples_count(self):
        """The sample count thread.

        Count类每次工作时间花费0.2秒。

        只要开启线程，并且event没有阻塞，就会进入一次工作。

        此时调用stop方法，线程暂停，当前工作结束后将会被event阻塞。
        """
        count = Count()
        assert count.mock_count == 0
        count.start()
        sleep(0.1)
        count.stop()
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

        counter0.start()
        counter1.start()
        counter2.start()
        counter3.start()

        # 三次计数
        time.sleep(0.5)

        # 暂停
        counter0.stop()
        # event.clear()

        time.sleep(0.5)

        assert counter0.event is counter1.event is counter2.event

        assert counter0.mock_count == 3
        assert counter1.mock_count == 3
        assert counter2.mock_count == 3
        assert counter3.mock_count == 5

    def test_class_thread(self):
        """The subclass of threading.Thread
        """
        assert issubclass(BaseThread, threading.Thread)
        assert issubclass(Count, threading.Thread)

    def test_property_daemon(self):
        """The property daemon default value is True.
        """
        base = BaseThread()
        assert base.daemon is True

    def test_property_is_alive(self):
        """The thread will not start after initial.

        初始化后不会自动运行线程。
        """
        base = BaseThread()
        assert base.is_alive() is False

    def test_argument_event(self):
        """The argument event: to get a shared event.

        可以传入event对象，默认为false状态。

        如果没有传，将会自动生成一个event。
        """
        event = threading.Event()
        base = BaseThread(event)

        assert base.event is event

    # def test_parameter_start_thread(self):
    #     """
    #     初始化参数start_thread默认为False，设置为False后将不会自动运行线程。
    #     """
    #     base = BaseThread(start_thread=False)
    #     assert base.is_alive() is False

    # def test_parameter_start_thread_true(self):
    #     base = BaseThread(start_thread=True)
    #     assert base.is_alive() is True

    def test_method_start(self):
        count = Count()

        assert count.event.is_set() == False

        count.start()
        assert count.is_alive() is True
        assert count.event.is_set() == True

    def test_method_stop(self):
        count = Count()
        count.start()
        sleep(0.1)
        count.stop()
        assert count.mock_count == 1

        sleep(0.4)

        assert count.mock_count == 1


if __name__ == '__main__':
    unittest.main()
