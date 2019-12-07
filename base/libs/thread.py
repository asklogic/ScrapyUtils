from typing import List, Callable, Generator
from abc import abstractmethod
import time
import copy

from queue import Queue, Empty
from threading import Event, Thread, Lock


class BaseThreading(Thread):
    """
    BaseThreading
    提供简单启停的线程类 通过threading.Event来控制启停.
    若不提供默认event 则会使用全局同一的Event对象.
    默认为守护进程 和主线程一同退出 故只有暂停方法.
    """
    _stopped_event: Event = None
    _waiting: bool = False

    def __init__(self, event: Event = Event(), **kwargs):
        assert isinstance(event, Event), 'need event instance.'
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

    @property
    def waiting(self):
        return self._waiting

    def wait(self):
        self._waiting = True
        self.event.wait()
        self._waiting = False

    def stop(self):
        self._stopped_event.clear()

    def start(self):
        if self.is_alive():
            self.event.set()
        else:
            Thread.start(self)
            self.event.set()


class Consumer(BaseThreading):
    """
    消费者类
    具体消费者行为继承consuming方法
    """
    _queue: Queue
    _delay: int

    _lock: Lock

    def __init__(self, queue, delay=1, lock=None, **kw):

        # !python default params will be initialized only once.
        BaseThreading.__init__(self, kw.pop('event', Event()), **kw)

        self._delay = delay

        assert isinstance(queue, Queue), 'Consumer need queue object.'

        self._queue = queue if queue else Queue()
        self._lock = lock if lock else Lock()

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

            # lock to delay
            if self.delay:
                self.lock.acquire()
                time.sleep(self.delay)
                self.lock.release()

            # consuming.
            try:
                obj = self._queue.get(block=True, timeout=0.1)
                self.queue.task_done()

                self.consuming(obj)
            # empty. continue loop.
            except Empty as e:
                continue

            self.wait()
            # TODO: other excetion?


class ConsumerSuit(object):
    _lock = Lock
    _delay = 1
    _consumers: List[Consumer]

    def __init__(self, consumer_class: type(Consumer), queue: Queue = None, number: int = 1, delay: int = 1,
                 name: str = 'Consumer',
                 **kwargs):
        """

        :param consumer_class: consumer class
        :param queue: queue in consumer
        :param number: thread's number
        :param delay: delay in consumer
        :param name: thread name
        :param kwargs: other kwargs
        """

        assert isinstance(consumer_class, type), 'need consumer class'
        assert issubclass(consumer_class, Consumer), 'must extend consumer'

        assert type(number) == int

        self._lock = Lock()
        self._delay = delay
        self._queue = queue if queue else Queue
        self._consumers = []

        for i in range(number):
            self.consumers.append(consumer_class(queue=self.queue, delay=self._delay, lock=self.lock,
                                                 name='{}-{}'.format(name, str(i)), **kwargs))

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


class ThreadSuit(object):
    def __init__(self, thread_class, number: int = 1, kw: dict = None, copy_attr: List[str] = ()):
        kw = kw if kw else {}

        assert isinstance(thread_class, type), 'ThreadSuit need BaseThreading class.'
        assert callable(thread_class), 'ThreadSuit must extend BaseThreading.'
        assert issubclass(thread_class, BaseThreading), 'ThreadSuit must extend BaseThreading.'

        assert type(number) == int, 'need int.'

        # property
        self._event = Event()
        self._consumers: List[BaseThreading] = []

        kw['event'] = self.event

        for i in range(number):

            # copy
            for attr in copy_attr:
                kw[attr] = copy.deepcopy(kw.get(attr))

            thread = thread_class(**kw)
            self._consumers.append(thread)

    @property
    def consumers(self):
        return self._consumers

    @property
    def event(self):
        return self._event

    def stop(self):
        self.consumers[0].event.clear()

    def start(self):
        if self.is_alive():
            self.event.set()
        else:
            Thread.start(self)
            self.event.set()

    def start_all(self):
        for consumer in self.consumers:
            consumer.start()

    def stop_all(self):
        for consumer in self.consumers:
            consumer.stop()


class Pool(BaseThreading):
    def __init__(self, generate: Callable, queue=None, limit=5, **kw):
        BaseThreading.__init__(self, kw.pop('event', Event()), **kw)

        self._queue = queue if queue else Queue()
        self._limit = limit if limit else 5

        assert callable(generate), 'Pool need callable.'
        self._generate = generate

    @property
    def generate(self):
        return self._generate

    @property
    def queue(self):
        return self._queue

    @property
    def limit(self):
        return self._limit

    def generation(self):

        try:
            for model in self.generate(self.limit * 2):
                self.queue.put(model)
        except Exception as e:
            time.sleep(1.5)
            self.generation()

    def run(self) -> None:
        while True:

            if self.queue.qsize() < self.limit:
                self.generation()
            # time.sleep(0.3154)
            time.sleep(0.2)

    # ----------------------------------------------------------------------
    # pool methods

    def size(self):
        return self.queue.qsize()

    def get(self):
        return self.queue.get(timeout=10)
