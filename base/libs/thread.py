from typing import List
from abc import abstractmethod
from collections import Iterable
import time

from queue import Queue, Empty
from threading import Event, Thread, Lock


class BaseThreading(Thread):

    def __init__(self, event: Event = Event(), **kwargs):
        Thread.__init__(self, name=kwargs.get('name'))

        self.setDaemon(True)
        self._stopped_event = event

    def run(self) -> None:
        """
        demo
        :return:
        """
        while True:
            self.wait()
            time.sleep(1)
            print('run')

    @property
    def event(self):
        return self._stopped_event

    def wait(self):
        self.event.wait()

    def stop(self):
        self._stopped_event.clear()

    def start(self):
        if self.is_alive():
            self.event.set()
        else:
            Thread.start(self)
            self.event.set()


class Consumer(BaseThreading):
    _queue: Queue
    _delay: int

    _lock: Lock

    def __init__(self, queue, delay=1, **kw):

        # careful! python default params will be initialized only once.
        BaseThreading.__init__(self, kw.pop('event', Event()), **kw)

        self._queue = queue
        self._delay = delay

        self._lock = kw.pop('lock', Lock())

    @property
    def queue(self):
        return self._queue

    @property
    def delay(self):
        return self._delay

    @property
    def lock(self):
        return self._lock

    @abstractmethod
    def consuming(self, obj):
        pass

    def run(self):
        # infinite loop.exit by join or daemon.
        while True:
            # event to start or stop
            self.wait()

            # lock to delay
            if self.delay:
                self._lock.acquire()
                time.sleep(self.delay)
                self._lock.release()

            # consuming. do consuming method.
            try:
                obj = self._queue.get(block=True, timeout=0.1)
                self.queue.task_done()

                self.consuming(obj)
            except Empty as e:
                continue
            # TODO: other excetion?


class ConsumerSuit(object):
    _lock = Lock
    _delay = 1
    _consumers: List[Consumer]

    def __init__(self, consumer_class: type(Consumer), queue: Queue = None, number: int = 1, delay: int = 1,
                 name: str = 'Consumer',
                 kw_list=None,
                 **kwargs):
        if kw_list is None:
            kw_list = []
        assert isinstance(consumer_class, type), 'need consumer class'
        assert issubclass(consumer_class, Consumer), 'must extend consumer'

        assert type(number) == int

        self._lock = Lock()
        self._delay = delay
        self._queue = queue if queue else Queue
        self._consumers = []

        for i in range(number):
            self.consumers.append(consumer_class(queue=self.queue, delay=self._delay, lock=self.lock,
                                                 name='{}-{}'.format(name, str(i)), **kw_list[i], **kwargs))

    @property
    def lock(self):
        return self._lock

    @property
    def consumers(self):
        return self._consumers

    @property
    def queue(self):
        return self._queue

    def start_all(self):
        for consumer in self.consumers:
            consumer.start()

    def stop_all(self):
        for consumer in self.consumers:
            consumer.stop()

    def block(self):
        self.queue.join()
