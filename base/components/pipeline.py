from typing import *
from queue import Queue
from threading import Lock

from base.libs.thread import Consumer
from .proceesor import Processor
from base.libs.model import Model


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

    def __init__(self, failed: set, suit: ProcessorSuit, **kwargs):
        Consumer.__init__(self,
                          kwargs.pop('queue', Queue()),
                          kwargs.pop('delay', 1),
                          kwargs.pop('lock', Lock()),

                          **kwargs)

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
        consumer_kwargs = {
            'queue': self.queue,
            'delay': 0,
        }
        self.consumer = PipelineConsumer(self.failed, suit, **consumer_kwargs)
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

        while self.queue.qsize() > 0:
            model = self.queue.get()
            self.failed.add(model)
