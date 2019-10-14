import unittest

from threading import Event
from typing import *

from base.components import Processor
from base.libs import Task, Model, Field
from queue import Queue, Empty
from threading import Thread
import threading
import time

import threading
import time


class BaseThreading(threading.Thread):

    def __init__(self, event: Event = threading.Event()):

        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._stopped_event = threading.Event()

    def run(self) -> None:
        while True:
            self._stopped_event.wait()
            time.sleep(1)
            print('run')

    def stop(self):
        self._stopped_event.clear()

    def start(self):
        if self.isAlive():
            self._stopped_event.set()
        else:
            threading.Thread.start(self)
            self._stopped_event.set()


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


class PipelineConsumer(BaseThreading):
    _queue: Queue
    _suit: ProcessorSuit

    stop: bool = False

    def __init__(self, queue: Queue, suit: ProcessorSuit):
        super(PipelineConsumer, self).__init__()

        self._queue = queue
        self._suit = suit

    @property
    def queue(self):
        return self._queue

    def run(self) -> None:
        while not self.stop:
            try:
                model = self.queue.get(block=True, timeout=1)
            except Empty as em:
                continue
            except TimeoutError as te:
                if self.stop:
                    break
                continue
            # FIXME
            self._process(model=model)

    def _process(self, model):
        self._suit.process(model)

    def exit(self):
        self.stop = True


class Pipeline(object):
    _processors: List[Processor]
    _queue: Queue
    _failed: Queue

    def __init__(self, processors: List[type(Processor)]) -> None:
        # processor
        for processor in processors:
            assert issubclass(processor, Processor)
        self._processors = processors

        self._queue = Queue()
        self._failed = Queue()

        # init processor
        # FIXME: init processor suit
        suit = ProcessorSuit(processors)

        # consumer
        self.consumer = PipelineConsumer(self.queue, suit)

        # start consumer thread
        self.consumer.setDaemon(True)
        self.consumer.start()

    def _init_processor(self):
        pass

    @property
    def processors(self):
        return self._processors

    @property
    def queue(self):
        return self._queue

    @property
    def failed(self):
        return self._failed

    def push(self, obj):
        self.queue.put_nowait(obj)

    def size(self) -> int:
        return self.queue.qsize()

    def pop(self) -> object:
        return self.queue.get_nowait()

    def process(self, model: Model):
        pass

    def exit(self):
        self.consumer.exit()


class Person(Model):
    name = Field()


class MyTestCase(unittest.TestCase):

    def test_test(self):


        t = BaseThreading()

        assert True

    def test_init(self):
        class TestProcessor(Processor):
            def process_item(self, model: Model) -> Any:
                return model

        t = Task(url='http://127.0.0.1:8090')

        processors = [TestProcessor]
        pipeline = Pipeline(processors)

        [pipeline.push(t) for x in range(500)]
        assert pipeline.size() == 500

        # TODO: Empty
        # pipeline.pop()
        import time
        time.sleep(0.5)

        assert pipeline.size() == 0
        pipeline.exit()
        time.sleep(0.5)
        assert pipeline.consumer.stop is True

    def test_processor_suit(self):
        class NormalProcessor(Processor):
            count = 0

            def process_item(self, model: Model) -> Any:
                self.count += 1
                return model

        class FalseProcessor(Processor):
            count = 0

            def process_item(self, model: Model) -> Any:
                self.count += 1
                return False

        class BlankProcessor(Processor):
            count = 0

            def process_item(self, model: Model) -> Any:
                self.count += 1

        class ExceptionProcesssor(Processor):
            count = 0

            def process_item(self, model: Model) -> Any:
                self.count += 1
                raise Exception()

        class TargetProcessor(Processor):
            count = 0
            target = Person

            def process_item(self, model: Model) -> Any:
                self.count += 1

        t = Task(url='http://xx.cn')

        # processor class
        with self.assertRaises(TypeError) as te:
            ProcessorSuit([NormalProcessor()])
        # abort
        # assert 'Processor must be init' in str(te.exception)

        normal = NormalProcessor
        blank = BlankProcessor
        error = ExceptionProcesssor
        tar = TargetProcessor
        false = FalseProcessor

        suit0 = ProcessorSuit([normal])
        suit0.process(t)
        assert suit0.processors[0].count == 1

        suit1 = ProcessorSuit([normal, tar])
        suit1.process(t)
        assert suit1.processors[0].count == 1
        assert suit1.processors[1].count == 0

        suit2 = ProcessorSuit([blank])
        suit2.process(t)
        assert suit2.processors[0].count == 1

        suit3 = ProcessorSuit([blank, normal])
        suit3.process(t)
        assert suit3.processors[0].count == 1
        assert suit3.processors[1].count == 1

        suit4 = ProcessorSuit([false, blank, normal])
        suit4.process(t)
        assert suit4.processors[0].count == 1
        assert suit4.processors[1].count == 0
        assert suit4.processors[1].count == 0


if __name__ == '__main__':
    unittest.main()
