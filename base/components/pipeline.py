from typing import *
import time
from queue import Queue
from collections import deque
from threading import Lock

from base.libs.threads import Consumer
from .proceesor import Processor
from .base import ComponentSuit
from base.libs.model import Model

from . import log


class ProcessorSuit(ComponentSuit):
    _components: List[Processor] = None
    target_components: type(Processor) = Processor

    config: dict = None

    @property
    def processor(self):
        return self._components

    def process(self, model):
        """
        Args:
            model:
        """
        current = model
        next_model = None
        try:
            for processor in self.components:
                if not isinstance(current, processor.target):
                    continue

                next_model = processor.process_item(current)

                if next_model:
                    # return model: continue processing.
                    current = next_model
                elif next_model is None:
                    # no return: next processor
                    continue
                else:
                    # return false: abort processing
                    break
        except Exception as e:
            # TODO: continue by config
            log.exception('Processor', e, line=1)
            return False
        else:
            return True


class PipelineConsumer(Consumer):

    def __init__(self, failed: deque, suit: ProcessorSuit, **kwargs):
        """
        Args:
            failed (deque):
            suit (ProcessorSuit):
            **kwargs:
        """
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
        """
        Args:
            model (Model):
        """
        if not self.suit.process(model=model):
            self._failed.append(model)


class Pipeline(object):
    _queue: Queue
    _failed: deque

    _suit: ProcessorSuit
    consumer: PipelineConsumer

    def __init__(self, suit: ProcessorSuit) -> None:
        """
        Args:
            suit (ProcessorSuit):
        """
        self._queue = Queue()
        self._failed = deque()

        self._suit = suit

        # consumer
        consumer_kwargs = {
            'queue': self.queue,
            'delay': 0,
        }
        self.consumer = PipelineConsumer(self.failed, suit, **consumer_kwargs)
        self.consumer.start()

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
        """
        Args:
            obj:
        """
        self.queue.put_nowait(obj)

    def size(self) -> int:
        return self.queue.qsize()

    def pop(self) -> object:
        return self.queue.get_nowait()

    def exit(self, timeout: int = 1):

        """
        Args:
            timeout (int):
        """
        while timeout > 0 and self.queue.qsize() > 0:
            timeout = timeout - 0.1
            time.sleep(0.1)

        # exit consumer
        self.consumer.stop()

        while self.queue.qsize() > 0:
            model = self.queue.get()
            self.failed.append(model)
