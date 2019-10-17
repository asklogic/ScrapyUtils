import unittest

import threading
import time

from queue import Queue, Empty
from abc import abstractmethod


class BaseThreading(threading.Thread):

    def __init__(self, event: threading.Event = threading.Event()):

        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._stopped_event = threading.Event()

    def run(self) -> None:
        """
        demo
        :return:
        """
        while True:
            self.wait()
            print('run')
            time.sleep(0.5)

    @property
    def event(self):
        return self._stopped_event

    def wait(self):
        self.event.wait()

    def stop(self):
        self._stopped_event.clear()

    def start(self):
        if self.isAlive():
            self._stopped_event.set()
        else:
            threading.Thread.start(self)
            self._stopped_event.set()


class Consumer(BaseThreading):

    def __init__(self, queue: Queue = Queue(), **kwargs):
        super(Consumer, self).__init__(**kwargs)

        self._queue = queue

    @property
    def queue(self):
        return self._queue

    @abstractmethod
    def consuming(self, obj):
        pass

    def run(self):
        while True:
            self.wait()
            try:
                obj = self._queue.get(block=True, timeout=0.1)
                self.consuming(obj)
            except Empty as e:
                continue


class TestThread(unittest.TestCase):
    def test_base(self):
        base = BaseThreading()

        base.start()
        time.sleep(3)
        base.stop()

        print('stop')
        time.sleep(1)

        pass


q = Queue()
for i in range(200):
    q.put(i)


class MyConsumer(Consumer):

    def consuming(self, obj):
        time.sleep(0.33)
        print(obj)

c = MyConsumer(q)

if __name__ == '__main__':
    # unittest.main()
    base = BaseThreading()
    base.start()

    time.sleep(5)
