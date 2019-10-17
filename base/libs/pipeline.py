import threading
import time
from typing import *
from queue import Queue, Empty
from abc import abstractmethod

from base.components import Processor
from .model import Model


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


class ProcessorSuit(object):
    _processors: List[Processor]

    def __init__(self, processors: List[type(Processor)]):
        assert isinstance(processors, Iterable)
        for processor in processors:
            # assert isinstance(processor, Processor), 'Processor must be init'
            assert issubclass(processor, Processor), 'Processor class'

        self._processors = []
        # init
        for processor in processors:
            try:
                current = processor()
                self._processors.append(current)
            except Exception as e:
                pass
                # TODO : log out
            finally:
                pass
                # TODO : log out

    @property
    def processors(self):
        return self._processors

    def process(self, model):
        current = model
        next = None
        # FIXME: linked?
        for processor in self.processors:
            if not isinstance(current, processor.target):
                continue

            next = processor.process_item(current)

            if next is False:
                break
            elif next is None:
                continue
            else:
                current = next


class PipelineConsumer(Consumer):

    def __init__(self, queue: Queue, failed: set, suit: ProcessorSuit, **kwargs):
        kwargs['queue'] = queue
        super(PipelineConsumer, self).__init__(**kwargs)

        self._failed = failed
        self._suit = suit

    @property
    def suit(self):
        return self._suit

    @property
    def failed(self):
        return self._failed

    def consuming(self, model: Model):
        # TODO: log out
        try:
            self.suit.process(model=model)
        except Exception as e:
            # other exception in process_item method
            self._failed.add(model)

            # TODO: necessary process
            # failed in process. break down all process


class Pipeline(object):
    _queue: Queue
    _failed: set

    _suit: ProcessorSuit
    consumer: PipelineConsumer

    def __init__(self, processors: List[type(Processor)]) -> None:
        # processor
        for processor in processors:
            assert issubclass(processor, Processor)

        self._queue = Queue()
        self._failed = set()

        # init processor (processor's on_start method)
        suit = ProcessorSuit(processors)
        # TODO: log out
        self._suit = suit

        # consumer
        self.consumer = PipelineConsumer(self.queue, self.failed, suit)
        self.consumer.start()

    def _start_processor(self):
        """
        in processor suit
        """
        pass

    def _exit_processor(self):
        pass

    @property
    def queue(self):
        return self._queue

    @property
    def failed(self):
        return self._failed

    @property
    def suit(self):
        return self._suit

    def push(self, obj):
        self.queue.put_nowait(obj)

    def size(self) -> int:
        return self.queue.qsize()

    def pop(self) -> object:
        return self.queue.get_nowait()

    def process(self, model: Model):
        pass

    def exit(self):
        # exit consumer
        self.consumer.stop()

        # execute on_exit
        for processor in self._suit.processors:
            processor.on_exit()

        queue = self.queue.qsize()
        failed = len(self.failed)
        print('queue', queue)
        print('failed', failed)

        while self.queue.qsize() > 0:
            model = self.queue.get()
            self.failed.add(model)
