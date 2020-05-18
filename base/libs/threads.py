from typing import List
from abc import abstractmethod
import time

from collections import deque
from queue import Queue, Empty, Full
from threading import Event, Thread, Lock
from multiprocessing.dummy import Pool as ThreadPool


class BaseThread(Thread):
    """
    BaseThreading
    提供简单启停的线程类 通过threading.Event来控制启停.
    若不提供默认event 则会使用全局同一的Event对象.
    默认为守护进程 和主线程一同退出 故只有暂停方法.

    创建好对象时开始就执行Thread.start.
    event.wait将会阻塞线程 需要调用BaseThreading.start来运行.
    """
    _stopped_event: Event = None
    _stopped: bool = False

    def __init__(self, event: Event = Event(), **kwargs):
        assert isinstance(event, Event), 'need event instance.'
        Thread.__init__(self, name=kwargs.get('name'))
        self.setDaemon(True)

        # set event before start.
        self._stopped_event = event
        self.event.clear()

        Thread.start(self)

        # block at self.wait() in method run()
        self.stop(True)

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
    def stopped(self):
        return self._stopped

    def wait(self) -> bool:
        self._stopped = True
        self.event.wait()
        self._stopped = False
        return True

    def stop(self, block=True):
        self._stopped_event.clear()
        if block:
            while self.stopped is not True:
                time.sleep(0.1)

    def start(self, block=True):
        # TODO: abort block?
        self.event.set()
        if block:
            while self.stopped is True:
                time.sleep(0.1)


class Consumer(BaseThread):
    """
    消费者类
    具体消费者行为继承consuming方法
    """
    _queue: Queue
    _delay: int

    _lock: Lock

    def __init__(self, queue, delay=1, lock=None, **kw):
        # default
        lock = lock if lock else Lock()

        # assert
        assert isinstance(queue, Queue), 'Consumer need queue object.'

        # property
        self._queue = queue
        self._lock = lock
        self._delay = delay

        # super
        BaseThread.__init__(self, kw.pop('event', Event()), **kw)

    @property
    def queue(self):
        return self._queue

    @property
    def delay(self):
        return self._delay

    @property
    def lock(self):
        return self._lock

    @delay.setter
    def delay(self, value):
        self._delay = value

    @abstractmethod
    def consuming(self, obj):
        pass

    def wait_exit(self):
        # assert self.stopped is True, 'Consumer has stopped.'

        while self.queue.qsize() != 0:
            time.sleep(0.1)
        self.stop(True)

    def run(self):
        # infinite loop.exit by join or main thread exit.
        while self.wait():

            with self.lock:
                time.sleep(self.delay)

            # consuming.
            try:
                obj = self._queue.get(block=True, timeout=0.1)
                self.queue.task_done()

                self.consuming(obj)
            # empty. continue loop.
            except Empty as e:
                continue
            except Exception as e:
                self.stop(False)

            # except Exception as e:
            #     self.stop(False)

            # TODO: other excetion?


class Producer(BaseThread):
    def __init__(self, queue, delay=0.1, lock=None, **kw):
        # default
        lock = lock if lock else Lock()

        # assert
        assert isinstance(queue, Queue), 'Consumer need queue object.'

        # property
        self._queue = queue
        self._lock = lock
        self._delay = delay

        self.current = None

        # super
        BaseThread.__init__(self, kw.pop('event', Event()), **kw)

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
    def producing(self):
        pass

    def run(self):

        # only delay when producing.
        delay_flag = True

        while self.wait():

            if delay_flag:
                with self.lock:
                    time.sleep(self.delay)
                delay_flag = False

            # TODO: refactor. temp loop
            try:
                self.current = self.current if self.current else self.producing()
                self.queue.put(self.current, timeout=1)
                self.current = None
            except Full as full:
                # full and continue loop.
                continue
            except Exception as e:
                # TODO: log out
                # error in method producing
                self.stop(False)
            else:
                # producing success.
                delay_flag = True


class MultiProducer(Producer):
    def __init__(self, increment: int, **kwargs):
        # TODO: new init?

        self.increment = int(increment)

        # super
        super(MultiProducer, self).__init__(**kwargs)

        # overwrite
        self.current = deque()

    def run(self):
        delay_flag = True

        while self.wait():
            # TODO: temp loop
            if delay_flag:
                with self.lock:
                    time.sleep(self.delay)
                delay_flag = False

            # FIXME: new or add?
            try:
                if not self.current:
                    for item in self.producing(self.increment):
                        self.current.append(item)
                    delay_flag = True
            except Exception as e:
                # TODO: log out
                self.stop(False)
                continue

            item = self.current.popleft()
            try:
                self.queue.put(item, timeout=1)
            except Full as full:
                self.current.appendleft(item)

    @abstractmethod
    def producing(self, increment):
        pass


class PoolProducer(BaseThread):
    def __init__(self, queue, delay=0.1, lock=None, concurrent=10, **kw):
        # default
        lock = lock if lock else Lock()

        # assert
        assert isinstance(queue, Queue), 'Consumer need queue object.'

        # property
        self._queue = queue
        self._lock = lock
        self._delay = delay

        self.current = None

        #
        self._futures = Queue(queue.maxsize)
        self.pool = ThreadPool(concurrent)

        # super
        BaseThread.__init__(self, kw.pop('event', Event()), **kw)

    @property
    def queue(self):
        return self._queue

    @property
    def delay(self):
        return self._delay

    @property
    def lock(self):
        return self._lock

    @property
    def future_queue(self):
        return self._futures

    def run(self):

        while self.wait():

            with self.lock:
                time.sleep(self.delay)

            try:
                self.current = self.current if self.current else self.pool.apply_async(producing_wrapper, args=(self,))
                self.future_queue.put(self.current, timeout=1)
                self.current = None
            except Full as full:
                pass
            except Exception as e:
                self.stop(False)

    def get(self):
        future = self.future_queue.get()
        return self.queue.get()

    def exit(self):

        self.stop(True)
        # self.pool.shutdown(wait=False)
        self.pool.terminate()


def producing_wrapper(producer: Producer):
    item = producer.producing()
    producer.queue.put(item)


class ThreadSuit(object):
    def __init__(self, thread_class, number: int = 1, kw: dict = None, kw_list: List[dict] = ()):
        kw = kw if kw else {}

        assert isinstance(thread_class, type), 'ThreadSuit need BaseThreading class.'
        assert callable(thread_class), 'ThreadSuit must extend BaseThreading.'
        assert issubclass(thread_class, BaseThread), 'ThreadSuit must extend BaseThreading.'

        assert type(number) == int, 'need int.'
        if kw_list:
            # TODO: assert
            assert len(kw_list) == number, 'kw_list'

        # property
        self._event = Event()
        self._consumers: List[BaseThread] = []

        kw['event'] = self.event
        name = thread_class.__name__

        for i in range(number):
            if kw_list:
                kw.update(kw_list[i])
            kw['name'] = '-'.join((name, str(i)))

            thread = thread_class(**kw)
            self._consumers.append(thread)

    @property
    def consumers(self):
        return self._consumers

    @property
    def event(self):
        return self._event

    def stop(self):
        self.event.clear()

    def start(self):
        self.event.set()

    def start_all(self):
        for consumer in self.consumers:
            consumer.start()

    def stop_all(self):
        # TODO: thread suit exit
        for consumer in self.consumers:
            consumer.stop()


# class ItemPool(BaseThread):
#     def __init__(self, generate: Callable, queue=None, limit=5, **kw):
#         BaseThread.__init__(self, kw.pop('event', Event()), **kw)
#
#         self._queue = queue if queue else Queue()
#         self._limit = limit if limit else 5
#
#         assert callable(generate), 'Pool need callable.'
#         self._generate = generate
#
#     @property
#     def generate(self):
#         return self._generate
#
#     @property
#     def queue(self):
#         return self._queue
#
#     @property
#     def limit(self):
#         return self._limit
#
#     def generation(self):
#
#         try:
#             for model in self.generate(self.limit * 2):
#                 self.queue.put(model)
#         except Exception as e:
#             time.sleep(1.5)
#             self.generation()
#
#     def run(self) -> None:
#         while True:
#             if self.queue.qsize() < self.limit:
#                 self.generation()
#             # time.sleep(0.3154)
#             time.sleep(0.2)
#
#     # ----------------------------------------------------------------------
#     # pool methods
#
#     def size(self):
#         return self.queue.qsize()
#
#     def get(self):
#         return self.queue.get(timeout=10)


# class ThreadWrapper(Thread):
#
#     def __init__(self, callable: Callable, args=None, timeout: int = 3):
#         # thread property
#         super(ThreadWrapper, self).__init__()
#         self.setDaemon(True)
#
#         self.callable = callable
#         self.timeout = timeout
#         self.args = args
#
#         # property
#         self._result = None
#
#     def run(self) -> None:
#         current_pool = ThreadPool(1)
#         async_result = current_pool.apply_async(self.callable, args=self.args)
#         try:
#             self._result = async_result.get(self.timeout)
#         except TimeoutError as te:
#             pass
#         current_pool.terminate()
#         # TODO:sys garbage collect?
#
#     @property
#     def result(self):
#         return self._result

